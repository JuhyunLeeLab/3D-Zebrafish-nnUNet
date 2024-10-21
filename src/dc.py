# The modified dc.py file. We made some changes to reflect our experimentation needs 
# You can either copy and paste this, replacing and saving the file , or make the changes manually 

# Code courtesy of https://github.com/nasyxx/zebrafish_seg 

#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
Python ♡ Nasy.

    |             *         *
    |                  .                .
    |           .                              登
    |     *                      ,
    |                   .                      至
    |
    |                               *          恖
    |          |\___/|
    |          )    -(             .           聖 ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Dec  22, 2023
email    : Nasy <nasyxx+python@gmail.com>
filename : dc.py
project  : zebrafish
license  : GPL-3.0+

Data converter.
"""
# Standard Library
import os
from pathlib import Path

# Utils
from rich import print
from rich.prompt import Confirm
from tqdm import tqdm

# Config
from config import Conf, config

# Others
import tifffile
from nnunet.dataset_conversion.utils import generate_dataset_json
from nnunet.utilities.file_conversions import (
    convert_3d_segmentation_nifti_to_tiff,
    convert_3d_tiff_to_nifti,
)


def to_dataset(conf: Conf) -> None:
    """Convert to dataseit."""
    dbase = f"{conf.raw_}nnUNet_raw_data/{conf.name}"
    target_imtr = f"{dbase}/imagesTr"
    target_imts = f"{dbase}/imagesTs"
    target_lbtr = f"{dbase}/labelsTr"
    target_lbts = f"{dbase}/labelsTs"
