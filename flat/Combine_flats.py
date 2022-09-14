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
import matplotlib.pyplot as plt
import numpy as np

from convenience_functions import show_image

# Use custom style for larger fonts and figures
#plt.style.use('guide.mplstyle')

from astropy.nddata import CCDData
from astropy.visualization import hist

import numpy as np

from convenience_functions import show_image

one_flats = CCDData.read('flat/metis_f.00003512.Entered Coordinates.FlatField.fits', unit='adu')
one_flats_fin = CCDData.read('flat/metis_f.00003547.Entered Coordinates.FlatField.fits', unit='adu')


fig, (ax_1_bias, ax_avg_bias) = plt.subplots(1, 2, figsize=(30, 15))

show_image(one_flats.data, cmap='gray', ax=ax_1_bias, fig=fig, input_ratio=8)
ax_1_bias.set_title('Single flats image')
show_image(one_flats_fin.data, cmap='gray', ax=ax_avg_bias, fig=fig, input_ratio=8)
ax_avg_bias.set_title('100 flats images combined');

calibrated_path = Path('.')
reduced_images = ccdp.ImageFileCollection(calibrated_path)


calibrated_biases = []

calibrated_biases = os.listdir('flat')
files = []

for image in calibrated_biases:
    files.append(CCDData.read("flat/"+image, unit='adu'))


# combined_bias = ccdp.combine(files,
#                              method='average',
#                              sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
#                              sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std,
#                              mem_limit=350e6
#                             )

# combined_bias.meta['combined'] = True

# combined_bias.write(calibrated_path / 'combined_bias.fit')


# fig, (ax_1_bias, ax_avg_bias) = plt.subplots(1, 2, figsize=(30, 15))

# show_image(one_bias.data, cmap='gray', ax=ax_1_bias, fig=fig, input_ratio=8)
# ax_1_bias.set_title('Single bias image')
# show_image(combined_bias.data, cmap='gray', ax=ax_avg_bias, fig=fig, input_ratio=8)
# ax_avg_bias.set_title('100 bias images combined');
