try:
	from configparser import ConfigParser
except ImportError:
	from ConfigParser import ConfigParser

import urllib
import netifaces
import os
import os.path
import click
import sys
import re
import platform
import subprocess

# Import my classes
from classes import *

# File names variables
configFile = 'config.ini'
vendorFile = 'oui.py'
vendorOrigin = 'oui.txt'

def which(program):
	"""Determines whether program exists"""
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

def createFile(interface):
	config = ConfigParser()
	config.add_section('config')
	config.set('config', 'interface', interface)

	with open(configFile, 'w') as newConfigFile:
		config.write(newConfigFile)

	print ("Configuration file created")
	print ("Program restored")

def getInterfaces():
	netInterfaces = netifaces.interfaces()
	for item in netInterfaces:
		print (item)

def askForInterface():
	print ("\nConfiguration file not found")
	print ("This are the available interfaces, choose one.")
	print ("- - - - - - - - - - - - - - - - - -")
	getInterfaces()
	print ("- - - - - - - - - - - - - - - - - -")
	interChoice = raw_input("\nWhich interface do you want to setup? ")
	createFile(interChoice)

def checkForConfiguration(update):
	if not os.path.isfile(configFile):
		print ("[x] Configuration file")
		askForInterface()
	else:
		print ("[<] Configuration file")

	if update:
		askForInterface()

def dlProgress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\r" + vendorOrigin + " ========= -> %d%%" % percent)
	sys.stdout.flush()

def checkMacVendorFile():
	if not os.path.isfile(vendorFile):
		print ("[x] Mac Vendor File")
		getMacVendorFile()
	else:
		print ("[<] Mac Vendor File")

def fileToMacSet(path):
	with open(path, 'r') as f:
		maclist = f.readlines()
	return set([x.strip() for x in maclist])

def getMacVendorFile():
	# download oui.txt
	OUI_URL = "http://standards.ieee.org/develop/regauth/oui/oui.txt"
	print ("Downloading from " + OUI_URL)
	urllib.urlretrieve(OUI_URL, vendorOrigin, reporthook=dlProgress)

	# open file and rewrite
	f = open(vendorFile,'w')
	f.write('# -*- coding: utf-8 -*-\noui = {\n')

	# parsing oui.txt data
	with open(vendorOrigin) as infile:
		for line in infile:
			if re.search("(hex)", line):
				try:
					mac, vendor = line.strip().split("(hex)")
				except:
					mac = vendor = ''

				n = '\t"%s": ' % mac.strip().replace("-",":").lower()
				n += '"%s",\n' % vendor.strip().replace("'","`")
				f.write(n)

	f.write('}')

	# close file
	f.close()

	# Remove the temp oui.txt file
	os.remove(vendorOrigin)
	print ("\noui.py updated")

def checkFiles(update):
	checkForConfiguration(update)
	checkMacVendorFile()

@click.command()
@click.option('-u','--update', is_flag=True, help='Enables interface select modification')
def main(update):
	print('''
	 _       ___ _____                          _ __            
	| |     / (_) __(_)  ____ ___  ____  ____  (_) /_____  _____
	| | /| / / / /_/ /  / __ `__ \/ __ \/ __ \/ / __/ __ \/ ___/
	| |/ |/ / / __/ /  / / / / / / /_/ / / / / / /_/ /_/ / /    
	|__/|__/_/_/ /_/  /_/ /_/ /_/\____/_/ /_/_/\__/\____/_/     
                                                            
     ''')

	print ("\nChecking system config files")
	checkFiles(update)

	config = ConfigParser()
	config.read(configFile)

	# Save config file into the class
	interface.name = config.get('config', 'interface')

	tshark = which("tshark")
	#try:
	#	tshark = which("tshark")
	#except:
	#		if platform.system() != 'Darwin':
	#		print('tshark not found, install using\n\napt-get install tshark\n')
	#	else:
	#		print('wireshark not found, install using: \n\tbrew install wireshark')
	#		print('you may also need to execute: \n\tbrew cask install wireshark-chmodbpf')
	#	sys.exit(1)

	print("Using %s interface and scanning for %s seconds..." % (interface.name, interface.scantime))

	dump_file = "C:\Users\mikel\Documents\wifimonitor\wifimonitor"
	
	# Read tshark output
	#command = [tshark, '-r', dump_file, '-T', 'fields', '-e', 'wlan.sa', '-e', 'wlan.bssid', '-e', 'radiotap.dbm_antsignal']
	targetmacs = ''
	command = 'tshark -i Wi-Fi'
	run_tshark = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

	print run_tshark.returncode
	#output, nothing = run_tshark.communicate()

    # read target MAC address
	targetmacset = set()
	if targetmacs != '':
		targetmacset = fileToMacSet(targetmacs)

	foundMacs = {}
	for line in output.decode('utf-8').split('\n'):
		if line.strip() == '':
			continue
		mac = line.split()[0].strip().split(',')[0]
		dats = line.split()
		if len(dats) == 3:
			if ':' not in dats[0] or len(dats) != 3:
				continue
			if mac not in foundMacs:
				foundMacs[mac] = []
			dats_2_split = dats[2].split(',')
			if len(dats_2_split) > 1:
				rssi = float(dats_2_split[0]) / 2 + float(dats_2_split[1]) / 2
			else:
				rssi = float(dats_2_split[0])
			foundMacs[mac].append(rssi)

	if not foundMacs:
		print("Found no signals, are you sure %s supports monitor mode?" % adapter)
		sys.exit(1)

if __name__ == '__main__':
	main()
	
		