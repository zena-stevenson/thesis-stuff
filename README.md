# thesis-stuff
Code from the master's thesis. 
This is a bit of a dumping ground that I keep saying I'll organize later. The actually useful and interesting files include:

  stevenson_thesis_final.pdf : the actual thesis document
  
  make_file_lists_clean.ipynb : code for data preprocessing and organization prior to using data for training or testing. Mostly useful for smaller datasets
  
  convert_to_tiff.py : piece of code from make_file_lists that converts fits files to tiff, separate so it can be run in the background for large datasets
  
  fits_nan_check.py : same as above, but this one checks fits files for nans and excludes any that have them
  
  results.py : functions for displaying results, generating figures, etc
  
