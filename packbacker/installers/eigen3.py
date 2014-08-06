"""
Downloads Eigen3 library with sparse matrix support.
"""

__author__ = 'Christof Pieloth'

import os
from subprocess import call

from packbacker.constants import Parameter
from packbacker.errors import ParameterError
from packbacker.utils import Utils
from packbacker.utils import UtilsUI
from packbacker.installers.installer import Installer


class Eigen3(Installer):
    REPO_FOLDER = "eigen321"

    def __init__(self):
        Installer.__init__(self, 'eigen3', 'Eigen version 3')

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
        if UtilsUI.ask_for_execute("Download " + self.name):
            self._download()

        print()

        if UtilsUI.ask_for_execute("Initialize " + self.name):
            self._initialize()

        return True

    def _post_install(self):
        include_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        UtilsUI.print_env_var('EIGEN3_INCLUDE_DIR', include_dir)
        return True

    def _download(self):
        UtilsUI.print_step_begin("Downloading")
        repo = "https://bitbucket.org/eigen/eigen/"
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        call("hg clone " + repo + " " + repo_dir, shell=True)
        UtilsUI.print_step_end("Downloading")

    def _initialize(self):
        UtilsUI.print_step_begin("Initializing")
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        os.chdir(repo_dir)
        version = "3.2.1"
        call("hg update " + version, shell=True)
        UtilsUI.print_step_end("Initializing")