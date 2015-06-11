# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.stats as st
import itertools as it


def binomial_sign_test(*args):
    k = len(args)
    if k != 2: raise ValueError('The test needs two samples')
    n = len(args[0])
    
    d_plus = 0
    d_minus = 0
    for i in range(n):
        # Zero differences are eliminated
        if args[0][i] < args[1][i]: 
            d_plus = d_plus+1
        elif args[0][i] > args[1][i]:
            d_minus = d_minus+1
    
    x = max(d_plus, d_minus)
    n = d_plus + d_minus
    
    p_value = 2*(1 - st.binom.cdf(x, n, 0.5)) # Two-tailed of the smallest p-value
    
    return x, p_value
    
        

def friedman_test(*args):
    k = len(args)
    if k < 2: raise ValueError('Less than 2 levels')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')

    rankings = []
    for i in range(n):
        row = [col[i] for col in args]
        row_sort = sorted(row)
        rankings.append([row_sort.index(v) + 1 + (row_sort.count(v)-1)/2. for v in row])

    rankings_avg = [sp.mean([case[j] for case in rankings]) for j in range(k)]
    rankings_cmp = [r/sp.sqrt(k*(k+1)/(6.*n)) for r in rankings_avg]

    chi2 = ((12*n)/float((k*(k+1))))*((sp.sum(r**2 for r in rankings_avg))-((k*(k+1)**2)/float(4)))
    iman_davenport = ((n-1)*chi2)/float((n*(k-1)-chi2))

    p_value = 1 - st.f.cdf(iman_davenport, k-1, (k-1)*(n-1))

    return iman_davenport, p_value, rankings_avg, rankings_cmp



def friedman_aligned_ranks_test(*args):
    k = len(args)
    if k < 2: raise ValueError('Less than 2 levels')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')

    aligned_observations = []
    for i in range(n):
        loc = sp.mean([col[i] for col in args])
        aligned_observations.extend([col[i] - loc for col in args])
        
    aligned_observations_sort = sorted(aligned_observations)
    
    aligned_ranks = []
    for i in range(n):
        row = []
        for j in range(k):
            v = aligned_observations[i*k+j]
            row.append(aligned_observations_sort.index(v) + 1 + (aligned_observations_sort.count(v)-1)/2.)
        aligned_ranks.append(row)

    rankings_avg = [sp.mean([case[j] for case in aligned_ranks]) for j in range(k)]
    rankings_cmp = [r/sp.sqrt(k*(n*k+1)/6.) for r in rankings_avg]

    r_i = [np.sum(case) for case in aligned_ranks]
    r_j = [np.sum([case[j] for case in aligned_ranks]) for j in range(k)]
    T = (k-1) * (sp.sum(v**2 for v in r_j) - (k*n**2/4.) * (k*n+1)**2) / float(((k*n*(k*n+1)*(2*k*n+1))/6.) - (1./float(k))*sp.sum(v**2 for v in r_i))

    p_value = 1 - st.chi2.cdf(T, k-1)

    return T, p_value, rankings_avg, rankings_cmp



def quade_test(*args):
    k = len(args)
    if k < 2: raise ValueError('Less than 2 levels')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')

    rankings = []
    ranges = []
    for i in range(n):
        row = [col[i] for col in args]
        ranges.append(max(row) - min(row))
        row_sort = sorted(row)
        rankings.append([row_sort.index(v) + 1 + (row_sort.count(v)-1)/2. for v in row])
   
    ranges_sort = sorted(ranges)
    ranking_cases = [ranges_sort.index(v) + 1 + (ranges_sort.count(v)-1)/2. for v in ranges]

    S = []
    W = []
    for i in range(n):
        S.append([ranking_cases[i] * (r - (k + 1)/2.) for r in rankings[i]])
        W.append([ranking_cases[i] * r for r in rankings[i]])

    Sj = [np.sum(row[j] for row in S) for j in range(k)]
    Wj = [np.sum(row[j] for row in W) for j in range(k)]
    
    rankings_avg = [w / (n*(n+1)/2.) for w in Wj]
    rankings_cmp = [r/sp.sqrt(k*(k+1)*(2*n+1)*(k-1)/(18.*n*(n+1))) for r in rankings_avg]

    A = sp.sum(S[i][j]**2 for i in range(n) for j in range(k))
    B = sp.sum(s**2 for s in Sj)/float(n)
    F = (n-1)*B/(A-B)

    p_value = 1 - st.f.cdf(F, k-1, (k-1)*(n-1))

    return F, p_value, rankings_avg, rankings_cmp

def bonferroni_dunn_test(ranks, control=None):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    if not control:
        control_i = values.index(min(values))
    else:
        control_i = keys.index(control)

    comparisons = [keys[control_i] + " vs " + keys[i] for i in range(k) if i != control_i]
    z_values = [abs(values[control_i] - values[i]) for i in range(k) if i != control_i]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [min((k-1)*p_value,1) for p_value in p_values]
    
    return comparisons, z_values, p_values, adj_p_values
    
    
def holm_test(ranks, control=None):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    if not control:
        control_i = values.index(min(values))
    else:
        control_i = keys.index(control)

    comparisons = [keys[control_i] + " vs " + keys[i] for i in range(k) if i != control_i]
    z_values = [abs(values[control_i] - values[i]) for i in range(k) if i != control_i]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [min(max((k-(j+1))*p_values[j] for j in range(i+1)), 1) for i in range(k-1)]
    
    return comparisons, z_values, p_values, adj_p_values
    
    
def hochberg_test(ranks, control=None):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    if not control:
        control_i = values.index(min(values))
    else:
        control_i = keys.index(control)

    comparisons = [keys[control_i] + " vs " + keys[i] for i in range(k) if i != control_i]
    z_values = [abs(values[control_i] - values[i]) for i in range(k) if i != control_i]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [min(max((k-j)*p_values[j-1] for j in range(k-1, i, -1)), 1) for i in range(k-1)]
    
    return comparisons, z_values, p_values, adj_p_values

def li_test(ranks, control=None):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    if not control:
        control_i = values.index(min(values))
    else:
        control_i = keys.index(control)

    comparisons = [keys[control_i] + " vs " + keys[i] for i in range(k) if i != control_i]
    z_values = [abs(values[control_i] - values[i]) for i in range(k) if i != control_i]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [p_values[i]/(p_values[i]+1-p_values[-1]) for i in range(k-1)]
    
    return comparisons, z_values, p_values, adj_p_values

def finner_test(ranks, control=None):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    if not control:
        control_i = values.index(min(values))
    else:
        control_i = keys.index(control)

    comparisons = [keys[control_i] + " vs " + keys[i] for i in range(k) if i != control_i]
    z_values = [abs(values[control_i] - values[i]) for i in range(k) if i != control_i]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [min(max(1-(1-p_values[j])**((k-1)/float(j+1)) for j in range(i+1)), 1) for i in range(k-1)]
    
    return comparisons, z_values, p_values, adj_p_values


def nemenyi_multitest(ranks):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    versus = list(it.combinations(range(k), 2))

    comparisons = [keys[vs[0]] + " vs " + keys[vs[1]] for vs in versus]
    z_values = [abs(values[vs[0]] - values[vs[1]]) for vs in versus]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    m = int(k*(k-1)/2.)
    adj_p_values = [min(m*p_value,1) for p_value in p_values]
    
    return comparisons, z_values, p_values, adj_p_values


def holm_multitest(ranks):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    versus = list(it.combinations(range(k), 2))

    comparisons = [keys[vs[0]] + " vs " + keys[vs[1]] for vs in versus]
    z_values = [abs(values[vs[0]] - values[vs[1]]) for vs in versus]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    m = int(k*(k-1)/2.)
    adj_p_values = [min(max((m-j)*p_values[j] for j in range(i+1)), 1) for i in range(m)]
    
    return comparisons, z_values, p_values, adj_p_values


def hochberg_multitest(ranks):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    versus = list(it.combinations(range(k), 2))

    comparisons = [keys[vs[0]] + " vs " + keys[vs[1]] for vs in versus]
    z_values = [abs(values[vs[0]] - values[vs[1]]) for vs in versus]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    m = int(k*(k-1)/2.)
    adj_p_values = [max((m+1-j)*p_values[j-1] for j in range(m, i, -1))for i in range(m)]
    
    return comparisons, z_values, p_values, adj_p_values
    

def finner_multitest(ranks):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    versus = list(it.combinations(range(k), 2))

    comparisons = [keys[vs[0]] + " vs " + keys[vs[1]] for vs in versus]
    z_values = [abs(values[vs[0]] - values[vs[1]]) for vs in versus]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    m = int(k*(k-1)/2.)
    adj_p_values = [min(max(1-(1-p_values[j])**(m/float(j+1)) for j in range(i+1)), 1) for i in range(m)]
    
    return comparisons, z_values, p_values, adj_p_values


def S(k):
    if k == 0 or k == 1:
        return {0}
    else:
        result = set()
        for j in reversed(range(1, k+1)):
            tmp = S(k - j)
            for s in tmp:
                result = result.union({sp.special.binom(j, 2) + s})
        return list(result)


def shaffer_multitest(ranks):
    k = len(ranks)
    values = ranks.values()
    keys = ranks.keys()
    versus = list(it.combinations(range(k), 2))
    
    m = int(k*(k-1)/2.)
    A = S(int((1 + sp.sqrt(1+4*m*2))/2))
    t = [max([a for a in A if a <= m-i]) for i in range(m)]

    comparisons = [keys[vs[0]] + " vs " + keys[vs[1]] for vs in versus]
    z_values = [abs(values[vs[0]] - values[vs[1]]) for vs in versus]
    p_values = [2*(1-st.norm.cdf(abs(z))) for z in z_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, z_values, comparisons = map(list, zip(*sorted(zip(p_values, z_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [min(max(t[j]*p_values[j] for j in range(i+1)), 1) for i in range(m)]
    
    return comparisons, z_values, p_values, adj_p_values

