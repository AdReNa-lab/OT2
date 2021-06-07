from __future__ import absolute_import

import numpy as np
from opentrons import types

############################################################
### These functions are designed as protocol tools to be used in other functions ###
def get_tip_length(pipette: types.Mount):
    # Get tip length currently in use for a pipette
    tip_racks = pipette._tip_racks[0]
    tip_length = tip_racks.tip_length
    return tip_length

def get_default_flow_rates(pipette: types.Mount):
    default_flow_rates = {}
    default_flow_rates['aspirate'] = pipette._implementation._flow_rates.aspirate
    default_flow_rates['dispense'] = pipette._implementation._flow_rates.dispense
    default_flow_rates['blow_out'] = pipette._implementation._flow_rates.blow_out
    return default_flow_rates
############################################################

def set_c_info(well: types.Location, c_info: dict):
    # Set the c_info dictionary attribute of a well from a properly formatted dictionary
    well._geometry.custom_well_info = c_info
def get_c_info(well: types.Location):
    # Read and returns the c_info attribute of a well
    c_info = well._geometry.custom_well_info
    return c_info
############################################################

def get_h_from_v(well: types.Location, volume: float):
    # Converts a volume in headroom for a particular well
    info = get_c_info(well)
    h_given_v = info['vh_functions']['h_given_v']
    headroom = h_given_v(volume)
    return headroom
def get_v_from_h(well: types.Location, headroom: float):
    # Converts a headroom in volume for a particular well
    info = get_c_info(well)
    v_given_h = info['vh_functions']['v_given_h']
    volume = v_given_h(headroom)
    return volume
############################################################

def set_headroom(well: types.Location, headroom: float):
    # Set the headroom and volume attributes of a well from a headroom input
    info = get_c_info(well)
    info['headroom'] = headroom
    volume = get_v_from_h(well, headroom)
    info['volume'] = volume
    set_c_info(well, info)
def get_headroom(well: types.Location):
    # Reads and return the headroom of a well
    info = get_c_info(well)
    headroom = info['headroom']
    return headroom
############################################################

def set_volume(well: types.Location, volume: float):
    # Set the headroom and volume attributes of a well from a volume input
    info = get_c_info(well)
    info['volume'] = volume
    headroom = get_h_from_v(well, volume)
    info['headroom'] = headroom
    set_c_info(well, info)
def get_volume(well: types.Location):
    # Reads and return the volume of a well
    info = get_c_info(well)
    volume = info['volume']
    return volume
############################################################

def get_relative_from_flow_rate_aspirate(pipette: types.Mount, flow_rate: float):
    # Converts a flow rate in uL/s in a ratio of the default aspirate flow rate 
    flow_rates = get_default_flow_rates(pipette)
    default_aspirate = flow_rates['aspirate']
    relative_flow_rate = flow_rate/default_aspirate
    return relative_flow_rate
def get_relative_from_flow_rate_dispense(pipette: types.Mount, flow_rate: float):
    # Converts a flow rate in uL/s in a ratio of the default dispense flow rate 
    flow_rates = get_default_flow_rates(pipette)
    default_dispense = flow_rates['dispense']
    relative_flow_rate = flow_rate/default_dispense
    return relative_flow_rate
############################################################

def set_constituent(well: types.Location, 
                    constituent: str,
                    concentration: float,
                    c_uncertainty: float = 0,
                    v_uncertainty: float = 0):
    """
    This function is used to input concentration and uncertainties information of a constituent in a protocol.
    
    - constituent is a string containing the name used to designate the constituent throughout the protocol
    - concentration is given in ng/ml of the constituent
    - uncertainties on the concentration are split between a random and systematic one. 
      If one is 0 or unknown, it doesn't need to be inputed (defaults to 0)
    """
    c_info = get_c_info(well)
    c_info['constituents_number'] += 1
    c_info['constituents'].append(constituent)
    c_info['concentrations_stock'][constituent] = concentration
    c_info['concentration_uncertainty_stock'][constituent] = c_uncertainty
    c_info['volume_stock'][constituent] = get_volume(well)
    c_info['volume_uncertainty_stock'][constituent] = v_uncertainty
    set_c_info(well, c_info)
def get_constituents(well: types.Location):
    # This function reads and returns all the constituents present in a well
    c_info = get_c_info(well)
    constituents = c_info['constituents']  
    return constituents
############################################################

def set_pipette_uncertainties(pipette: types.Mount,
                              vu_function: list):
    # This function creates an attribute for a pipette allowing calculation of uncertainties 
    # on volumes transferred with this pipette
    uncertainties_functions = {
        'random': vu_function[0],
        'systematic': vu_function[1]
    }
    pipette.uncertainties_dict = uncertainties_functions
def get_pipette_uncertainties(pipette: types.Mount):
    # This function reads and return the volume uncertainties functions linked to a pipette

    return pipette.uncertainties_dict
############################################################

def get_concentration(well: types.Location,
                      constituent: str):
    # Reads and returns the concentration and uncertainty of a constituent in a well. Dependent on stored stock information
    c_info = get_c_info(well)
    
    try:
        # Extracts info from the well
        stock_volume = c_info['volume_stock'][constituent]
        # Volume of the well is corrected for the systematic uncertainty in calculations
        corrected_well_volume = get_volume(well) + c_info['volume_uncertainty']['systematic']
        well_volume_unc = c_info['volume_uncertainty']['random']
        stock_concentration = c_info['concentrations_stock'][constituent]
        stock_c_unc = c_info['concentration_uncertainty_stock'][constituent]
        stock_v_unc = c_info['volume_uncertainty_stock'][constituent]
        # Calculates concentration and uncertainty in the well
        stock_ratio = stock_volume/corrected_well_volume
        concentration = stock_ratio*stock_concentration
        # Lower-end calculation, considering stock volume as a constant without associated uncertainty 
        # (i.e. fully correlated to well volume)
        low_c_unc_pc = np.sqrt((stock_c_unc/stock_concentration)**2 + (well_volume_unc/corrected_well_volume)**2)
        low_c_unc = low_c_unc_pc*concentration
        # Higher-end calculation, considering stock volume as independent from well volume, with own unertainty 
        high_c_unc_pc = np.sqrt((stock_v_unc/stock_volume)**2 + (stock_c_unc/stock_concentration)**2 + (well_volume_unc/corrected_well_volume)**2)
        high_c_unc = high_c_unc_pc*concentration
        # Returns the concentration and uncertainty in the same unit (not in %)
        return concentration, low_c_unc, high_c_unc
        
    except KeyError:
        print('Warning, constituent {} is not present in well {}'.format(constituent,well))
        return 0,0,0
############################################################
### This function is used to initiate well attributes ###
def initiate_well(well: types.Location, 
                  volume_function: list):
    """
    This function is used to initiate a well's custom attributes. Those attributes are regrouped as a dictionary 
    with default values as follows:
    
    - Numerical values as 0
    - Headroom and vh_functions specific to the well
    - concentrations and uncertainties are dependent on thesubstances used in the protocol 
      and thus initiated as 'None' or left empty
    """
    c_info = {'constituents_number': 0, 
              'volume': 0,
              'headroom': None,
              'vh_functions': {
                  'v_given_h': None,
                  'h_given_v': None},
              'volume_uncertainty': {
                  'random': 0,
                  'systematic': 0},
              'constituents': [], 
              'concentrations_stock': {},
              'concentration_uncertainty_stock': {},
              'volume_stock': {},
              'volume_uncertainty_stock': {}
             }
    
    c_info['headroom'] = well._geometry._depth
    c_info['vh_functions']['v_given_h'] = volume_function[0]
    c_info['vh_functions']['h_given_v'] = volume_function[1]
    set_c_info(well, c_info)
############################################################

def print_solution_info(well: types.Location):
    # Reads and print the entire dictionary 'c_info' of a well
    c_info = get_c_info(well)
    #return (well, c_info)
    print('\nInformation of well {}:'.format(well))
    for key, val in c_info.items():
        print(key, ': ', val)
    print()
def print_constituent_concentration(well: types.Location,
                                    constituent: str,
                                    label: str = None):
    info = get_c_info(well)
    if label:
        name = label
    else:
        name = well
    
    if constituent in info['constituents']:
        concentration, low_unc, high_unc = get_concentration(well, constituent)
        print('\nConcentration of constituent {} in well {} is {} \u00B1 ({} - {}) ng/mL'.format(constituent, name, round(concentration, 2), round(low_unc, 2), round(high_unc, 2)))
    else:
        print('\nConstituent ' + constituent + ' is not present in well: ' +str(well))
############################################################