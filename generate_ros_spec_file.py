#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de>
#
# Distributed under terms of the MIT license.

"""
Generate Spec files for ROS packages with the rosinstall_generator.
"""

import argparse
import copr_build
import jinja2
import os
import re
import spec_utils
import subprocess
import sys
import textwrap
import time
import yaml

from rosinstall_generator import generator
from defusedxml import ElementTree

def get_system_package_name(pkg_name, rosdistro):
    cmd = subprocess.run(
        ['rosdep', '--rosdistro={}'.format(rosdistro),
         'resolve', pkg_name],
        stdout=subprocess.PIPE
    )
    assert cmd.returncode == 0, 'Could not find system package {}: {}'.format(
        pkg_name, cmd.stderr or cmd.stdout.decode())
    lines = cmd.stdout.decode().split('\n')
    deps = [ dep for dep in lines if not (dep == '' or dep == '#dnf') ]
    assert len(deps) == 1, 'Expected exactly one name, got: {}'.format(deps)
    return deps[0]

def get_changelog_from_spec(spec):
    """ Get the changelog of an existing Spec file.

    Args:
        spec: The path to the Spec file.
    Returns:
        The changelog in the Spec file as string, excluding the %changelog tag.
    """
    spec_as_list = open(spec, 'r').readlines()
    return ''.join(spec_as_list[spec_as_list.index('%changelog\n')+1:])

class RosPkg:
    def __init__(self, name, distro):
        self.rosdistro = distro
        self.name = name
        self.distro_info = generator.get_wet_distro(distro)
        xml_string = self.distro_info.get_release_package_xml(name)
        self.xml = ElementTree.fromstring(xml_string)
        self.build_deps = { 'ros': set(), 'system': set() }
        self.run_deps = { 'ros': set(), 'system': set() }
        try:
            common_config = yaml.load(open('cfg/common.yaml'))
        except FileNotFoundError:
            common_config = {}
        try:
            pkg_specific_config = yaml.load(
                open('cfg/{}.yaml'.format(self.name), 'r'))
        except FileNotFoundError:
            pkg_specific_config = {}
        self.pkg_config = { **common_config, **pkg_specific_config }
        self.release = self.pkg_config.get('release', 1)
        self.compute_dependencies()

    def compute_dependencies(self):
        for child in self.xml:
            for dep_key, dep_lists in {'build_depend': [self.build_deps],
                                      'test_depend': [self.build_deps],
                                      'run_depend': [self.run_deps],
                                      'buildtool_depend': [self.build_deps],
                                      'build_export_depend': [self.run_deps,
                                                              self.build_deps],
                                      'buildtool_export_depend':
                                        [self.run_deps, self.build_deps],
                                      'depend': [self.run_deps, self.build_deps]
                                     }.items():
                if child.tag == dep_key:
                    pkg = child.text
                    try:
                        self.distro_info.get_release_package_xml(pkg)
                        for dep_list in dep_lists:
                            dep_list['ros'].add(pkg)
                    except KeyError:
                        system_pkg = get_system_package_name(pkg, self.rosdistro)
                        for dep_list in dep_lists:
                            dep_list['system'].add(system_pkg)

    def get_dependencies_from_cfg(self, dependency_type):
        try:
            deps = self.pkg_config['dependencies'][dependency_type]
        except KeyError:
            deps = {}
        for key, val in deps.items():
            deps[key] = set(val)
        return deps

    def get_build_dependencies(self):
        build_deps = {}
        for key, val in self.build_deps.items():
            build_deps[key] = val | \
                    self.get_dependencies_from_cfg('build').get(key, set())
            build_deps[key] -= \
                    self.get_dependencies_from_cfg('exclude_build').get(
                        key, set())
        if self.name != 'catkin':
            build_deps['ros'].add('catkin')
        return build_deps

    def get_run_dependencies(self):
        run_deps = {}
        for key, val in self.run_deps.items():
            # merge with additional dependencies from the config
            run_deps[key] = val | \
                    self.get_dependencies_from_cfg('run').get(key, set())
            # remove dependencies excluded in the config
            run_deps[key] -= \
                    self.get_dependencies_from_cfg('exclude_run').get(
                        key, set())
            # remove all devel packages
            run_deps[key] -= set(
                [dep for dep in run_deps[key] if re.match('.*-devel', dep)])
        return run_deps

    def get_ros_dependencies(self):
        return self.get_build_dependencies()['ros'] | \
            self.get_run_dependencies()['ros']

    def get_sources(self):
        ros_pkg = generator.generate_rosinstall(
            self.rosdistro, [self.name], deps=False, wet_only=True, tar=True)
        return [ros_pkg[0]['tar']['uri']]

    def get_version(self):
        ros_pkg = generator.generate_rosinstall(
            self.rosdistro, [self.name], deps=False, wet_only=True, tar=True)
        return re.match('[\w-]*-([0-9-_.]*)(-[0-9-]*)',
                        ros_pkg[0]['tar']['version']).group(1)

    def get_license(self):
        return self.xml.find('license').text

    def get_description(self):
        return textwrap.fill(self.xml.find('description').text \
                             or 'ROS {} package {}.'.format(self.rosdistro,
                                                            self.name))

    def get_website(self):
        for url in self.xml.findall('url'):
            if url.get('type') == 'website':
                return url.text
        return 'http://www.ros.org/'

    def get_release(self):
        return self.release

    def set_release(self, release):
        self.release = release

    def get_version_release(self):
        return '{}-{}'.format(self.get_version(), self.get_release())

    def is_noarch(self):
        return self.pkg_config.get('noarch', False)

    def get_patches(self):
        return self.pkg_config.get('patches', [])

    def get_build_flags(self):
        return self.pkg_config.get('build_flags', '')

    def has_no_debug(self):
        return self.pkg_config.get('no_debug', False)

def main():
    parser = argparse.ArgumentParser(
        description='Generate Spec files for ROS packages with the '
                    'rosinstall_generator.')
    parser.add_argument('-r', '--recursive', action='store_true', default=False,
                        help='Also generate Spec files for dependencies')
    parser.add_argument('--distro', default='kinetic',
                        help='The ROS distro')
    parser.add_argument('-t', '--template', default='templates/pkg.spec.j2',
                        help='Path to the Jinja template for the Spec file')
    parser.add_argument('--user_string', default = '',
                        help='The user string to use for the changelog')
    parser.add_argument('--bump-release', default=False, action='store_true',
                        help='If set to true, bump the Release: tag by 1')
    parser.add_argument('--release-version', default='',
                        help='The Release: of the resulting Spec files')
    parser.add_argument('--no-arch', action='store_true', default=False,
                        help='Set BuildArch to noarch')
    parser.add_argument('-d', '--destination', default='./specs',
                        help='Write generated Spec files to this directory')
    parser.add_argument('-c', '--changelog', type=str,
                        default='',
                        help='The new changelog entry line')
    build_args = parser.add_argument_group('build arguments')
    build_args.add_argument('-b', '--build', action='store_true', default=False,
                            help='Build the generated SPEC file')
    build_args.add_argument('--copr-project-id', type=int,
                            help='The ID of the COPR project to use for builds')
    build_args.add_argument('--chroot', action='append', type=str,
                            help='The chroot used for building the packages, '
                                 'specify multiple chroots by using the flag '
                                 'multiple times')
    parser.add_argument('-B', '--build-order-file', type=argparse.FileType('w'),
                        default=None,
                        help='Print the order in which the packages should be '
                             'built, requires -r')
    parser.add_argument('ros_pkg', nargs='+',
                        help='ROS package name')
    args = parser.parse_args()
    os.makedirs(args.destination, exist_ok=True)
    if not args.user_string:
        user_string = subprocess.run(["rpmdev-packager"],
                                      stderr=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE).stdout
        if sys.version_info[0] > 2:
            user_string = user_string.decode(errors='replace')
        args.user_string = user_string.strip()
    # TODO: Improve design, we should not resolve dependencies and generate SPEC
    # files in one step, these are not really related.
    packages = generate_spec_files(args.ros_pkg, args.distro,
                                       args.bump_release,
                                       args.release_version, args.user_string,
                                       args.changelog, args.recursive,
                                       args.no_arch, args.destination)
    if args.build_order_file:
        order = get_build_order(packages)
        for stage in order:
            args.build_order_file.write(" ".join(stage) + '\n')
    if args.build:
        assert args.copr_project_id, 'You need to provide a COPR Project ID.'
        assert args.chroot, 'You need to provide a chroot to use for builds.'
        copr_builder = copr_build.CoprBuilder(project_id=args.copr_project_id)
        for chroot in args.chroot:
            for stage in get_build_order(packages):
                stage_builds = []
                for package in stage:
                    pkg_name = 'ros-{}-{}'.format(args.distro, package)
                    ver_rel = packages[package].get_version_release()
                    if copr_builder.pkg_is_built(chroot, pkg_name, ver_rel):
                        print('Skipping {}, package is already built!'.format(
                            pkg_name))
                    else:
                        spec = os.path.join(args.destination, pkg_name+'.spec')
                        build = copr_builder.build_spec(chroot, spec)
                        stage_builds.append(build)
                copr_builder.wait_for_completion(stage_builds)
                # update all builds
                stage_builds = [ build.get_self() for build in stage_builds ]
                for build in stage_builds:
                    assert build.state == 'succeeded', \
                            'Failed to build {}!'.format(build.package_name)

def get_build_order(packages):
    """ Get the order in which to build the given dictionary of packages.
        Each key is a ROS package name, each value is the set of RosPkgs."""
    order = []
    resolved_pkgs = set()
    while resolved_pkgs != set(packages.keys()):
        leaves = set()
        for pkg_name, pkg in packages.items():
            if pkg_name in resolved_pkgs:
                continue
            remaining_deps = set(pkg.get_ros_dependencies()) - resolved_pkgs
            if not remaining_deps.intersection(packages.keys()):
                # No remaining dependencies that are pending to be built.
                # We can build this package.
                leaves.add(pkg_name)
        assert leaves, 'No dependency leaves found, cyclic dependencies?'
        order.append(leaves)
        resolved_pkgs |= leaves
    return order

def generate_spec_files(packages, distro, bump_release, release_version,
                        user_string, changelog_entry, recursive, no_arch,
                        destination):
    """ Generate Spec files for the given list of packages. """
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    i = 0
    generated_packages = {}
    while i < len(packages):
        print('Generating Spec file for {}.'.format(packages[i]))
        # TODO: skip if already in generated_packages
        ros_pkg = RosPkg(name=packages[i], distro=distro)
        i += 1
        build_deps = ros_pkg.get_build_dependencies()
        run_deps = ros_pkg.get_run_dependencies()
        ros_deps = ros_pkg.get_ros_dependencies()
        generated_packages[ros_pkg.name] = ros_pkg
        if recursive:
            # Append all items that are not already in packages. We cannot use a
            # set, because we need to loop over it while we append items.
            packages += [ dep for dep in ros_deps if  not dep in packages ]
        sources = ros_pkg.get_sources()
        version = ros_pkg.get_version()
        outfile = os.path.join(destination,
                               'ros-{}-{}.spec'.format(distro, ros_pkg.name))
        pkg_changelog_entry = changelog_entry
        if os.path.isfile(outfile):
            changelog = get_changelog_from_spec(outfile)
            if not release_version:
                # Release is not specified and Spec file exists, use new version
                # or bump release if it is the same version.
                version_info = spec_utils.get_version_from_spec(outfile)
                if version_info['version'] == version:
                    pkg_release_version = int(version_info['release'])
                    if bump_release:
                        assert pkg_changelog_entry, \
                                'Please provide a changelog entry.'
                        pkg_release_version += 1
                    else:
                        pkg_changelog_entry = ''
                    ros_pkg.set_release(pkg_release_version)
                else:
                    assert pkg_changelog_entry, \
                            'Please provide a changelog entry.'
                    ros_pkg.set_release(1)
        else:
            changelog = ''
            assert pkg_changelog_entry, 'Please provide a changelog entry.'
        try:
            spec_template = jinja_env.get_template(
                '{}.spec.j2'.format(ros_pkg.name))
        except jinja2.exceptions.TemplateNotFound:
            spec_template = jinja_env.get_template('pkg.spec.j2')
        spec = spec_template.render(
            pkg_name=ros_pkg.name,
            distro=distro,
            pkg_version=version,
            license=ros_pkg.get_license(),
            pkg_url=ros_pkg.get_website(),
            source_urls=sources,
            build_dependencies=build_deps,
            run_dependencies=run_deps,
            pkg_description=ros_pkg.get_description(),
            pkg_release=ros_pkg.get_release(),
            user_string=user_string,
            date=time.strftime("%a %b %d %Y", time.gmtime()),
            changelog=changelog,
            changelog_entry=pkg_changelog_entry,
            noarch=no_arch or ros_pkg.is_noarch(),
            patches=ros_pkg.get_patches(),
            build_flags=ros_pkg.get_build_flags(),
            no_debug=ros_pkg.has_no_debug(),
        )
        with open(outfile, 'w') as spec_file:
            spec_file.write(spec)
    return generated_packages


if __name__ == '__main__':
    main()
