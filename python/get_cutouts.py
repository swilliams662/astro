#!/usr/bin/env python
# coding: utf-8

def get_cutouts(radius, browser, file_path, downloads_filepath, desired_output_filepath):
    '''
    Parameters:
        - Radius in arcminutes (int)
        - Name of your browser: must be either Chrome, Safari, or Firefox (str, case insensitive)
        - Path to the csv file containing the coordinate(s) you want to look at (str)
        - Path to the folder in your computer where downloads from a browser go automatically (str)
        - Path to the folder you want the resulting fits files to appear in (str)
    
    Returns:
        - Fits files of each sky survey result for each set of coordinates you entered
        - Shows images of sky survey + location
    
    Requirements:
        - Make sure you have a webdriver installed or, for Safari, Remote Automation enabled
        
    '''
    
    import time
    import numpy as np
    from astropy.io import fits
    from astropy.utils.data import get_pkg_data_filename
    import matplotlib.pyplot as plt
    import os
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import tarfile
    
    
    positions = open(file_path,"r")
    positionsdata = positions.read()
    entries = positionsdata.split("\n")
    totalobj = ((len(entries)) - 1)
    
    
    if "firefox" in browser.lower():
        driver = webdriver.Firefox()
    elif "safari" in browser.lower():
        driver = webdriver.Safari()
    elif "chrome" in browser.lower():
        driver = webdriver.Chrome()
    else:
        print("The browser you input is not supported. Try with either Chrome, Safari, or Firefox")
        return
        
    
    driver.get('http://cutouts.cirada.ca/')
    upload = driver.find_element(By.ID, 'id_batch_locations')
    upload.send_keys(file_path)
    checkbox = driver.find_element(By.ID, 'id_surveys_0')
    checkbox.click()
    checkbox = driver.find_element(By.ID, 'id_surveys_3') #FIRST
    checkbox.click()
    checkbox = driver.find_element(By.ID, 'id_surveys_4') #NVSS
    checkbox.click()
    radiusenter = driver.find_element(By.ID, 'id_radius')
    radiusenter.send_keys(str(radius))
    mosaic = driver.find_element(By.ID, 'id_groups')
    mosaic.send_keys('MOSAIC')
    submit = driver.find_element(By.ID, 'form_submit')
    submit.click()
    
    WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, 
                                                                        "/html/body/div/main/div[3]/div/span[2]/div/div[3]/div[2]/table/tbody/tr[" + str(totalobj) + "]/td[1]")))
    WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[3]/div/span[2]/div/div[3]/div[1]/div/table/thead/tr/th[5]/input"))).click()
    WebDriverWait(driver, timeout=100).until(EC.element_to_be_clickable((By.ID, "download_batch"))).click()
    time.sleep(10)
    name = os.path.basename(file_path)
    name = name.replace('.csv', '')
    filename = downloads_filepath + name + "_cutoutResults.tgz"
    tf = tarfile.open(filename)
    names = tf.getnames()
    num = len(names)
    tf.extractall(desired_output_filepath)
    os.remove(downloads_filepath + name + "_cutoutResults.tgz")
    driver.close()
    
    VLASSimg = []
    FIRSTimg = []
    NVSSimg = []
    allimg = []
    VLASSdata = []
    FIRSTdata = []
    NVSSdata = []
    alldata = []
    
    for x in range(num):
        y = get_pkg_data_filename(desired_output_filepath + names[x])
        z = fits.getdata(y, ext=0)
        allimg.append(z)
        a = fits.open(desired_output_filepath + names[x])
        print(repr(a.info()))
        a = a[0]
        alldata.append(a)
        if ((x+1)%3) == 0:
            NVSSimg.append(z)
            NVSSdata.append(a)
        elif ((x+2)%3) == 0:
            FIRSTimg.append(z)
            FIRSTdata.append(a)
        elif (x%3)==0:
            VLASSimg.append(z)
            VLASSdata.append(a)
    for x in range(len(alldata)):
        print(repr(alldata[x].header))
    
    radius_arcsec = radius * 60
    
    nrows = len(VLASSimg)
    ncols = 3
    plt.figure()
    for y in range(num):
        if (y%3) == 0:
            ax = plt.subplot(nrows, ncols, (y+1))
            ax.imshow(np.squeeze(allimg[y]),cmap='gray',extent=(-radius_arcsec,radius_arcsec,-radius_arcsec,radius_arcsec))
            ax.set_title("VLASS")
        elif ((y+2)%3) == 0:
            ax = plt.subplot(nrows, ncols, (y+1))
            ax.imshow(np.squeeze(allimg[y]),cmap='gray',extent=(-radius_arcsec,radius_arcsec,-radius_arcsec,radius_arcsec))
            plt.title("FIRST")
        elif ((y+1)%3)==0:
            ax = plt.subplot(nrows, ncols, (y+1))
            ax.imshow(np.squeeze(allimg[y]),cmap='gray',extent=(-radius_arcsec,radius_arcsec,-radius_arcsec,radius_arcsec))
            plt.title("NVSS")
            #weird framing/direction in NVSS image
    plt.show()



