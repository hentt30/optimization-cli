# Optimization cli

## Install dependencies

1 - Create virtual environment
```bash
python3 -m venv opt-env
```
2 - Activate virtual ennvironment
```bash
source ./opt-env/bin/activate
```

3 - Install dependencies

``` bash
python3 setup.py install
```
Or

``` bash
sudo python3 setup.py install
```

## Define entry points

```bash
python3 setup.py develop
```

## About CLI
```bash
usage: optimization.py [-h] [-np NUMBER_CORES] [-g] [-td]
                       {encut,lattice_constant,kpoint} min_value max_value
                       step

Calculate encut optimization

positional arguments:
  {encut,lattice_constant,kpoint}
  min_value             minimum value of optimization parameter
  max_value             maximum optimization parameter
  step                  step of variation between minimum and maximum

optional arguments:
  -h, --help            show this help message and exit
  -np NUMBER_CORES, --number_cores NUMBER_CORES
                        plot the optimization graph - Optional argument
  -g, --graph           plot the optimization graph - Optional argument
  -td, --two_dimensions
                        Adjust kpoints for two dimentional materials
```