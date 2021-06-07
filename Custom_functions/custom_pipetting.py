"""
These functions give fine control over the height at which an aspiration is made. This is implemented by tracking meniscus heights in each well. Thereby,
* maximising the accuracy of the pipette stroke (by pipetting at the top of a liquid)
* avoiding the formation of droplets along the outer pipette shaft
* preventing silent failures of a protocol e.g. if stock solution volumes are low and a pipette stroke fails to pick up liquid
"""
############################################################
from __future__ import absolute_import

import numpy as np

from opentrons import types

from Vesynta_Tech.OpenTrons2 import building_blocks as bb
from Vesynta_Tech.OpenTrons2 import calculate_uncertainties as calcunc

############################################################

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
    rate_rel = bb.get_relative_from_flow_rate_aspirate(pipette, rate)
    
    # Extraction or calculation of headrooms and volumes before and after aspiration
    initial_volume = bb.get_volume(location)
    final_volume = initial_volume - transfer_volume
    initial_headroom = bb.get_headroom(location)
    final_headroom = bb.get_h_from_v(location, final_volume)
    
    # depth_to_aspirate is the distance from the top of the well at which aspiration will take place
    depth_to_aspirate = final_headroom + immersion_depth
    
    # Modifies the headroom in the well attributes
    bb.set_headroom(location, final_headroom)
    
    # Safety checking
    # ...avoidance of these errors are also covered by the use 
    # of specified extrapolation fill_values in the gradations_to_vh() function
    
    # Low volume/aspiration height warning
    depth = bb.get_h_from_v(location, 0)
    if depth_to_aspirate > depth - safety_height:
        depth_to_aspirate = depth - safety_height  # e.g. 0.5mm above the bottom of the well
        print('Warning, aspiration height for well ' +str(location) +' is lower than ' +str(safety_height) +' mm')
    
    # Avoids tip submersion in liquid
    tip_length = bb.get_tip_length(pipette)
    if depth_to_aspirate > 0.8*tip_length + initial_headroom:  # Checks that the pipette tip will not be fully submerged
        depth_to_aspirate = 0.8*tip_length + initial_headroom
        print('Warning, aspiration depth was set lower then pipette tip length, it has been changed to ' +str(depth_to_aspirate))
    
    if depth_to_aspirate < 0: 
        depth_to_aspirate = 0 # i.e. at the top of the well
        
    pipette.aspirate(transfer_volume, location.top(-depth_to_aspirate), rate = rate_rel)
    return #return None explicitly
############################################################
### This function records the volume of fluid added to a well ###
def custom_dispense(pipette: types.Mount,
                    transfer_volume: float,
                    location: types.Location,
                    dispense_meniscus: bool = True,
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
    rate_rel = bb.get_relative_from_flow_rate_dispense(pipette, rate)
    
    # Extraction or calculation of headrooms and volumes before and after aspiration
    initial_volume = bb.get_volume(location)
    final_volume = initial_volume + transfer_volume
    initial_headroom = bb.get_headroom(location)
    final_headroom = bb.get_h_from_v(location, final_volume)
    
    # dispense_depth is the distance from the top of the well at which dispense will take place
    if dispense_meniscus:
        # Depth defined relative to the meniscus
        dispense_depth = final_headroom + immersion_depth
    else:
        # Depth defined relative to the top of the well
        dispense_depth = immersion_depth
    
    # Modifies the headroom in the well attributes
    bb.set_headroom(location, final_headroom)
    
     # Avoids tip submersion in liquid   
    tip_length = bb.get_tip_length(pipette)
    if dispense_depth > 0.8*tip_length + initial_headroom:  # Checks that the pipette tip will not be fully submerged
        dispense_depth = 0.8*tip_length + initial_headroom
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
############################################################
### The custom_touch_tip() function removes droplets from the shaft of a pipette tip by running the tip around the perimiter of a circular tube ###
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
        thetas = np.linspace(start=0, stop=2*np.pi, num=increments, endpoint=False)
        x_offsets = radius*np.cos(thetas)
        y_offsets = radius*np.sin(thetas)
        touch_locations = [] # initialise list
        for i in range(increments):
            offset = types.Point(x_offsets[i], y_offsets[i], -depth)
            # Populate list of locations
            touch_locations.append(types.Location(well_top.__add__(offset), 'Touch point '+str(i+1)))
        pipette.move_to(well.top())
        for location in touch_locations:
            pipette.move_to(location, force_direct=True, speed=speed)
        pipette.move_to(well.top())  # Might not be required
    else:
        print('Well is not circular, so just using standard touch_tip() command')
        pipette.touch_tip(location=well, v_offset=depth)
############################################################

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
############################################################

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
    max_volume = bb.get_volume(location)
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
############################################################

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
    max_volume = bb.get_volume(location)
    min_volume = max_volume - mixing_volume
    max_headroom = bb.get_h_from_v(location, min_volume)
    # Depth of a well is determined by reading the headroom of an empty well container (volume = 0)
    well_depth = bb.get_h_from_v(location, 0)
    # dispense_depth is the distance from the top of the well, 
    # immersion_depth from the meniscus (used for custom_dispense())
    dispense_depth = well_depth - dispense_height
    dispense_immersion_depth = dispense_depth - max_headroom
    custom_mixing(pipette, mixing_volume, location, cycles, aspiration_immersion_depth, dispense_immersion_depth, aspirate_rate, dispense_rate)
############################################################
### This function takes liquid from the bottom of the well and pipettes it to the top of the well i.e. layering the solution in order to aid mixing ###
def custom_mixing_bottom_to_top(pipette: types.Mount,
                                mixing_volume: float,
                                location: types.Location, 
                                cycles: int,
                                aspirate_height: float = 1,
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
    max_volume = bb.get_volume(location)
    min_volume = max_volume - mixing_volume
    max_headroom = bb.get_h_from_v(location, min_volume)
    # Depth of a well is determined by reading the headroom of an empty well container (volume = 0)
    well_depth = bb.get_h_from_v(location, 0)
    # dispense_depth is the distance from the top of the well, 
    # immersion_depth from the meniscus (used for custom_aspirate())
    aspirate_depth = well_depth - aspirate_height
    aspiration_immersion_depth = aspirate_depth - max_headroom
    custom_mixing(pipette, mixing_volume, location, cycles, aspiration_immersion_depth, dispense_immersion_depth, aspirate_rate, dispense_rate)
############################################################

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
    max_volume = bb.get_volume(location)
    min_volume = max_volume - mixing_volume
    min_headroom = bb.get_headroom(location)
    max_headroom = bb.get_h_from_v(location, min_volume)
    # Depth of a well is determined by reading the headroom of an empty well container (volume = 0)
    well_depth = bb.get_h_from_v(location, 0)
    # Determination of the mixing positon within the liquid
    mixing_position = relative_depth*(well_depth - max_headroom)
    custom_mixing(pipette, mixing_volume, location, cycles, mixing_position, mixing_position, aspirate_rate, dispense_rate)
############################################################

def custom_transfer_forward(pipette: types.Mount,
                            volume: float,
                            source: types.Location, 
                            destination: types.Location, 
                            pre_wet: int = 0,
                            aspirate_rate: float = 75,
                            aspirate_depth: float = 2,
                            dispense_rate: float = 300,
                            dispense_meniscus: bool = True,
                            dispense_depth: float = 0,                            
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
    - dispense_meniscus set to True if a dispense position relative to the meniscus is desired, if False will be relative to the top of the well
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
        calcunc.uncertainties_calculation(pipette, pass_volume, source, destination) # Uncertainties function need to be called 
                                                                             # before custom_aspirate and custom_dispense
        custom_aspirate(pipette, pass_volume, source, immersion_depth = aspirate_depth, rate = aspirate_rate)
        custom_touch_tip(pipette, source)
        custom_dispense(pipette, pass_volume, destination, dispense_meniscus = dispense_meniscus, immersion_depth = dispense_depth, rate = dispense_rate)
        pipette.blow_out(destination.top(-2))
        if touch_tip_position == 'destination':
            custom_touch_tip(pipette, destination)
        elif touch_tip_position == 'source':
            custom_touch_tip(pipette, source)
        # Generally do NOT touch_tip() on the destination
        # as this could cause backwards contamination
############################################################

def custom_transfer_reverse(pipette: types.Mount,
                            volume: float,
                            source: types.Location, 
                            destination: types.Location,
                            disposal_volume: float = 5,
                            aspirate_rate: float = 37,
                            aspirate_depth: float = 2,
                            dispense_rate: float = 150,
                            dispense_meniscus: bool = True,
                            dispense_depth: float = 0,
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
    # Transfer splitting, the total volume is split in however many equal strokes needed to be fully transferred
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
        calcunc.uncertainties_calculation(pipette, pass_volume, source, destination)
        custom_aspirate(pipette, pass_volume + disposal_volume, source, immersion_depth = aspirate_depth, rate = aspirate_rate)
        custom_touch_tip(pipette, source)
        custom_dispense(pipette, pass_volume, destination, dispense_meniscus = dispense_meniscus, immersion_depth = dispense_depth, rate = dispense_rate)
        if touch_tip_position == 'destination':
            custom_touch_tip(pipette, destination)
        elif touch_tip_position == 'source':
            custom_touch_tip(pipette, source)
        # Return the remainder to the source 
        custom_dispense(pipette, disposal_volume, source, dispense_meniscus = False)
        pipette.blow_out(source.top(-2))
        custom_touch_tip(pipette, source)
############################################################

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
############################################################