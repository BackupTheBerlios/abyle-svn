#!/bin/bash
. ./abyle-pkg.vars
echo "welcome to make a new abyle release"
echo .
echo .

configpath_ok=0
while [ "$configpath_ok" -eq 0 ]
do

	echo -n "enter the configuration directory path ["$default_configpath"]: "
	read configpath

	if [ "$configpath" =  "" ]
	then
		configpath="$default_configpath"
	fi

	if [ -d $configpath ]
	then
		echo "$configpath, exists accepted"
		configpath_ok=1
	else
		echo "$configpath does not exist"
	fi

done

sbinpath_ok=0
while [ "$sbinpath_ok" -eq 0 ]
do

        echo -n "enter the installation path for the main python script ["$default_sbinpath"]: "
        read sbinpath

        if [ "$sbinpath" =  "" ]
        then
                sbinpath="$default_sbinpath"
        fi

	abylesbin="$sbinpath/$abyle_sbin_filename"
        if [ -r "$abylesbin" ]
        then
                echo "$abylesbin exists, accepted"
                sbinpath_ok=1
        else
                echo "$abylesbin does not exist"
        fi

done

pythonpath_ok=0
while [ "$pythonpath_ok" -eq 0 ]
do

        echo -n "enter where your python2.4 site-packages are located ["$default_python_sitepackagepath"]: "
        read python_sitepackagepath

        if [ "$python_sitepackagepath" =  "" ]
        then
                python_sitepackagepath="$default_python_sitepackagepath"
        fi

	abyle_python_sitepackagepath="$python_sitepackagepath/$abyle_sbin_filename"
        if [ -d "$abyle_python_sitepackagepath" ]
        then
                echo "$abyle_python_sitepackagepath exists, accepted"
                pythonpath_ok=1
        else
                echo "$abyle_python_sitepackagepath does not exist"
		echo $abyle_sbin_filename > "$python_sitepackagepath/$abyle_sbin_filename.pth"
        fi


done

rm -rf "$pkg_path"

mkdir "$pkg_path"
mkdir "$pkg_path/config"
mkdir "$pkg_path/sbin"
mkdir "$pkg_path/site-packages"

cp -r $configpath/* $pkg_path/config/
cp -r $configpath/.template $pkg_path/config/
cp -r $abylesbin $pkg_path/sbin/
cp -r $abyle_python_sitepackagepath/* $pkg_path/site-packages/
