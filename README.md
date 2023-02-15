# Electronics Calulators

A mix of python scripts to speed up working on electronics. 

This repository was created while enrolled in [eCornell's Mechatronics Program](https://ecornell.cornell.edu/certificates/engineering/mechatronics/), but I may keep adding to it in the future.

## Closest Resistor

Set your inventory of resistors and this script will find the closest combination in both series and parallel so you don't have to do the math

### Input:
```
# list of resistors to choose from
resistors = [1.5, 4.7, 100, 220, 330, 470, 680, 1000, 2200, 3300, 4700, 10000, 22000, 47000, 100000, 330000, 1000000]

# desired output resistance
target = 1190

# tolerance of the desired output resistance
tolerance = .005

# set the maximum number of resistors to use in the combination
max_resistors = 5

# set the maximum number of repeats of the same resistor (assuming you don't just have one of each resistor)
max_repeats = 10
```

### Output:
```
Resistor Inventory: [1.5, 4.7, 100, 220, 330, 470, 680, 1000, 2200, 3300, 4700, 10000, 22000, 47000, 100000, 330000, 1000000]

-----

Target Resistance: 1190 ohms ± 0.5%

---SERIES---

Series Combination: (330, 330, 330, 100, 100)
Series Total Resistance: 1190 ohms (0 off)

---PARALLEL---

Parallel Combination: [47000, 4700, 3300, 3300]
Parallel Total Resistance: 1190.33 ohms (0.33 off)
```
