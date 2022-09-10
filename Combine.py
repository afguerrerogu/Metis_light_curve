from pathlib import Path
import os

from astropy.nddata import CCDData
from astropy.stats import mad_std

import ccdproc as ccdp
import matplotlib.pyplot as plt
import numpy as np

from convenience_functions import show_image

# Use custom style for larger fonts and figures
plt.style.use('guide.mplstyle')

def Combine(path):
  
  calibrated_path = Path(path)
  reduced_images = ccdp.ImageFileCollection(calibrated_path)
  
  calibrated_biases = reduced_images.files_filtered(imagetyp='bias', include_path=True)

  combined_bias = ccdp.combine(calibrated_biases,
                             method='average',
                             sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
                             sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std,
                             mem_limit=350e6
                            )

  combined_bias.meta['combined'] = True

  combined_bias.write(calibrated_path / 'combined_bias.fit')
  
  Return None
