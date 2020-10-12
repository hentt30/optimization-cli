class Parser:
    def __init__(self, argparse):
        self.parser = argparse.ArgumentParser(
            description='Calculate encut optimization')
        self.add_arguments()
        self.add_options()

    def add_arguments(self):
        self.parser.add_argument('action',
                                 choices=('encut', 'lattice_constant',
                                          'kpoint'))

        self.parser.add_argument(
            'min_value', help='minimum value of optimization parameter')

        self.parser.add_argument('max_value',
                                 help='maximum optimization parameter')
        self.parser.add_argument(
            'step', help='step of variation between minimum and maximum')

    def add_options(self):
        self.parser.add_argument(
            '-np',
            '--number_cores',
            default=1,
            help='plot the optimization graph - Optional argument')
        self.parser.add_argument(
            '-g',
            '--graph',
            action='store_true',
            help='plot the optimization graph - Optional argument')
        self.parser.add_argument(
            '-td',
            '--two_dimensions',
            action='store_true',
            help='Adjust kpoints to two dimentional materials')

    def parse_args(self):
        return self.parser.parse_args()
