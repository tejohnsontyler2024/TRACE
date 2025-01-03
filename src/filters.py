
import numpy as np 
from scipy.signal import savgol_filter

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

def get_matched_filter_fft(signal, template):
		# Reverse the template
		template = template[::-1]
		
		# Calculate the FFT of the signal and template
		signal_fft = np.fft.fft(signal)
		template_fft = np.fft.fft(template)
		
		# Multiply the FFTs element-wise
		convolution_result_fft = signal_fft * template_fft
		
		# Perform the inverse FFT to get the convolution result
		convolution_result = np.fft.ifft(convolution_result_fft)
		
		# Take the real part of the result (due to numerical precision)
		convolution_result = np.real(convolution_result)
		
		return convolution_result

def SF_filter(waveform, sg_smoothing_window):
    
    smoothed_wf = savgol_filter(waveform, sg_smoothing_window, 3)