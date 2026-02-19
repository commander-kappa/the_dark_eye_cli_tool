import random

def ROLL_DICE(times, size):
    result = []
    for t in range(times):
        result.append(random.randint(1, size))
    return result