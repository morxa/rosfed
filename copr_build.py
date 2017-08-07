#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de>
#
# Distributed under terms of the MIT license.

"""
For a given SPEC file, this module can check if the package was already built in
the specified COPR and if not, will submit a new build to the COPR.
"""

import argparse
import copr
import json
import re
import subprocess

class CoprBuilder:
    def __init__(self, project_id):
        """ Initialize the CoprBuilder using the given project ID.

        Args:
            project_id: The ID of the COPR project to use for builds.
        """
        self.project_id = project_id
        self.copr_client = copr.create_client2_from_file_config()

    def build_spec(self, chroot, spec):
        """ Build a package in COPR from a SPEC file.

        Args:
            project_id: The COPR project where the package should be built.
            chroot: The chroot to use for the build, e.g., fedora-26-x86_64
            spec: The path to the SPEC file of the package.
        """
        print('Building {} for chroot {}'.format(spec, chroot))
        res = subprocess.run(['rpmbuild', '-bs', spec],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        assert res.returncode == 0, 'Failed to build SRPM for ' + spec
        match = re.match('Wrote: (\S+)', res.stdout)
        assert match, 'Unexpected output from rpmbuild: "%s"'.format(res.stdout)
        srpm = match.group(1)
        self.build_srpm(chroot, srpm)

    def build_srpm(self, chroot, srpm):
        """ Build a package in COPR from a SRPM.

        Args:
            project_id: The COPR project where the package should be built.
            chroot: The chroot to use for the build, e.g., fedora-26-x86_64
            srpm: The path to the SRPM file of the package.
        """
        print('Building {} for project {} with chroot {}'.format(
            srpm, self.project_id, chroot))
        build = self.copr_client.builds.create_from_file(
            project_id=self.project_id, file_path=srpm, chroots=[chroot])
        while not build.is_finished():
            build = build.get_self()
        assert build.state == 'succeeded', \
                'Build failed, state is {}.'.format(build.state)
        print('Building {} was successful.'.format(srpm))

    def pkg_is_built(self, chroot, pkg_name):
        """ Check if the given package is already built in the COPR.

        Args:
            copr_project_id: The ID of the COPR project to check for the package.
            chroot: The chroot to check, e.g., fedora-26-x86_64.
            pkg_name: The name of the package to look for.

        Returns:
            True iff the package was already built in the project and chroot.
        """
        builds = self.copr_client.builds.get_list(self.project_id)
        for build in builds:
            if build.package_name == pkg_name:
                build_tasks = build.get_build_tasks()
                for build_task in build_tasks:
                    # TODO: add version check
                    if build_task.state == 'succeeded' and \
                       build_task.chroot_name == chroot:
                        return True
        return False

def main():
    """ Main function to directly build a SPEC file. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='Force a rebuild if package was already built')
    parser.add_argument('--chroot', action='append',
                        help='The chroot(s) to use for the packages')
    parser.add_argument('--project-id', type=int, default=14923,
                        help='The COPR project ID to build the packages in')
    parser.add_argument('--spec-dir', default='./specs/',
                        help='The directory where to look for SPEC files')
    parser.add_argument('pkg_name', nargs='+')
    args = parser.parse_args()
    copr_builder = CoprBuilder(args.project_id)
    for chroot in args.chroot:
        for pkg in args.pkg_name:
            if args.force or not copr_builder.pkg_is_built(chroot, pkg):
                spec = args.spec_dir + pkg + '.spec'
                copr_builder.build_spec(chroot=chroot, spec=spec)

if __name__ == '__main__':
    main()
