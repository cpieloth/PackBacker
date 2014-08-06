#!/usr/bin/env python3

__author__ = 'Christof Pieloth'

import logging
import sys

from packbacker.installers import installer_prototypes
from packbacker.job import Job


def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='[%(levelname)s] %(name)s: %(message)s')

    # TODO(cpieloth): CLI args, ...
    job = Job()
    for i in installer_prototypes():
        i.dest_dir = '~'
        job.add_installer(i)
    job.execute()


if __name__ == '__main__':
    main()