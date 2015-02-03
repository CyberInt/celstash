#!/bin/bash

# exit on 1st error
set -e

find . -name '*.py[co]' -exec rm {} \;
flake8 celstash.py test_celstash.py
py.test --ignore=test-requirements.txt -v $@
