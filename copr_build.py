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
import spec_utils
import subprocess

class CoprBuildError(Exception):
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return repr(self.error)

class CoprBuilder:
    def __init__(self, project_id):
        """ Initialize the CoprBuilder using the given project ID.

        Args:
            project_id: The ID of the COPR project to use for builds.
        """
        self.project_id = project_id
        self.copr_client = copr.create_client2_from_file_config()

    def build_spec(self, chroot, spec, wait_for_completion=False):
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
        return self.build_srpm(chroot, srpm, wait_for_completion)

    def build_srpm(self, chroot, srpm, wait_for_completion):
        """ Build a package in COPR from a SRPM.

        Args:
            project_id: The COPR project where the package should be built.
            chroot: The chroot to use for the build, e.g., fedora-26-x86_64
            srpm: The path to the SRPM file of the package.
            wait_for_completion: If set to True, wait until the build has
                                 terminated.

        Returns:
            The build object created for this build.
        """
        print('Building {} for project {} with chroot {}'.format(
            srpm, self.project_id, chroot))
        build = self.copr_client.builds.create_from_file(
            project_id=self.project_id, file_path=srpm, chroots=[chroot])
        assert build, 'COPR client returned build object "{}"'.format(build)
        if wait_for_completion:
            self.wait_for_completion([build])
            assert build.state == 'succeeded', \
                    'Build failed, state is {}.'.format(build.state)
            print('Building {} was successful.'.format(srpm))
        return build

    def pkg_is_built(self, chroot, pkg_name, pkg_version):
        """ Check if the given package is already built in the COPR.

        Args:
            chroot: The chroot to check, e.g., fedora-26-x86_64.
            pkg_name: The name of the package to look for.
            pkg_version: Check for the given version in format $version-$release

        Returns:
            True iff the package was already built in the project and chroot.
        """
        offset = 0
        builds = self.copr_client.builds.get_list(self.project_id)
        # workaround for https://pagure.io/copr/copr/issue/119
        # get_list returns at most 100 builds
        while builds:
            offset += len(builds)
            for build in builds:
                # We expect package versions of the format 1.0-2.fc23 or 1.0-2
                build_version = \
                        re.fullmatch('(.+?)(?:\.(?:fc|rhel|epel|el)\d+)?',
                                     build.package_version).group(1)
                if build_version != pkg_version:
                    continue
                if build.package_name == pkg_name:
                    try:
                        build_tasks = build.get_build_tasks()
                    except marshmallow.exceptions.ValidationError:
                        print('Failed to get build tasks of build {}, skipping',
                              build.id)
                        continue
                    for build_task in build_tasks:
                        # TODO: add version check
                        if build_task.state == 'succeeded' and \
                           build_task.chroot_name == chroot:
                            return True
            builds = self.copr_client.builds.get_list(self.project_id,
                                                      offset=offset)
        return False

    def wait_for_completion(self, builds):
        """ Wait until all given builds are finished.

        Args:
            builds: A list of builds to wait for.
        """
        print('Waiting for {} build(s) to complete...'.format(len(builds)))
        completed = set()
        builds = set(builds)
        while completed != builds:
            for build in builds - completed:
                if build.get_self().is_finished():
                    completed.add(build)
                    print('{}/{}: {} finished building.'.format(
                        len(completed), len(builds),
                        build.get_self().package_name))
                elif build.get_self().state == 'canceled':
                    raise CoprBuildError(
                        'Build {} of package {} was canceled'.format(
                            build.get_self().id, build.get_self().package_name))

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
            spec = args.spec_dir + pkg + '.spec'
            need_build = args.force
            if not need_build:
                version_info = spec_utils.get_version_from_spec(spec)
                ver_rel = '{}-{}'.format(
                    version_info['version'], version_info['release'])
                need_build = not copr_builder.pkg_is_built(chroot, pkg, ver_rel)
            if need_build:
                copr_builder.build_spec(chroot=chroot, spec=spec,
                                        wait_for_completion=True)

if __name__ == '__main__':
    main()
