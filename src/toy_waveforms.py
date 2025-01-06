# toy_waveforms.py
import numpy as np
import statistics
import os
import matplotlib.pyplot as plt
from .filters import mean_absolute_deviation, getCMAFilter, level_threshold_bool, check_clipping_from_sample

def get_waveform_snippet(wf, onset_sample, pre_onset_samples, post_onset_samples):
    
    waveform_snippet = wf[onset_sample-pre_onset_samples:onset_sample+post_onset_samples]
    
    return waveform_snippet

def harvest_noise(waveforms, path_to_trace, name_tag, toy_waveform_params):
    
    num_noise_waveforms = toy_waveform_params['NUM_NOISE_WAVEFORMS']
    num_signal_waveforms = toy_waveform_params['NUM_SIGNAL_WAVEFORMS']
    level_threshold_sigma = toy_waveform_params['LEVEL_THRESHOLD_SIGMA']

    pre_onset_samples = toy_waveform_params['PRE_ONSET_SAMPLES']
    post_onset_samples = toy_waveform_params['POST_ONSET_SAMPLES']
    
    noise_waveforms, signal_waveforms = [], []
        
    # I need to comb through the raw waveforms to harvest noise traces
    
    for wf_i in waveforms:
        
        wf_np_i = np.array(wf_i) # convert the waveform to a numpy array for easier manipulation. Could cause speed bottle neck for larger files.
    
        # step 1: get the baseline estimate and the MAD
        
        mode_i = statistics.mode(wf_np_i)
        
        mad_i = mean_absolute_deviation(wf_np_i, mode_i)
        
        threshold_i = level_threshold_sigma * mad_i # recall that electron signals are negative polarity
        
        
        # baseline subtracted waveform
        
        wf_baseline_subtracted_i = wf_np_i - mode_i
        
        # reverse the polarity
        
        wf_baseline_subtracted_i = -1 * wf_baseline_subtracted_i
        
        

        # get indices about the threshold
        
        hit_bool, first_hit_sample = level_threshold_bool(wf_baseline_subtracted_i, threshold_i)
        
        
        if not hit_bool:
            
            noise_waveforms.append(wf_i)
            
        else:
                        
            clipping_bool = check_clipping_from_sample(first_hit_sample, len(wf_i), pre_onset_samples, post_onset_samples)
            
            # if there's NO clipping (clipping_bool == False) then we can consider this a signal waveform
            
            if not clipping_bool:
                
                # get the waveform snippet
                
                waveform_snippet = get_waveform_snippet(wf_baseline_subtracted_i, first_hit_sample, pre_onset_samples, post_onset_samples)
            
                signal_waveforms.append(waveform_snippet) 
        
        
        num_noise_waveforms_found = len(noise_waveforms)
        
        num_signal_waveforms_found = len(signal_waveforms)
        
        if (num_noise_waveforms_found == num_noise_waveforms and num_signal_waveforms_found == num_signal_waveforms):
            
            break
        
    # save the noise waveforms as a numpy file
    
    noise_waveform_file_name = path_to_trace + '/toy_waveforms/noise/noise_waveforms_'+name_tag+'.npy'    
    
    # make the signal template
    
    
    signal_waveforms = np.array(signal_waveforms)
    
    signal_template = np.mean(signal_waveforms, axis=0)
    
    signal_template_file_name = path_to_trace + '/toy_waveforms/noise/signal_template_'+name_tag+'.npy'
    
    
    # TODO check if the file already exists and ask the user if they want to overwrite it
    
    file_exist = os.path.exists(noise_waveform_file_name)
    
    if file_exist:
        
        print("The file: ", noise_waveform_file_name, " already exists.")
        
        user_input = input("Would you like to overwrite it? (y/n): ")
        
        if user_input.lower() == 'y':
            
            np.save(noise_waveform_file_name, noise_waveforms)
            
            np.save(signal_template_file_name, signal_template)
            
        else:
            
            print("The file will not be overwritten.")
            
    else:
        
        print("The file: ", noise_waveform_file_name, " does not exist. It will be created.")
    
        np.save(noise_waveform_file_name, noise_waveforms)
        
        np.save(signal_template_file_name, signal_template)

def make_toy_waveforms(path_to_trace, waveform_file_name, name_tag, toy_waveform_params):
    
    # open the output_file_name.npy file
    waveforms = np.load(waveform_file_name)
    
    
    # harvest the noise waveforms and make signal template
    harvest_noise(waveforms,  path_to_trace, name_tag, toy_waveform_params)
        
    
    # make the signal waveforms
        
        