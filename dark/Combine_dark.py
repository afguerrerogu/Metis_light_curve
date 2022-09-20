# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:11:16 2022

@author: andre
"""

#%load_ext autoreload
#%autoreload 2

#%matplotlib inline
import matplotlib.pyplot as plt
from pathlib import Path
import os

from astropy.stats import mad_std

import ccdproc as ccdp
import numpy as np

from convenience_functions import show_image

# Use custom style for larger fonts and figures
#plt.style.use('guide.mplstyle')

from astropy.nddata import CCDData


one_dark = CCDData.read('dark/metis_f.00003439.Entered Coordinates.Dark.fits', unit='adu')
one_dark_fin = CCDData.read('dark/metis_f.00003485.Entered Coordinates.Dark.fits', unit='adu')


fig, (ax_1_bias, ax_avg_bias) = plt.subplots(1, 2, figsize=(30, 15))

show_image(one_dark.data, cmap='gray', ax=ax_1_bias, fig=fig, input_ratio=8)
ax_1_bias.set_title('Single dark image')
show_image(one_dark_fin.data, cmap='gray', ax=ax_avg_bias, fig=fig, input_ratio=8)
ax_avg_bias.set_title('single dark image');

#calibrated_path = Path('.')
# reduced_images = ccdp.ImageFileCollection(calibrated_path)


calibrated_dark = []

calibrated_dark = os.listdir('dark')
B_dark = []
V_dark = []
Ic_dark = []

for image in calibrated_dark:
    fit = CCDData.read("dark/"+image, unit='adu')    
    print(fit[0].header["EXPTIME"])
    if(fit[0].header["FILTER"] == "B"):        
        B_dark.append(fit)
    elif(fit[0].header["FILTER"] == "V"):
        V_dark.append(fit)
    else:
        Ic_dark.append(fit)
    
images = [B_dark,V_dark, Ic_dark]


for filte in images:
    
    combined_dark = ccdp.combine(filte,
                                 method='average',
                                 sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
                                 sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std,
                                 mem_limit=350e6
                                )

    combined_dark.meta['combined'] = True

    dark_file_name = 'combined_dark'+filte[1][0].header["FILTER"] +'.fit'
    combined_dark.write(dark_file_name, overwrite = True)


# def inv_median(a):
#     return 1 / np.median(a)


# for filte in images:
#     combined_flat = ccdp.combine(filte,
#                                  method='average', scale=inv_median,
#                                  sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
#                                  sigma_clip_func=np.ma.median, signma_clip_dev_func=mad_std,
#                                  mem_limit=350e6
#                                 )

#     combined_flat.meta['combined'] = True
#     dark_file_name = 'combined_flat_filter_'+filte[1][0].header["FILTER"] +'.fit'
#     combined_flat.write(dark_file_name, overwrite = True)


