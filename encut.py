import pandas as pd
from tqdm import tqdm
import re
import os
import subprocess
import matplotlib.pyplot as plt


class EncutOptimization:
    def __init__(self, args):
        self.min_encut = int(args.min_value)
        self.max_encut = int(args.max_value)
        self.step = int(args.step)
        self.number_cores = args.number_cores
        self.need_graph = args.graph
        self.validate_params()
        self.permited_encuts = self.generate_encuts()
        self.optimization_results = pd.DataFrame()

    def validate_params(self):
        if (self.max_encut <= self.min_encut):
            raise Exception('Minimum encut is greater than maximum encut')
        if (self.step <= 0):
            raise Exception('Step is less or equal than zero')

    def generate_encuts(self):

        encuts = []

        initial_encut = self.min_encut

        while (initial_encut <= self.max_encut):
            encuts.append(initial_encut)
            initial_encut += self.step

        if (self.max_encut != encuts[-1]):
            encuts.append(self.max_encut)

        return encuts

    def run(self):

        for encut in tqdm(self.permited_encuts):

            self.modify_incar_file(encut)
            self.run_vasp(self.number_cores)
            parsed_results = self.parse_results(encut)
            self.optimization_results = self.optimization_results.append(
                parsed_results, ignore_index=True)

        self.optimization_results.to_csv('./test_encut_results.csv')

        if (self.need_graph):
            self.make_graph()

    def modify_incar_file(self, encut: int) -> None:
        with open('INCAR', 'rt+') as file:
            content = file.read()
            new_content = re.sub('ENCUT\s*=\s*-?\s*([0-9]+)?',
                                 r'ENCUT={}'.format(encut),
                                 content,
                                 flags=re.IGNORECASE)
            # absolute file positioning
            file.seek(0)
            # truncate data
            file.truncate()
            file.write(new_content)

    def run_vasp(self, number_cores: int) -> None:
        process = subprocess.Popen(
            ['mpirun', '-np', str(self.number_cores), 'vasp'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if (stderr):
            raise Exception('VASP raise an error')

    def parse_results(self, encut: int):
        line = str(subprocess.check_output(['tail', '-1', 'OSZICAR']))
        regex = re.compile(r'([+-]\d?(\.\d+)[Ee][+-]\d+)+')
        results = re.findall(regex, line)
        final_results = [i[0] for i in results]
        return {
            'Encut (eV)': encut,
            'Total energy (eV/cell)': float(final_results[0]),
            'E0': float(final_results[1]),
            'dE': float(final_results[2])
        }

    def make_graph(self):
        self.optimization_results.plot(kind='scatter',
                                       x='Encut (eV)',
                                       y='Total energy (eV/cell)',
                                       color='blue')
        plt.savefig('output.png')