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
import json
import re
import requests
import subprocess

""" Base URL of the COPR, will be appended with the API URL suffix. """
copr_url = 'https://copr.fedorainfracloud.org'

def build_spec(project_id, chroot, spec, auth):
    """ Build a package in COPR from a SPEC file.

    Args:
        project_id: The COPR project where the package should be built.
        chroot: The chroot to use for the build, e.g., fedora-26-x86_64
        spec: The path to the SPEC file of the package.
        auth: A tuple (user, password) used with BasicAuth for the COPR API.
    """
    print('Building {} for chroot {}'.format(spec, chroot))
    res = subprocess.run(['rpmbuild', '-bs', spec],
                         universal_newlines=True,
                         stdout=subprocess.PIPE)
    assert res.returncode == 0, 'Failed to build SRPM for ' + spec
    match = re.match('Wrote: (\S+)', res.stdout)
    assert match, 'Unexpected output from rpmbuild: "%s"'.format(res.stdout)
    srpm = match.group(1)
    build_srpm(project_id, chroot, srpm, auth)

def build_srpm(project_id, chroot, srpm, auth):
    """ Build a package in COPR from a SRPM.

    Args:
        project_id: The COPR project where the package should be built.
        chroot: The chroot to use for the build, e.g., fedora-26-x86_64
        srpm: The path to the SRPM file of the package.
        auth: A tuple (user, password) used with BasicAuth for the COPR API.
    """
    print('Building {} for project {} with chroot {}'.format(
        srpm, project_id, chroot))
    metadata = {
        'project_id': project_id,
        'chroots': [chroot],
        'enable_net': False
    }
    r = requests.post(url=copr_url + '/api_2/builds',
                      files={'file': open(srpm, 'rb')},
                      json=json.dumps(metadata),
                      auth=auth)
    print(r)
    assert r.status_code == 200, \
            'Request failed, returned {}'.format(r.status_code)

def pkg_is_built(copr_project_id, chroot, pkg_name):
    """ Check if the given package is already built in the COPR.

    Args:
        copr_project_id: The ID of the COPR project to check for the package.
        chroot: The chroot to check, e.g., fedora-26-x86_64.
        pkg_name: The name of the package to look for.

    Returns:
        True iff the package was already built in the given project and chroot.
    """
    builds = json.loads(requests.get(copr_url + '/api_2/builds',
                          {'project_id': copr_project_id}).text)['builds']
    for build in builds:
        if build['build']['package_name'] == pkg_name:
            build_info = json.loads(requests.get(
                copr_url + build['_links']['build_tasks']['href']).text)
            # We can always use the first item in the list because we
            # query for the build id and therefore there is only one.
            build_task = build_info['build_tasks'][0]['build_task']
            if build_task['state'] == 'succeeded' and \
               build_task['chroot_name'] == chroot:
                return True
    return False

def main():
    """ Main function to directly build a SPEC file. """
    parser = argparse.ArgumentParser()
    parser.add_argument('--chroot', action='append',
                        help='The chroot(s) to use for the packages')
    parser.add_argument('--project_id', default='14923',
                        help='The COPR project ID to build the packages in')
    parser.add_argument('--spec-dir', default='./specs/',
                        help='The directory where to look for SPEC files')
    parser.add_argument('-u', '--user',
                        help='The COPR API user which is used to send requests')
    parser.add_argument('-p', '--password',
                        help='The password to use to send requests to COPR')
    parser.add_argument('pkg_name', nargs='+')
    args = parser.parse_args()
    for chroot in args.chroot:
        for pkg in args.pkg_name:
            if not pkg_is_built(args.project_id, chroot, pkg):
                spec = args.spec_dir + pkg + '.spec'
                build_spec(project_id=args.project_id, chroot=chroot, spec=spec,
                           auth=(args.user, args.password))


if __name__ == '__main__':
    main()
