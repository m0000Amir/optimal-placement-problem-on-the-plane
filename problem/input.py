"""
Input data for the Problem
"""
problem = 'ILP'
# problem = 'LP'

gtw_pos = {0: (8, 3)}
obj_pos = {1: (1, 6),
           2: (5, 7),
           3: (8, 7),
           4: (1, 3)}
sta_pos = {5: (3, 6),
           6: (7, 5),
           7: (4, 3)}


'''Limits'''
gtw_lim = {0: float('inf')}
obj_lim = {1: 10,
           2: 15,
           3: 17,
           4: 18}
sta_lim = {5: 100,
           6: 100,
           7: 100}

'''Station parameter'''
limit = [100]
coverage = [5]
link_distance = [5]









