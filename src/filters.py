# filters.py
import numpy as np 
from scipy.signal import savgol_filter

def param_keys():
    
    param_dict = {
        'MAD': ['baseline_guess'],
        'CMA': ['preloadValue', 'halfWidth', 'rejectThreshold'],
        'matched_filter_fft': ['template'],
        'SF_filter': ['sg_smoothing_window'],
        'FIR':['baseline', 'windowSize', 'gapSize', 'firThresh', 'fraction', 'holdOffSamples', 'FIRSamples']
    }

def mean_absolute_deviation(waveform, baseline_guess):
    
    # Calculate the absolute deviations from the mean and store them in a list
    absolute_deviations = [abs(x - baseline_guess) for x in waveform]
    
    # Calculate the MAD by taking the average of the absolute deviations
    mad = sum(absolute_deviations) / len(waveform)
    
    return mad

def getCMAFilter( waveform, preloadValue, halfWidth, rejectThreshold ):
		#Initialize our filter.
		cmaFilter = []
		
		if halfWidth > len(waveform):
			print("Halfwidth greater than waveform length! Setting filter to zero.")
			return cmaFilter


		#Preload the filter.
		movingBaselineSum = 0.
		movingBaselineFilter = []
		for i in range(0,int(halfWidth)):
			movingBaselineFilter.append(preloadValue)
			movingBaselineSum += preloadValue
			
		#Now step through the first halfWidth of values, adding to the average if within reject threshold.
		for j in range(0, int(halfWidth)):
			#Calculate the current moving average.
			movingAverage = movingBaselineSum / len( movingBaselineFilter )
			#Check that we're within the reject threshold.
			if abs( waveform[j] - movingAverage ) < rejectThreshold:
				movingBaselineFilter.append( waveform[j] )
				movingBaselineSum += waveform[j]

		#print len( movingBaselineFilter )
		#Now moving average full. Start at element 0 and compute moving average.
		for k in range(0, len( waveform )):
			movingAverage = movingBaselineSum / len( movingBaselineFilter )
			cmaFilter.append( movingAverage )
			if ((k + int(halfWidth)) < len( waveform )):
				#print("k + halfwidth < len( waveform )")
				movingAverage = movingBaselineSum / len( movingBaselineFilter )
				#Check that the value at k + halfWidth is within reject threshold.
				if abs( waveform[k + int(halfWidth)] - movingAverage ) < rejectThreshold:
					movingBaselineFilter.append( waveform[k + int(halfWidth)] )
					movingBaselineSum += waveform[k + int(halfWidth)]
					#Check if the filter is larger than 2*halfWidth + 1. If so, pop off the front element.
				if len( movingBaselineFilter ) > 2 * int(halfWidth) + 1:
					#print("2*halfwidth+1 < len( movingbaselinefilter ), popping off elements.")
					movingBaselineSum -= movingBaselineFilter[0]
					del movingBaselineFilter[0]
			else:
				#print("k + halfwidth > len( waveform ), popping off elements.")
				movingBaselineSum -= movingBaselineFilter[0]
				del movingBaselineFilter[0]
			
		return cmaFilter

def get_matched_filter_fft(waveform, template):
		# Reverse the template
		template = template[::-1]
		
		# Calculate the FFT of the signal and template
		signal_fft = np.fft.fft(waveform)
		template_fft = np.fft.fft(template)
		
		# Multiply the FFTs element-wise
		convolution_result_fft = signal_fft * template_fft
		
		# Perform the inverse FFT to get the convolution result
		convolution_result = np.fft.ifft(convolution_result_fft)
		
		# Take the real part of the result (due to numerical precision)
		convolution_result = np.real(convolution_result)
		
		return convolution_result

def SG_filter(waveform, sg_smoothing_window):
    
    smoothed_wf = savgol_filter(waveform, sg_smoothing_window, 3)
    
    return smoothed_wf
    
def getPulsesFromFIR( waveform, baseline, windowSize, gapSize, firThresh, fraction, holdOffSamples, FIRSamples):
    
    #Holds the locations of found pulses.
    pulseTimes = []
    
    #Holds the moving average of two windows.
    leadingWindow = []
    trailingWindow = []
    sumLeadingWindow = 0.
    sumTrailingWindow = 0.
    
    #Holds the difference between the moving averages.
    firVector = []
    triggerSample = 0
    
    #Calculate the FIR vector.
    for i in range(0, len( waveform )):
        #For the first window+gapSize samples, load baseline values.
        if i < windowSize + gapSize:
            leadingWindow.append( baseline )
            sumLeadingWindow += baseline
            trailingWindow.append( baseline )
            sumTrailingWindow += baseline
            
        else:
            #Push new values and sum.
            leadingWindow.append( waveform[i] )
            sumLeadingWindow += waveform[i]
            trailingWindow.append( waveform[i - windowSize - gapSize] )
            sumTrailingWindow += waveform[i - windowSize - gapSize]
            
        #If vector sizes are > windowSize, remove oldest values.
        if len( leadingWindow ) > windowSize:
            sumLeadingWindow -= leadingWindow[0]
            del leadingWindow[0]
        if len( trailingWindow ) > windowSize:
            sumTrailingWindow -= trailingWindow[0]
            del trailingWindow[0]
            
        #Calculate the difference.
        firVector.append( sumLeadingWindow - sumTrailingWindow )
        
    #Now look for stuff above threshold.
    j = 0
    while j < len( waveform ):
        if firVector[j] >= firThresh:
            maxValue = 0
            maxSample = 0
            triggerSample = 0
            #Search for max value up to FIRSamples.
            for k in range(j, j + FIRSamples):
                #Make sure we don't extend  beyond the range of the waveform.
                if k > len( waveform ):
                    break
                if firVector[k] > maxValue:
                    maxValue = firVector[k]
                    maxSample = k
                    
            #Check if we have a maxValue at position > 0
            if maxSample > 0:
                for k in range(maxSample, j + FIRSamples):
                    if k > len( waveform ):
                        break
                    if firVector[k] <= fraction*maxValue:
                        triggerSample = k
                        break
                #Make sure we can interpolate and then do so.
                if triggerSample > 0:
                    valueAtTrigger = firVector[triggerSample]
                    valueBeforeTrigger = firVector[triggerSample-1]
                    
                    #Interpolation.
                    diffMaxDiv2AndMaxAtTrig = maxValue / 2. - valueAtTrigger
                    diffBeforeAndAtTrig = valueBeforeTrigger - valueAtTrigger
                    corrector = diffMaxDiv2AndMaxAtTrig / diffBeforeAndAtTrig
                    
                    pulseTimes.append( triggerSample - corrector )
            j += holdOffSamples
            
        else:
            j += 1
            
    return pulseTimes

def check_clipping_from_sample(sample_i, length_of_wf, pre_onset_samples, post_onset_samples):
    
    # it's kind of backwards sounding but it IS clipping if TRUE is returned
        
    min_sample = pre_onset_samples 
    
    max_sample = length_of_wf - post_onset_samples
    
    if sample_i < min_sample or sample_i > max_sample:
        
        return True
    
    else:
        
        return False

def level_threshold_bool(waveform, threshold):
    
    # IMPORTANT NOTE: The waveform must be baseline subtracted before using this function
    
    # the purpose of this function is simply to determine IF the waveform contains any samples above the threshold and what the first index is
    # a truer level threshold function will likely require the usage of a hold off time/sample to counter multi counting of the same pulse
    
    # check if the waveform is a numpy array or list
    
    if type(waveform) == list:
        waveform = np.array(waveform)
    
    indices = np.where(waveform > threshold)[0]
    
        
    # number of indices above threshold
    
    num_indices = len(indices)
    
    if num_indices == 0:
        
        return False, None
    
    else:
            
        return True, indices[0]