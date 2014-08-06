#!/usr/bin/env python

"""
Downloads necessary files for CxxTest.
"""

__author__ = 'Christof Pieloth'

import os
from subprocess import call

from packbacker.constants import Parameter
from packbacker.errors import ParameterError
from packbacker.utils import Utils
from packbacker.utils import UtilsUI
from packbacker.installers.installer import Installer


class CxxTest(Installer):
    REPO_FOLDER = "cxxtest"

    def __init__(self):
        Installer.__init__(self, "CxxTest")

    @classmethod
    def instance(cls, params):
        installer = CxxTest()
        if Parameter.DEST_DIR in params:
            installer.dest_dir = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        return installer

    @classmethod
    def prototype(cls):
        return CxxTest()

    def _pre_install(self):
        success = True
        success = success and Utils.check_program("git", "--version")
        success = success and Utils.check_program("python", "--version")
        return success

    def _install(self):
        if UtilsUI.ask_for_execute("Download " + self.name):
            self._download()

        print()

        if UtilsUI.ask_for_execute("Initialize " + self.name):
            self._initialize()

        return True

    def _post_install(self):
        envs = {}

        root_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        envs['CXXTEST_ROOT'] = root_dir

        include_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        envs['CXXTEST_INCLUDE_DIR'] = include_dir

        UtilsUI.print_env_var(envs)

        return True

    def _download(self):
        UtilsUI.print_step_begin("Downloading")
        repo = "https://github.com/CxxTest/cxxtest.git"
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        call("git clone " + repo + " " + repo_dir, shell=True)
        UtilsUI.print_step_end("Downloading")

    def _initialize(self):
        UtilsUI.print_step_begin("Initializing")
        repo_dir = os.path.join(self.dest_dir, self.REPO_FOLDER)
        os.chdir(repo_dir)
        version = "4.4"  # 2014-06-03
        call("git checkout " + version, shell=True)
        UtilsUI.print_step_end("Initializing")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Installs CxxTest.")
#     parser.add_argument("-d", "--destdir", help="Destination path.")
#     args = parser.parse_args()
#
#     destdir = AInstaller.get_default_destdir()
#     if args.destdir:
#         destdir = args.destdir
#
#     installer = Installer(destdir)
#     if installer.do_install():
#         sys.exit(AInstaller.EXIT_SUCCESS)
#     else:
#         sys.exit(AInstaller.EXIT_ERROR)
