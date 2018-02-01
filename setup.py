# -*- coding: utf-8 -*-
from codecs import open
from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

setup(
    name='pytistory',
    version='0.0.1',
    description="티스토리 블로그 api client입니다.",
    install_requires=[
        'flask',
        'requests'
    ],
    long_description=README,
    url='https://github.com/JeongUkJae/pytistory',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet :: WWW/HTTP :: Site Management',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

        'Operating System :: OS Independent',
    ],
    keywords='tistory blogging',
    packages=find_packages(exclude=['tests'])
)
