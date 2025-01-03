# utils.py
import json
import numpy as np

def read_config_file(config_file_name):
    
    with open(config_file_name, 'r') as f:
        config = json.load(f)
        
    return config 

def get_path(config_file_name):
    
    config_path_split = config_file_name.split('/')[:-1]
        
    config_path = ''
    
    for item in config_path_split:
        config_path += item + '/'
    
    return config_path

def decode_binary(binary_file, name_tag, waveform_length):
    
    config_path = get_path(binary_file)
    
    output_file_name = config_path + 'decoded_waveforms_'+name_tag+'.npy'
    
    waveform_length = int(waveform_length)
    
    data = np.fromfile(binary_file, dtype=np.int16)
    
    length_of_data = len(data)
        
    num_waveforms = length_of_data // waveform_length
    
    waveforms = np.zeros((num_waveforms, waveform_length))

    for i in range(num_waveforms):
        
        index_start = int(i*waveform_length)
        index_end = int((i+1)*waveform_length)
        
        waveforms[i] = data[index_start:index_end]
    
    # save the waveforms as a numpy file
    
    number_of_waveforms = len(waveforms)
    
    print("Number of waveforms: ", number_of_waveforms)
    
    np.save(output_file_name, waveforms)
    
    return output_file_name