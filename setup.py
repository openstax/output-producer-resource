from setuptools import setup
import os

HERE = os.path.abspath(os.path.dirname(__file__))

requirements = ["requests"]


def read_readme():
    with open(os.path.join(HERE, 'README.md')) as f:
        return f.read()


setup(
    name="output-producer-resource",
    version='1.0.0',
    description='Concourse CI resource for Content Output Producer Service (COPS)',
    long_description=read_readme(),
    url='https://github.com/openstax/output-producer-resource',
    author='OpenStax Content Engineering',
    license='AGPLv3.0',
    packages=['tests', 'src'],
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest',
            'pytest-vcr',
            'pytest-cov'
        ]
    },
    tests_require=['pytest', 'pytest-vcr'],
    test_suite='tests',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'check = src.check:main',
            'in = src.in_:main',
            'out = src.out:main',
        ]
    }
)
