from setuptools import setup, find_packages, Extension

setup(name='mimcvdf',
      version='1.1.0',
      description='Generic high level VDF using MiMC',
      author='Kevin Froman',
      author_email='beardog@mailbox.org',
      url='https://www.chaoswebs.net/',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[],
      ext_package="mimcvdf",
      ext_modules=[
        Extension('mimc.native', ['mimcvdf/mimc/native.c'],
                  libraries=['gmp'], optional=True,
                  extra_compile_args=['-O2'])
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ],
     )
