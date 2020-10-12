# -*- coding: utf-8 -*-
import argparse
from parser import Parser
from encut import EncutOptimization
from lattice_constant import LatticeConstatOptimization


def run_encut(args):
    encut_optimization = EncutOptimization(args)
    encut_optimization.run()


def run_lattice_constant(args):
    lattice_constant_optimization = LatticeConstatOptimization(args)
    lattice_constant_optimization.run()


def optimization(args, options):
    options[args.action](args)


def run():
    parser = Parser(argparse)
    args = parser.parse_args()
    options = {'encut': run_encut, 'lattice_constant': run_lattice_constant}
    optimization(args, options)


if __name__ == '__main__':
    run()
