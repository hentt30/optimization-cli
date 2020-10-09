# -*- coding: utf-8 -*-
import argparse
import re
import os
import subprocess
import pandas as pd
import seaborn as sns


def optimization(min_encut: int, max_encut: int, step: int, graph: bool):
    validate_params(min_encut, max_encut, step)

    permited_encuts = generate_encuts(min_encut, max_encut, step)
    run_process(permited_encuts)

    if (graph):
        make_graph()


def validate_params(min_encut: int, max_encut: int, step: int) -> list:
    if (max_encut < min_encut):
        raise Exception('Minimum encut is greater than maximum encut')
    if (step <= 0):
        raise Exception('Step is less than zero')


def generate_encuts(min_encut: int, max_encut: int, step: int) -> list:

    encuts = []

    initial_encut = min_encut

    while (initial_encut <= max_encut):
        encuts.append(initial_encut)
        initial_encut += step

    if (max_encut != encuts[-1]):
        encuts.append(max_encut)

    return encuts


def run_process(permited_encuts: list) -> None:
    results_df = pd.DataFrame()

    for encut in permited_encuts:

        modify_incar_file(encut)
        run_vasp()
        parsed_results = parse_results(encut)
        results_df = results_df.append(parsed_results, ignore_index=True)

    results_df.to_csv('./test_encut_results.csv')


def modify_incar_file(encut: int) -> None:
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


def run_vasp() -> None:
    if (os.path.isfile('WAVECAR')):
        os.remove('WAVECAR')

    process = subprocess.Popen(['mpirun', 'vasp541-05FEB16'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if (stderr):
        raise Exception('VASP raise an error')


def parse_results(encut: int) -> dict:
    line = subprocess.check_output(['tail', '-1', 'OSZICAR'])
    regex = re.compile(r'([+-]\d?(\.\d+)[Ee][+-]\d+)+')
    results = re.findall(regex, line)
    final_results = [i[0] for i in results]
    return {
        'Encut (eV)': encut,
        'Energy (eV)': final_results[0],
        'E0': final_results[1],
        'dE': final_results[2]
    }


def make_graph():
    df = pd.read_csv('./test_encut_results.csv')
    plot = sns.scatterplot(data=df, x="encut", y="F")
    fig = plot.get_figure()
    fig.savefig('output.eps')


def main():
    parser = argparse.ArgumentParser(
        description='Calculate encut optimization')
    parser.add_argument('min_encut', type=int, help='minimum value of encut')
    parser.add_argument('max_encut', type=int, help='maximum value of encut')
    parser.add_argument(
        'step',
        type=int,
        help='step of variation between minimum and maximum encut')
    parser.add_argument('-g',
                        '--graph',
                        action='store_true',
                        help='plot the optimization graph - Optional argument')

    args = parser.parse_args()

    optimization(args.min_encut, args.max_encut, args.step, args.graph)


if __name__ == '__main__':
    main()
