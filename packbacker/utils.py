__author__ = 'Christof Pieloth'

import logging
import subprocess


class Utils:
    log = logging.getLogger(__name__)

    @staticmethod
    def check_program(program, arg):
        try:
            subprocess.call([program, arg], stdout=subprocess.PIPE)
            return True
        except OSError:
            Utils.log.error("Could not found: " + program)
            return False


class UtilsUI:
    COLUMNS_INSTALL = 80
    COLUMNS_STEP = 40

    @staticmethod
    def ask_for_execute(action):
        var = input(action + " y/n? ")
        if var.startswith('y'):
            return True
        else:
            return False

    @staticmethod
    def ask_for_make_jobs():
        jobs = 2
        try:
            jobs = int(input("Number of jobs (default: 2): "))
        except ValueError:
            print("Wrong input format.")
        if jobs < 1:
            jobs = 1
        print("Using job=" + str(jobs))
        return jobs

    @staticmethod
    def print_install_begin(dep_name):
        print('=' * UtilsUI.COLUMNS_INSTALL)
        print(dep_name)
        print('-' * UtilsUI.COLUMNS_INSTALL)

    @staticmethod
    def print_install_end(dep_name):
        print('-' * UtilsUI.COLUMNS_INSTALL)
        print(dep_name)
        print('=' * UtilsUI.COLUMNS_INSTALL)

    @staticmethod
    def print_step_begin(action_str):
        info = action_str + " ..."
        print(info)
        print('-' * UtilsUI.COLUMNS_STEP)

    @staticmethod
    def print_step_end(action_str):
        info = action_str + " ... finished!"
        print('-' * UtilsUI.COLUMNS_STEP)
        print(info)

    @staticmethod
    def print_env_var(name_env, value=None):
        if value is None:
            if len(name_env) == 1:
                print('Environment variable to set:')
            else:
                print('Environment variables to set:')
            print()
            for name, value in name_env.items():
                print(name + "=" + value)
        else:
            print('Environment variable to set:')
            print()
            print(name_env + "=" + value)
        print()