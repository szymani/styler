"""
Copyright (C) 2018 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

from __future__ import print_function
import os
import torch
from Fast_lite.photo_wct import PhotoWCT
from Fast_lite.photo_gif import GIFSmoothing
from Fast_lite.process_stylization_lite import stylization


def change_style(content_image, style_image):
    # Load model
    p_wct = PhotoWCT()
    p_wct.load_state_dict(torch.load(os.path.abspath(
        os.path.dirname(__file__)) + '/PhotoWCTModels/photo_wct.pth'))

    p_pro = GIFSmoothing(r=35, eps=0.001)
    p_wct.cuda(0)

    return stylization(
        stylization_module=p_wct,
        smoothing_module=p_pro,
        content_image=content_image,
        style_image=style_image,
        cuda=0,
        no_post=False
    )
