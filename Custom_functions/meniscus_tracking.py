"""
Generate volume_headroom_functions for each type of tube in use from 
measured gradations
"""
############################################################
from __future__ import absolute_import

import numpy as np
############################################################

### Below, we define the gradation profiles for our standard tubes/wells. These are then converted to 'volume_headroom_functions' using gradations_to_vh(), above. The 'volume_headroom_functions' are then ascribed to each well instance at the beginning of the protocol ###
# Measured gradations
"""
Classification
- cuvette = cuvette for UV-Vis samples
- epptube = Eppendorf tubes
- ftube = Falcon tubes
- vial = glass vials

Variables detail:
- Gradations defined as a numpy array (cast from a list of sublists)
- Each sublot is structured as [meniscus_to_top_in_mm, uL_volume]

Note
Individual containers of the same type vary in actual depth, therefore an error is to be expected. 
This has been observed in 2 mL and 4 mL vials in particular, but is likely the case for other as well
Given the use of headroom functions as security factors, this should not massively affect the protocols
"""
#####
# 1.5ml Eppendorf tubes
gradations_epptube_1500ul = np.array([[8,1500], # Top gradation of container i.e. maximum liquid fill
                                      [16.4,1000],
                                      [27.4,400],
                                      [35.2, 100],
                                      [40, 20],
                                      [42.2,0]]) # Bottom of container i.e. no liquid
#####
# 1.5ml amber Eppendorf tubes
gradations_ambtube_1500ul = np.array([[4.827, 1506], # Top gradation of container i.e. maximum liquid fill,
                                      [5, 1493],
                                      [6, 1421],
                                      [7, 1353],
                                      [8, 1285],
                                      [9, 1218],
                                      [10, 1151],
                                      [11, 1085],
                                      [12, 1020],
                                      [13, 956],
                                      [14, 892],
                                      [15, 829],
                                      [16, 766],
                                      [17, 705],
                                      [18, 644],
                                      [19, 583],
                                      [20, 523],
                                      [21, 466],
                                      [22, 413],
                                      [23, 364],
                                      [24, 318],
                                      [25, 276],
                                      [26, 238],
                                      [27, 203],
                                      [28, 171],
                                      [29, 142],
                                      [30, 117],
                                      [31, 93],
                                      [32, 73],
                                      [33, 55],
                                      [34, 39],
                                      [35, 25],
                                      [36, 13],
                                      [37, 4],
                                      [37.9,0]]) # Bottom of container i.e. no liquid
#####
# 15ml Falcon tubes
gradations_ftube_15ml = np.array([[13.8, 15000], # Top gradation of container i.e. maximum liquid fill
                                  [93.8, 2000],
                                  [101.6, 1000],
                                  [118.1, 0]]) # Bottom of container i.e. no liquid
#####
# 5 mL Eppendorf tubes
gradations_epptube_5ml = np.array([[7.46, 5034], # Top gradation of container i.e. maximum liquid fill,
                                   [8, 4952],
                                   [10, 4648],
                                   [12, 4346],
                                   [14, 4046],
                                   [16, 3748],
                                   [18, 3453],
                                   [20, 3159],
                                   [22, 2869],
                                   [24, 2580],
                                   [26, 2293],
                                   [28, 2009],
                                   [30, 1727],
                                   [32, 1447],
                                   [34, 1172],
                                   [35, 1045],
                                   [36, 928],
                                   [37, 819],
                                   [38, 720],
                                   [39, 628],
                                   [40, 544],
                                   [41, 468],
                                   [42, 400],
                                   [43, 338],
                                   [44, 283],
                                   [45, 233],
                                   [46, 190],
                                   [47, 152],
                                   [48, 119],
                                   [49, 91],
                                   [50, 67],
                                   [51, 47],
                                   [52, 31],
                                   [53, 18],
                                   [54, 8],
                                   [55.4,0]]) # Bottom of container i.e. no liquid
#####
# 15 mL Eppendorf tubes
gradations_epptube_15ml = np.array([[1.2, 16210], # Top gradation of container i.e. maximum liquid fill,
                                   [2, 16070],
                                   [4, 15710],
                                   [6, 15350],
                                   [8, 14990],
                                   [10, 14640],
                                   [15, 13760],
                                   [20, 12900],
                                   [25, 12050],
                                   [30, 11210],
                                   [35, 10380],
                                   [40, 9573],
                                   [45, 8774],
                                   [50, 7988],
                                   [55, 7214],
                                   [60, 6453],
                                   [65, 5704],
                                   [70, 4967],
                                   [75, 4243],
                                   [80, 3531],
                                   [85, 2830],
                                   [90, 2142],
                                   [95, 1465],
                                   [97.5, 1131],
                                   [100, 837],
                                   [105, 407],
                                   [110, 153],
                                   [115, 28],
                                   [117.6, 0]]) # Bottom of container i.e. no liquid
#####
# 50 mL Eppendorf tubes
gradations_epptube_50ml = np.array([[5, 53910], # Top gradation of container i.e. maximum liquid fill,
                                   [10, 50910],
                                   [15, 47950],
                                   [20, 45010],
                                   [25, 42110],
                                   [30, 39230],
                                   [35, 36380],
                                   [40, 33560],
                                   [45, 30780],
                                   [50, 28020],
                                   [55, 25290],
                                   [60, 22580],
                                   [65, 19910],
                                   [70, 17270],
                                   [75, 14650],
                                   [80, 12060],
                                   [85, 9505],
                                   [90, 6974],
                                   [95, 4470],
                                   [98, 2982],
                                   [100, 2091],
                                   [105, 667],
                                   [110, 92],
                                   [113,0]]) # Bottom of container i.e. no liquid
#####
# 50ml Falcon tubes
gradations_ftube_50ml = np.array([[8, 50000], # Top gradation of container i.e. maximum liquid fill
                                  [94.9, 4000],
                                  [103.5, 1000],
                                  [113.5, 0]]) # Bottom of container i.e. no liquid
#####
# 1.5 mL vials
gradations_vial_1500ul = np.array([[12.7, 1500], # Top gradation of container i.e. maximum liquid fill
                                   [30.9, 0]]) # Bottom of container i.e. no liquid
#####
# 2 ml vials
gradations_vial_2ml = np.array([[11, 2000], # Top gradation of container i.e. maximum liquid fill
                                [34.2, 0]]) # Bottom of container i.e. no liquid
#####
# 4 mL vials
gradations_vial_4ml = np.array([[15,4000], # Top gradation of container i.e. maximum liquid fill
                                [44,0]])   # Bottom of container i.e. no liquid
#####
# 8 ml vials
gradations_vial_8ml = np.array([[12.8, 8000], # Top gradation of container i.e. maximum liquid fill
                                [58.7, 0]]) # Bottom of container i.e. no liquid
#####
# 20 ml vials
gradations_vial_20ml = np.array([[17.26, 20000], # Top gradation of container i.e. maximum liquid fill
                                 [55.6, 0]]) # Bottom of container i.e. no liquid
#####
# 30 ml vials
gradations_vial_30ml = np.array([[16.3, 30000], # Top gradation of container i.e. maximum liquid fill
                                 [93.3, 0]]) # Bottom of container i.e. no liquid
#####
# 70 uL cuvettes
gradations_cuvette_70ul = np.array([[10, 900],
                                    [15, 600], # Top gradation of container i.e. maximum liquid fill
                                    [21, 300],
                                    [28.5, 70],
                                    [32.2, 0]]) # Bottom of container i.e. no liquid
#####
# 50 uL TLC wells
gradations_tlc_50ul = np.array([[0, 50], # Top gradation of container i.e. maximum liquid fill
                                [0.1, 0]]) # Bottom of container i.e. no liquid
############################################################

def gradations_to_vh(gradations: np.ndarray):
    # Converts gradations (numpy array):
    # to tuple containg the v_given_h and h_given_v interpolation functions
    assert np.shape(gradations)[1] == 2
    maximum_headroom = np.max(gradations[:,0])
    maximum_volume = np.max(gradations[:,1])
    # Sorting (required for interpolation functions to work correctly)
    gradations_sorted_by_headroom = gradations[gradations[:,0].argsort()]
    gradations_sorted_by_volume = gradations[gradations[:,1].argsort()]
    # Slicing the gradation arrays
    h_by_h = gradations_sorted_by_headroom[:,0] # headroom i.e. meniscus to top of container
    v_by_h = gradations_sorted_by_headroom[:,1] # fill volume
    h_by_v = gradations_sorted_by_volume[:,0] # headroom i.e. meniscus to top of container
    v_by_v = gradations_sorted_by_volume[:,1] # fill volume
    # Interpolation functions
    # Using linear interpolation (rather than cubic spline) to functions
    # becoming negative close to the bottom of the well
    v_given_h = lambda x : np.interp(x, h_by_h, v_by_h, left=maximum_volume, right=0)
    h_given_v = lambda x : np.interp(x, v_by_v, h_by_v, left=maximum_headroom, right=0)
    
    # The order of the returned function is referenced by 
    # the custom_aspirate() and custom_dispense() functions
    return [v_given_h, h_given_v]
############################################################

def call_gradations_epptube_1500ul():
    return gradations_to_vh(gradations_epptube_1500ul)
def call_gradations_ambtube_1500ul():
    return gradations_to_vh(gradations_ambtube_1500ul)
def call_gradations_ftube_15ml():
    return gradations_to_vh(gradations_ftube_15ml)
def call_gradations_epptube_5ml():
    return gradations_to_vh(gradations_epptube_5ml)
def call_gradations_epptube_15ml():
    return gradations_to_vh(gradations_epptube_15ml)
def call_gradations_epptube_50ml():
    return gradations_to_vh(gradations_epptube_50ml)
def call_gradations_ftube_50ml():
    return gradations_to_vh(gradations_ftube_50ml)
def call_gradations_vial_1500ul():
    return gradations_to_vh(gradations_vial_1500ul)
def call_gradations_vial_2ml():
    return gradations_to_vh(gradations_vial_2ml)
def call_gradations_vial_4ml():
    return gradations_to_vh(gradations_vial_4ml)
def call_gradations_vial_8ml():
    return gradations_to_vh(gradations_vial_8ml)
def call_gradations_vial_20ml():
    return gradations_to_vh(gradations_vial_20ml)
def call_gradations_vial_30ml():
    return gradations_to_vh(gradations_vial_30ml)
def call_gradations_cuvette_70ul():
    return gradations_to_vh(gradations_cuvette_70ul)
def call_gradations_tlc_50ul():
    return gradations_to_vh(gradations_tlc_50ul)
############################################################