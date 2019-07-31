"""
Input data for the Problem
"""
problem = 'ILP'
# problem = 'LP'

''' Coordinates'''
gtw_pos = {0: (8, 3)}
obj_pos = {1: (1, 6),
           2: (5, 7),
           3: (8, 7),
           4: (1, 3),
           5: (2, 6)}
sta_pos = {6: (7, 5),
           7: (4, 3),
           8: (2, 8),
           9: (4, 10),
           10: (1, 8)}

'''Limits'''
gtw_lim = {0: float('inf')}
obj_lim = {1: 10,
           2: 15,
           3: 17,
           4: 18,
           5: 16}

sta_lim = {6: 100,
           7: 100,
           8: 100,
           9: 100,
           10: 100}
# sta_lim = {5: 100,
#            6: 100,
#            7: 100,
#            9: (4, 10),
#            10: (1, 8)
#            }

'''Station parameter'''
limit = [100, 200, 100]
coverage = [7, 5, 4]
link_distance = [5, 6, 6]
