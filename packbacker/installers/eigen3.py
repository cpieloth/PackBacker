#!/usr/bin/env python

"""
Downloads Eigen library with sparse matrix support.
"""

__author__ = 'Christof Pieloth'

import os
from subprocess import call

from packbacker.installers.installer import Installer
from packbacker.installers.installer import Installer as Utils
from packbacker.constants import Parameter
from packbacker.errors import ParameterError


class Eigen3(Installer):
    REPO_FOLDER = "eigen321"

    def __init__(self):
        Installer.__init__(self, "eigen3")

    @classmethod
    def instance(cls, params):
        installer = Eigen3()
        if Parameter.DEST_DIR in params:
            installer.dest_dir = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        return installer

    @classmethod
    def prototype(cls):
        return Eigen3()

    def _pre_install(self):
        success = True
        success = success and Utils.check_program("hg", "--version")
        return success

    def _install(self):
        if Utils.ask_for_execute("Download " + self.name):
            self._download()

        print

        if Utils.ask_for_execute("Initialize " + self.name):
            self._initialize()

        return True

    def _post_install(self):
        print("Before compiling the toolbox, please set the following environment variables:\n")
        include_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        print("    EIGEN3_INCLUDE_DIR=" + include_dir)

        print
        return True

    def _download(self):
        Utils.print_step_begin("Downloading")
        repo = "https://bitbucket.org/eigen/eigen/"
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        call("hg clone " + repo + " " + repo_dir, shell=True)
        Utils.print_step_end("Downloading")

    def _initialize(self):
        Utils.print_step_begin("Initializing")
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        os.chdir(repo_dir)
        version = "3.2.1"
        call("hg update " + version, shell=True)
        Utils.print_step_end("Initializing")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Downloads Eigen library with sparse matrix support.")
#     parser.add_argument("-d", "--destdir", help="Destination path.")
#     args = parser.parse_args()
#
#     destdir = AInstaller.get_default_destdir()
#     if args.destdir:
#         destdir = args.destdir
#
#     installer = Eigen3(destdir)
#     if installer.install():
#         sys.exit(AInstaller.EXIT_SUCCESS)
#     else:
#         sys.exit(AInstaller.EXIT_ERROR)
