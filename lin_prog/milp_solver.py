"""
call MatLAB engine from Python to solve MILP problem
"""
import os
import matlab.engine
import scipy.io
import itertools


def save_mfile(path, array, name):
    """
    save numpy array as mat-file for triarea.m
    :param path: it is path to save .m-file
    :param array: numpy array which be saved
    :param name: name of .mat-array
    :return: .mat-file
    """
    scipy.io.savemat(path + name + '.mat', {str(name): array})
    return os.path.abspath(path + name + '.mat')


def solve_milp_problem(f, intcon, A, b, Aeq, beq, lb, ub,
                       path='../solve/matfiles/'):
    """
    call m-file with solver function
    :param path: it is path to save .m-file
    :param f: numpy array of objective function
    :param intcon: number of integer variables
    :param A: numpy array of inequality matrix
    :param b: numpy array of linear inequality constraint vector
    :param Aeq: numpy array of equality matrix
    :param beq: numpy array of linear equality constraint vector
    :param lb: numpy array of lower bounds vector
    :param ub: numpy array of upper bounds vector
    :return: solution of ILP problem
    """
    f = save_mfile(path, f, name='f')
    intcon = save_mfile(path, intcon, name='intcon')
    A = save_mfile(path, A, name='A')
    b = save_mfile(path, b, name='b')
    Aeq = save_mfile(path, Aeq, name='Aeq')
    beq = save_mfile(path, beq, name='beq')
    lb = save_mfile(path, lb, name='lb')
    ub = save_mfile(path, ub, name='ub')

    eng = matlab.engine.start_matlab()
    eng.cd(r'D:\Projects\optimal-placement-problem-on-the-plane\lin_prog',
           nargout=0)
    [x, fval, exitflag, output] = eng.triarea(f, intcon, A, b, Aeq, beq,
                                              lb, ub, nargout=4)
    out_x = [round(i) for i in list(itertools.chain(*x))]
    assert round(fval) == 0, ('There is no solution because the '
                              'objective function value of integer linear '
                              'programing problem is not zero')

    return out_x
