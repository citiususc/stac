

import itertools as it
import scipy as sp
import scipy.stats as st

def anova_test(*args):
    k = len(args)
    if k < 2: raise ValueError('Less than 2 levels')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')

    means = [sp.mean(sample) for sample in args]
    mean_global = sp.mean(means)
    ss_error = sp.sum([(args[i][j] - means[i])**2 for j in range(n) for i in range(k)])
    ss_population = sp.sum([n*(means[i] - mean_global)**2 for i in range(k)])
    sd = sp.sqrt(sp.sum([(means[i] - mean_global)**2 for i in range(k)])/float(n-k))
    pivots = [mean/(sd*sp.sqrt(2/float(n))) for mean in means]

    F = (ss_population/float(k-1))/(ss_error/float(n*k-k))
    p_value = 1 - st.f.cdf(F, k-1, n*k-k)

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
