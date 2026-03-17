"""
Utility functions to use in main calculator
"""

import numpy as np
from numpy.random import Generator
import random


def min_distance(n):
    """
    Returns the minimum distance the uncorrect function must be from n to be permissible.
    :param n: The number to find minimum distance for
    :return: Minimum distance
    """
    # this guarantees f(0) = 0.1 and f(1) = 0.05. abs means it works for negative numbers and log makes it scale with order
    return np.log10((10**0.1 - 10**0.05)*abs(n) + 10**0.1)


def stddev(n):
    """
    Returns the stddev or spread for the uncorrect function to use.
    :param n: The number to find stddev for
    :return: Standard deviation
    """
    # similar logic as above but we also divide by a certain number that is basically how confident we want to be this "maximum" holds. basically it's the empirical rule
    # note: the larger that confidence is, the longer it'll take for the uncorrect function to work (because the spread will be less and so there's a smaller chance you get past the min distance)
    # especially for large n
    return np.log10((10**0.1 - 10**0.05)*abs(n) + 10**0.1)/2


def uncorrect(n):
    """
    "Uncorrect" a number n by generating a random number via normal distribution centered around number
    :param n: The number to uncorrect.
    :return: Float close to number but incorrect.
    """

    if isinstance(n, float) or isinstance(n, int):

        result = n
        while abs(result - n) < min_distance(n):
            # normal distribution centered at n. we type hint rng as a generator because my ide is fucked up and i can't even bother
            rng: Generator = np.random.default_rng()
            result = rng.normal(loc=n, scale=stddev(n))

        return result

    elif isinstance(n, str):
        # turn result into a list for mutability
        result = list(n)
        # for every 4 characters we want to change 1
        for i in range(len(result) // 4):
            # pick a random index from the second character to the end (for legibility not the first) and change it to a random character from ASCII 65 (A) to 123 (z)
            result[random.randrange(1, len(result))] = chr(random.randrange(65, 123))

        # turn list into string
        result = "".join(result)
        return result

    # i don't know when this would happen but just in case let's just return n
    return n


def custom_round(n):
    """
    Custom round function that will round number if float or integer or return input if it's a different type (e.g. string)
    :param n: The value to round
    :return: Rounded value to 3 decimal places
    """

    if isinstance(n, float):
        return round(n, 3)
    else:
        return n  # this is so passing in a string won't error here


if __name__ == "__main__":
    import time  # we only need the time module for benchmarking when this program is being run as a script (not imported) so this is good practice

    # this isn't really a good way to do test cases but this is a hobby project so it doesn't matter too much. besides, have you seen equation_parser.py? it's just a shit ton of assert statements. ew.
    test_cases = [0, 1, 5, 10, 50, 100, 500, 1000, 5000, 10000]

    start = time.perf_counter()

    for case in test_cases:
        results = []  # the actual numbers we get
        deviations = []  # how far away output is from input (we want this to be far from the number but not too far because that isn't as funny)

        for j in range(10000):
            current_result = uncorrect(case)
            results.append(current_result)
            deviations.append(abs(current_result - case))

        print(f"Average at {case}: {sum(results)/10000}")
        print(f"Range at {case}: {min(results)} to {max(results)} ({max(results) - min(results)})")
        print(f"Average deviation at {case}: {sum(deviations)/10000}\n")

    end = time.perf_counter()

    print(f"Time per number on average: {(end - start)/(len(test_cases)*10000)}")

