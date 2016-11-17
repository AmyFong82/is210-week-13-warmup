#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A module that summarize data of 5-boro restaurants and green markets."""

import json

GRADES = {
    'A': 1,
    'B': 0.9,
    'C': 0.8,
    'D': 0.7,
    'F': 0.6
}


def get_score_summary(filename):
    """A function that returns the score summary of 5-boro restaurants.

    Args:
        filename (str): the file that contains the data to be analyzed.

    Returns:
        dict: A dictionary keyed by boro, with tuples of the number of
              restaurants in each boro, and the average scores for the boro.

    Examples:
    >>> get_score_summary('inspection_results.csv')
    {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
    (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
    'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
    (414, 0.9719806763285017)}
    """
    fhandler = open(filename, 'r')

    camis = []
    boro_grades = []

    line = fhandler.readline()
    while line != '':
        line = fhandler.readline()
        splited = line.split(',')
        if splited[0] != '':
            if splited[10] != '' and splited[10] != 'P':
                camis.append(splited[0])
                boro_grades.append((splited[1], splited[10]))

    fhandler.close()

    camis_dict = dict(zip(camis, boro_grades))

    m_score, m_count = 0, 0
    q_score, q_count = 0, 0
    bk_score, bk_count = 0, 0
    bx_score, bx_count = 0, 0
    si_score, si_count = 0, 0

    for value in camis_dict.itervalues():
        if 'MANHATTAN' in value:
            m_x = GRADES[value[1]]
            m_count += 1
            m_score += m_x
        elif 'QUEENS' in value:
            q_x = GRADES[value[1]]
            q_count += 1
            q_score += q_x
        elif 'BROOKLYN' in value:
            bk_x = GRADES[value[1]]
            bk_count += 1
            bk_score += bk_x
        elif 'BRONX' in value:
            bx_x = GRADES[value[1]]
            bx_count += 1
            bx_score += bx_x
        elif 'STATEN ISLAND' in value:
            si_x = GRADES[value[1]]
            si_count += 1
            si_score += si_x

    score_summary = {
        'MANHATTAN': (m_count, m_score / m_count),
        'QUEENS': (q_count, q_score / q_count),
        'BROOKLYN': (bk_count, bk_score / bk_count),
        'BRONX': (bx_count, bx_score / bx_count),
        'STATEN ISLAND': (si_count, si_score / si_count),
    }

    return score_summary


def get_market_density(filename):
    """A function that returns the green market density in NYC.

    Args:
        filename (string): the file that contains the data to be analyzed.

    Returns:
        dict: A dictionary with each boro as the keys and the number of markets
              as the value.

    Examples:
        >>> get_market_density('green_markets.json')
        {'BRONX': 32, 'BROOKLYN': 48, 'STATEN ISLAND': 2, 'MANHATTAN': 39,
        'QUEENS': 16}
    """
    fhandler = open(filename, 'r')
    j_data = json.load(fhandler)
    res_data = j_data['data']
    fhandler.close()

    bronx, brooklyn, manhattan, queens, staten_island = 0, 0, 0, 0, 0
    for item in res_data:
        if 'Bronx' in item:
            bronx += 1
        elif 'Brooklyn' in item:
            brooklyn += 1
        elif 'Manhattan' in item:
            manhattan += 1
        elif 'Queens' in item:
            queens += 1
        elif 'Staten Island' in item:
            staten_island += 1

    num_market = {
        'STATEN ISLAND': staten_island,
        'BROOKLYN': brooklyn,
        'BRONX': bronx,
        'MANHATTAN': manhattan,
        'QUEENS': queens
    }

    return num_market


def correlate_data(res_filename, j_filename, out_filename):
    """A function that combines data from 2 files into 1 json file.

    Args:
        res_filename (str): The name of a file with restaurant scores data.
        j_filename (str): The name of a JSON file with green_market data.
        out_filename (str): Name of a file with the output of this function.

    Returns:
        file (json): Writes a json file with a dictionary in it.
    """
    score_dict = get_score_summary(res_filename)
    market_dict = get_market_density(j_filename)

    final_dict = {}
    for key, value in score_dict.iteritems():
        final_dict[key] = (value[1], float(market_dict[key]) / float(value[0]))

    filepath = out_filename
    fhandler = open(filepath, 'w')
    json.dump(final_dict, fhandler)
    fhandler.close()
