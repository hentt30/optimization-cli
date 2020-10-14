# -*- coding: utf-8 -*-

from setuptools import setup
setup(name="optimization",
      version="0.0.1",
      author="Henrique Fernandes",
      author_email="hentt30@gmail.com",
      description ='Package for optimize parameters of vasp', 
      license ='MIT', 
      scripts=[
          "optimization.py", "encut.py", "kpoints.py", "lattice_constant.py",
          "parser.py"
      ],
      install_requires=["argparse", "pandas", "tqdm", "matplotlib"],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'optimization = optimization:run',
          ],
      })
