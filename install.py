__author__ = 'Christof Pieloth'

from packbacker.installers import installer_prototypes
from packbacker.job import Job


def main():
    # TODO(cpieloth): CLI args, ...
    job = Job()
    for i in installer_prototypes():
        i.dest_dir = '~'
        job.add_installer(i)
    job.execute()


if __name__ == '__main__':
    main()