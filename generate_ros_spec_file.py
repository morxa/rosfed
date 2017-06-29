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
import time
import yaml

from rosinstall_generator import generator

class RosPkg:
    def __init__(self, name, distro):
        self.rosdistro = distro
        self.name = name
    def get_ros_dependencies(self):
       dependency_dict = generator.generate_rosinstall(
           self.rosdistro, [self.name], deps=True, deps_depth=1, deps_only=True,
           wet_only=True, tar=True)
       return [ pkg['tar']['local-name'].split('/')[-1]
                for pkg in dependency_dict ]

    def get_system_dependencies(self, skip_keys):
        cmd = subprocess.run(
            ['rosdep', '--rosdistro={}'.format(self.rosdistro),
             'keys', self.name],
            stdout=subprocess.PIPE
        )
        deps_keys = cmd.stdout.decode().split('\n')
        deps = []
        for dep in deps_keys:
            if dep == '' or dep in skip_keys:
                continue
            cmd = subprocess.run(
                ['rosdep', '--rosdistro={}'.format(self.rosdistro),
                 'resolve', dep],
                stdout=subprocess.PIPE)
            deps += cmd.stdout.decode().split('\n')
        deps = [ dep for dep in deps if not (dep == '' or dep == '#dnf') ]
        return deps

    def get_sources(self):
        ros_pkg = generator.generate_rosinstall(
            self.rosdistro, [self.name], deps=False, wet_only=True, tar=True)
        return [ros_pkg[0]['tar']['uri']]

    def get_version(self):
        ros_pkg = generator.generate_rosinstall(
            self.rosdistro, [self.name], deps=False, wet_only=True, tar=True)
        return re.match('[\w-]*-([0-9-_.]*)(-[0-9-]*)',
                        ros_pkg[0]['tar']['version']).group(1)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Spec files for ROS packages with the '
                    'rosinstall_generator.')
    parser.add_argument('-r', '--recursive', action='store_true', default=False,
                        help='Also generate Spec files for dependencies')
    parser.add_argument('-u', '--update', action='store_true', default=False,
                        help='Update existing Spec files')
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
        ros_pkg = RosPkg(name=packages[i], distro=distro)
        i += 1
        print('Generating Spec file for {}.'.format(ros_pkg.name))
        ros_deps = ros_pkg.get_ros_dependencies()
        dependencies[ros_pkg.name] = ros_deps
        if recursive:
            # Append all items that are not already in packages. We cannot use a
            # set, because we need to loop over it while we append items.
            packages += [ dep for dep in ros_deps if  not dep in packages ]
        sys_deps = ros_pkg.get_system_dependencies(ros_deps)
        sources = ros_pkg.get_sources()
        version = ros_pkg.get_version()
        try:
            pkg_config = yaml.load(
                open('cfg/{}.yaml'.format(ros_pkg.name), 'r'))
        except FileNotFoundError:
            pkg_config = {}
        try:
            spec_template = jinja_env.get_template(
                '{}.spec.j2'.format(ros_pkg.name))
        except jinja2.exceptions.TemplateNotFound:
            spec_template = jinja_env.get_template('pkg.spec.j2')
        spec = spec_template.render(
            pkg_name=ros_pkg.name,
            distro=distro,
            pkg_version=version, license='BSD',
            pkg_url='https://wiki.ros.org/'+ros_pkg.name,
            source_urls=sources,
            ros_dependencies=sorted(ros_deps),
            system_dependencies=sorted(sys_deps),
            pkg_description='ROS package {}.'.format(ros_pkg.name),
            pkg_release=release_version or pkg_config.get('release', '1'),
            user_string=user_string,
            date=time.strftime("%a %b %d %Y", time.gmtime()),
            noarch=no_arch or pkg_config.get('noarch', False),
            patches=pkg_config.get('patches', []),
        )
        with open(os.path.join(destination,
                               'ros-{}-{}.spec'.format(distro, ros_pkg.name)),
                  'w') as spec_file:
            spec_file.write(spec)
    return dependencies


if __name__ == '__main__':
    main()
