# encut optimization cli

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

## Define entry points

```bash
python3 setup.py develop
```

## About CLI
```bash
usage: encut_optimization [-h] [--graph GRAPH]
                          min_encut [min_encut ...] max_encut [max_encut ...]
                          step [step ...]

Calculate encut optimization

positional arguments:
  min_encut      minimum value of encut
  max_encut      maximum value of encut
  step           step of variation between minimum and maximum encut

optional arguments:
  -h, --help     show this help message and exit
  --graph GRAPH  make the optimization graph
```