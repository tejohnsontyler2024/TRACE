import numpy as np
import sys 

def main():
	
	#This is the main function for the TRACE codebase 
 
	# The command line prompt should be in the form:
	# python3 main.py <config_file.json> <data_file.dat>
 
 
	# parse the command line argument
 
	args = sys.argv[1:]
 
	if len(args) != 2:
     
		print("Usage: python3 main.py <config_file.json> <data_file.dat>")
		sys.exit(1)
  
	config_file = args[0]
 
	data_file = args[1]
 
 
 
	# Load the configuration file json 
	
if __name__ == "__main__":
	main()