import math
import matrix
import numpy as np
from numpy.polynomial import Polynomial

def avg (dataset) :
    sum = 0
    for I in range(len(dataset)) :
        sum += int(dataset[I])
    return sum / len(dataset)

def pearson_correlation (dataset_1, dataset_2) :
    if len(dataset_1) <= len(dataset_2) :
        length = len(dataset_1) 
    else: 
        length = len(dataset_2) 

    avg_1 = avg(dataset_1)
    avg_2 = avg(dataset_2)

    top_sum = 0
    for I in range(length) :
        top_sum += (dataset_1[I]  - avg_1)* (dataset_2[I] - avg_2)

    set_1_magnitude = 0
    for I in range(length) :
        set_1_magnitude += (I - avg_1) ** 2

    set_2_magnitude = 0
    for I in range(length) :
        set_2_magnitude += (I - avg_2) ** 2

    bottom_sum = math.sqrt((set_1_magnitude * set_2_magnitude))

    return top_sum / bottom_sum

def construct_correlation_matrix (dataset) :
    cor_matrix = matrix.matrix(len(dataset), len(dataset))
    for I in range(len(dataset)) :
        for J in range(len(dataset)) :
            if I == J :
                cor_matrix.content[I][J] = 1
            elif J < I :
                cor_matrix.content[I][J] = pearson_correlation(dataset[I], dataset[J])


def cycle_data (data_set, next_point):
    data_set.pop(0) 
    data_set.append(next_point)
    return data_set


def regress (x, y, degree):
    coeffs = Polynomial.fit(x, y, degree).convert().coef
    return coeffs

