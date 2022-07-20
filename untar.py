#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:46:53 2019

@author: zenalisa

Jupyter doesn't want to go find these files I'm trying to un-tar so we're gonna try it from here

"""
import os
import glob
import subprocess
import tarfile
aia_files = '/mnt/zena/AIA/*/*.tar'
#hmi_files = '/mnt/zena/active_regions/2424/*.tar' #looks like all of these have been untarred already

untar_list = glob.glob(aia_files)#+glob.glob(hmi_files)
untar_list.sort()
for f in untar_list:
    print (f)
    p = '/'.join(f.split('/')[:-1])
    tar = tarfile.open(f)
    tar.extractall(path = p)
    tar.close()
