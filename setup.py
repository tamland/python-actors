from setuptools import setup

install_requires = ['six']

long_description = ""
with open('README.rst') as f:
    long_description += f.read()

with open('HISTORY.rst') as f:
    long_description += f.read()


setup(
    name='actors',
    version='0.5.1b1',
    author='Thomas Amland',
    author_email='thomas.amland@googlemail.com',
    url='https://github.com/tamland/python-actors/',
    description='Lightweight actor framework with supervision',
    long_description=long_description,
    license='Apache License 2.0',
    packages=['actors'],
    install_requires=install_requires,
    keywords=['actors', 'reactive', 'concurrent', 'threading', 'message passing', 'asynchronous'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy ',
        'Topic :: Software Development :: Libraries',
    ])
