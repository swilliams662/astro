#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
import pandas as pd
import os
import astroquery
from astroquery.ipac.ned import Ned
import requests
import csv


# In[22]:


def get_cutouts(file_path, radius):
    url = 'http://cutouts.cirada.ca/'
    payload = {'upload': (None, open(file_path, 'rb'), 'text/csv')}
    r = requests.post(url, files=payload)
    if r.status_code == 200:
        print('File upload successful.')
        options_payload = {
            'display': '2',
            'options[]': ['VLASS-QL', 'FIRST', 'NVSS'],
            'radius': str(radius),
            'group': 'mosaic'
        }
        r = requests.post(url, data=options_payload)
        #print(r.text)
    else:
        print('File upload failed. Status code:', r.status_code)


# In[23]:


get_cutouts('agnpositions.csv', 2)


# In[ ]:




