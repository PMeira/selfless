from setuptools import setup
import subprocess

# Convert README.md to RST for PyPi -- copied from (CC0) https://github.com/dhimmel/hetio
# Thank you, Daniel Himmelstein (dhimmel)!

# Try to create an rst long_description from README.md
try:
    args = 'pandoc', '--to', 'rst', 'README.md'
    long_description = subprocess.check_output(args)
    long_description = long_description.decode()
except Exception as error:
    print('README.md conversion to reStructuredText failed. Error:')
    print(error)
    print('Setting long_description to None.')
    long_description = None

setup(
    name="selfless",
    description="""A small experimental module for implicit "self" support in Python (in some restricted contexts)""",
    author="Paulo Meira",
    author_email="10246101+PMeira@users.noreply.github.com",
    version='0.0.3',
    license="BSD",
    py_modules=['selfless'],
    zip_safe=True,
    long_description=long_description,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
#        'Programming Language :: Python :: Implementation :: PyPy', -- needs to be tested 
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
    ]
)

