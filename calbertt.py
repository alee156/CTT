from dipy.reconst.dti import *

import os
import numpy as np
import math
from scipy import ndimage
import nibabel as nib
from PIL import Image
import scipy.misc
from scipy import signal
import warnings
from dipy.tracking.eudx import EuDX

from dipy.data import read_stanford_labels, fetch_stanford_t1, read_stanford_t1
from dipy.reconst import peaks, shm
from dipy.tracking import utils

hardi_img, gtab, labels_img = read_stanford_labels()
labels = labels_img.get_data()
t1_data = np.load('v571.npy')

streamlines = np.load('streamlines.npy')
dataga = nib.load('/home/albert/CalberTT/demo/result/dog1gau0.5/ga.nii.gz')
affine = dataga.get_affine()

cc_slice = labels == 2
cc_streamlines = utils.target(streamlines, cc_slice, affine=affine)
cc_streamlines = list(cc_streamlines)

other_streamlines = utils.target(streamlines, cc_slice, affine=affine,
                                 include=False)
other_streamlines = list(other_streamlines)
assert len(other_streamlines) + len(cc_streamlines) == len(streamlines)

from dipy.viz import fvtk
from dipy.viz.colormap import line_colors

# Make display objects
color = line_colors(cc_streamlines)
cc_streamlines_actor = fvtk.line(cc_streamlines, line_colors(cc_streamlines))
cc_ROI_actor = fvtk.contour(cc_slice, levels=[1], colors=[(1., 1., 0.)],
                            opacities=[1.])

vol_actor = fvtk.slicer(t1_data)

vol_actor.display(40, None, None)
vol_actor2 = vol_actor.copy()
vol_actor2.display(None, None, 35)

# Add display objects to canvas
r = fvtk.ren()
fvtk.add(r, vol_actor)
fvtk.add(r, vol_actor2)
fvtk.add(r, cc_streamlines_actor)
fvtk.add(r, cc_ROI_actor)

# Save figures
fvtk.record(r, n_frames=1, out_path='corpuscallosum_axial.png',
            size=(800, 800))
fvtk.camera(r, [-1, 0, 0], [0, 0, 0], viewup=[0, 0, 1])
fvtk.record(r, n_frames=1, out_path='corpuscallosum_sagittal.png',
            size=(800, 800))





