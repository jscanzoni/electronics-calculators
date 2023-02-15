'''
script to take an 
- array of resistors
- the desired output resistance 
- tolerance of the desired output resistance

to recommend the best combination of 1 to 5 resistors to use in either 
- parallel or 
- series 

to get the closest to the desired output resistance in both parallel and series along with the total resistance of the combination

'''

import itertools
import numpy as np


# list of resistors to choose from
resistors = [1.5, 4.7, 100, 220, 330, 470, 680, 1000, 2200,
             3300, 4700, 10000, 22000, 47000, 100000, 330000, 1000000]

# desired output resistance
target = 1190

# tolerance of the desired output resistance
tolerance = .005

# set the maximum number of resistors to use in the combination
max_resistors = 5

# set the maximum number of resistors to use in the combination
max_repeats = 10

# function to duplicate the resistors list to allow for repeats of the same resistor


def duplicate_resistors(resistors, max_resistors, max_repeats):
    return [r for r in resistors for i in range(min(max_resistors, max_repeats))]

# function to calculate the optimal combination of resistors in series


def series(resistors, target, tolerance, max_resistors):
    # filter out resistors greater than the target resistance plus the tolerance
    resistors = [r for r in resistors if r <= (target*(1+tolerance))]

    # sort the resistors list descending
    resistors.sort(reverse=True)

    # if there are no resistors remaining, return None
    if not resistors:
        return None

    # if the target resistance is equal to one of the resistors, return that resistor as a single-element tuple
    if target in resistors:
        return (target,), target

    # try combinations from series of one resistor to a series of max_resistors
    for i in range(1, max_resistors + 1):
        combinations = itertools.combinations(resistors, i)
        for combo in combinations:
            r_total = sum(combo)
            diff = abs(target - r_total)
            if diff / target <= tolerance:
                return combo, r_total

    # if no combination is found within the tolerance, return the closest combination
    deviations = [abs(target - r) for r in resistors]
    closest = resistors[np.argmin(deviations)]
    return (closest,), closest


def parallel(resistors, target, tolerance, max_resistors=5):
    # create a list of resistances that are at least `target` ohms
    # this helps to reduce the number of combinations we have to calculate
    candidate_resistors = [r for r in resistors if r > target]

    # initialize the closest combination and its total resistance
    closest = None
    closest_total = None

    # iterate through 1 to `max_resistors`
    for i in range(1, min(max_resistors, 5) + 1):

        # create a list of all possible combinations of `i` resistors
        combinations = itertools.combinations(candidate_resistors, i)

        # deduplicate the combinations so we don't have to calculate the same thing twice
        unique_combinations = set([tuple(sorted(c)) for c in combinations])

        # calculate the resistance of each parallel combination
        resistances = [1 / sum([1/c for c in combo])
                       for combo in unique_combinations]

        # check if any of the combinations are within tolerance
        for j in range(len(resistances)):
            if abs(target - resistances[j]) / target <= tolerance:
                return sorted(list(unique_combinations)[j], reverse=True), round(resistances[j], 2)

        # otherwise, update the closest combination if this combination is closer to the target resistance
        if closest_total is None or min([abs(target - r) for r in resistances]) < abs(target - closest_total):
            closest_index = np.argmin([abs(target - r) for r in resistances])
            closest = list(unique_combinations)[closest_index]
            closest_total = 1 / resistances[closest_index]

    # return the combination and total resistance
    return sorted(closest, reverse=True), round(closest_total, 2)


def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # return list
    return unique_list

 # output the results
if __name__ == '__main__':
    # duplicate the resistors list to allow for repeats of the same resistor
    resistors = duplicate_resistors(resistors, max_resistors, max_repeats)

    # calculate the optimal combination of resistors in series
    series_combination, series_total_resistance = series(
        resistors, target, tolerance, max_resistors)

    # calculate the optimal combination of resistors in parallel
    parallel_combination, parallel_total_resistance = parallel(
        resistors, target, tolerance, max_resistors)

    # output the results
    print('\n\n')
    print('Resistor Inventory: {}\n'.format(unique(resistors)))
    print('-----\n')
    print('Target Resistance: {} ohms ± {}%\n'.format(target, tolerance * 100))

    print('---SERIES---\n')

    if series_total_resistance is not None and series_total_resistance > 0:
        print('Series Combination: {}'.format(series_combination))
        print('Series Total Resistance: {} ohms ({} off)\n'.format(
            series_total_resistance, round(abs(series_total_resistance-target), 2)))
    else:
        print('No combination of resistors in series can get within {}% of {} ohms'.format(
            round(tolerance * 100, 5), target))

    print('---PARALLEL---\n')

    if parallel_total_resistance is not None and parallel_total_resistance > 0:
        print('Parallel Combination: {}'.format(parallel_combination))
        print('Parallel Total Resistance: {} ohms ({} off)\n'.format(
            parallel_total_resistance, round(abs(parallel_total_resistance-target), 2)))
    else:
        print('No combination of resistors in parallel can get within {}% of {} ohms'.format(
            round(tolerance * 100, 5), target))
    print('\n\n')
