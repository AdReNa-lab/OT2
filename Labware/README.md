# OT2-custom-labware
 Repository for custom labware used within the AdReNa group.


### Notes

- The "JSON files" subfolder contains all the files required to run a protocol.
  - When simulating a protocol, this directory must be selected (using the debugger script).
  - An up-to-date version of these files needs to be stored on the OT2 that will execute the protocol.
- The labware element has a corresponding subfolder within "Labware reference information" containing a README file specific to that labware.

### Consistency
Please maintain consistency between:
  - JSON filename.
  - Protocol load name ("loadName" within JSON file).
  - Name of folder containing reference info.



---



### General practice for contributions

Please:

- Make sure that the 'main' branch remains **fully functional**.
  - This means, work in a branch if your contributions are not yet ready to be implemented by an end-user.
- Close branches when possible (i.e. work in functional increments).
- Commit regularly, with clear descriptions.

- Where possible, name your commit using <u>semantic version numbering: "vXX.YY.ZZ"</u>
  - ZZ is a 'patch' (a bug fix)
  - YY is a 'minor' version (an additional feature that *is* backward compatible with previous code)
  - XX is a 'major' version (which may breaks things in previous scripts)

