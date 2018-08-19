
from setuptools import setup, find_packages

setup(
    name='pyPC',
    version='0.0.1',
    description='Create a parallel coordinates graph from csv file',
    url='https://bitbucket.org/JuanluOnieva/pyParallelCoordinates',
    author='Juan L. Onieva',
    author_email='juanluonieva@uma.es',
    license='MIT',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3.6'
    ],
    packages=find_packages(exclude=["test.*", "tests"]),
)