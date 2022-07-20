#same as the block(s) in make_file_list, just separate script so I can screen it while I do it for the whole dataset

#import stuff. way too much stuff, I keep not bothering to take out the ones that weren't actually used in the final version, sorry,
import csv
import glob
from astropy.io import fits
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import sys
import random
import datetime
import traceback
from tqdm import tqdm
import pandas as pd
#doesn't actually need all this I'm just being lazy and copypasta-ing from make_file_lists

def fits_to_tiff(filepath, img_type, r=False, outp_name=None, absval=False, log_10=True):
    '''Does the conversion from .fits data to .tiff images, saves .tiff files under new name and directory. 
    Inputs: filepath (string, full path to the file ie '/home/zenalisa/data/dataset_name/AR_number/filename.fits' )
            img_type (string, either 'aia' or 'hmi'. Have to specify because they need slightly different preprocessing steps before converting to a uint8 image)
            r (bool flag that controls whether or not to rotate the data- leftover from when I randomly rotated the training data by either 0 or 180 degrees to artificially remove any hemisphere bias, should be able to leave as False. If you did want to rotate, you'd want to randomly set r=True half the time you call this function, and be sure to have the same random flag for both the AIA and corresponding HMI image.)
            outp_name (string, new output directory for .tiff files. If left as default, will add /tiff just before the AR number in filepath argument to make a new directory and save there. ie if the original fits location is '/home/zenalisa/data/dataset_name/AR_number/file_name.fits', default output location is '/home/zenalisa/data/dataset_name/tiff', and new file will save as '/home/zenalisa/data/dataset_name/tiff/AR_number/file_name.tiff'. I didn't use the default often, preferred to specify my own new output spot, but kept it so I never accidentally mixed the tiff files in with the fits.)
            absval (bool flag controls whether or not to take absolute value of HMI data. Less relevant now/ should stay False since we're doing this for signed magnetograms, but I'll leave it in case anybody ever wants to use it.)
            log_10 (bool flag that controls whether or not to take log10 of AIA data. Can probably be left as True, but again I'll leave the option just in case.)
    Outputs: string name of new .tiff file, min data value, max data value.
    Notes: Current version doesn't do any clipping to AIA data before converting to uint8, just scales each image according to its own min and max values. I wrote more on why that's not the best way to do this and why I did it anyway in the thesis, but it's something to be aware of (and fix, in my opinion) if you're improving on this process in the future. I added some notes in the readme too on some weird technical difficulties that popped up when I did try the AIA clipping, highly recommend taking a peek at that if you're tackling the clipping problem, might spare you from the multiple days of NaN hunting that I suffered through.'''

    name, ext = os.path.splitext(filepath)
    
    if not outp_name:
        outp_name = name.replace(name.split('/')[-2], name.split('/')[-2]+'/tiff') #places new files in separate directory
    
    img = fits.open(filepath)
    img.verify('fix')

    #img.info()

    data = img[1].data #has to be img[1]
    
    if r:
        data=np.rot90(data)
        data=np.rot90(data)
    
    width = data.shape[1]
    height = data.shape[0]
    
    #aia_max=2550 
    #aia_min=1 #helps with log yelling at me
    hmi_offset=2550
    
    if img_type == 'aia':
        
        if log_10:
            data = np.log10(data - np.amin(data))
        else:
            data=data-np.amin(data)
        
        data=data.astype(float)/np.amax(data)*255
        data=np.round(data)
        data=data.astype(np.uint8)
    
            
        
    elif img_type == 'hmi':
        if absval:
            data = abs(data)
        
        data[data>hmi_offset]=hmi_offset
        data[data<-hmi_offset]=-hmi_offset
        data=data+hmi_offset
        data=data*255./(2*hmi_offset)
        data=np.round(data)
        data=data.astype(np.uint8)
        
    outputArray = np.array(data, dtype=np.uint8)

    output = Image.fromarray(outputArray.reshape((height, width)), "L")

    if not os.path.exists(outp_name + '/' +  name.split('/')[-2]):
        os.makedirs(outp_name + '/' +  name.split('/')[-2])
    
    output.save(outp_name + '/' +  name.split('/')[-2]+ '/'+ name.split('/')[-1]+".tiff")
    img.close()
    
    return(outp_name + '/' +  name.split('/')[-2]+ '/'+ name.split('/')[-1]+".tiff", data.min(), data.max())



oldlist=pd.read_csv('/home/zenalisa/data/whole_dataset/south_biglist_fixed.csv', delimiter=',')
aia_file_list=list(oldlist['aia'])
hmi_file_list=list(oldlist['hmi'])

#print(len(aia_file_list), len(hmi_file_list))
table = open('/home/zenalisa/data/whole_dataset/test_list_south.csv', 'w')
w = csv.writer(table, delimiter = ',')
w.writerow(['path_signal', 'path_target'])
for n in tqdm(range(len(aia_file_list))):
        #print(timediff(aia_file_list[n], hmi_file_list[n]))
        try:
 
            a, amin, amax = fits_to_tiff(aia_file_list[n], 'aia', outp_name='/mnt/zena/tiff/aia')
            h, hmin, hmax = fits_to_tiff(hmi_file_list[n], 'hmi', outp_name='/mnt/zena/tiff/hmi')
            #ha, hamin, hamax = fits_to_tiff(hmi_file_list[n], 'hmi', outp_name='/home/zenalisa/data/'+dataset_name+'/hmi_abs', absval=True)

            w.writerow([a, h])#, ha])
            #w.writerow([alog, ha])
            #v.writerow([a, amin, amax, alog, alogmin, alogmax, h, hmin, hmax])
            #v.writerow([alog, alogmin, alogmax, ha, hamin, hamax])


        except IndexError: #I don't remember why I had this here?
            pass
        #if n%100 ==0:
        #    print n


table.close()
