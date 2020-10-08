import argparse
import re
import os
import subprocess
import pandas as pd
import seaborn


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
        results_df.append(parse_results, ignore_index=True)

    results_df.to_csv('./test_encut_results.csv')


def modify_incar_file(encut: int) -> None:
    with open('INCAR', 'rw+') as file:
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

    process = subprocess.Popen(['mpirun', 'vasp541-05FEB16'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if (stderr):
        raise Exception('VASP raise an error')


def parse_results(encut: int) -> dict:
    line = subprocess.check_output(['tail', '-1', 'OSZICAR'])
    results = re.findall(r'[+-]?\d?(\.\d+)[Ee][+-]?\d+', line)

    return {
        'encut': encut,
        'F': results[0],
        'E0': results[1],
        'dE': results[2]
    }


def make_graph():
    df = pd.read_csv('./test_encut_results.csv')
    plot = sns.scatterplot(data=df, x="Encut (eV)", y="Energy (eV)")
    plot.savefig("output.eps")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate encut optimization')
    parser.add_argument('min_encut',
                        type=int,
                        nargs='+',
                        help='minimum value of encut')
    parser.add_argument('max_encut',
                        type=int,
                        nargs='+',
                        help='maximum value of encut')
    parser.add_argument(
        'step',
        type=int,
        nargs='+',
        help='step of variation between minimum and maximum encut')
    parser.add_argument('--graph',
                        type=bool,
                        default=False,
                        help='make the optimization graph')

    args = parser.parse_args()
    optimization(args.min_encut, args.max_encut, args.step, args.graph)