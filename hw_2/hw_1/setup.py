from setuptools import setup, find_packages

setup(name='fibonacci-ast-gen',
      version='1.2',
      package_dir={"": "src"},
      packages=find_packages(where='src'),
      python_requires=">=3.6",
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent", ])
