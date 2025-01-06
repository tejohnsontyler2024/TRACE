# fitting.py
from scipy.optimize import curve_fit
import numpy as np 
import matplotlib.pyplot as plt
import math

def gaussian(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def fit_baseline_with_gaussian(waveform):
    
    counts, bin_edges = np.histogram(waveform, bins=100) # adjust the binning as needed
    
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    
    
    initial_guess = [1, 0, 1]
    
    popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=initial_guess)
    
    
    amplitude, mean, sigma = popt
    
    ''' Plotting for diagnostic purposes
    x = np.linspace(min(bin_centers), max(bin_centers), 1000)
    fit_curve = gaussian(x, amplitude, mean, sigma)
    
    plt.stairs(counts, bin_edges, color='Black', lw=2.5, label='Data')
    plt.plot(x, fit_curve, color='r', lw=3.5, label='Gaussian fit', alpha=0.7)
    plt.xlabel('ADC counts')
    plt.ylabel('Counts')
    plt.show()
    '''
    
    return mean

# def waveform_function(t, t1, t2, const, shift):
    
#     # W. Xiao et al., “A new pulse model for NaI(Tl) detection systems,” 2014.
#     # this is for scintillation but has the things I want which is a rise and decay time. 
#     # In actuality, there's an overshoot on the decay side. The current digitizer doesn't have the resolution to see that very well.
#     # TODO: for future DAQs, consider the overshoot.
    
#     return np.exp(-(t-shift)/t2)*(1-np.exp(-(t-shift)/t1))+const#*((t1+t2)/math.pow(t2,2))+const

def safe_exp(x, max_val=500):
    # If x is less than -max_val, exp is ~0. If x is greater than max_val, exp is huge -> treat as np.inf or clamp
    return np.exp(np.clip(x, -max_val, max_val))

def waveform_function(t, A, t1, t2, const, shift):
    # clamp exponent to avoid floating overflow:
    # return A*safe_exp(-(t - shift)/t2) * (1 - safe_exp(-(t - shift)/t1)) + const
    return A*safe_exp(-(t-shift)/t2)*(1-safe_exp(-(t-shift)/t1))+const


    
def fit_waveform(waveform):
    
    # fit the waveform to the function
        
    # inital_guess = [6, 1, 5.5, 0, 20]
    inital_guess = [6, 20, 2]
    
    # bounds = ([5, 0, 5, -1, 19], [50, 10, 10, 1, 21])
    bounds = ([5, 0, 0.01], [50, 50, 10])
    
    popt, pcov = curve_fit(gaussian, np.arange(len(waveform)), waveform, p0=inital_guess, bounds=bounds)
    
    # plot the fit
    
    # print the parameters
    print("A: ", popt[0])
    print("t1: ", popt[1])
    print("t2: ", popt[2])
    # print("const: ", popt[2])
    # print("shift: ", popt[3])
    
    x = np.linspace(0, len(waveform), 1000)
    
    fit_curve = gaussian(x, *popt)
    
    plt.plot(np.arange(len(waveform)), waveform, color='Black', lw=2.5, label='Waveform')
    
    plt.plot(x, fit_curve, color='r', lw=3.5, label='Fit', alpha=0.7)
    
    plt.xlabel('Sample number')
    
    plt.ylabel('ADC counts')
    
    plt.legend()
    
    plt.tight_layout()
    
    plt.show()