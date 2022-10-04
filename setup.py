import io

from setuptools import find_packages, setup


def long_description():
    with io.open('README.rst', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(
    name='relation-analysis-engine',
    version='0.0.1',
    description='2021 hanyang univ. relation analysis engine',
    long_description=long_description(),
    url='http://211.39.140.235/hanyang-univ-2021/relation-analysis-engine',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pykomoran==0.1.6.post1',
        'py4j==0.10.9.2',
        'pandas==1.3.5',
        'openpyxl==3.0.9',
        'torch==1.10.1',
        'transformers==4.15.0',
        'seqeval==1.2.2',
    ],
    zip_safe=False
)


