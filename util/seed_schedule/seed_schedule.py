import random


def sort_tuples(tuples_list):
    sorted_tuples = sorted(tuples_list, key=lambda x: x[1], reverse=True)
    return sorted_tuples


def select_tuples(sorted_tuples, high_ratio):
    total_tuples = len(sorted_tuples)
    high_count = int(total_tuples * high_ratio)

    high_tuples = sorted_tuples[:high_count]
    random_tuple = random.choice(sorted_tuples[high_count:])

    selected_tuple = random.choice(high_tuples + [random_tuple])
    return selected_tuple


class SeedSchedule:
    def __init__(self, seeds, high_ratio=0.7):
        self.seeds = seeds
        self.high_ratio = high_ratio

    def schedule(self):
        sorted_tuples = sort_tuples(self.seeds)
        selected_tuple = select_tuples(sorted_tuples, self.high_ratio)

        return selected_tuple
