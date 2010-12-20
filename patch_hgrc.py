"""Patch the specified hgrc file to add a ui remotecmd key that points
to the Mercurial installed in the buildbot virtualenv on ocean. This
is necessary to make the changeset hook in the ocean repository
successfully send a notification to buildbot.

Usage: python patch_hgrc.py <path-to-hgrc> <buildbot-version>

"""
from __future__ import print_function
from ConfigParser import NoSectionError
from ConfigParser import SafeConfigParser
import os
import sys


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=[__name__]):
    try:
        if len(argv) < 3:
            raise Usage('too few arguments')
        hgrc = argv[1]
        buildbot_version = argv[2]
        remotecmd = (
            '/ocean/dlatorne/.virtualenvs/buildbot-{0}/bin/hg'
            .format(buildbot_version))
        config = SafeConfigParser()
        with open(hgrc, 'rb') as fp:
            config.readfp(fp)
            try:
                config.set('ui', 'remotecmd', remotecmd)
            except NoSectionError:
                config.add_section('ui')
                config.set('ui', 'remotecmd', remotecmd)
        with open(hgrc, 'wb') as fp:
            config.write(fp)
    except Usage as err:
        print(err.msg, end='\n\n', file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return os.EX_USAGE


if __name__ == '__main__':
    sys.exit(main(sys.argv))
