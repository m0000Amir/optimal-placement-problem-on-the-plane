"""
Input data for the Problem
"""
problem = 'ILPcp'
# problem = 'ILP'
# problem = 'LP'

''' Coordinates'''
gtw_pos = {0: (8, 3)}
obj_pos = {1: (1, 6),
           2: (5, 6),
           3: (8, 7),
           4: (1, 3),
           5: (2, 6),
           6: (7, 5),
           7: (4, 3),
           8: (10, 3),
           9: (4, 10),
           10: (5, 9),
           11: (1, 5),
           12: (2, 3),
           13: (2, 8),
           14: (6, 2),
           15: (10, 8),
           16: (7, 8),
           17: (10, 10),
           18: (7, 9),
           19: (6, 3),
           20: (3, 8),
           21: (10, 6),
           22: (11, 8),
           23: (1, 1),
           24: (4, 2),
           25: (0, 6),
           26: (10, 4),
           27: (4, 6),
           28: (0, 1),
           29: (12, 6),
           30: (8, 11),
           }
sta_pos = {31: (4, 1),
           32: (5, 4),
           33: (4, 7),
           34: (5, 8),
           35: (0, 8),
           36: (6, 8),
           37: (0, 4),
           38: (6, 10),
           39: (12, 10),
           40: (1, 7),
}

'''Limits'''
gtw_lim = {0: float('inf')}
obj_lim = {1: 10,
           2: 15,
           3: 17,
           4: 18,
           5: 16,
           6: 15,
           7: 16,
           8: 15,
           9: 14,
           10: 13,
           11: 16,
           12: 15,
           13: 14,
           14: 13,
           15: 15,
           16: 14,
           17: 13,
           18: 13,
           19: 15,
           20: 14,
           21: 13,
           22: 15,
           23: 14,
           24: 13,
           25: 13,
           26: 15,
           27: 13,
           28: 14,
           29: 15,
           30: 13,
           }

'''Station parameter'''
limit = [100, 200, 100, 100, 50, 50, 100, 50, 50]
coverage = [6, 5, 6, 6, 5, 5, 6, 4, 7]
link_distance = [5, 6, 6, 7, 6, 6, 7, 6, 7]
cost = [75, 85, 95, 105, 60, 70, 50, 55, 110]


#########################################

# ''' Coordinates'''
# gtw_pos = {0: (8, 3)}
# obj_pos = {1: (1, 6),
#            2: (5, 7),
#            3: (8, 7),
#            4: (1, 3)}
# sta_pos = {5: (4, 3),
#            6: (2, 8),
#            7: (4, 10),
#            8: (3, 10)}
#
#
# '''Limits'''
# gtw_lim = {0: float('inf')}
# obj_lim = {1: 10,
#            2: 15,
#            3: 17,
#            4: 18}
#
# '''Station parameter'''
# limit = [100, 100, 100]
# coverage = [5, 6, 7]
# link_distance = [8, 9, 10]
# cost = [75, 85, 95]

###################################


# ''' Coordinates'''
# gtw_pos = {0: (8, 3)}
# obj_pos = {1: (1, 6),
#            2: (5, 7),
#            3: (8, 7),
#            4: (1, 3),
#            5: (2, 6),
#            6: (7, 5)}
# sta_pos = {7: (4, 3),
#            8: (2, 8),
#            9: (4, 10),
#            10: (4, 8),
#            11: (1, 5),
#            12: (2, 3)}
#
# '''Limits'''
# gtw_lim = {0: float('inf')}
# obj_lim = {1: 10,
#            2: 15,
#            3: 17,
#            4: 18,
#            5: 16,
#            6: 15}
#
#
#
# '''Station parameter'''
# limit = [100]
# coverage = [15]
# link_distance = [20]
#
# s_num = 5









