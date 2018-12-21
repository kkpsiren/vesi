# -*- coding: utf-8 -*-
"""
get all filenames and correct wrong names

Created on Wed May  30 13:31:02 2017

@author: Siren_Kimmo & Vestner_Jochen
https://github.com/kkpsiren/vesi
"""
import os
import time
import numpy as np
from pympler.asizeof import asizeof
import scipy.io.netcdf as cdf
from joblib import Parallel, delayed
import multiprocessing




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

    chrom = np.zeros((maxmz-minmz, scan_index.shape[0])) # create emtpy matrix
    #chrom = np.zeros((mzscan.shape[0], scan_index.shape[0])) # create emtpy matrix

    chrom = chrom.astype(int)

    for i in range(scan_index.shape[0]-1):
        mzscan = np.around(mass_values[scan_index[i]:scan_index[i+1]])   #round all mz value to unit mz!!! change this for high res data
        mzscan = mzscan.astype(int)
        intensscan = intensity_values[scan_index[i]:scan_index[i+1]]
        for ii in range(mzscan.shape[0]):
            if mzscan[(ii)] < maxmz:
                chrom[(mzscan[ii]-minmz),i] += intensscan[ii]
            else:
                break
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

def import2array3d_get_list(cdf):
    """
    @summary: Get the variables needed to build the correct array shape. Need to have defined x_list, rt_list, mzrange_list
    """
    x_list = []
    rt_list = []
    mzrange_list = []    
    x,rt,mzrange = cdf_import_gcms_unitmz(cdf)
    x_list.append(x),rt_list.append(rt),mzrange_list.append(mzrange)
    return x_list, rt_list, mzrange_list

def build_the_ar3d(one_list):
    """
    @summary: parallel looping
    """
    ar3d[:len(one_list[0]),:len(one_list[0][0]),i] = one_list[0][:, 0:l]

    return ar3d
	

def import2array3d(cdfs):
    """
    @summary:   Function import GC-MS raw data of multiple files and store
    in a 3way array
      
    """  
    t = time.time()
    num_cores = multiprocessing.cpu_count() 
    #x, rt, mzrange = cdf_import_gcms_unitmz(cdfs[1]) # problem unterschiedlich lange mz!
    r = Parallel(n_jobs=num_cores)(delayed(import2array3d_get_list)(i) for i in cdfs)
    x_list, rt_list, mzrange_list = zip(*r)
    #x = max(x_list)
    #rt = max(rt_list)
    #mzrange = max(mzrange_list)

    #l = int(np.floor(np.shape(x)[1]/10)*10) # cut lenght of chrom to next ten step # tän tehtävä on pilkkoa kaikki chrom samankokoiseksi. ja sitten pysähtyä tähän
    l = int(np.max([x_list[i][0].shape[1] for i in range(len(x_list))]).round())  # let's take the total median of the scan length.
    mass_l = int(np.max([x_list[i][0].shape[0] for i in range(len(x_list))]).round())
    #rt = rt[-1] 
    ar3d = np.zeros((mass_l, l, len(cdfs)))         
    for i, one_list in enumerate(x_list):
        ar3d[:len(one_list[0]),:len(one_list[0][0]),i] = one_list[0][:, 0:l]  
        print('File no. ' + str(i+1) + ' of ' + str(len(cdfs)))


        
    elapsed = time.time() - t 
    print('Total time: ' + str(round(elapsed)) + ' sec; ' + str(round(asizeof(ar3d)/1024/1024)) + ' MB') # 50 sec
     # 2737 MB
    
    return ar3d, x_list, rt_list, mzrange_list
