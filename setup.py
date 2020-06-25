#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'attrs==19.3.0',
    'importlib-metadata==1.6.1',
    'inflect==4.1.0',
    'jsonschema==3.2.0',
    'psycopg2-binary==2.8.5',
    'pyrsistent==0.16.0',
    'python-dotenv==0.13.0',
    'PyYAML==5.3.1',
    'simplejson==3.17.0',
    'six==1.15.0',
    'sqlacodegen==2.2.0',
    'SQLAlchemy==1.3.17',
    'sqlathanor==0.5.1',
    'validator-collection==1.4.2',
    'zipp==3.1.0'
 ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Vitor Avancini",
    author_email='vitor.avancini@indicium.tech',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An attempt to serialize and keep dashboards in a VCS",
    entry_points={
        'console_scripts': [
            'metabase_vcs=metabase_vcs.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='metabase_vcs',
    name='metabase_vcs',
    packages=find_packages(include=['metabase_vcs', 'metabase_vcs.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/techindicium/metabase_vcs',
    version='0.1.0',
    zip_safe=False,
)
