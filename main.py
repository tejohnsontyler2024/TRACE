import numpy as np
import sys 

# from src.utils import *
from src.utils import read_config_file, decode_binary

def main():
	
	#This is the main function for the TRACE codebase 
 
	# The command line prompt should be in the form:
	# python3 main.py <config_file.json> 
 
 
	# parse the command line argument
 
	args = sys.argv[1:]
 
	if len(args) != 1:
     
		print("Usage: python3 main.py <config_file.json>")
		sys.exit(1)
  
	config_file = args[0]
 
	print("Reading configuration file: ", config_file)
 
 
	# Load the configuration file json 
 
	config = read_config_file(config_file)
 
	data_file_name = config['DATA_FILE']
	waveform_length = config['WAVEFORM_LENGTH']
	processes = config['PROCESSES']
 
	binary_parser_bool = processes['BINARY_PARSER']
	make_toy_waveform_bool = processes['MAKE_TOY_WAVEFORMS']
 
	print("Reading data file: ", data_file_name)
	print("Waveform length: ", waveform_length)
 
	# now we will decode the binary file. 
	# Rather than keep in memory, it will be saved as a numpy file.
 
	if binary_parser_bool:
		output_file_name = decode_binary(data_file_name, waveform_length)
  
  
  
	# now we will make a toy waveform if the user wants to.
	if make_toy_waveform_bool:
		print("Making toy waveforms")
  
		# get the toy waveform parameters from the config file
  
		toy_waveform_params = config['TOY_WAVEFORM_PARAMS']
  
		num_noise_waveforms = toy_waveform_params['NUM_NOISE_WAVEFORMS']
		num_signal_waveforms = toy_waveform_params['NUM_SIGNAL_WAVEFORMS']
  
  
		# make_toy_waveform()
	
if __name__ == "__main__":
	main()