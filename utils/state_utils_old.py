from itertools import product
from sympy.ntheory.multinomial import multinomial_coefficients
import numpy as np

###############################################################################
# Auxiliary Methods for State preparation
###############################################################################


def get_controls(n, d):
    t = [0] * (n - 1) + [1]
    cdict = {tuple(t): 0}
    clist = list(product([0,1], repeat=n))
    index = 0
    while index < len(clist):
        tsum = 0
        i = clist[index]
        for j in i:
            tsum = tsum + j
        if tsum > d:
            clist.remove(i)
        else:
            index = index+1
    clist.remove(tuple([0]*n))
    # For now set all angles to 0
    for i in clist:
        cdict[i] = 0
    return cdict

def get_thetas(cdict, p, n):
    # For p1 to pd, we have pj*(q0+2q1+...+2^nqn)^j. Thus we calculate the coefficients
    for j in range(1,len(p)):
        # List of multinomial coefficients
        mlist = multinomial_coefficients(n, j)
        # Add angles
        for m in mlist:
            temp_t = []
            powers = 1
            # Get controls
            for k in range(0, len(m)):
                if m[k] > 0:
                    temp_t.append(1)
                    powers *= 2**(k*m[k])
                else:
                    temp_t.append(0)
            temp_t = tuple(temp_t)
            # Add angle
            cdict[temp_t] += p[j]*mlist[m]*powers
    return cdict

def get_delta(epsilon, lambda_min, lambda_max):
    nl = np.abs(np.log2(epsilon))+1
    formatstr = "#0"+str(nl+2)+"b"
    lambda_min_tilde = lambda_min*(2**nl -1)/lambda_max
    binstr = format(int(lambda_min_tilde), formatstr)[2::]
    lamb_min_rep = 0
    for i in range(0,len(binstr)):
        lamb_min_rep += int(binstr[i])/(2**(i+1))
    return lamb_min_rep

def get_pxlambda(epsilon, t, a, b, N):
    nl = np.abs(np.log2(epsilon))+1

    xtofit = []
    yfit = []
    tries = [k for k in range(1,N+1)]
    for j in tries:
        xtofit.append((a - 2*b*np.cos(j*np.pi/(N+1)))*t*(2**nl) / (2*np.pi))
        yfit.append(np.arcsin((a - 2*b*np.cos(np.pi/(N+1))) / (a - 2*b*np.cos(j*np.pi/(N+1)))))

    z = np.polyfit(np.asarray(xtofit, dtype=float), np.asarray(yfit, dtype=float), len(tries)-1)

    pxlambda = []
    for i in reversed(z):
        pxlambda.append(i)
    return pxlambda

