#!/bin/bash
#-SEEING IF THE PORTS ARE OPEN-#
FastScan()
{
	temp=$(nc -zv -w 5 $1 $2 2>&1 | grep "open")
	if [[ -z "$temp" ]]; then
		continue
	else
		if [[ $(echo "$temp" | awk '{print $1}') == "(UNKNOWN)" ]]; then
			$(echo "$temp" | awk '{print $3}') >> $3
			$(echo "$temp" | awk '{print $4}' | awk -F '[()]' '{print $2}') >> $3
		else
			$(echo "$temp" | awk '{print $2}') >> $3
			$(echo "$temp" | awk '{print $3}' | awk -F '[()]' '{print $2}') >> $#
		fi
	fi
}
ScanPorts()
{
	touch tempFile
	#A VARIABLE FOR HOLDING OPEN PORTS AND SERVICES#
	local returnArray=()
	#SCANNING THE IP TO SEE THE OPEN PORTS AND SERVICES#
	local smlPortsToScan=(7 9 13 21 22 23 25 26 37 53 79 80 81 88 106 110 111 113 119 135 139 143 144 179 199 389 427 443 444 445 465 513 514 515 543 544 548 554 587 631 646 873 990 993 995 1025 1026 1027 1028 1029 1110 1433 1720 1723 1755 1900 2000 2001 2049 2121 2717 3000 3128 3306 3389 3986 4899 5000 5009 5051 5060 5101 5109 5357 5432 5631 5666 5800 5900 6000 6001 6646 7070 8000 8008 8009 8080 8081 8443 8888 9100 9999 10000 32768 49152 49153 49154 49155 49156 49157)
	#LOOPING THROUGH THE PORTS#
	for port in ${smlPortsToScan[@]}; do
		FastScan $1 $port tempFile &
	done
	wait
	cat tempFile
}

echo " _____                        ___"
echo "| ____|_ __ _ __ _____  __   ( _ )"
echo "|  _| | '__| '__/ _ \\ \\/ /   / _ \\"
echo "| |___| |  | | | (_) >  <   | (_) |"
echo "|_____|_|  |_|  \___/_/\\_\\___\\___/ "
echo "                        |_____|"
#-STARTUP LOGIC, USED TO FIND WHAT MODE THE SCRIPT WILL RUN IN-#
if [[ $# == 0 ]]; then
	echo "Enter the ip you wish to scan"
	read -p ">" target
	echo "What type of scan do you want to do"
	echo "small, medium, large, or type a port number (sm/md/lr/(port number))"
	read -p ">" port
	echo "Get service info (y/n)"
	read -p ">" Yn
	if [[ $Yn == 'y' ]]; then
		ScanPorts $target $port 1
	else
		ScanPorts $target $port
	fi
elif [[ $1 == "-help" ]]; then
	#HELP PAGE FOR USERS#
	echo "WARNING!"
	echo "THIS FILE IS OPTIMIZED FOR LAN NETWORKS AND HAS NOT BEEN TESTED ON ANY WLAN NETWORKS OR FORIN IPS"
	echo "THIS FILE HAS ONLY BEEN TESTEN ON THE eth0 INTERFACE AND NONE OTHERS, BE SURE TO CHANGE IF NEEDED"
	echo "Programed by: That1EthicalHacker"
	echo "Errox_8.sh is a script for port scanning, this will not replace nmap but is anoter option for those who want to use just bash"
	echo "Simply run the script and answer the prompts, and the script will do the rest"
	echo "If you encounter a problem, or want something added, add it to github.com/vel2006/Errox_8"
	echo "Happy pentesting"
else
	#FIRST TIME?#
	echo "Run './Errox_7Server.sh -help' or read 'README.md' for assistance"
fi
