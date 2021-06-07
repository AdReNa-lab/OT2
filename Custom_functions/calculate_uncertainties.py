"""
* The function `initiate_well()` must be used for all wells
* The correct `volume_headroom_functions` name must be inputted in the function for each well type

* Specifics for stock solutions (i.e. solutions that are not prepared during the protocol):
 `set_constituent` must be used with known concentrations and uncertainties to enable further calculations
 
* See the Uncertainties Calculation report for the formulas of calculations used in this Py module
"""
############################################################
from __future__ import absolute_import

import numpy as np

from opentrons import types
from Custom_functions import building_blocks as bb
############################################################

def profile_to_vu(experimental_uncertainties_data: np.ndarray):
    """
    Convert uncertainties profiles (experimentally determined) into functions 
    allowing interpolation for volumes within the arrays
    
    Nomenclature - the following abreviations are used in variable names:
    - r: random
    - s: systematic
    - u: uncertainty
    - v: volume
    """
    assert np.shape(experimental_uncertainties_data)[1] == 3
    maximum_random_error = np.max(experimental_uncertainties_data[:, 0])
    maximum_systematic_error = np.max(experimental_uncertainties_data[:, 1])
    # Sorting (required for interpolation functions to work correctly)
    error_profile_sorted_by_volume = experimental_uncertainties_data[experimental_uncertainties_data[:,2].argsort()]
    ur_by_v = error_profile_sorted_by_volume[:,0]
    us_by_v = error_profile_sorted_by_volume[:,1]
    v_by_v = error_profile_sorted_by_volume[:,2]
    # Interpolation function
    ur_given_v = lambda x : np.interp(x, v_by_v, ur_by_v, left=maximum_random_error, right=0)
    us_given_v = lambda x : np.interp(x, v_by_v, us_by_v, left=maximum_systematic_error, right=0)
    return [ur_given_v, us_given_v]
############################################################

def volume_uncertainty(pipette: types.Mount, 
                       volume: float):
    """ This function calculates the uncertainties for a volume depending on what pipette is used
     and extracts pipette uncertainty functions"""
    functions_dict = bb.get_pipette_uncertainties(pipette)
    volume_to_random_uncertainty = functions_dict['random']
    volume_to_systematic_uncertainty = functions_dict['systematic']
    # Calculates the uncertainties associated with the volume
    volume_uncertainty_r = volume_to_random_uncertainty(volume)
    volume_uncertainty_s = volume_to_systematic_uncertainty(volume)
    return [volume_uncertainty_r, volume_uncertainty_s]
############################################################

def uncertainties_calculation(pipette: types.Mount, 
                                volume_transfer: float, 
                                source:types.Location, 
                                destination: types.Location):
    """
    This function should be called BEFORE the actual transfer, as the initial headroom is needed
    
    It calculates the concentrations as well as uncertainties on both concentration and volume for all wells implicated 
    in a transfer step (i.e. 1 stroke of a pipette)
    
    Nomenclature:
    - 1: any variable containing '1' refers to the source (well 1) of the transfer
    - 2: any variable containing '2' refers to the destination (well 2) before the transfer
    - 3: any variable containing '3' refers to the destination (well 2) after the transfer (final)
    - c: 'concentration'
    - del: 'delta', designates an uncertainty
    - pc: 'percent'
    - r: 'random'
    - s: 'systematic'
    - t: used in 'vt' to designate the transferred volume
    - v: 'volume'
    """
    # Extracts all information for the source and destination
    source_info = bb.get_c_info(source)
    destination_info = bb.get_c_info(destination)
    initial_volume_source = bb.get_volume(source)
    # Variables name simplification for calculation readability
    vt = volume_transfer
    v1 = initial_volume_source
    # Volume uncertainties extractions (deltas = del_ in names, r and s stand for random and systematic)
    del_r_vt = volume_uncertainty(pipette, volume_transfer)[0]
    del_r_v1 = source_info['volume_uncertainty']['random']
    del_r_v2 = destination_info['volume_uncertainty']['random']
    del_s_vt = volume_uncertainty(pipette, volume_transfer)[1]
    del_s_v1 = source_info['volume_uncertainty']['systematic']
    del_s_v2 = destination_info['volume_uncertainty']['systematic']
    # New volume uncertainties calculations
    del_r_v3 = np.sqrt(del_r_vt**2 + del_r_v2**2)
    del_s_v3 = del_s_vt + del_s_v2
    if del_r_v1 != 0:
        del_r_v1 = np.sqrt(del_r_vt**2 + del_r_v1**2)
    if del_s_v1 != 0:    
        del_s_v1 = del_s_vt + del_s_v1
    # Transmission of calculated volume uncertainties to the local dictionary
    source_info['volume_uncertainty']['random'] = del_r_v1
    source_info['volume_uncertainty']['systematic'] = del_s_v1
    destination_info['volume_uncertainty']['random'] = del_r_v3
    destination_info['volume_uncertainty']['systematic'] = del_s_v3
    # Creation of a list containing all the constituents a single time
    source_constituents_list = source_info['constituents']
    destination_constituents_list = destination_info['constituents']
    final_destination_constituents_list = np.unique(source_constituents_list + destination_constituents_list)
    r = vt/v1
    # Transmission of stock information
    for constituent in final_destination_constituents_list:
        if constituent in source_constituents_list:
            vs1 = source_info['volume_stock'][constituent]                  # Initial stock volume in the source
            del_vs1 = source_info['volume_uncertainty_stock'][constituent]  # Stock volume uncertainty in source
            del_vs_t_pc = np.sqrt((del_r_vt/vt)**2+(del_r_v1/v1)**2+(del_vs1/vs1)**2)
            del_vs_t = del_vs_t_pc * (r*vs1)
            source_info['volume_uncertainty_stock'][constituent] = del_vs_t_pc * (1-r)*vs1  
            source_info['volume_stock'][constituent] = vs1*(1-r)
        else: 
            vs1 = 0  
            del_vs_t = 0
        if constituent in destination_constituents_list:
            vs2 = destination_info['volume_stock'][constituent] # Initial stock volume in the destination
            del_vs2 = destination_info['volume_uncertainty_stock'][constituent]
        else:    
            destination_info['concentrations_stock'][constituent] = source_info['concentrations_stock'][constituent]
            destination_info['concentration_uncertainty_stock'][constituent] = source_info['concentration_uncertainty_stock'][constituent]
            vs2 = 0
            del_vs2 = 0
            destination_info['constituents'].append(constituent)
        destination_info['volume_stock'][constituent] = vs2 + r*vs1        
        destination_info['volume_uncertainty_stock'][constituent] = np.sqrt(del_vs2**2 + del_vs_t**2)
    destination_info['constituents_number'] = len(final_destination_constituents_list)
    # Final transmission from local dictionary to well attributes   
    bb.set_c_info(source, source_info)
    bb.set_c_info(destination, destination_info)
############################################################

########
# P50
profile_p50_error = np.array([[0.16, -1.08, 50], # Max pipette volume (100% fill)
                               [0.10, -0.83, 37.5],
                               [0.17, -0.44, 25],
                               [0.05, -0.53, 12.5],
                               [0.14, -0.61, 5]]) # Min pipette volume, i.e. 10% fill
########
# P300
profile_p300_error = np.array([[0.38, -4.4, 300], # Max pipette volume (100% fill)
                               [0.27, -3.88, 225],
                               [0.24, -3.18, 150],
                               [0.15, -2.17, 75],
                               [0.15, -0.83, 30]]) # Min pipette volume, i.e. 10% fill
########
# P1000
profile_p1000_error = np.array([[0.44, 4.56, 1000], # Max pipette volume (100% fill)
                               [0.22, -1.39, 750],
                               [0.31, -1.08, 500],
                               [0.14, -0.25, 250],
                               [0.25, 0.10, 100]])  # Min pipette volume, i.e. 10% fill
############################################################

def call_p50_error_to_vu():
    return profile_to_vu(profile_p50_error)
def call_p300_error_to_vu():
    return profile_to_vu(profile_p300_error)
def call_p1000_error_to_vu():
    return profile_to_vu(profile_p1000_error)
############################################################