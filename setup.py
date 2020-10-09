# -*- coding: utf-8 -*-

from setuptools import setup
setup(name="encut-opt",
      version="0.0.1",
      scripts=["encut_optimization.py"],
      install_requires=["argparse", "pandas", "seaborn", "tqdm"],
      entry_points="""
        [console_scripts]
        encut_optimization=encut_optimization:main
    """)
