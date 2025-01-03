import numpy as np
import sys 

# from src.utils import *
from src.utils import read_config_file, decode_binary
from src.toy_waveforms import make_toy_waveforms

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
 
	path_to_trace = config['PATH_TO_TRACE']
 
	data_file_name = path_to_trace+'/data/'+config['DATA_FILE']
	waveform_length = config['WAVEFORM_LENGTH']
	name_tag = config['NAME_TAG']
	processes = config['PROCESSES']
 
	binary_parser_bool = processes['BINARY_PARSER']
	make_toy_waveform_bool = processes['MAKE_TOY_WAVEFORMS']
 
	print("Reading data file: ", data_file_name)
	print("Waveform length: ", waveform_length)
 
	# now we will decode the binary file. 
	# Rather than keep in memory, it will be saved as a numpy file.
 
	if binary_parser_bool:
		output_file_name = decode_binary(data_file_name, name_tag, waveform_length)
  
  
	# now we will make a toy waveform if the user wants to.
	if make_toy_waveform_bool:
		print("Making toy waveforms")
  
		# get the toy waveform parameters from the config file
  
		toy_waveform_params = config['TOY_WAVEFORM_PARAMS']
  
		num_noise_waveforms = toy_waveform_params['NUM_NOISE_WAVEFORMS']
		num_signal_waveforms = toy_waveform_params['NUM_SIGNAL_WAVEFORMS']
		level_threshold_sigma = toy_waveform_params['LEVEL_THRESHOLD_SIGMA']
  
		make_toy_waveforms(path_to_trace, output_file_name, level_threshold_sigma, num_signal_waveforms, num_noise_waveforms, name_tag)
	
if __name__ == "__main__":
	main()