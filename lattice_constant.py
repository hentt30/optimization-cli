import pandas as pd
from tqdm import tqdm
import re
import os
import subprocess
import matplotlib.pyplot as plt


class LatticeConstatOptimization:
    def __init__(self, args):
        self.min_param = float(args.min_value)
        self.max_param = float(args.max_value)
        self.step = float(args.step)
        self.number_cores = args.number_cores
        self.need_graph = args.graph
        self.validate_params()
        self.permited_params = self.generate_params()
        self.optimization_results = pd.DataFrame()

    def validate_params(self):
        if (self.max_param <= self.min_param):
            raise Exception('Minimum encut is greater than maximum encut')
        if (self.step <= 0):
            raise Exception('Step is less or equal than zero')

    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def generate_params(self):

        params = []

        initial_param = self.min_param

        while (initial_param <= self.max_param):
            params.append(initial_param)
            initial_param += self.step

        if (not self.isclose(self.max_param, params[-1])):
            params.append(self.max_param)

        return params

    def run(self):

        for param in tqdm(self.permited_params):

            self.modify_poscar_file(param)
            self.run_vasp(self.number_cores)
            parsed_results = self.parse_results(param)
            self.optimization_results = self.optimization_results.append(
                parsed_results, ignore_index=True)

        self.optimization_results.to_csv('./test_param_results.csv')

        if (self.need_graph):
            self.make_graph()

    def modify_poscar_file(self, param: int) -> None:
        with open('POSCAR', 'rt+') as file:
            content = file.read()
            chunks = re.split(r"\n\s*\n", content.rstrip(), flags=re.MULTILINE)
            try:
                if chunks[0] == "":
                    chunks.pop(0)
                    chunks[0] = "\n" + chunks[0]
            except IndexError:
                raise ValueError("Empty POSCAR")

            # Parse positions
            lines = list(self.clean_lines(chunks[0].split("\n"), False))
            lines[1] = str(param)
            new_content = '\n'.join(lines)
            # absolute file positioning
            file.seek(0)
            # truncate data
            file.truncate()
            file.write(new_content)

    def clean_lines(self, string_list, remove_empty_lines=True):
        """
        Strips whitespace, carriage returns and empty lines from a list of strings.
        Args:
            string_list: List of strings
            remove_empty_lines: Set to True to skip lines which are empty after
                stripping.
        Returns:
            List of clean strings with no whitespaces.
        """

        for s in string_list:
            clean_s = s
            if '#' in s:
                ind = s.index('#')
                clean_s = s[:ind]
            clean_s = clean_s.strip()
            if (not remove_empty_lines) or clean_s != '':
                yield clean_s

    def run_vasp(self, number_cores: int) -> None:
        process = subprocess.Popen(
            ['mpirun', '-np', str(self.number_cores), 'vasp'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if (stderr):
            raise Exception('VASP raise an error')

    def parse_results(self, param: int):
        line = str(subprocess.check_output(['tail', '-1', 'OSZICAR']))
        regex = re.compile(r'([+-]\d?(\.\d+)[Ee][+-]\d+)+')
        results = re.findall(regex, line)
        final_results = [i[0] for i in results]
        return {
            'Param (A)': param,
            'Total energy (eV/cell)': float(final_results[0]),
            'E0': float(final_results[1]),
            'dE': float(final_results[2])
        }

    def make_graph(self):
        self.optimization_results.plot(kind='scatter',
                                       x='Param (A)',
                                       y='Total energy (eV/cell)',
                                       color='blue')
        plt.savefig('output.png')
