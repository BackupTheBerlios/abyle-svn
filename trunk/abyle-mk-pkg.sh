#!/bin/bash
. ./abyle-pkg.vars
echo "welcome to make a new abyle release"
echo .
echo .


if [ "$1" = "" ]
then 
echo "give \$1 a version string"
else
tar cvf abyle-pkg-"$1".tar $pkg_path/
tar rvf abyle-pkg-"$1".tar $abyle_install_script
bzip2 abyle-pkg-"$1".tar
fi
