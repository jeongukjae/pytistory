# -*- coding: utf-8 -*-
from codecs import open
from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

with open('pytistory/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if '__version__' in line:
            version = line.split("'")[1]

setup(
    name='pytistory',
    version=version,
    description="티스토리 블로그 api client입니다.",
    install_requires=[
        'Flask',
        'requests'
    ],
    long_description=README,
    url='https://github.com/JeongUkJae/pytistory',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet :: WWW/HTTP :: Site Management',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: OS Independent',
    ],
    keywords='tistory blogging',
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    tests_require=['nose']
)
