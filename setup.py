# -*- coding: utf-8 -*-

from setuptools import setup
setup(name="optimization",
      version="0.0.1",
      scripts=["optimization.py"],
      requires=["argparse", "pandas", "seaborn", "tqdm"],
      include_package_data=True,
      entry_points="""
        [console_scripts]
        optimization=optimization:run
    """)
