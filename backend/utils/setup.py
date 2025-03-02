# common_utils/setup.py
from setuptools import setup, find_packages

setup(
    name='common_utils',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'celery',  

    ],
    author='Lynn',
    author_email='linhlnt.work@gmail.com',
    description='Common utilities for this microservices system, including history logging functionality',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://your.repository.url',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
