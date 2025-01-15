from setuptools import setup, find_packages

setup(
    name='e5nlp',
    version='0.1.0',
    author='Andrey Pshenitsyn',
    description='Bitrix24 nlp library',
    packages=find_packages(),
    install_requires=[
        'pymorphy3',
        'pydantic'
    ],
)