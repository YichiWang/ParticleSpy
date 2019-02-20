# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 12:23:59 2018

@author: qzo13262
"""

import h5py
from ParticleSpy.ptcl_class import Particle, Particle_list
import hyperspy as hs
import numpy as np
import csv

def save_plist(p_list,filename):
    f = h5py.File(filename,'w')
    
    for i, particle in enumerate(p_list.list):
        p_group = f.create_group("Particle "+str(i))
        
        p_group.attrs["Area"] = particle.area
        p_group.attrs["Area units"] = particle.area_units
        p_group.attrs["Circularity"] = particle.circularity
        #p_group.attrs["Zone"] = particle.zone
        
        p_group.create_dataset("Mask",data=particle.mask)
        
        if hasattr(particle, 'image'):
            p_group.create_dataset("Image",data=particle.image.data)
        
    f.close()
        
def load_plist(filename):
    f = h5py.File(filename,'r')
    p_list = Particle_list()
    
    for p_name in list(f.keys()):
        if p_name[:8] == 'Particle':
            p_group = f[p_name]
            particle = Particle()
            
            particle.set_area(p_group.attrs['Area'],p_group.attrs['Area units'])
            particle.set_circularity(p_group.attrs["Circularity"])
            #particle.set_zone(p_group.attrs["Zone"])
            
            particle.set_mask(np.array(p_group['Mask'][:]))
            
            if "Image" in p_group:
                particle.store_im(hs.signals.Signal2D(np.array(p_group['Image'][:])))
                
            p_list.append(particle)
    
    f.close()
    return(p_list)

def read_csv(dir_csv, col_index=None, delimiter=' ',  dtype='float'):
    '''
    Read csv files, 
    give column index and return all values under than column as a list
    '''
    with open(dir_csv, newline='') as f:
        reader = csv.reader(f)
        f_aslist = []
        for row in reader:
            f_aslist.append(row)   
            
    col_list = []
    for i, row in enumerate(f_aslist):
        col_list.append(row[col_index])
    col_list.pop(0)#remove the title row
    
    if dtype == 'float':
        col_list = [float(x) for x in col_list]
    
    return col_list