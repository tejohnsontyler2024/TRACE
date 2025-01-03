# TRACE
Tracking Rydberg Atoms by Counting Electrons

Here lives the software package for processing RAY data through the Channel Electron Multiplier (CEM)

There are several aspects of the code 
1. parse the binary file and output to a either a ROOT or HF5 file.
2. Run a basic DSP on the waveforms to make a repository of noise and signal pulses according to a basic level threshold
3. Make a set of toy waveforms for DSP optimization
4. Run a DSP optimization routine using a minimizer and cost function
5. Run the optimal filters/steps on the raw waveforms and package the observables in either HF5 or ROOT
6. A separate script for SPE-style fitting using RooFit
