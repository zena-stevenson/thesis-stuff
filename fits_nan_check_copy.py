#same as the block in make_file_lists that verifies/fixes/nan-checks fits files (except for some alterations to read/write to/from csv's instad of list variables), but as a separate script so I can screen it and run it in the background. Since doing this for the whole dataset is going to take roughly 50 hours and I simply will not deal with trying to keep a notebook running through a putty tunnel on the nmsu vpn for 50 hours because I don't deserve that kind of torture

import pandas as pd
import csv #don't ask me why I'm mixing csv and pandas, I don't know
from astropy.io import fits
import numpy as np
from tqdm import tqdm

newlist=open('/home/zenalisa/data/whole_dataset/south_biglist_fixed.csv', 'w')
w=csv.writer(newlist, delimiter = ',')
w.writerow(['aia', 'hmi'])

oldlist=pd.read_csv('/home/zenalisa/data/whole_dataset/south_biglist.csv', delimiter=',')
aia_file_list=list(oldlist['aia'])
hmi_file_list=list(oldlist['hmi'])

for n in tqdm(range(len(aia_file_list))):
    #if n%100 == 0:
    #    print n
    a_fits = fits.open(aia_file_list[n])
    a_fits.verify('fix')
    a = a_fits[1].data
    h_fits = fits.open(hmi_file_list[n])
    h_fits.verify('fix')
    h = h_fits[1].data
    
    a_fits.close()
    h_fits.close()
    
    if np.isnan(a).any() or np.isnan(h).any():
        pass
    else:
        w.writerow([aia_file_list[n], hmi_file_list[n]])
         