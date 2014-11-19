#!/usr/bin/env python

"""
Setup MNE-CPP library and includes for compilation.
"""

__author__ = 'Christof Pieloth'

import os
from subprocess import call

from packbacker.constants import Parameter
from packbacker.errors import ParameterError
from packbacker.utils import Utils
from packbacker.utils import UtilsUI
from packbacker.installers.installer import Installer


class MNECPP(Installer):
    REPO_FOLDER = "mne-cpp"
    PARAM_QMAKE5 = "qmake5"

    def __init__(self):
        Installer.__init__(self, 'MNE-CPP', 'MNE-CPP')
        self.__qmake5 = 'qmake5'

    @property
    def qmake5(self):
        """Alias or symlink to Qt5's qmake."""
        return self.__qmake5

    @qmake5.setter
    def qmake5(self, dest):
        self.__qmake5 = dest

    @classmethod
    def instance(cls, params):
        installer = MNECPP()
        if Parameter.DEST_DIR in params:
            installer.dest_dir = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        if installer.PARAM_QMAKE5 in params:
            installer.qmake5 = params[installer.PARAM_QMAKE5]
        return installer

    @classmethod
    def prototype(cls):
        return MNECPP()

    def _pre_install(self):
        success = True
        success = success and Utils.check_program("git", "--version")
        success = success and Utils.check_program("make", "--version")
        success = success and Utils.check_program(self.qmake5, "--version")
        if not Utils.check_program("g++", "--version") and not Utils.check_program("c++", "--version"):
            success = False
        return success

    def _install(self):
        if UtilsUI.ask_for_execute("Download " + self.name):
            self._download()

        print()

        if UtilsUI.ask_for_execute("Initialize " + self.name):
            self._initialize()

        print()

        if UtilsUI.ask_for_execute("Configure " + self.name):
            self._configure()

        print()

        if UtilsUI.ask_for_execute("Compile " + self.name):
            self._compile()

        return True

    def _post_install(self):
        include_dir = os.path.join(self.dest_dir, self.REPO_FOLDER, "MNE")
        UtilsUI.print_env_var("MNE_INCLUDE_DIR", include_dir)

        library_path = os.path.join(self.dest_dir, self.REPO_FOLDER, "lib")
        UtilsUI.print_env_var("MNE_LIBRARY_DIR", library_path)
        return True

    def _download(self):
        UtilsUI.print_step_begin("Downloading")
        repo = "https://github.com/mne-tools/mne-cpp.git"
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        call("git clone " + repo + " " + repo_dir, shell=True)
        UtilsUI.print_step_end("Downloading")

    def _initialize(self):
        UtilsUI.print_step_begin("Initializing")
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        os.chdir(repo_dir)
        version = "38667b56a09aa2e15c58eba85f455d99c42ce880"  # 2014-11-19
        call("git checkout " + version, shell=True)
        UtilsUI.print_step_end("Initializing")

    def _configure(self):
        UtilsUI.print_step_begin("Configuring")
        mne_dir = os.path.join(self.dest_dir, self.REPO_FOLDER, "MNE")
        os.chdir(mne_dir)
        mne_configure = self.qmake5 + " -recursive"
        call(mne_configure, shell=True)
        UtilsUI.print_step_end("Configuring")

    def _compile(self):
        UtilsUI.print_step_begin("Compiling")
        mne_dir = os.path.join(self.dest_dir, self.REPO_FOLDER, "MNE")
        os.chdir(mne_dir)
        jobs = UtilsUI.ask_for_make_jobs()
        call("make -j" + str(jobs), shell=True)
        UtilsUI.print_step_end("Compiling")
