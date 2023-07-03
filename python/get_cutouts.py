#!/usr/bin/env python
# coding: utf-8

# In[9]:


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
from requests_html import HTMLSession
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#things just for my firefox stuff:
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


# In[52]:


#just for me
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


# In[5]:


#just for me
driver = webdriver.Firefox()


# In[10]:


def get_cutouts(file_path, radius):
    driver.get('http://cutouts.cirada.ca/')
    upload = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #upload = driver.find_element(By.ID, "id_batch_locations")
    upload.send_keys(file_path)
    #upload.submit()
    checkbox = driver.find_element(By.ID, 'id_surveys_0')
    checkbox.click()
    checkbox = driver.find_element(By.ID, 'id_surveys_3') #FIRST
    checkbox.click()
    checkbox = driver.find_element(By.ID, 'id_surveys_4') #NVSS
    checkbox.click()
    radius = driver.find_element(By.ID, 'id_radius')
    radius.send_keys(str(radius))
    mosaic = driver.find_element(By.ID, 'id_groups')
    mosaic.send_keys('MOSAIC')
    submit = driver.find_element(By.ID, 'form_submit')
    submit.click()


# In[11]:


get_cutouts('/Users/summerwilliams/Desktop/blanton/agnpositions.csv',2)


# In[ ]:




