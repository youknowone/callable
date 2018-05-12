from __future__ import with_statement

from setuptools import setup
import sys

install_requires = [
]
tests_require = [
    'pytest>=3.0.2', 'pytest-cov',
]

if sys.version_info[0] == 2:
    install_requires.extend([
        'inspect2',
    ])

if sys.version_info[:2] == (3, 3):
    tests_require.extend([
        'asyncio',
    ])

if sys.version_info >= (3, 3):
    if sys.version_info < (3, 5):
        tests_require.append('pytest-asyncio==0.5.0')
    else:
        tests_require.append('pytest-asyncio')


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='callable',
    version='0.2.0',
    description='Deprecated. Use `inspect.signature`.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='callable@youknowone.org',
    url='https://github.com/youknowone/callable',
    py_modules=(
        'callable',
    ),
    install_requires=install_requires,
    tests_require=tests_require + ['tox', 'tox-pyenv'],
    extras_require={
        'tests': tests_require,
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)  # noqa
