#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de>
#
# Distributed under terms of the MIT license.
"""
Util functions for Spec files.
"""

import re


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
