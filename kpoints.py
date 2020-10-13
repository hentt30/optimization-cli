import pandas as pd
from tqdm import tqdm
import re
import os
import subprocess
import matplotlib.pyplot as plt


class KpointsOptimization:
    def __init__(self, args):
        self.min_kpoint = int(args.min_value)
        self.max_kpoint = int(args.max_value)
        self.step = int(args.step)
        self.is_2d = args.two_dimensions
        self.number_cores = args.number_cores
        self.need_graph = args.graph
        self.validate_params()
        self.permited_kpoints = self.generate_kpoints()
        self.optimization_results = pd.DataFrame()

    def validate_params(self):
        if (self.max_kpoint <= self.min_kpoint):
            raise Exception('Minimum encut is greater than maximum encut')
        if (self.step <= 0):
            raise Exception('Step is less or equal than zero')

    def generate_kpoints(self):

        kpoints = []

        initial_kpoint = self.min_kpoint

        while (initial_kpoint <= self.max_kpoint):
            kpoints.append(initial_kpoint)
            initial_kpoint += self.step

        if (self.max_kpoint != kpoints[-1]):
            kpoints.append(self.max_kpoint)

        return kpoints

    def run(self):

        for kpoint in tqdm(self.permited_kpoints):

            self.modify_kpoint_file(kpoint)
            self.run_vasp(self.number_cores)
            parsed_results = self.parse_results(kpoint)
            self.optimization_results = self.optimization_results.append(
                parsed_results, ignore_index=True)

        self.optimization_results.to_csv('./test_kpoints_results.csv')

        if (self.need_graph):
            self.make_graph()

    def modify_kpoint_file(self, kpoint: int) -> None:
        with open('KPOINTS', 'rt+') as file:
            content = file.read()
            chunks = re.split(r"\n\s*\n", content.rstrip(), flags=re.MULTILINE)
            try:
                if chunks[0] == "":
                    chunks.pop(0)
                    chunks[0] = "\n" + chunks[0]
            except IndexError:
                raise ValueError("Empty KPOINT")

            # Parse positions
            lines = list(self.clean_lines(chunks[0].split("\n"), False))
            if (self.is_2d):
                lines[3] = '{} {} 1'.format(kpoint, kpoint)

            else:
                lines[3] = '{} {} {}'.format(kpoint, kpoint, kpoint)

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

    def parse_results(self, kpoint: int):
        line = str(subprocess.check_output(['tail', '-1', 'OSZICAR']))
        regex = re.compile(r'([+-]\d?(\.\d+)[Ee][+-]\d+)+')
        results = re.findall(regex, line)
        final_results = [i[0] for i in results]
        return {
            'Kpoint': kpoint,
            'Total energy (eV/cell)': float(final_results[0]),
            'E0': float(final_results[1]),
            'dE': float(final_results[2])
        }

    def make_graph(self):
        self.optimization_results.plot(kind='scatter',
                                       x='Kpoint',
                                       y='Total energy (eV/cell)',
                                       color='blue')
        plt.savefig('output.png')
