__author__ = 'Christof Pieloth'

import logging

from packbacker.installers import installer_prototypes
from packbacker.errors import ParameterError


class Job(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self._installers = []

    def add_installer(self, installer):
        self._installers.append(installer)

    def execute(self):
        Job.log.info('Starting ...')
        errors = 0
        for i in self._installers:
            # TODO(cpieloth): if Installer.ask_for_execute("Install Qt5 Framework"):
            try:
                if i.install():
                    self.log.info(i.name + ' executed.')
                else:
                    errors += 1
                    Job.log.error('Error on executing ' + i.name + '!')
            except Exception as ex:
                errors += 1
                Job.log.error('Unknown error:\n' + str(ex))

        Job.log.info('Finished with errors: ' + str(errors))
        return errors

    @staticmethod
    def read_job(fname):
        prototypes = []
        prototypes.extend(installer_prototypes())

        job_file = None
        job = None
        try:
            job_file = open(fname, 'r')
            job = Job()
            for line in job_file:
                if line[0] == '#':
                    continue
                for p in prototypes:
                    if p.matches(line):
                        params = Job.read_parameter(line)
                        try:
                            cmd = p.instance(params)
                            job.add_installer(cmd)
                        except ParameterError as err:
                            Job.log.error("Installer '" + p.name + "' is skipped: " + str(err))
                        continue
        except IOError as err:
            job.log.critical('Error on reading job file:\n' + str(err))
            job = None
        except Exception as ex:
            Job.log.critical('Unknown error: \n' + str(ex))
            job = None
        finally:
            if job_file:
                job_file.close()

        return job

    @staticmethod
    def read_parameter(line):
        params = {}
        i = line.find(': ') + 2
        line = line[i:]
        pairs = line.split(';')
        for pair in pairs:
            pair = pair.strip()
            par = pair.split('=')
            if len(par) == 2:
                params[par[0]] = par[1]
        return params