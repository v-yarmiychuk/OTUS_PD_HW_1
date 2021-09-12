from setuptools import find_packages
from setuptools import setup

setup(
    name='log_analyzer',
    version='',
    packages=find_packages(),
    url='',
    license='',
    author='v.yarmiychuk',
    author_email='v.yarmiychuk@gmail.com',
    description='Python Developer Professional  Log Analyzer',
    install_requires=[
        'PyYAML',
        'argcomplete',
    ],
    entry_points={
        'console_scripts': [
            'log_analyser = analyzer.entrypoint:run',
        ]
    },
)
