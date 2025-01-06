# toy_waveforms.py
import numpy as np
import statistics
import os
import matplotlib.pyplot as plt
from .filters import mean_absolute_deviation, getCMAFilter, level_threshold_bool, check_clipping_from_sample, SG_filter
from .fitting import fit_baseline_with_gaussian, fit_waveform

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
    
    # baseline subtract the signal template
    # fit the template with a gaussian
    
    baseline_fitted = fit_baseline_with_gaussian(signal_template)
    
    signal_template = signal_template - baseline_fitted
    
    # replace negatives with zeros
    
    signal_template[signal_template < 0] = 0
    
    
    # fit the waveform with the Xiao equation
    
    # fit_waveform(signal_template)
    
    
    # area normalize the signal template
    
    signal_template = signal_template / np.sum(signal_template)
    
    
    signal_template_file_name = path_to_trace + '/toy_waveforms/signals/signal_template_'+name_tag+'.npy'
    
    
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
        
    return noise_waveform_file_name, signal_template_file_name

def sample_pdf_n_times(pdf, pdf_x_axis, num_samples, onset_sample, noise_wf_i):
        
    for i in range(num_samples):
        
        sample = np.random.choice(pdf_x_axis, p=pdf)
        
        try:
        
            noise_wf_i[sample+onset_sample] -= 1 # subtract because the polarity of the raw waveforms is negative
            
        except IndexError:
            
            continue
    
    return noise_wf_i

def generate_toy_waveform(waveform_length, onset_sample, integral, signal_template, noise_wf_i):
    
    # make a blank template that is the length of the waveform
        
    signal_waveform_x_axis = np.arange(0, len(signal_template))
    
    
    # randomly sample the signal template
    
    integral_int, onset_sample_int = int(integral), int(onset_sample)
    
    signal_waveform = sample_pdf_n_times(signal_template, signal_waveform_x_axis, 
                                         integral_int, onset_sample_int, 
                                         noise_wf_i)
    
    
    return signal_waveform

def generate_integral_onset_values(toy_waveform_params):
    
    true_integral_min = toy_waveform_params['TRUE_INTEGRAL_MIN']
    true_integral_max = toy_waveform_params['TRUE_INTEGRAL_MAX']
    
    true_onset_min = toy_waveform_params['TRUE_ONSET_MIN']
    true_onset_max = toy_waveform_params['TRUE_ONSET_MAX']
    
    num_toy_waveforms = toy_waveform_params['NUM_TOY_WAVEFORMS']
    
    
    integrals = np.random.uniform(true_integral_min, true_integral_max, num_toy_waveforms)
    
    onsets = np.random.uniform(true_onset_min, true_onset_max, num_toy_waveforms)
    
    
    # pair them into tuples
    
    integral_onset_pairs = [(integral, onset) for integral, onset in zip(integrals, onsets)]
    
    return integral_onset_pairs
    

def make_toy_waveforms(path_to_trace, waveform_file_name, name_tag, toy_waveform_params):
    
    # open the output_file_name.npy file
    # Might need to do this function in chunks/buffers in the future depending on raw waveform file size (when the file is too large to fit in memory)
    waveforms = np.load(waveform_file_name)
    
    
    # harvest the noise waveforms and make signal template
    noise_waveform_file_name, signal_template_file_name = harvest_noise(waveforms,  path_to_trace, name_tag, toy_waveform_params)
        
    
    # make the signal waveforms
    
    waveform_length = len(waveforms[0])
        
    signal_template = np.load(signal_template_file_name)
    
    
    noise_repo = np.load(noise_waveform_file_name)
    
    integral_onset_pairs = generate_integral_onset_values(toy_waveform_params)
    
    
    for integral_onset_pair in integral_onset_pairs:
        
        integral, onset = integral_onset_pair
        
        random_index = np.random.randint(0, len(noise_repo))
        
        noise_wf_i = noise_repo[random_index]
        
        toy_waveform_i = generate_toy_waveform(waveform_length, onset, integral, signal_template, noise_wf_i)
        
        plt.plot(toy_waveform_i)
        
        plt.title('integral: '+str(integral)+' onset: '+str(onset))
        
        plt.show()
        
        break