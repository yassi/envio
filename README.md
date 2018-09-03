# envio
Environment variable parser library for python.

Mostly created as a reference for how basic package creation works. Many
similar projects exist; the goal of this one to make the most basic
implementation possible and also establish the minimum amount of boilerplate
to create a package for submission.

## Installation

run `pip install envio`

## Usage

Basic usage

```python
import envio

# Fetch the envirnment variable MYARG and use value 'yay' if not found
MYARG = envio.get_var('MYARG', default='yay')

# If a default is not specified, then an exception will be raised if the
# environment variable does not exist. This is how we can specify required
# variables.
MYARG = envio.get_var('MYARG') # MYARG is required
```

Environment variables can also be coerced into multiple different types

```python
# coerce required variable MYINT into an integer
MYINT = envio.get_var('MYINT', var_type=int)

MYFLOAT = envio.get_var('MYFLOAT', var_type=float)

# Acceptable inputs for boolean values include:
# case insensitive versions of 'true' and 'false'
# case insensitive words 'on' and 'off'
# '1' and '0'
# case insensitive letters 't' and 'f'
MYBOOL = envio.get_var('MYBOOL', var_type=bool)

# Dictionaries are also supported but require the environment variable to be
# a valid json string. Below is an example of how to specify a simple dict
# through a json string.
MYDICT = envio.get_var('MYDICT', var_type='json', default='{"hello": "world"}')
```

Variables can also be coerced into lists by using the *many=True* argument.

```python
# e.g MYLIST <-- '1,hello, 7, 12.0'
# the following will parse as
# MYLIST = ['1', 'hello', '7', '12.0']
MYLIST = envio.get_var('MYLIST', many=True)

# list parsing can be combined with type coercion. This will enforce that
# every member of the list be parsed as 'var_type'.
MYINTS = envio.get_var('MYINTS', var_type=int, many=True)

# The delimmiter used for parsing lists defaults to a comma, but it can be
# changed with an optional 'delimmiter' param.
MYINTS = envio.get_var('MYINTS', var_type=int, many=True, delimmiter='||', default='1||2||3')

# using 'var_type'=json also allows the parsing of integers, lists of integers
# and the like. It allows mixed types in lists and should be used carefully.
# the example below will produce [1, 2, '3']
MYLIST = envio.get_var('MYLIST', var_type='json', default='[1, 2, "3"]')
```

Default values can only be **STRING** values. This is done so that even the
default value we choose has to go through the same parser as if we had gotten
it as an environment variable. This avoids a class of errors where an
incompatible default can be chosen. e.g. expecting a integer but defaulting
to a boolean.

```python
# this is the correct way to specify a default for a list of integers
MYINTS = envio.get_var('MYINTS', var_type=int, many=True, default='1,2,3')
```

## Development

You'll want to clone the package somewhere and have either pipenv or virtualenv available on your environment.

A *Pipfile* is included in this project. It comes mostly with packages used
to run *twine* - the utility used to submit packages to pypi. It can also be
used to install this project's distributions locally.

All commands assume the working directory is the repo root.

```bash
# install a virtual env and the pipfile requirements.
pipenv install
# activate the virtualenv in the shell. All commands should be run after this
# activation
pipenv shell

# builds can be generated like so:
python setup.py sdist bdist_wheel

# builds can then be submitted to pypi using twine like so:

# upload to test pypi
twine upload --repository-url  https://test.pypi.org/legacy/ dist/*

# upload to the actual pypi servers.
twine upload --repository-url  https://upload.pypi.org/legacy/ dist/*

# tests can be run using setup.py as well
python setup.py test
```
