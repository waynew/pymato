#!/bin/sh

echo "Building latest version - did you remember a version bump?"
python3.6 setupy.py bdist_wheel sdist
echo "Uploading latest version"
twine upload dist/pymato-(grep version setup.py | awk -F= '{ print $2 }' | sed 's/[^0-9.]//g')*
