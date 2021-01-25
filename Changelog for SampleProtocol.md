## Header info

If you make any significant modificiation to this file, please update the infomation in this cell...

### Changelog
**Version:** 1.0.0 (old v1)<br>
_Comitted by:_ Alaric Taylor <alaric.taylor@ucl.ac.uk><br>
_Commit date:_ 2020-09-24<br>
* First committ

**Version:** 1.1.0 (old v2)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk><br>
_Commit date:_ 2020-09-25<br>
* Added the following functions:
    * `custom_wetting()`
    * `custom_transfer_simple()`
    * `custom_transfer_reverse()`
    * `custom_mixing_basic()`
    * `custom_mixing_static()`

**Version:** 2.0.0 (old v3)<br>
_Comitted by:_  Alaric Taylor <alaric.taylor@ucl.ac.uk><br>
_Commit date:_ 2020-09-25<br>
* Restructured Header info
* Added reference links
* Removed additional aspiration command from `custom_wetting()` function
* Removed pick_up_tip() and return_tip() from `custom_mixing_basic()` function (not flexible enough for use in protocols)
* ...then commented-out `custom_mixing_basic()` and replaced it with `custom_mixing_bottom_to_top()`, which was much more efficient.
* Significant overhaul of `custom_mixing_static()`...now mixing in the middle of the liquid
* Changes to `custom_transfer_simple()`:
    * Now called `custom_transfer_forward()`
    * Don't need `pipette_max_V` argument as this is an attribute of the `pipette` instance
* Re-build of `custom_transfer_reverse()`
* Added `rate` variable to `custom_aspirate()` function
* Added `custom_touch_tip()` which swirls an arc around the opening of a circular tube to remove droplets.

**Version:** 2.0.1 (old v4)<br>
_Comitted by:_  Alaric Taylor <alaric.taylor@ucl.ac.uk><br>
_Commit date:_ 2020-09-25<br>
* Removed dependancy on `scipy` library by modifying interpolation function in `gradations_to_vh()` - now using lambda function derived from numpy.
* Mixing functions now calculate their volume_mixing_fraction and warn if it is too low or too high.

**Version:** 2.1.0 (old v5)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-09-25<br>
* Uniformized functions input order - `pipette, volume, location(s), other function-specific inputs`
* Removed "tip" from the inputs of `custom_mixing_static()` function
* Added function testing to the main script for: `custom_wetting()`, `custom_touch_tip()`, `custom_mixing_bottom_to_top()`, `custom_mixing_static()`, `custom_transfer_forward()` and `custom_transfer_reverse()`
* Modified all `np.ceil()` instances in `int(np.ceil())` as this function returns a float number whereas integer are required in other functions

**Version:** 2.2.0 (old v6)<br>
_Comitted by:_ Alaric Taylor <alaric.taylor@ucl.ac.uk><br>
_Commit date:_ 2020-09-25<br>
* Circumventing radial movement in `custom_touch_tip()` function as the move_to location is not understood when defined explicitly in terms of polar coordinates (or cartesian coordinates!)

**Version:** 2.3.0 (old v7)<br>
_Comitted by:_ Alaric Taylor <alaric.taylor@ucl.ac.uk><br>
_Commit date:_ 2020-09-28<br>
* Circular movement within the `custom_touch_tip()` has been fixed!
* Model function, `custom_aspirate()`:
    * Begun to implement type-checking for input arguments
    * Begun to implement multi-line function info at top
* Added `check_well_attributes()` function to check the instance attributes have been correctly set for wells in which the meniscus is tracked. This is used by custom functions (where necessary) to avoid potential inconsitencies in type-checking.

**Version:** 2.4.0 (old v8)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-09-29<br>
* Type checking of input arguments implemented in all custom functions
* Multi-line function info at top implmented in all custom functions
* Modifications to `custom_dispense()`:
    * Security checks added to avoid overflows
    * New argument `dispense_depth` to allow modification of the dispensing position
* Signs fixed for `custom_mixing_bottom_to_top()` to ensure aspirate and dispense occur at the desired heights
* Modified `custom_transfer_forward()` to prevent air gaps from affecting the headroom. 
* Added security check in `custom_aspirate()`, `custom_mixing_bottom_to_top()` and `custom_mixing_static()` functions to avoid going deeper in a container than the height of the pipette tip, added argument tip_length to this effect
* Uniformization: all "depth" variables are now defined as positive numbers in all functions, changed in: `custom_touch_tip`
* Overhaul of `Measured gradations`:
    * Naming convention established: tube-type_volume_vh for a vh function
    * Gradation arrays have been added for the following labware: 1.5 mL Eppendorf tubes; 15 mL and 50 mL Falcon tubes; 2 mL, 4 mL, 8 mL, 20 mL and 30 mL vials; 70 uL cuvettes 
    * Information header updated
    * Instructions added for `well.volume_headroom_functions` in the main protocol
* Added custom labware import and basic movement functions to test correct loading of custom hardware
  

**Version:** 2.5.0 (old v9)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-09-30<br>
* Addition of custom labware:
    * Custom labware definition and import
    * Wells naming
    * Definition of wells headroom functions for each labware
    * Headroom setting for each used well
* Implementation of testing on-robot for:
    * Custom labware positioning
    * All custom functions
* Added pipette.move_to(source.top()) to `custom_transfer_forward()` to prevent `custom_touch_tip()` from going in direct line from the destination to the source (i.e. avoid collisions on the path)
* Most `move_to()` commands related to aspirate/dispense functions commented out and positions included in related function: reasoning is that move_to tend to cause double mouvements - e.g. the pipette moves in the desired position, then goes back to the top of the position and down again when a function is used
* Added `custom_tlc_spotting()` function with testing in main 
* Suggestion: consider writing down updated headrooms in a separate or updatable file - improved tracing, prevents constant headroom measurements in the case of sequential experiments

**Version:** 2.5.1 (old v10)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-10-14<br>
* Added number of wetting cycles to `custom_wetting()`
* Modified `custom_transfer_forward()` and `custom_transfer_reverse()` accordingly to include number of wetting steps instead of boolean pre_wet parameter (default unchanged)

**Version:** 2.6.0 (old v11)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-10-16<br>
* Added the option to touch tip at the destination when using `custom_transfer_forward()` and `custom_transfer_reverse()`
    * Idea: last drop is often not effectively blown out, this can represent the majority of the transfer volume in the case of small transfers
* Moved air gap aspiration before liquid aspiration for `custom_transfer_forward()`
    * Idea: air is now above the liquid in the pipette and helps pushing out all of the liquid
* Movement up (in z-axis) added at the end of `custom_touch_tip()`
    * Idea: under some conditions, the next move after a touch tip will use the direct path instead of going back up at a security distance, this extra step adds security in this scenario
* Modified graduation definition of 70 ul cuvettes to allow filling to the mark
* Overflow security check for destination moved from `custom_dispense()` to `custom_transfer_forward()` and `custom_transfer_reverse()`
    * Idea: previously, the protocol would stop after aspirating and before dispensing, it now stops before starting the transfer
    

**Version:** 2.7.0 (old v12)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-11-02<br>
* Added a "move_to(well)" command at the start of `custom_touch_tip()`
    * Idea: if a different well than the current location was specified for a touch tip, the function would use direct movement to the new well (thus crashing the tip)
* Added arguments to `custom_touch_tip()`
    * `radius_position` allows modification of the radial coordinate of the touch tip, i.e. allowing gentler touch
    * `speed` allows setting of the movement speed during touch tip
* Modified warning message in `custom_mixing_static()` and `custom_mixing_bottom_to_top()` to include location

**Version:** 2.8.0 (old v13)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-11-25<br>
* Added a `custom_mixing_top_to_bottom()` function for use on conical containers
* Default flow rates modified for `custom_aspirate()` and `custom_dispense()`
* Addition of `aspirate_rate` and `dispense_rate` parameters to all custom mixing and transfer functions, with default values
* Overhaul of `calibration()` function to allow more flexibility
* Modified or added gradations definitions according to CAD files measurements for the following labware: Eppendorf tubes 1.5 ml, 5 mL, 15 mL and 50 mL

**Version:** 3.0.0 (old v14)<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-12-01<br>
* **Adaptation to API v2.8, released along app v4.0.0**
* `apiLevel` modified to '2.8' in metadata
* Well attributes are now in `well._geometry`, all instances have been adapted (e.g. well.\_depth becomes well.\_geometry.\_depth)
* Attributes `.headroom` and `.headroom_functions` can no longer be added directly to wells, instead they are now added to `well._geometry`
* All custom functions adapted to above changes:
    * `location_informations = location._geometry` used to access geometrical and headroom informations
* `custom_touch_tip()` current state: 
    * Instances of `well._diameter` and `well._position` changed to `well._geometry._diameter` and `well._geometry._position`
    * Shape recognition changed from reading `well._shape` to verifying existence of `well._geometry._diameter`
    * New function `from_center_cartesian()` could potentially be used for better movement, but not currently implemented
        * Needs Opentrons functions inside custom function
        

**Version:** 3.1.0<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-12-17<br>
* Main `run()` function modified to clearly explain protocol structure and contain an instance of each custom function
* `calibration()` function removed - now used as a standalone protocol
* Modified default of `custom_transfer_forward()` to air_gap = 0 and description accordingly
* Modified descriptions of `custom_mixing_top_to_bottom()`, `custom_transfer_reverse()` and `custom_tlc_spotting()` to be more comprehensive
* Added a section `Uncertainties calculations and propagations`
    * Markdown description and to-do list
    * Function `uncertainties_calculation()` is mathematically working but missing other protocol elements
    * Function `volume_uncertainty()` and error gradations both incomplete and currently non-functional
* New versioning semantic included in changelog: xx.yy.zz format
    * x = breaks what has happened previsouly
    * y = new functionality
    * z = patches/bug fixes
* Old system version numbers have been kept for reference

**Version:** 4.0.0<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-01-18<br>
* Systematic error calculations and tracking added
* `uncertainties_calculation()` now functional
* Gradations and `volume_uncertainty()` now functional 
* Concentrations and uncertainties can now be tracked for a multi-substance system <br><br>

* Well attributes are now separated in two levels:
    * Headroom and headroom functions for the well are contained directly in `well._geometry`
    * Concentrations and uncertainties are contained in a new attribute `well._geometry.c_info`

* Added a function `initiate_well()` which initializes all the headroom and concentration-related attributes for each well
* Added a function `set_solution_info()` allowing definition of the initial concentration and uncertainties of a non-empty well (i.e. stock solution)
* Added a function `get_solution_info()` currently printing all the well information
    * Idea: Use this function to read all wells and compile info in a file
    
* `uncertainties_calculation()` modified to accomodate above changes
* Example structure modified in the main function to adopt above changes
* Custom transfer functions now call `uncertainties_calculation()`
* Missing: experimental data to fill brackets
  

**Version:** 5.0.0<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-01-18<br>
    
* **Overhaul following code review 19-22.01.21**
* `time` removed from imports as was only used in `custom_tlc_spotting()`, which needs to be reworked
* Information added in markdown sections:
    * Units list
    * AdReNa Github links
    * New sections `Building block functions` and `Well attributes handling functions`
    * New section `Uncertainties calculations formula` details how the concentrations and uncertainties are calculated
* New well attributes structure, each well is now initiated with a dictionary `custom_well_info()` (abbreviated `c_info()`) containing headroom, vh functions and concentration/uncertainties information
    * New function `initiate_well()` to create well attribute and input default values
* Set and get functions created:
    * Tip length: `get_tip_length`
    * Pipette flow rates: `get_default_flow_rates`
    * Flow rate conversion from uL/s to relative to default: `get_relative_from_flow_rate_aspirate``get_relative_from_flow_rate_dispense`
    * Headroom and volumes: `set_headroom()`, `get_headroom()`, `set_volume()`, `get_volume()`
    * Conversion functions: `get_v_from_h()` and `get_h_from_v`
    * General well information: `set_c_info()` and `get_c_info()`
    * Protocol constituents (substances): `set_constituent()`, `get_constituent()`
    * Pipette uncertainties: `set_pipette_uncertainties`, `get_pipette_uncertainties`
* Print functions created:
    * `print_c_info()` prints the full c_info dictionary
    * `print_constituent_concentration()` prints the concentration corrected for systematic error, +/- the random error
* Generic streamlining and overhaul of all custom functions
    * All functions revised to use set and get instead of calling well attributes directly
    * Uniformization of position calls in `custom_aspirate()` and `custom_dispense`
        * `immersion_depth` is now used
        * Defined as the position relative to the meniscus
            * \<0 above the meniscus
            * \>0 below the meniscus
    * For functions using `custom_aspirate()` and `custom_dispense()`: removal of redundant security checks
    * `air_gap` removed from `custom_transfer_forward()`
*  Mixing functions modifications:
    * Creation of `custom_mixing()` as a general mixing function to be used by other more specific ones
    * `custom_mixing_top_to_bottom()` streamlined and modified with `custom_mixing()`
    * `custom_mixing_static()` and `custom_mixing_bottom_to_top()` rewritten on the same model
* Uncertainties profiles, `profile_to_vu` and `uncertainties_calculations()` restructured
* `check_well_attributes()` removed (redundant)
* Tip length security checks (to avoid submersion) reworked:
    * New `get_tip_length()` function reading tip length from pipette's attributes
    * Function  called in `custom_aspirate()` and `custom_dispense()` for security checks
* Main run function modified to include and test above changes

**Version:** 5.0.1<br>
_Comitted by:_ Yann Mamie <y.mamie@ucl.ac.uk>:<br>
_Commit date:_ 2020-01-25<br>

* New API version 2.9
* Pipettes' flow rate access now through `pipette._implementation._flow_rates` instead of `pipette._flow_rates`