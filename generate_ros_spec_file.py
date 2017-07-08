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
import jinja2
import os
import re
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

def get_version_from_spec(spec):
    """ Get the version and release from a Spec file.

    Args:
        spec: the path to the Spec file
    Returns:
        A dictionary with keys 'version' and 'release'
    """
    version_info = {}
    for line in open(spec, 'r').readlines():
        version_match = re.match('^Version:\s+([\w\.]+)', line)
        if version_match:
            version_info['version'] = version_match.group(1)
            continue
        release_match = re.match('Release:\s+([\w\.]+)(%\{\?dist\})?', line)
        if release_match:
            version_info['release'] = release_match.group(1)
    assert 'version' in version_info, 'Could not find a Version: tag'
    assert 'release' in version_info, 'Could not find a Release: tag'
    return version_info

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
            self.pkg_config = yaml.load(
                open('cfg/{}.yaml'.format(self.name), 'r'))
        except FileNotFoundError:
            self.pkg_config = {}
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
        if self.name != 'catkin':
            build_deps['ros'].add('catkin')
        return build_deps

    def get_run_dependencies(self):
        run_deps = {}
        for key, val in self.run_deps.items():
            run_deps[key] = val | \
                    self.get_dependencies_from_cfg('run').get(key, set())
        return run_deps

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
        return self.pkg_config.get('release', 1)

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
    parser.add_argument('--release-version', default='',
                        help='The Release: of the resulting Spec files')
    parser.add_argument('--no-arch', action='store_true', default=False,
                        help='Set BuildArch to noarch')
    parser.add_argument('-d', '--destination', default='./specs',
                        help='Write generated Spec files to this directory')
    parser.add_argument('-B', '--build-order-file', type=argparse.FileType('w'),
                        default=None,
                        help='Print the order in which the packages should be '
                             'built, requires -r')
    parser.add_argument('ros_pkg', nargs='+',
                        help='ROS package name')
    args = parser.parse_args()
    os.makedirs(args.destination, exist_ok=True)
    if args.build_order_file:
        assert args.recursive, 'Build order requires --recursive'
    if not args.user_string:
        user_string = subprocess.run(["rpmdev-packager"],
                                      stderr=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE).stdout
        if sys.version_info[0] > 2:
            user_string = user_string.decode(errors='replace')
        args.user_string = user_string.strip()
    dependencies = generate_spec_files(args.ros_pkg, args.distro,
                                       args.release_version, args.user_string,
                                       args.recursive, args.no_arch,
                                       args.destination)
    if args.build_order_file:
        order = get_build_order(dependencies)
        for stage in order:
            args.build_order_file.write(" ".join(stage) + '\n')

def get_build_order(packages):
    """ Get the order in which to build the given dictionary of packages. """
    order = []
    resolved_pkgs = set()
    while resolved_pkgs != set(packages.keys()):
        leaves = set()
        for pkg, deps in packages.items():
            if pkg in resolved_pkgs:
                continue
            if not set(deps) - resolved_pkgs:
                leaves.add(pkg)
        assert leaves, 'No dependency leaves found, cyclic dependencies?'
        order.append(leaves)
        resolved_pkgs |= leaves
    return order

def generate_spec_files(packages, distro, release_version, user_string,
                        recursive, no_arch, destination):
    """ Generate Spec files for the given list of packages. """
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    i = 0
    dependencies = {}
    while i < len(packages):
        print('Generating Spec file for {}.'.format(packages[i]))
        ros_pkg = RosPkg(name=packages[i], distro=distro)
        i += 1
        build_deps = ros_pkg.get_build_dependencies()
        run_deps = ros_pkg.get_run_dependencies()
        ros_deps = build_deps['ros'] | run_deps['ros']
        dependencies[ros_pkg.name] = ros_deps
        if recursive:
            # Append all items that are not already in packages. We cannot use a
            # set, because we need to loop over it while we append items.
            packages += [ dep for dep in ros_deps if  not dep in packages ]
        sources = ros_pkg.get_sources()
        version = ros_pkg.get_version()
        outfile = os.path.join(destination,
                               'ros-{}-{}.spec'.format(distro, ros_pkg.name))
        if os.path.isfile(outfile):
            changelog = get_changelog_from_spec(outfile)
            if not release_version:
                # Release is not specified and Spec file exists, use new version
                # or bump release if it is the same version.
                version_info = get_version_from_spec(outfile)
                if version_info['version'] == version:
                    release_version = int(version_info['release']) + 1
                else:
                    release_version = 1
        else:
            changelog = ''
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
            pkg_release=release_version or ros_pkg.get_release(),
            user_string=user_string,
            date=time.strftime("%a %b %d %Y", time.gmtime()),
            changelog=changelog,
            noarch=no_arch or ros_pkg.is_noarch(),
            patches=ros_pkg.get_patches(),
            build_flags=ros_pkg.get_build_flags(),
            no_debug=ros_pkg.has_no_debug(),
        )
        with open(outfile, 'w') as spec_file:
            spec_file.write(spec)
    return dependencies


if __name__ == '__main__':
    main()
