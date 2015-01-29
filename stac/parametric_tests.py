

import itertools as it
import scipy as sp
import scipy.stats as st

def anova_test(*args):
    k = len(args)
    if k < 2: raise ValueError('Less than 2 groups')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')

    # Precalcs
    x_j = [sp.sum(group) for group in args]
    x_t = sp.sum(x_j)

    # Variances
    ss_t = sp.sum([v**2 for v in group for group in args]) - x_t**2/float(k*n)
    ss_bg = sp.sum(x_j[j]**2/float(n) for j in range(k)) - x_t**2/float(k*n)
    ss_wg = ss_t - ss_bg

    # Degrees of freedom
    df_bg = k - 1
    df_wg = n*k - k

    F = (ss_bg/df_bg)/(ss_wg/df_wg)
    p_value = 1 - st.f.cdf(F, df_bg, df_wg)
    
    # Pivots
    pivots = [sp.mean(group)/sp.sqrt(2*(ss_wg/df_wg)/float(n)) for group in args]

    return F, p_value, pivots
    
def anova_within_test(*args):
    k = len(args)
    if k < 2: raise ValueError('Less than 2 groups')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')

    # Precalcs
    x_j = [sp.sum(group) for group in args]
    x_t = sp.sum(x_j)
    s_i = [sp.sum([group[i] for group in args]) for i in range(n)]

    # Variances
    ss_t = sp.sum([v**2 for v in group for group in args]) - x_t**2/float(k*n)
    ss_bg = sp.sum([x_j[j]**2/float(n) for j in range(k)]) - x_t**2/float(k*n)
    ss_bs = sp.sum([s_i[i]**2/float(k) for i in range(n)]) - x_t**2/float(k*n)
    ss_wg = ss_t - ss_bg
    ss_res = ss_t - ss_bg - ss_bs

    # Degrees of freedom
    df_bg = k - 1
    df_wg = n*k - k
    df_res = (n-1)*(k-1)

    F = (ss_bg/df_bg)/(ss_res/df_res)
    p_value = 1 - st.f.cdf(F, df_bg, df_res)
    
    # Pivots
    pivots = [sp.mean(group)/sp.sqrt(2*(ss_wg/df_wg)/float(n)) for group in args]

    return F, p_value, pivots

def bonferroni_test(pivots, n):
    k = len(pivots)
    values = pivots.values()
    keys = pivots.keys()

    m = (k*(k-1))/2.

    versus = list(it.combinations(range(k), 2))

    comparisons = [keys[vs[0]] + " vs " + keys[vs[1]] for vs in versus]
    t_values = [abs(values[vs[0]] - values[vs[1]]) for vs in versus]
    p_values = [1-st.t.cdf(t, n*k-k) for t in t_values]
    # Sort values by p_value so that p_0 < p_1
    p_values, t_values, comparisons = map(list, zip(*sorted(zip(p_values, t_values, comparisons), key=lambda t: t[0])))
    adj_p_values = [min(m*p_value,1) for p_value in p_values]
    
    return comparisons, t_values, p_values, adj_p_values
