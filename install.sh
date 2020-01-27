#!/bin/bash

PIP=`which pip3`
test -z $PIP && {
    PIP=`which pip`
    test -z $PIP && {
        echo -e "pip not found.\n    =>  apt-get install python3-pip"
        exit 1
    }
}


echo "pip version used: ${PIP}"

FULLNAME=`python3 setup.py --fullname`
NAME=`python3 setup.py --name`



# test -d dist && {
#     echo "You should remove the dist dir first"
#     exit 1
# }

echo "Building sdist"
python3 setup.py sdist  > build.log 2>&1

echo -e "Done building ${FULLNAME}\n"

echo "Uninstalling old version of ${NAME}"
${PIP} uninstall -y ${NAME}

echo -e "\nInstalling ${FULLNAME}"
${PIP} install -U dist/${FULLNAME}*tar.gz

