try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import urllib
import netifaces
import os.path
import click
import sys
import re

# Import my classes
from classes import *

# File names variables
configFile = 'config.ini'
vendorFile = 'oui.py'
vendorOrigin = 'oui.txt'

def createFile(interface):
	config = ConfigParser()
	config.add_section('config')
	config.set('config', 'interface', interface)

	with open(configFile, 'w') as newConfigFile:
		config.write(newConfigFile)

	print "Configuration file created"
	print "Program restored"

def getInterfaces():
	netInterfaces = netifaces.interfaces()
	for item in netInterfaces:
		print item

def askForInterface():
	print "\nConfiguration file not found"
	print "This are the available interfaces, choose one."
	print "- - - - - - - - - - - - - - - - - -"
	getInterfaces()
	print "- - - - - - - - - - - - - - - - - -"
	interChoice = raw_input("\nWhich interface do you want to setup? ")
	createFile(interChoice)

def checkForConfiguration(update):
	if not os.path.isfile(configFile):
		print color.RED + "[x]" + color.END +" Configuration file"
		askForInterface()
	else:
		print color.OKBLUE + "["+u"\u2713]" + color.END +" Configuration file"

	if update:
		askForInterface()

def dlProgress(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\r" + vendorOrigin + " ========= -> %d%%" % percent)
	sys.stdout.flush()

def checkMacVendorFile():
	if not os.path.isfile(vendorFile):
		print color.RED + "["+u"\u00D7]" + color.END +" Mac Vendor File"
		getMacVendorFile()
	else:
		print color.OKBLUE + "["+u"\u2713]" + color.END +" Mac Vendor File"

def getMacVendorFile():
	# download oui.txt
	OUI_URL = "http://standards.ieee.org/develop/regauth/oui/oui.txt"
	print "Downloading from",OUI_URL
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
	print "\noui.py updated"

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

	print "\nChecking system config files"
	checkFiles(update)

	config = ConfigParser()
	config.read(configFile)

	# Save config file into the class
	interface.name = config.get('config', 'interface')

if __name__ == '__main__':
	main()
	
		