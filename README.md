# TRACE
Tracking Rydberg Atoms by Counting Electrons

Here lives the software package for processing RAY data through the Channel Electron Multiplier (CEM)

The goal of the code is to be a highly generalized signal processing routine where the user(s) can
decide what combination of signal processing tools to use, decide to set the values of the input 
parameters via domain knowledge (guesses) or through an optimization routine involving the generation
of toy monte carlo waveforms followed by the minimization of a cost function.

USAGE
example:
python3 main.py <basic.json>

There are several aspects of the code 
1. parse the binary file and output to a either a ROOT or HF5 file.
2. Run a basic DSP on the waveforms to make a repository of noise and signal pulses according to a basic level threshold
3. Make a set of toy waveforms for DSP optimization
4. Run a DSP optimization routine using a minimizer and cost function
5. Run the optimal filters/steps on the raw waveforms and package the observables in either HF5 or ROOT
6. A separate script for SPE-style fitting using RooFit


BINARY PARSER
(Mon Jan 6, 2024)
Kind of janky at the moment honestly. It could use a revamp in the near to medium term. My main complaint is that the length of the waveforms is user defined and I wonder if there's a way to simply pull that from the binary words themselves. Also, the output binary does not contain a timestamp at the moment. That all should be amended.

TOY MONTE CARLO WAVEFORMS
The first pass of this is using the average pulse shape as a PDF create individual waveforms of user-defined integrals and onset samples. However, given the discrete nature of electrons, it may be improper to break these signals into integer ADC quantities. The more proper method by be to determine an average single electron pulse shape then sample those in order to make larger pulses. That will be the upgrade path. 

The single electron pulse shape can either be extracted by creating a single electron calibration source out of a photocathode 

OR

Amassing a collection of pulse integrals and fitting it with Polya functions and noise pedestal (maybe) to elicit a range of integral that is all or mostly populated by single electrons. This may or may not be a practical approach. We'll see!