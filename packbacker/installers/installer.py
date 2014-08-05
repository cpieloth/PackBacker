#!/usr/bin/env python

"""
Install and setup 3rd software which is not contained in distribution's packet management.
All installers must implement AInstaller and check CLI arguments -d and --destdir for destination path.
Furthermore the __main__ must invoke the installation with installers.do_install().
"""

__author__ = 'Christof Pieloth'

import argparse
import logging
import os
import subprocess
from subprocess import call
import sys

DEPENDENCY_PATH_PREFIX = "na-online_dependencies"


class Installer(object):
    """Abstract installers with default implementations of pre_install and post_install."""
    EXIT_SUCCESS = 0
    EXIT_ERROR = 1

    def __init__(self, name):
        self._name = name
        self._log = logging.getLogger(self._name)

    @property
    def name(self):
        """Name of the installers."""
        return self._name

    @property
    def dest_dir(self):
        """Destination directory."""
        return self._dest_dir

    @dest_dir.setter
    def dest_dir(self, dest):
        self._dest_dir = os.path.expanduser(dest)

    @property
    def log(self):
        """Logger for this installers."""
        return self._log

    def _pre_install(self):
        """Is called before the installation. It can be used to check for tools which are required."""
        return True

    def _install(self):
        """Abstract method, implements the installation."""
        self.log.debug('No yet implemented: ' + str(self.name))
        return False

    def _post_install(self):
        """Is called after a successful installation. Can be used to test installation or for user instructions."""
        return True

    def install(self):
        """Starts the installation process."""
        Installer.print_install_begin(self._name)

        try:
            success = self._pre_install()
            if success:
                success = self._install()

            if success:
                success = self._post_install()
        except Exception as ex:
            success = False
            self.log.error("Unexpected error:\n" + str(ex))

        Installer.print_install_end(self._name)
        return success

    @classmethod
    def instance(cls, params):
        """
        Abstract method, returns an initialized instance of a specific command.
        Can throw a ParameterError, if parameters are missing.
        """
        raise Exception('Instance method not implemented for: ' + str(cls))

    @classmethod
    def prototype(cls):
        """Abstract method, returns an instance of a specific command, e.g. for matches() or is_available()"""
        raise Exception('Prototype method not implemented for: ' + str(cls))

    def matches(self, installer):
        """Checks if this command should be used for execution."""
        return installer.lower().startswith(self.name)

# TODO(cpieloth): move to UiUtils or similar
    @staticmethod
    def ask_for_execute(action):
        var = raw_input(action + " y/n? ")
        if var.startswith('y'):
            return True
        else:
            return False


    @staticmethod
    def ask_for_make_jobs():
        jobs = 2
        try:
            jobs = int(raw_input("Number of jobs (default: 2): "))
        except ValueError:
            print("Wrong input format.")
        if jobs < 1:
            jobs = 1
        print("Using job=" + str(jobs))
        return jobs

    @staticmethod
    def print_install_begin(dep_name):
        # print('=' * len(dep_name))
        print('=' * 80)
        print(dep_name)
        print('-' * 80)

    @staticmethod
    def print_install_end(dep_name):
        print('-' * 80)
        print(dep_name)
        print('=' * 80)

    @staticmethod
    def print_step_begin(action_str):
        info = action_str + " ..."
        print(info)
        print('-' * 40)

    @staticmethod
    def print_step_end(action_str):
        info = action_str + " ... finished!"
        print('-' * 40)
        print(info)

    @staticmethod
    def check_program(program, arg):
        try:
            call([program, arg], stdout=subprocess.PIPE)
            return True
        except OSError as e:
            print("Could not found: " + program)
            return False

    @staticmethod
    def get_default_destdir():
        homedir = os.path.expanduser("~")
        destdir = os.path.join(homedir, DEPENDENCY_PATH_PREFIX)
        return destdir
    

# class InstallerJob(Installer):
#
#     def __init__(self, dest_dir):
#         Installer.__init__(self, "Install Dependencies", dest_dir)
#
#     def _install(self):
#         destdir_arg = "-d " + self._dest_dir
#         rc = 0
#
#         if Installer.ask_for_execute("Install Qt5 Framework"):
#             rc += call("python install_qt5_static.py " + destdir_arg, shell=True)
#
#         print
#
#         if Installer.ask_for_execute("Install MNE-CPP"):
#             rc += call("python install_mne.py " + destdir_arg, shell=True)
#
#         print
#
#         if Installer.ask_for_execute("Install FielTrip Buffer"):
#             rc += call("python install_ft_buffer.py " + destdir_arg, shell=True)
#
#         print
#
#         # Optional libraries, depending on versions in package repository
#         if Installer.ask_for_execute("Install Point Cloud Library"):
#             rc += call("python install_pcl.py " + destdir_arg, shell=True)
#
#         print
#
#         if Installer.ask_for_execute("Install Eigen with sparse matrix support"):
#             rc += call("python eigen3.py " + destdir_arg, shell=True)
#
#         if rc == 0:
#             return True
#         else:
#             print("\nErrors occurred during installation! Please check and solve it manually.\n")
#             return False
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Installs 3rd party software and libraries for NA-Online Toolbox.")
#     parser.add_argument("-d", "--destdir", help="Destination path.")
#     args = parser.parse_args()
#
#     destdir = Installer.get_default_destdir()
#     if args.destdir:
#         destdir = args.destdir
#
#     installer = InstallerJob(destdir)
#     if installer.install():
#         sys.exit(Installer.EXIT_SUCCESS)
#     else:
#         sys.exit(Installer.EXIT_ERROR)
