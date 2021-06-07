from opentrons import protocol_api
import numpy as np
from opentrons.types import Point
from opentrons.types import Location
from opentrons import types
from opentrons import protocols
metadata = {
    'apiLevel': '2.9', # maximum supported API level is visible in the Opentrons App
    'protocolName':'Reference Protocol',
    'description':'Reference document containing most up to date custom functions for OT-2',
    'author': 'Alaric Taylor'}
def run(protocol: protocol_api.ProtocolContext):
    #############
    # Deck layout
    # Tiprack import - different tips for the same pipette have their own custom labware definition
    tiprack300 = protocol.load_labware('adrena_tiprack_300ul_8row_12column',
                                        location='5',
                                        label='tiprack')
    tiprack1000 = protocol.load_labware('adrena_tiprack_1250ul_8row_12column',
                                        location='8',
                                        label='tiprack')
    # Custom labware import - example of easy to remember/use later naming
    tuberack_epp1500 = protocol.load_labware('adrena_epptube_1500ul_rack_5row_8column',
                                        location='2',
                                        label='eppendorf')
    tuberack_falc50 = protocol.load_labware('adrena_falctube_50ml_rack_2row_3column',
                                        location='3',
                                        label='falcon_50ml')
    sdfsg
    # Pipettes import, non-mounted pipettes should be commented out
    #p50 = protocol.load_instrument('p50_single', 'left', tip_racks=[tiprack50])
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack300])
    p1000 = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack1000])
    # Associate an uncertainties array to each pipette 
    #set_pipette_uncertainties(p50, p50_vu)
    set_pipette_uncertainties(p300, p300_vu)
    #set_pipette_uncertainties(p1000, p1000_vu)
    """
    Template "for" loop to initiate tubes headroom and concentration/uncertainties data, 
    should be added for each different kind of labware used (examples below)
    for well in tubes.wells():
        initiate_well(well, tube_type_vh, substances_names)  
    This function Initiates: 
    headroom (empty well)
    volume_headroom_functions uniques for each well type by defining gradations 
    and then running this through the gradations_to_vh() function, above
    c_info with all concentrations and uncertainties set to 0
    """    
    #### All custom labware headroom definitions
    for well in tuberack_epp1500.wells():
        initiate_well(well, epptube_1500ul_vh)
    for well in tuberack_falc50.wells():
        initiate_well(well, ftube_50ml_vh)
    """
    volume_headroom_functions must be transmitted for each kind of tubes used, below is a list of common function names:    
    Type of tube       Function name
    TLC well 50 uL     tlc_50ul_vh
    Eppendorf 1.5 mL   epptube_1500ul_vh
    Eppendorf 5 mL     epptube_50ml_vh
    Eppendorf 15 mL    epptube_15ml_vh
    Eppendorf 50 mL    epptube_50ml_vh
    Falcon 15 mL       ftube_15ml_vh
    Falcon 50 mL       ftube_50ml_vh
    Vial 2 mL          vial_2ml_vh
    Vial 4 mL          vial_4ml_vh
    Vial 8 mL          vial_8ml_vh
    Vial 20 mL         vial_20ml_vh
    Vial 30 mL         vial_30ml_vh
    Cuvette 70 uL      cuvette_70ul_vh
    """
    # Well and tips naming - wells and tips can be named to ease protocol writing, examples are given below
    tip_water = tiprack300['A1']
    solvent = tuberack_falc50['A1']
    stock_dox = tuberack_falc50['A2']
    stock_epi = tuberack_falc50['A3']
    destination = tuberack_epp1500['A1']
    # Headroom definition - headroom must be manually inputed for non-empty containers at the start of the experiment
    set_headroom(solvent, 10)
    set_headroom(stock_dox, 10)
    set_headroom(stock_epi, 10)
    # Solution definition - initiates concentration and uncertainties for stock solutions, example values are given below
    set_constituent(stock_dox, constituent = 'dox', concentration = 15000, c_uncertainty = 150)
    set_constituent(stock_epi, constituent = 'epi', concentration = 10000, c_uncertainty = -80)    
    # Example of parameters definition
    pipette = p300     
    volume = 100       
    wetting_cycles = 3
    mixing_cycles = 5
    aspirate_rate = 100
    dispense_rate = 200
    # Example protocol testing all the custom functions - most functions can be given additional parameters, 
    # see the functions definitions for more information
    pipette.pick_up_tip()
    custom_aspirate(pipette, volume, solvent, rate = aspirate_rate)
    custom_dispense(pipette, volume, destination, rate = dispense_rate)
    print('Verify that {} uL have been aspirated in {} and dispensed in {}'.format(volume, solvent, destination))
    print('The following rates should have been used: {} uL/s for aspiration and {} uL/s for dispense \n'.format(aspirate_rate, dispense_rate))
    custom_wetting(pipette, volume, solvent, wetting_cycles)
    print('Verify that wetting has been performed in well {}, with {} cycles of {} uL \n'.format(solvent, wetting_cycles, volume))
    uncertainties_calculation(pipette, volume, solvent, destination)
    custom_touch_tip(pipette, destination)
    print('Verify that touch tip occured with 3 touch points \n')
    custom_transfer_forward(pipette, volume, stock_dox, destination, aspirate_rate = aspirate_rate/2, dispense_rate = dispense_rate*2)
    print('Verify that {} uL have been aspirated in {} and dispensed in {}'.format(volume, stock_dox, destination))
    print('The following rates should have been used: {} uL/s for aspiration and {} uL/s for dispense \n'.format(aspirate_rate/2, dispense_rate*2))
    custom_transfer_reverse(pipette, volume*2, stock_epi, destination)
    print('Verify that {} uL have been aspirated in {} and dispensed in {} \n'.format(volume, stock_epi, destination))
    current_volume = get_volume(destination)
    custom_mixing_static(pipette, volume, destination, mixing_cycles)
    print('Verify that mixing occured in the middle of well {}, with {} cycles {} uL and a mixing ratio = {} \n'.format(destination, mixing_cycles, volume, volume/current_volume))
    custom_mixing_top_to_bottom(pipette, volume, destination, mixing_cycles)
    print('Verify that mixing occured top to bottom in well {}, with {} cycles {} uL and a mixing ratio = {} \n'.format(destination, mixing_cycles, volume, volume/current_volume))
    pipette.return_tip()
    # Function to print all the attributes of a well in a simulation
    # IMPORTANT: use custom_transfer functions for automatic tracking, 
    #or call `uncertainties_calculation()` BEFORE custom_aspirate in the main function
    # Example of well info printing
    print_solution_info(destination)
    print("\nConcentration information for constituent 'dox' in well {}".format(destination))
    print(get_concentration(destination, 'dox'))
    print("\nConcentration information for constituent 'epi' in well {}".format(destination))
    print(get_concentration(destination, 'epi'))
    print_constituent_concentration(destination, 'dox')
    print('\nVerify that calculated concentrations and uncertainties are correct for the given data')
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
def set_headroom(well: types.Location, 
                 headroom: float):
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
def get_h_from_v(well: types.Location, 
                 volume: float):
    # Converts a volume in headroom for a particular well
    info = get_c_info(well)
    h_given_v = info['vh_functions']['h_given_v']
    headroom = h_given_v(volume)
    return headroom
def get_v_from_h(well: types.Location, 
                 headroom: float):
    # Converts a headroom in volume for a particular well
    info = get_c_info(well)
    v_given_h = info['vh_functions']['v_given_h']
    volume = v_given_h(headroom)
    return volume
def set_volume(well: types.Location, 
               volume: float):
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
def set_c_info(well: types.Location, 
               c_info: dict):
    # Set the c_info dictionary attribute of a well from a properly formatted dictionary
    well._geometry.custom_well_info = c_info
def get_c_info(well: types.Location):
    # Read and returns the c_info attribute of a well
    c_info = well._geometry.custom_well_info
    return c_info
def get_relative_from_flow_rate_aspirate(pipette: types.Mount,
                                         flow_rate: float):
    # Converts a flow rate in uL/s in a ratio of the default aspirate flow rate 
    flow_rates = get_default_flow_rates(pipette)
    default_aspirate = flow_rates['aspirate']
    relative_flow_rate = flow_rate/default_aspirate
    return relative_flow_rate
def get_relative_from_flow_rate_dispense(pipette: types.Mount,
                                         flow_rate: float):
    # Converts a flow rate in uL/s in a ratio of the default dispense flow rate 
    flow_rates = get_default_flow_rates(pipette)
    default_dispense = flow_rates['dispense']
    relative_flow_rate = flow_rate/default_dispense
    return relative_flow_rate
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
    constituents = c_info[constituents]
    return constituents
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
    uncertainties_functions = pipette.uncertainties_dict
    return pipette.uncertainties_dict
def get_concentration(well: types.Location,
                      constituent: str):
    # Reads and returns the concentration and uncertainty of a constituent in a well. Dependent on stored stock information
    c_info = get_c_info(well)
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
    """
    Example full dictionary:
    custom_well_info = {'constituents_number': 2, 
                        'volume': 500,
                        'headroom': 20,
                        'vh_functions': {
                            'v_given_h': epptube_1500ul_vh[0],
                            'h_given_v': epptube_1500ul_vh[1]},
                        'volume_uncertainty': {
                            'random': 0.9006664199358163,
                            'systematic': -1.56},
                        'substances': ['dox', 'epi'], 
                        'concentrations_stock': {
                            'dox': 3333.3333333333335, 
                            'epi': 4999.999999999999},
                        'concentration_uncertainty_stock': {
                              'dox': 63.85400013572628,
                              'epi': 33.342221037352985}
                        'volume_stock': {
                              'dox': 100,
                              'epi': 50}
          }
    """
def print_solution_info(well: types.Location):
    # Reads and print the entire dictionary 'c_info' of a well
    c_info = get_c_info(well)
    print('Information of well {}:'.format(well))
    print(c_info)
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
        print('Concentration of constituent {} in well {} is {} \u00B1 ({} - {}) ng/mL'.format(constituent, name, round(concentration, 2), round(low_unc, 2), round(high_unc, 2)))
    else:
        print('Constituent ' +constituent + ' is not present in well: ' +str(well))
def custom_aspirate(pipette: types.Mount,
                    transfer_volume: float,
                    location: types.Location,
                    immersion_depth: float = 2,
                    safety_height: float = 0.5,                    
                    rate: float = 75):
    """
    Custom aspiration function
    By default: aspirates 2 mm below the meniscus level
    Function-specific arguments:
    - immersion_depth (in mm) beneath meniscus
    - safety_height prevents the tip from crashing into bottom of the well
    - rate in uL/s
    """
    # Arguments checking
    assert transfer_volume > 0
    assert safety_height >= 0
    # Conversion from a rate in ul/s to a relative rate
    rate_rel = get_relative_from_flow_rate_aspirate(pipette, rate)
    # Extraction or calculation of headrooms and volumes before and after aspiration
    initial_volume = get_volume(location)
    final_volume = initial_volume - transfer_volume
    initial_headroom = get_headroom(location)
    final_headroom = get_h_from_v(location, final_volume)
    # depth_to_aspirate is the distance from the top of the well at which aspiration will take place
    depth_to_aspirate = final_headroom + immersion_depth
    # Modifies the headroom in the well attributes
    set_headroom(location, final_headroom)
    # Safety checking
    # ...avoidance of these errors are also covered by the use 
    # of specified extrapolation fill_values in the gradations_to_vh() function
    # Low volume/aspiration height warning
    depth = get_h_from_v(location, 0)
    if depth_to_aspirate > depth - safety_height:
        depth_to_aspirate = depth - safety_height  # e.g. 0.5mm above the bottom of the well
        print('Warning, aspiration height for well ' +str(location) +' is lower than ' +str(safety_height) +' mm')
    # Avoids tip submersion in liquid
    tip_length = get_tip_length(pipette)
    if depth_to_aspirate > 0.8*tip_length + initial_headroom:  # Checks that the pipette tip will not be fully submerged
        depth_to_aspirate = 0.8*tip_length + initial_headroom
        print('Warning, aspiration depth was set lower then pipette tip length, it has been changed to ' +str(depth_to_aspirate))
    if depth_to_aspirate < 0: 
        depth_to_aspirate = 0 # i.e. at the top of the well
    pipette.aspirate(transfer_volume, location.top(-depth_to_aspirate), rate = rate_rel)
def custom_dispense(pipette: types.Mount,
                    transfer_volume: float,
                    location: types.Location,
                    immersion_depth: float = 0,
                    safety_height: float = 1,
                    rate: float = 300):
    """
    Custom dispense function, by default: 
    - Dispenses in air (at the top of a position)
    Function-specific arguments:
    - immersion_depth is the position relative to the meniscus, a positive number is lower than the meniscus (in liquid)
    - safety_height is used to prevent overflow of a container
    - rate in uL/s
    """ 
    # Arguments checking
    assert transfer_volume > 0
    assert safety_height >= 0
    # Conversion from a rate in ul/s to a relative rate to the default
    rate_rel = get_relative_from_flow_rate_dispense(pipette, rate)
    # Extraction or calculation of headrooms and volumes before and after aspiration
    initial_volume = get_volume(location)
    final_volume = initial_volume + transfer_volume
    initial_headroom = get_headroom(location)
    final_headroom = get_h_from_v(location, final_volume)
    # dispense_depth is the distance from the top of the well at which dispense will take place
    dispense_depth = final_headroom + immersion_depth
    # Modifies the headroom in the well attributes
    set_headroom(location, final_headroom)
     # Avoids tip submersion in liquid   
    tip_length = get_tip_length(pipette)
    if dispense_depth > 0.8*tip_length + initial_headroom:  # Checks that the pipette tip will not be fully submerged
        depth_to_aspirate = 0.8*tip_length + initial_headroom
        print('Warning, dispense depth was set lower then pipette tip length, it has been changed to ' +str(dispense_depth))
    # Safety checking for overflow
    if safety_height == 0:
        print('Warning, anti-overflow check has been deactivated by setting the safety height to 0')
    elif final_headroom <= safety_height:
        print('Overflow risks! Dispense cancelled for ' + str(location))
    else:
        if final_headroom < safety_height + 1:
            print('Warning, container is almost full: ' + str(location))
        pipette.dispense(transfer_volume, location.top(-dispense_depth), rate = rate_rel)
def custom_wetting(pipette: types.Mount,
                   volume: float,
                   location: types.Location,
                   wetting_cycles: int = 3):
    """
    This function performs an aspiration followed by a dispense in order to wet the pipette tip
    Security checks for this function are the ones included in custom_aspirate and custom_dispense
    """
    # Arguments checking
    assert volume > 0
    for i in range(wetting_cycles):
        custom_aspirate(pipette, volume, location)
        custom_dispense(pipette, volume, location)
    pipette.blow_out(location.top(-2))
    custom_touch_tip(pipette, location)
def custom_mixing(pipette: types.Mount,
                  mixing_volume: float,
                  location: types.Location, 
                  cycles: int,
                  aspiration_depth: float,
                  dispense_immersion_depth: float,
                  aspirate_rate: float = 75,
                  dispense_rate: float = 600):  
    """
    Mixing function aspirating close to the meniscus and dispensing at the bottom of the container.
    This can be interesting to improve mixing in conical containers to created vortices in the tapered area
    Function-specific arguments:
    - aspiration_depth is how deep in the liquid the tip will aspirate
    - dispense_height is the distance from the bottom of the container at which dispense will take place
    - rates in uL/s
    """
    # Arguments checking
    assert mixing_volume > 0
    assert cycles >= 1
    # Mixing fraction calculation and print
    max_volume = get_volume(location)
    volume_mixing_fraction = mixing_volume / max_volume
    print('Volume mixing fraction at ' +str(location), ' is '+str(np.round(volume_mixing_fraction, 2)))
    if volume_mixing_fraction <0.2:
        print('...which may be too low!')
    if volume_mixing_fraction >0.8:
        print('...which may be too high!')
    for i in range(0, cycles):
        custom_aspirate(pipette, mixing_volume, location, rate = aspirate_rate, immersion_depth = aspiration_depth)
        custom_dispense(pipette, mixing_volume, location, rate = dispense_rate, immersion_depth = dispense_immersion_depth) 
    pipette.blow_out(location.top(-2))
    custom_touch_tip(pipette, location)
def custom_mixing_top_to_bottom(pipette: types.Mount,
                                mixing_volume: float,
                                location: types.Location, 
                                cycles: int,
                                aspiration_immersion_depth: float = 2,
                                dispense_height: float = 1,
                                aspirate_rate: float = 75,
                                dispense_rate: float = 600):  
    """
    Mixing function aspirating close to the meniscus and dispensing at the bottom of the container.
    This can be interesting to improve mixing in conical containers to created vortices in the tapered area
    Function-specific arguments:
    - aspiration_depth is how deep in the liquid the tip will aspirate
    - dispense_height is the distance from the bottom of the container at which dispense will take place
    - rates in uL/s
    """
    # Extraction or calculation of headrooms and volumes before and after aspiration
    max_volume = get_volume(location)
    min_volume = max_volume - mixing_volume
    max_headroom = get_h_from_v(location, min_volume)
    # Depth of a well is determined by reading the headroom of an empty well container (volume = 0)
    well_depth = get_h_from_v(location, 0)
    # dispense_depth is the distance from the top of the well, 
    # immersion_depth from the meniscus (used for custom_dispense())
    dispense_depth = well_depth - dispense_height
    dispense_immersion_depth = dispense_depth - max_headroom
    custom_mixing(pipette, mixing_volume, location, cycles, aspiration_immersion_depth, dispense_immersion_depth, aspirate_rate, dispense_rate)
def custom_mixing_bottom_to_top(pipette: types.Mount,
                                mixing_volume: float,
                                location: types.Location, 
                                cycles: int,
                                aspiration_height: float = 1,
                                dispense_immersion_depth: float = 1,
                                aspirate_rate: float = 75,
                                dispense_rate: float = 600):  
    """
    Mixing function aspirating close to the meniscus and dispensing at the bottom of the container.
    This can be interesting to improve mixing in conical containers to created vortices in the tapered area
    Function-specific arguments:
    - aspirate_height is the distance from the bottom of the container at which aspiration will take place
    - dispense_depth is how deep in the liquid the tip will dispense
    - rates in uL/s
    """
    # Extraction or calculation of headrooms and volumes before and after aspiration
    max_volume = get_volume(location)
    min_volume = max_volume - mixing_volume
    max_headroom = get_h_from_v(location, min_volume)
    # Depth of a well is determined by reading the headroom of an empty well container (volume = 0)
    well_depth = get_h_from_v(location, 0)
    # dispense_depth is the distance from the top of the well, 
    # immersion_depth from the meniscus (used for custom_aspirate())
    aspiration_depth = well_depth - aspirate_height
    aspiration_immersion_depth = aspirate_depth - max_headroom
    custom_mixing(pipette, mixing_volume, location, cycles, aspiration_immersion_depth, dispense_immersion_depth, aspirate_rate, dispense_rate)
def custom_mixing_static(pipette: types.Mount,
                                mixing_volume: float,
                                location: types.Location, 
                                cycles: int,
                                relative_depth: float = 0.5,
                                aspirate_rate: float = 75,
                                dispense_rate: float = 600):  
    """
    Mixing function aspirating and dispensing in the same predefined position
    Function-specific arguments:
    - relative_depth give the position in the liquid at which mixing will take place, e.g. 0.5 in the middle of the liquid
    - rates in uL/s
    """
    # Extraction or calculation of headrooms and volumes before and after aspiration
    max_volume = get_volume(location)
    min_volume = max_volume - mixing_volume
    min_headroom = get_headroom(location)
    max_headroom = get_h_from_v(location, min_volume)
    # Depth of a well is determined by reading the headroom of an empty well container (volume = 0)
    well_depth = get_h_from_v(location, 0)
    # Determination of the mixing positon within the liquid
    mixing_position = relative_depth*(well_depth - max_headroom)
    custom_mixing(pipette, mixing_volume, location, cycles, mixing_position, mixing_position, aspirate_rate, dispense_rate)
def custom_transfer_forward(pipette: types.Mount,
                            volume: float,
                            source: types.Location, 
                            destination: types.Location, 
                            pre_wet: int = 0,
                            aspirate_rate: float = 75,
                            dispense_rate: float = 300,
                            touch_tip_position: str = 'none'):
    """
    A transfer function aspirating the exact desired volume from the source 
    Split in several equal transfers if the volume is higher than the pipette capacity
    Can typically be used for low-viscosity/aqueous solutions, such as buffers, diluted acids or alkalis
    By default:
    - Will not perform a pre-wetting operation before the first transfer
    Function-specific arguments:
    - pre_wet defines the number of pre-wetting steps that will be done (0 = no pre wetting)
    - touch_tip_position allows touching tip at the source or destination after each transfer step if desired
    - rates in uL/s
    """
    # Arguments checking
    assert volume > 0
    # If the transfer volume is lower than the pipette max volume, only 1 step is required, otherwise splits in equal strokes
    if volume <= pipette.max_volume:
        volume_list = [volume]
    else:
        number_of_passes = int(np.ceil((volume / (pipette.max_volume))))
        volume_per_pass = volume/number_of_passes
        volume_list = np.ones(number_of_passes)*volume_per_pass
    # pre_wet determines the number of wetting cycles
    if pre_wet != 0:
        custom_wetting(pipette, volume_list[0], source, pre_wet)
    for pass_volume in volume_list:
        uncertainties_calculation(pipette, pass_volume, source, destination) # Uncertainties function need to be called 
                                                                             # before custom_aspirate and custom_dispense
        custom_aspirate(pipette, pass_volume, source, rate = aspirate_rate)
        custom_touch_tip(pipette, source)
        custom_dispense(pipette, pass_volume, destination, rate = dispense_rate)
        pipette.blow_out(destination.top(-2))
        if touch_tip_position == 'destination':
            custom_touch_tip(pipette, destination)
        elif touch_tip_position == 'source':
            custom_touch_tip(pipette, source)
        # Generally do NOT touch_tip() on the destination
        # as this could cause backwards contamination
def custom_transfer_reverse(pipette: types.Mount,
                            volume: float,
                            source: types.Location, 
                            destination: types.Location,
                            disposal_volume: float = 5,
                            aspirate_rate: float = 37,
                            dispense_rate: float = 150,
                            pre_wet: int = 0,
                            touch_tip_position: str = 'none'):
    """
    A transfer function aspirating more than required, dispensing the exact volume at destination and excess back at source
    Typically used for solution with high viscosity or a tendency to foam
    Also recommended for small volumes of low-viscosity solution
    By default:
    - Takes a supplementary (disposal_volume) of 5 ml
    - Does not perform a pre-wetting step
    Function-specific arguments:
    - disposal_volume is the supplementary volume to aspirate at source and return after dispensing
    - pre_wet defines the number of pre-wetting steps that will be done (0 = no pre wetting)
    - touch_tip_position allows touching tip at the destination after each transfer step if desired
    - rates in uL/s
    """
    # Arguments checking
    assert volume > 0
    assert disposal_volume >= 0
    # Transfer splitting, the toal volume is split in however many equal strokes needed to be fully transferred
    if volume <= pipette.max_volume:
        if volume + disposal_volume > pipette.max_volume:
            print('Warning, in order to include a disposal volume this transfer will be split into several passes...')
    if volume + disposal_volume <= pipette.max_volume:
        volume_list = [volume]
    else:
        number_of_passes = int(np.ceil((volume / (pipette.max_volume - disposal_volume))))
        volume_per_pass = volume/number_of_passes
        volume_list = np.ones(number_of_passes)*volume_per_pass
    if pre_wet != 0:
        custom_wetting(pipette, volume_list[0]+disposal_volume, source, pre_wet)
    for pass_volume in volume_list:
        uncertainties_calculation(pipette, pass_volume, source, destination)
        custom_aspirate(pipette, pass_volume + disposal_volume, source, rate = aspirate_rate)
        custom_touch_tip(pipette, source)
        custom_dispense(pipette, pass_volume, destination, rate = dispense_rate)
        if touch_tip_position == 'destination':
            custom_touch_tip(pipette, destination)
        elif touch_tip_position == 'source':
            custom_touch_tip(pipette, source)
        # Return the remainder to the source 
        custom_dispense(pipette, disposal_volume, source)
        pipette.blow_out(source.top(-2))
        custom_touch_tip(pipette, source)
def custom_touch_tip(pipette: types.Mount,
                     well: types.Location, 
                     depth: float = 2,
                     radius_offset: float = 1,
                     speed: float = 200,
                     increments: int = 3):
    """
    Movement function that follows the edge of a circular well with the tip in contact with the glass
    Allows complete removal of any pending drop on the tip
    Function-specific arguments:
    - depth is the distance from the top of the well at which the tip will touch, a positive number
    - radius_position defines how close to the wall the tip is brought, 
      it allows touching the wall more lightly or simply come in close distance without touching
    - speed changes the movement speed during the touch tip
    - increments are the number of stopping steps along the perimeter of the circle
    """   
    # Arguments checking
    assert increments >= 1
    depth = abs(depth)    # depth must be positive, however inputing a negative number for a depth is an easy mistake
    if well._geometry._diameter:
        radius = (well._geometry._diameter/2) - radius_offset
        well_top = well._geometry._position
        #print(well_top)
        thetas = np.linspace(start=0, stop=2*np.pi, num=increments, endpoint=False)
        x_offsets = radius*np.cos(thetas)
        y_offsets = radius*np.sin(thetas)
        touch_locations = [] # initialise list
        for i in range(increments):
            offset = Point(x_offsets[i], y_offsets[i], -depth)
            # Populate list of locations
            touch_locations.append(Location(well_top.__add__(offset), 'Touch point '+str(i+1)))
        pipette.move_to(well.top())
        for location in touch_locations:
            #print(location)
            pipette.move_to(location, force_direct=True, speed=speed)
        pipette.move_to(well.top())  # Might not be required
    else:
        print('Well is not circular, so just using standard touch_tip() command')
        pipette.touch_tip(location=well, v_offset=depth)
def custom_tlc_spotting(pipette: types.Mount,
                        source: types.Location, 
                        destination: types.Location,
                        volume: float = 5,
                        air_gap: float = 10):
    """
    Fonction used to spot a tlc plate placed on the custom holder for the OT-2
    For tlc spotting, we don't necessary want to dispense...going to the position, in contact with the paper could be sufficient
    """
    pipette.aspirate(air_gap*2/3, source.top())
    custom_aspirate(pipette, volume, source)
    custom_touch_tip(pipette, source)
    pipette.aspirate(air_gap/3, source.top())
    pipette.move_to(destination.top())
    #protocol.pause(2)
    pipette.dispense(volume, destination, rate = 0.2)
    pipette.blow_out()
"""
Generate volume_headroom_functions for each type of tube in use from 
measured gradations
"""
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
gradations_epptube_1500ul = np.array([[8,1500], # Top gradation of container i.e. maximum liquid fill
                                      [16.4,1000],
                                      [27.4,400],
                                      [35.2, 100],
                                      [40, 20],
                                      [42.2,0]]) # Bottom of container i.e. no liquid
epptube_1500ul_vh = gradations_to_vh(gradations_epptube_1500ul)
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
ambtube_1500ul_vh = gradations_to_vh(gradations_ambtube_1500ul)
gradations_ftube_15ml = np.array([[13.8, 15000], # Top gradation of container i.e. maximum liquid fill
                                  [93.8, 2000],
                                  [101.6, 1000],
                                  [118.1, 0]]) # Bottom of container i.e. no liquid
ftube_15ml_vh = gradations_to_vh(gradations_ftube_15ml)
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
epptube_5ml_vh = gradations_to_vh(gradations_epptube_5ml)
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
epptube_15ml_vh = gradations_to_vh(gradations_epptube_15ml)
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
epptube_50ml_vh = gradations_to_vh(gradations_epptube_50ml)
gradations_ftube_50ml = np.array([[8, 50000], # Top gradation of container i.e. maximum liquid fill
                                  [94.9, 4000],
                                  [103.5, 1000],
                                  [113.5, 0]]) # Bottom of container i.e. no liquid
ftube_50ml_vh = gradations_to_vh(gradations_ftube_50ml)
gradations_vial_1500ul = np.array([[12.7, 1500], # Top gradation of container i.e. maximum liquid fill
                                   [30.9, 0]]) # Bottom of container i.e. no liquid
vial_1500ul_vh = gradations_to_vh(gradations_vial_1500ul)
gradations_vial_2ml = np.array([[11, 2000], # Top gradation of container i.e. maximum liquid fill
                                [34.2, 0]]) # Bottom of container i.e. no liquid
vial_2ml_vh = gradations_to_vh(gradations_vial_2ml)
gradations_vial_4ml = np.array([[15,4000], # Top gradation of container i.e. maximum liquid fill
                                [44,0]])   # Bottom of container i.e. no liquid
vial_4ml_vh = gradations_to_vh(gradations_vial_4ml)
gradations_vial_8ml = np.array([[12.8, 8000], # Top gradation of container i.e. maximum liquid fill
                                [58.7, 0]]) # Bottom of container i.e. no liquid
vial_8ml_vh = gradations_to_vh(gradations_vial_8ml)
gradations_vial_20ml = np.array([[17.26, 20000], # Top gradation of container i.e. maximum liquid fill
                                 [55.6, 0]]) # Bottom of container i.e. no liquid
vial_20ml_vh = gradations_to_vh(gradations_vial_20ml)
gradations_vial_30ml = np.array([[16.3, 30000], # Top gradation of container i.e. maximum liquid fill
                                 [93.3, 0]]) # Bottom of container i.e. no liquid
vial_30ml_vh = gradations_to_vh(gradations_vial_30ml)
gradations_cuvette_70ul = np.array([[10, 900],
                                    [15, 600], # Top gradation of container i.e. maximum liquid fill
                                    [21, 300],
                                    [28.5, 70],
                                    [32.2, 0]]) # Bottom of container i.e. no liquid
cuvette_70ul_vh = gradations_to_vh(gradations_cuvette_70ul)
gradations_tlc_50ul = np.array([[0, 50], # Top gradation of container i.e. maximum liquid fill
                                [0.1, 0]]) # Bottom of container i.e. no liquid
tlc_50ul_vh = gradations_to_vh(gradations_tlc_50ul)
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
profile_p50_error = np.array([[0.16, -1.08, 50], # Max pipette volume (100% fill)
                               [0.10, -0.83, 37.5],
                               [0.17, -0.44, 25],
                               [0.05, -0.53, 12.5],
                               [0.14, -0.61, 5]]) # Min pipette volume, i.e. 10% fill
p50_vu = profile_to_vu(profile_p50_error)
profile_p300_error = np.array([[0.38, -4.4, 300], # Max pipette volume (100% fill)
                               [0.27, -3.88, 225],
                               [0.24, -3.18, 150],
                               [0.15, -2.17, 75],
                               [0.15, -0.83, 30]]) # Min pipette volume, i.e. 10% fill
p300_vu = profile_to_vu(profile_p300_error)
profile_p1000_error = np.array([[0.44, 4.56, 1000], # Max pipette volume (100% fill)
                               [0.22, -1.39, 750],
                               [0.31, -1.08, 500],
                               [0.14, -0.25, 250],
                               [0.25, 0.10, 100]])  # Min pipette volume, i.e. 10% fill
p1000_vu = profile_to_vu(profile_p1000_error)
def volume_uncertainty(pipette: types.Mount, 
                       volume: float):
    # This function calculates the uncertainties for a volume depending on what pipette is used
    # Extracts pipette uncertainty functions
    functions_dict = get_pipette_uncertainties(pipette)
    volume_to_random_uncertainty = functions_dict['random']
    volume_to_systematic_uncertainty = functions_dict['systematic']
    # Calculates the uncertainties associated with the volume
    volume_uncertainty_r = volume_to_random_uncertainty(volume)
    volume_uncertainty_s = volume_to_systematic_uncertainty(volume)
    return [volume_uncertainty_r, volume_uncertainty_s]
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
    source_info = get_c_info(source)
    destination_info = get_c_info(destination)
    initial_volume_source = get_volume(source)
    initial_volume_destination = get_volume(destination)
    # Variables name simplification for calculation readability
    vt = volume_transfer
    v1 = initial_volume_source
    v2 = initial_volume_destination
    v3 = v2 + vt
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
    set_c_info(source, source_info)
    set_c_info(destination, destination_info)

