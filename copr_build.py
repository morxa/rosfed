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
import build_tree
import copr.v3
import functools
import json
import marshmallow
import os
import re
import spec_utils
import subprocess

from termcolor import cprint


class CoprBuildError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class SrpmBuilder:
    def build_spec(self, chroot, spec):
        """ Build a SPEC file into a SRPM

        Args:
            chroot: The chroot to use for the build, e.g., fedora-26-x86_64
            spec: The path to the SPEC file of the package.
            wait_for_completion: If set to true, wait for the build to finish
        """
        print('Building {} for chroot {}'.format(spec, chroot))
        res = subprocess.run(
            [
                'spectool', '-g', spec, '-C',
                os.path.expanduser('~/rpmbuild/SOURCES')
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        assert res.returncode == 0, 'Failed to fetch sources for ' + spec
        res = subprocess.run(['rpmbuild', '-bs', spec],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        assert res.returncode == 0, 'Failed to build SRPM for ' + spec
        match = re.search('Wrote: (\S+)', res.stdout)
        assert match, 'Unexpected output from rpmbuild: "%s"'.format(
            res.stdout)
        srpm = match.group(1)
        return srpm


class CoprBuilder:
    def __init__(self, copr_owner, copr_project):
        """ Initialize the CoprBuilder using the given project ID.

        Args:
            copr_owner: the owner of the COPR project
            copr_project: the name of the COPR project
        """
        self.owner = copr_owner
        self.project = copr_project
        self.copr_client = copr.v3.Client.create_from_config_file()
        self.srpm_builder = SrpmBuilder()

    def build_spec(self, chroot, spec, wait_for_completion=False):
        """ Build a package in COPR from a SPEC.

        Args:
            chroot: The chroot to use for the build, e.g., fedora-26-x86_64
            spec: The path to the SPEC file of the package.
            wait_for_completion: If set to true, wait for the build to finish

        Returns:
            The build object created for this build.
        """
        self.build_srpm(chroot, self.srpm_builder.build_spec(chroot, spec),
                        wait_for_completion)

    def build_srpm(self, chroot, srpm, wait_for_completion):
        """ Build a package in COPR from a SRPM.

        Args:
            chroot: The chroot to use for the build, e.g., fedora-26-x86_64
            srpm: The path to the SRPM file of the package.
            wait_for_completion: If set to true, wait for the build to finish

        Returns:
            The build object created for this build.
        """
        print('Building {} for project {}/{} with chroot {}'.format(
            srpm, self.owner, self.project, chroot))
        build = self.copr_client.build_proxy.create_from_file(
            ownername=self.owner,
            projectname=self.project,
            path=srpm,
            buildopts={'chroots': [chroot]})
        assert build, 'COPR client returned build object "{}"'.format(build)
        if wait_for_completion:
            self.wait_for_completion([build])
            assert build.state == 'succeeded', \
                    'Build failed, state is {}.'.format(build.state)
            cprint('Building {} was successful.'.format(srpm), 'green')
        return build

    def get_node_of_build(self, nodes, build_id):
        for node in nodes:
            if node.build_id == build_id:
                return node
        raise Exception(
            'Could not find node of build {} in build tree'.format(build))

    def build_tree(self, chroot, tree, only_new=False):
        """ Build a set of packages in order of dependencies. """
        build_ids = []
        while not tree.is_built():
            wait_for_build = True
            leaves = tree.get_build_leaves()
            print('Found {} leave node(s)'.format(len(leaves)))
            if not build_ids and not leaves:
                raise Exception(
                    'No pending builds and no leave packages, abort.')
            for node in leaves:
                if only_new:
                    pkg_version = None
                else:
                    pkg_version = node.pkg.get_version_release()
                if self.pkg_is_built(chroot, node.pkg.get_full_name(),
                                     pkg_version):
                    node.state = build_tree.BuildState.SUCCEEDED
                    build_progress = tree.get_build_progress()
                    cprint(
                        '{}/{}/{}: {} is already built, skipping!'.format(
                            build_progress['building'],
                            build_progress['finished'],
                            build_progress['total'], node.name), 'green')
                    wait_for_build = False
                else:
                    assert node.state == build_tree.BuildState.PENDING, \
                            'Unexpected build state {} of package node ' \
                            '{}'.format(node.state, node.name)
                    build = self.build_spec(chroot=chroot, spec=node.pkg.spec)
                    node.build_id = build.id
                    node.state = build_tree.BuildState.BUILDING
                    build_ids.append(node.build_id)
            if not wait_for_build:
                continue
            print('Waiting for a build to finish...')
            finished_build = self.wait_for_one_build(build_ids)
            node = self.get_node_of_build(tree.nodes.values(),
                                          finished_build.id)
            build_ids.remove(finished_build.id)
            if finished_build.state == 'succeeded':
                node.state = build_tree.BuildState.SUCCEEDED
                build_progress = tree.get_build_progress()
                cprint(
                    '{}/{}/{}: Successful build: {}'.format(
                        build_progress['building'], build_progress['finished'],
                        build_progress['total'], node.name), 'green')
            else:
                node.state = build_tree.BuildState.FAILED
                build_progress = tree.get_build_progress()
                cprint(
                    '{}/{}/{}: Failed build: {}'.format(
                        build_progress['building'], build_progress['finished'],
                        build_progress['total'], node.name), 'red')

    @functools.lru_cache(16)
    def get_builds(self):
        return self.copr_client.build_proxy.get_list(self.owner, self.project)

    def pkg_is_built(self, chroot, pkg_name, pkg_version):
        """ Check if the given package is already built in the COPR.

        Args:
            chroot: The chroot to check, e.g., fedora-26-x86_64.
            pkg_name: The name of the package to look for.
            pkg_version: Check for the given version in format $version-$release

        Returns:
            True iff the package was already built in the project and chroot.
        """
        for build in self.copr_client.build_proxy.get_list(
                self.owner, self.project, pkg_name):
            if build.state != 'succeeded':
                continue
            if chroot not in build.chroots:
                continue
            build_version = re.fullmatch(
                '(.+?)(?:\.(?:fc|rhel|epel|el)\d+)?',
                build['source_package']['version']).group(1)
            if build_version == pkg_version:
                return True
        return False

    def wait_for_completion(self, builds):
        """ Wait until all given builds are finished.

        Args:
            builds: A list of builds to wait for.
        """
        print('Waiting for {} build(s) to complete...'.format(len(builds)))
        finished = wait(builds)

    def wait_for_one_build(self, build_ids):
        """ Wait for one of the given builds to complete.

        Args:
            build_ids: A list of COPR build IDs.
        Returns:
            The build that completed.
        """
        while True:
            for build_id in build_ids:
                build = self.copr_client.build_proxy.get(build_id)
                if build.state in [
                        'succeeded', 'failed', 'canceled', 'cancelled'
                ]:
                    return build


def main():
    """ Main function to directly build a SPEC file. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        '--force',
                        action='store_true',
                        default=False,
                        help='Force a rebuild if package was already built')
    parser.add_argument('--copr-owner',
                        type=str,
                        help='The owner of the COPR project to use for builds')
    parser.add_argument('--copr-project',
                        type=str,
                        help='The COPR project to use for builds')
    parser.add_argument('--chroot',
                        action='append',
                        help='The chroot(s) to use for the packages')
    parser.add_argument('--spec-dir',
                        default='./specs/',
                        help='The directory where to look for SPEC files')
    parser.add_argument('pkg_name', nargs='+')
    args = parser.parse_args()
    copr_builder = CoprBuilder(args.copr_owner, args.copr_project)
    for chroot in args.chroot:
        for pkg in args.pkg_name:
            spec = args.spec_dir + pkg + '.spec'
            need_build = args.force
            if not need_build:
                version_info = spec_utils.get_version_from_spec(spec)
                ver_rel = '{}-{}'.format(version_info['version'],
                                         version_info['release'])
                need_build = not copr_builder.pkg_is_built(
                    chroot, pkg, ver_rel)
            if need_build:
                copr_builder.build_spec(chroot=chroot,
                                        spec=spec,
                                        wait_for_completion=True)


if __name__ == '__main__':
    main()
