#!/bin/sh

echo "Building latest version - did you remember a version bump?"
python3.6 setup.py bdist_wheel sdist
echo "Uploading latest version"
twine upload dist/pymato-$(python3 pymato.py version | awk '{ print $2 }')*
