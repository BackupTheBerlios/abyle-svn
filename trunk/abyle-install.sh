#!/bin/bash

echo "Welcome to abyle firewallscript installer!"
echo .
echo "License Terms:"
echo"
# Copyright (C) 2005  Stefan Nistelberger (scuq@gmx.net)
# abyle firewall
# abyle - python iptables config script
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# http://www.gnu.org/licenses/gpl.txt
"
echo .
echo .
echo .

default_configpath='/etc/abyle'
default_sbinpath='/usr/local/sbin'
default_python_sitepackagepath='/usr/local/lib/python2.4/site-packages'

abyle_sbin_filename='abyle'
pkg_path='./abyle-pkg'

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
		echo "$configpath already exists"
	else
		echo "$configpath accepted"
		configpath_ok=1
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
                echo "$abylesbin already exists"
        else
                echo "$abylesbin accepted"
                sbinpath_ok=1
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
                echo "$abyle_python_sitepackagepath already exists"
        else
                echo "$abyle_python_sitepackagepath accepted"
                pythonpath_ok=1
        fi


done

mkdir $configpath
mkdir $abylesbin
mkdir $abyle_python_sitepackagepath
echo $abyle_sbin_filename > "$python_sitepackagepath/$abyle_sbin_filename.pth"

cp -r $pkg_path/config/* $configpath/
cp -r $pkg_path/sbin/$abyle_sbin_filename $abylesbin/
cp -r $pkg_path/site-packages/* $abyle_python_sitepackagepath/

echo "all files should reside on the right place now"
