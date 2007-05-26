#!/bin/bash

version="0.0.3"
progname="abyle"
srcpath="src"
pkgdir="$progname-pkg"

echo


backupUniqueString=`date +"%Y%m%d%H%M%S"`

toLower() {
  str=`echo $1 | tr "[:upper:]" "[:lower:]"`
} 

toUpper() {
  str=`echo $1 | tr "[:lower:]" "[:upper:]"` 
} 

get-distri-pathes() {

        case "$1" in
        debian)
		default_configpath='/etc/abyle'
		default_sbinpath='/usr/local/sbin'
		default_abyle_bin='abyle'
		default_python_sitepackagepath="/usr/local/lib/python"$python_version"/site-packages"
		default_backup_dir="/var/backups/$progname.$backupUniqueString/"
        ;;

        ubuntu)
                default_configpath='/etc/abyle'
                default_sbinpath='/usr/local/sbin'
                default_abyle_bin='abyle'
                default_python_sitepackagepath="/usr/local/lib/python"$python_version"/site-packages"
		default_backup_dir="/var/backups/$progname.$backupUniqueString/"
        ;;

        *)
                default_configpath='/etc/abyle'
                default_sbinpath='/usr/local/sbin'
                default_abyle_bin='abyle'
                default_python_sitepackagepath="/usr/local/lib/python"$python_version"/site-packages"
		default_backup_dir="/tmp/$progname.$backupUniqueString/"
        esac
	

}

get-distri-help() {

	case "$1" in
	debian)
	echo 
	echo
	echo "you are on debian use \"apt-get install python\" to install python"
	echo 
	echo
	;;

	ubuntu)
	echo
	echo
	echo "you are on ubuntu use \"apt-get install python\" to install python"
	echo
	echo
	;;

	*)
	echo
	echo
	echo "your distribution couldn't be determined read the documentation of your distribution for installing  python"
	echo
	echo
	esac
	

}

get-distri() {

	distributionType="unknown"

	if [ `cat /etc/issue |grep -i debian | wc -l` -eq 1 ]; then
		distributionType="debian"
	fi

	if [ `cat /etc/issue |grep -i ubuntu | wc -l` -eq 1 ]; then
		distributionType="ubuntu"
	fi

	return


}

check-python() {
	

	pythonInPathFound=`which python`
	#pythonInPathFound=""
	if [ "$pythonInPathFound" = "" ]; then
		echo "No python found in Path, python is a must for abyle, exiting."

		get-distri
		get-distri-help $distributionType

		exit 1
	else
		python_version=`python -V 2>&1 | sed 's:Python ::' | cut -d. -f1-2`
		python_version="2.5"
		echo "Python Version $python_version found."
	fi

}

install-abyle() {

	echo "Abyle Installation started."

	if [ "$UID" -ne "0" ]; then 
		echo "you must be root for installing abyle."
		exit 1
	fi


	check-python

	get-distri
	get-distri-pathes $distributionType

	#echo $python_version

### install python site-package modules

	pythonpath_ok=0
	pythonpath_overwrite_ok=0
	while [ "$pythonpath_ok" -eq 0 ]
	do
       		echo -n "Enter where your python$python_version site-packages are located ["$default_python_sitepackagepath"]: "
        	read python_sitepackagepath

        	if [ "$python_sitepackagepath" =  "" ]
        	then
                	python_sitepackagepath="$default_python_sitepackagepath"
        	fi

        	abyle_python_sitepackagepath="$python_sitepackagepath/$progname"
        	if [ -d "$abyle_python_sitepackagepath" ]
        	then
                	echo "$abyle_python_sitepackagepath already exists"

			overwritedir="n"	
			echo
			echo
			echo -n "do you want to overwrite this directory? [yN]"

			read overwritedir

			toLower "$overwritedir"
			overwritedir="$str"
			str=""

			if [ "$overwritedir" = "y" ]; then
				pythonpath_ok=1
				pythonpath_overwrite_ok=1
			fi
				
        	else
                	echo "$abyle_python_sitepackagepath accepted"
                	pythonpath_ok=1
        	fi
	done

### END install python site-package modules


### install abyle main script

	sbinpath_ok=0
	sbinpath_overwrite_ok=0
	while [ "$sbinpath_ok" -eq 0 ]
	do

        	echo -n "enter the installation path for the main python script ["$default_sbinpath"]: "
        	read sbinpath

        	if [ "$sbinpath" =  "" ]
        	then
                	sbinpath="$default_sbinpath"
        	fi

        	abylesbin="$sbinpath/$progname"
        	if [ -r "$abylesbin" ]
        	then
                	echo "$abylesbin already exists"

                        overwritebin="n"
                        echo
                        echo
                        echo -n "do you want to overwrite this file? [yN]"

                        read overwritebin

                        toLower "$overwritebin"
                        overwritebin="$str"
                        str=""

                        if [ "$overwritebin" = "y" ]; then
                                sbinpath_ok=1
				sbinpath_overwrite_ok=1
                        fi



        	else
                	echo "$abylesbin accepted"
                	sbinpath_ok=1
        	fi

	done

### END install abyle main script

### install config directory

	configpath_ok=0
	configpath_overwrite_ok=0
	configpath_keep=0
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


                        echo
                        echo
                        echo -n "do you want to overwrite this directory? [yN]"

                        read overwritedir
	
			if [ "$overwritedir" =  "" ]
			then
				overwritedir="n"
			fi

                        toLower "$overwritedir"
                        overwritedir="$str"
                        str=""

                        if [ "$overwritedir" = "y" ]; then
                                configpath_ok=1
				configpath_overwrite_ok=1
                        fi

			if [ "$overwritedir" = "n" ]; then
			
				echo
				echo	
				echo -n "do you want to keep your config directory? [Yn]"

				read keepdir

				if [ "$keepdir" =  "" ]
				then
					keepdir="y"
				fi

				toLower "$keepdir"
				keepdir="$str"
				str=""

				if [ "$keepdir" = "y" ]; then
					configpath_ok=1
					configpath_keep_ok=1
				fi

			fi	




        	else
                	echo "$configpath accepted"
                	configpath_ok=1
        	fi

	done

### END install config directory


### do the install job

## site-packages

	if [ "$pythonpath_overwrite_ok" -eq "1" ]; then

		echo "deleting directory: $abyle_python_sitepackagepath."
		rm -rf $abyle_python_sitepackagepath

		echo "copying new files to: $abyle_python_sitepackagepath."
		mkdir $abyle_python_sitepackagepath/
		cp -r $srcpath/site-packages/* $abyle_python_sitepackagepath/
		echo $progname > "$python_sitepackagepath/$progname.pth"

	else
	
		echo "copying new files to: $abyle_python_sitepackagepath."
		mkdir $abyle_python_sitepackagepath/
		cp -r $srcpath/site-packages/* $abyle_python_sitepackagepath/
		echo $progname > "$python_sitepackagepath/$progname.pth"

	fi

## abyle bin

	if [ "$sbinpath_overwrite_ok" -eq "1" ]; then
	
		echo "deleting file: $abylesbin."
		rm -rf $abylesbin

		echo "copying new abyle file to: $abylesbin"
		cp $srcpath/sbin/$progname $abylesbin

	else

		echo "copying new abyle file to: $abylesbin"
		cp $srcpath/sbin/$progname $abylesbin
	fi

## config

	if [ "$configpath_keep_ok" -eq "1" ]; then
		echo "keeping your config directory: $configpath."

	else


	if [ "$configpath_overwrite_ok" -eq "1" ]; then

		echo "backuping config files to: $default_backup_dir." 
		mkdir $default_backup_dir
		mv $configpath/* $default_backup_dir
		echo "deleting directory: $configpath"
		rm -rf $configpath

		echo "copying default config to: $configpath"
		mkdir $configpath
		cp -r $srcpath/config/* $configpath/

	else

		echo "copying default config to: $configpath"
		mkdir $configpath
		cp -r $srcpath/config/* $configpath/
	fi

	fi

	echo "all files should reside on the right place now"	

}

collect-abyle() {

	check-python
	get-distri
	get-distri-pathes $distributionType


### collect python site-packages directory

	pythonpath_ok=0
	default_python_sitepackagepath="$default_python_sitepackagepath/abyle"
	while [ "$pythonpath_ok" -eq 0 ]
	do
        echo -n "where are your abyle python site-packages?  ["$default_python_sitepackagepath"]: "
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
        fi


	done

### collect abyle python script

	sbinpath_ok=0
	while [ "$sbinpath_ok" -eq 0 ]
	do

        	echo -n "where is the abyle main script? ["$default_sbinpath"]: "
        	read sbinpath

        	if [ "$sbinpath" =  "" ]
        	then
                	sbinpath="$default_sbinpath"
        	fi

        	abylesbin="$sbinpath/$progname"
        	if [ -r "$abylesbin" ]
        	then
                	echo "$abylesbin exists, accepted"
                	sbinpath_ok=1
        	else
                	echo "$abylesbin does not exist"
        	fi

	done

### collect config template directory

	configpath_ok=0
	while [ "$configpath_ok" -eq 0 ]
	do

        	echo -n "where is your configuration template directory? ["$default_configpath/template"]: "
        	read configpath

        	if [ "$configpath" =  "" ]
        	then
                	configpath="$default_configpath/template"
        	fi

        	if [ -d $configpath ]
        	then
                	echo "$configpath, exists accepted"
                	configpath_ok=1
        	else
                	echo "$configpath does not exist"
        	fi

	done


### do the collect

	rm -rf "$pkgdir"
	mkdir "$pkgdir"

	mkdir "$pkgdir"/"$srcpath"
	
	mkdir "$pkgdir/$srcpath/config"
	mkdir "$pkgdir/$srcpath/config/template"
	mkdir "$pkgdir/$srcpath/sbin"
	mkdir "$pkgdir/$srcpath/site-packages"	

	cp -r $configpath/* "$pkgdir/$srcpath/config/template"
	cp $abylesbin $pkgdir/$srcpath/sbin/
	cp -r $abyle_python_sitepackagepath/* $pkgdir/$srcpath/site-packages/
	cp $0 $pkgdir/

}

tarIt() {

	if [ "$1" = "" ]; then
		pkgVersion=`date +"%Y%m%d_%H%M"`
	else
		pkgVersion=$1

	fi

	if [ -d $pkgdir ]; then

		tar cf $progname-"$pkgVersion".tar $pkgdir/
		bzip2 $progname-"$pkgVersion".tar

		if [ -f $progname-"$pkgVersion".tar.bz2 ]; then
	
			echo "$progname-$pkgVersion.tar.bz2 created."

		else
	
			echo "tar.bz2 generation failed."

		fi
		

	fi


}


case "$1" in
install)
install-abyle
;;

mkpkg)
collect-abyle
tarIt $2
;;

uninstall)
echo "not done yet."
exit 1
uninstall-abyle
;;

*)

echo "Welcome to abyle firewall-script installer! (v$version)"
echo
echo "License Terms:"
echo "
Copyright (C) 2005  Stefan Nistelberger (scuq@gmx.net)
abyle firewall
abyle - python iptables config script

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

http://www.gnu.org/licenses/gpl.txt
"
echo
echo
echo


echo $"Usage: $0 {install|mkpkg <version>|uninstall}"
esac

