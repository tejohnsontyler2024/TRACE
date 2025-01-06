# toy_waveforms.py
import numpy as np
import statistics
import os
import matplotlib.pyplot as plt
from .filters import mean_absolute_deviation, getCMAFilter, level_threshold_bool

def harvest_noise(waveforms, level_threshold, num_signal_waveforms, num_noise_waveforms, path_to_trace, name_tag):
    
    noise_waveforms, signal_waveforms = [], []
        
    # I need to comb through the raw waveforms to harvest noise traces
    
    for wf_i in waveforms:
        
        wf_np_i = np.array(wf_i) # convert the waveform to a numpy array for easier manipulation. Could cause speed bottle neck for larger files.
    
        # step 1: get the baseline estimate and the MAD
        
        mode_i = statistics.mode(wf_np_i)
        
        mad_i = mean_absolute_deviation(wf_np_i, mode_i)
        
        threshold_i = level_threshold * mad_i # recall that electron signals are negative polarity
        
        
        # baseline subtracted waveform
        
        wf_baseline_subtracted_i = wf_np_i - mode_i
        
        # reverse the polarity
        
        wf_baseline_subtracted_i = -1 * wf_baseline_subtracted_i
        
        

        # get indices about the threshold
        
        hit_bool = level_threshold(wf_baseline_subtracted_i, threshold_i)
        
        
        if not hit_bool:
            
            noise_waveforms.append(wf_i)
            
        else:
            
            signal_waveforms.append(wf_i) 
        
        
        num_noise_waveforms_found = len(noise_waveforms)
        
        num_signal_waveforms_found = len(signal_waveforms)
        
        if (num_noise_waveforms_found == num_noise_waveforms and num_signal_waveforms_found == num_signal_waveforms):
            
            break
        
    # save the noise waveforms as a numpy file
    
    noise_waveform_file_name = path_to_trace + '/toy_waveforms/noise/noise_waveforms_'+name_tag+'.npy'
    
    signal_waveform_file_name = path_to_trace + '/toy_waveforms/signals/signal_waveforms_'+name_tag+'.npy'
    
    # TODO check if the file already exists and ask the user if they want to overwrite it
    
    file_exist = os.path.exists(noise_waveform_file_name)
    
    if file_exist:
        
        print("The file: ", noise_waveform_file_name, " already exists.")
        
        user_input = input("Would you like to overwrite it? (y/n): ")
        
        if user_input.lower() == 'y':
            
            np.save(noise_waveform_file_name, noise_waveforms)
            
            np.save(signal_waveform_file_name, signal_waveforms)
            
        else:
            
            print("The file will not be overwritten.")
            
    else:
        
        print("The file: ", noise_waveform_file_name, " does not exist. It will be created.")
    
        np.save(noise_waveform_file_name, noise_waveforms)
        
        np.save(signal_waveform_file_name, signal_waveforms)

def make_toy_waveforms(path_to_trace, waveform_file_name, level_threshold, num_signal_waveforms, num_noise_waveforms, name_tag):
    
    # open the output_file_name.npy file
    waveforms = np.load(waveform_file_name)
    
    
    # harvest the noise waveforms
    harvest_noise(waveforms, level_threshold, num_signal_waveforms, num_noise_waveforms, path_to_trace, name_tag)
        
        
        
        