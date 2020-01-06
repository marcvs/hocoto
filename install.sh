#!/bin/bash

PIP=`which pip3`
test -z $PIP && {
    PIP=`which pip`
    test -z $PIP && {
        echo -e "pip not found.\n    =>  apt-get install python3-pip"
        exit 1
    }
}

echo "pip: ${PIP}"


# test -d dist && {
#     echo "You should remove the dist dir first"
#     exit 1
# }

echo "Building sdist"
python3 setup.py sdist  > build.log 2>&1

FULLNAME=`python3 setup.py --fullname`

echo -e "Done building ${FULLNAME}\n"

echo "Installing ${FULLNAME}"

${PIP} install dist/${FULLNAME}*tar.gz


