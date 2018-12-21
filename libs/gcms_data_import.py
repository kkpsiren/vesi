# -*- coding: utf-8 -*-
"""
get all filenames and correct wrong names

Created on Wed Jan  4 13:31:02 2017

@author: Siren_Kimmo & Vestner_Jochen
https://github.com/kkpsiren/vesi
"""
import os
import time
import numpy as np
from pympler.asizeof import asizeof
import scipy.io.netcdf as cdf



def cdf_import_gcms_unitmz(self):
    """
    @summary:   Function for GC-MS NetCDF files (unit mass resolution),
                returns a 2D numpy array of the intensity values (mz x scans) and 
                two 1D numpy arrays with the retention time in sec and the mz values
      
    """
    data = cdf.netcdf_file(self, mmap=False)

    #tic = data.variables['total_intensity'][:]        # this is the TIC
    mass_values = data.variables['mass_values'][:]
    scan_index = data.variables['scan_index'][:]
    intensity_values = data.variables['intensity_values'][:]
    scan_acquisition_time = data.variables['scan_acquisition_time'][:]

    minmz = int(round(np.min(mass_values)))      # get min mz
    maxmz = int(round(np.max(mass_values)))      # get max mz

    chrom = np.zeros((maxmz-minmz+1, scan_index.shape[0])) # create emtpy matrix
    chrom = chrom.astype(int)

    for i in np.arange(scan_index.shape[0]-1):
        mzscan = np.around(mass_values[scan_index[i]:scan_index[i+1]])   #round all mz value to unit mz!!! change this for high res data
        mzscan = mzscan.astype(int)
        intensscan = intensity_values[scan_index[i]:scan_index[i+1]]
        for ii in np.arange(mzscan.shape[0]):
#           chrom[mzscan[ii]-minmz,i] = intensscan[ii]
            chrom[mzscan[ii]-minmz,i] = chrom[mzscan[ii]-minmz,i] + intensscan[ii]
    
    rt = scan_acquisition_time
    mzrange = np.arange(minmz,maxmz+1)        
    
    return np.array(chrom), np.array(rt), np.array(mzrange)


def getfilenames(path):
    """
    @summary:   Function obtain a list of all cdf files in the current directory 
      
    """    
    files = os.listdir(path)
    cdfs = [os.path.join(path, f) for f in files if f.upper().endswith('CDF')]  # filter only cdf          
 
    return cdfs


     

def import2array3d(cdfs):
    """
    @summary:   Function import GC-MS raw data of multiple files and store
    in a 3way array
      
    """  
    t = time.time()
    x_list = []
    rt_list = []
    mzrange_list = [] 
    # x, rt, mzrange = cdf_import_gcms_unitmz(cdfs[5]) # problem unterschiedlich lange mz!
    for cdf in cdfs:
        x,rt,mzrange = cdf_import_gcms_unitmz(cdf)
        x_list.append(x),rt_list.append(rt),mzrange_list.append(mzrange)
    x = max(x_list)
    rt = max(rt_list)
    mzrange = max(mzrange_list)


    l = int(np.floor(np.shape(x)[1]/10)*10) # cut lenght of chrom to next ten step
    rt = rt[l] 
    ar3d = np.zeros((np.shape(x)[0], l, len(cdfs)))
         
    for c in cdfs:
        x, rt, mzrange = cdf_import_gcms_unitmz(c) # problem unterschiedlich lange mz!
        ar3d[:, :, cdfs.index(c)] = x[:, 0:l] 
        print('File no. ' + str(cdfs.index(c)+1) + ' of ' + str(len(cdfs)))
         
    elapsed = time.time() - t 
    print('Total time: ' + str(round(elapsed)) + ' sec; ' + str(round(asizeof(ar3d)/1024/1024)) + ' MB') # 50 sec
     # 2737 MB
    
    return ar3d, rt, mzrange, x_list, rt_list, mzrange_list
