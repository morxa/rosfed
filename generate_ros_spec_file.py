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
import re
import subprocess
import sys
import time

from rosinstall_generator import generator

def get_ros_dependencies(rosdistro, pkg_name):
   dependency_dict = generator.generate_rosinstall(
       rosdistro, [pkg_name], deps=True, deps_depth=1, deps_only=True,
       wet_only=True, tar=True)
   return [ pkg['tar']['local-name'].split('/')[-1] for pkg in dependency_dict ]

def get_system_dependencies(rosdistro, pkg_name, skip_keys):
    cmd = subprocess.run(
        ['rosdep', '--rosdistro={}'.format(rosdistro), 'keys', pkg_name],
        stdout=subprocess.PIPE
    )
    deps_keys = cmd.stdout.decode().split('\n')
    deps = []
    for dep in deps_keys:
        if dep == '' or dep in skip_keys:
            continue
        cmd = subprocess.run(
            ['rosdep', '--rosdistro={}'.format(rosdistro), 'resolve', dep],
            stdout=subprocess.PIPE)
        deps += cmd.stdout.decode().split('\n')
    deps = [ dep for dep in deps if not (dep == '' or dep == '#dnf') ]
    return deps

def get_sources(rosdistro, pkg_name):
    ros_pkg = generator.generate_rosinstall(
        rosdistro, [pkg_name], deps=False, wet_only=True, tar=True)
    return [ros_pkg[0]['tar']['uri']]

def get_version(rosdistro, pkg_name):
    ros_pkg = generator.generate_rosinstall(
        rosdistro, [pkg_name], deps=False, wet_only=True, tar=True)
    return re.match('[\w-]*-([0-9-_.]*)(-[0-9-]*)', ros_pkg[0]['tar']['version']).group(1)


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
    parser.add_argument('--release-version', default='1',
                        help='The Release: of the resulting Spec files')
    parser.add_argument('--no-arch', action='store_true', default=False,
                        help='Set BuildArch to noarch')
    parser.add_argument('ros_pkg', nargs='+',
                        help='ROS package name')
    args = parser.parse_args()
    if not args.user_string:
        user_string = subprocess.run(["rpmdev-packager"],
                                      stderr=subprocess.DEVNULL,
                                      stdout=subprocess.PIPE).stdout
        if sys.version_info[0] > 2:
            user_string = user_string.decode(errors='replace')
        args.user_string = user_string.strip()
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    spec_template = jinja_env.get_template('pkg.spec.j2')
    for ros_pkg in args.ros_pkg:
        ros_deps = get_ros_dependencies(args.distro, ros_pkg)
        sys_deps = get_system_dependencies(args.distro, ros_pkg, ros_deps)
        sources = get_sources(args.distro, ros_pkg)
        version = get_version(args.distro, ros_pkg)
        spec = spec_template.render(
            pkg_name=ros_pkg,
            distro=args.distro,
            pkg_version=version, license='BSD',
            pkg_url='https://wiki.ros.org/'+ros_pkg,
            source_urls=sources,
            ros_dependencies=sorted(ros_deps),
            system_dependencies=sorted(sys_deps),
            pkg_description='ROS package {}.'.format(ros_pkg),
            pkg_release=args.release_version,
            user_string=args.user_string,
            date=time.strftime("%a %b %d %Y", time.gmtime()),
            noarch=args.no_arch,
        )
        with open('ros-{}-{}.spec'.format(args.distro, ros_pkg), 'w') as spec_file:
            spec_file.write(spec)


if __name__ == '__main__':
    main()
