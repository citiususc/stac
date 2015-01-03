# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.stats as st

def test_ranking(test, post_hoc, data, alpha=0.05, objective=0):

    resultado_ranking = test(data, alpha, objective)

    post_hoc_metodo_control = ["bonferroni_dunn_test", "holm_test", "hochberg_test", "li_test", "finner_test"]

    resultado_post_hoc = {}
    if post_hoc.__name__ in post_hoc_metodo_control:
        K, nombres, valores_z, p_valores, metodo_control = datos_comunes_tests(test.__name__, resultado_ranking["names"], resultado_ranking["ranking"], N)
        resultado_post_hoc = post_hoc(K, nombres, valores_z, p_valores, metodo_control, alpha)
    else:
        m, comparaciones, valores_z, p_valores = datos_comunes_multitests(test.__name__, resultado_ranking["names"], resultado_ranking["ranking"], N)
        resultado_post_hoc = post_hoc(m, comparaciones, valores_z, p_valores, alpha)

    return {"test_ranking" : resultado_ranking, "post_hoc" : resultado_post_hoc}



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

    rankings_avg = [sp.mean([row[i] for row in rankings]) for i in range(k)]

    chi2 = ((12*n)/float((k*(k+1))))*((sp.sum(r**2 for r in rankings_avg))-((k*(k+1)**2)/float(4)))
    iman_davenport = ((n-1)*chi2)/float((n*(k-1)-chi2))

    p_value = 1 - st.f.cdf(iman_davenport, k-1, (k-1)*(n-1))

    return iman_davenport, p_value, rankings_avg



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

    rankings_avg = [sp.mean([row[i] for row in aligned_ranks]) for i in range(k)]

    r_i = [np.sum(row) for row in aligned_ranks]
    r_j = [np.sum([row[j] for row in aligned_ranks]) for j in range(k)]
    T = (k-1) * (sp.sum(v**2 for v in r_j) - (k*n**2/4.) * (k*n+1)**2) / float(((k*n*(k*n+1)*(2*k*n+1))/6.) - (1./float(k))*sp.sum(v**2 for v in r_i))

    p_value = 1 - st.chi2.cdf(T, k-1)

    return T, p_value, rankings_avg



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

    A = sp.sum(S[i][j]**2 for i in range(n) for j in range(k))
    B = sp.sum(s**2 for s in Sj)/float(n)
    T = (n-1)*B/(A-B)

    p_value = 1 - st.f.cdf(T, k-1, (k-1)*(n-1))

    return T, p_value, rankings_avg



def datos_comunes_tests(test_principal, nombres, ranking, N):
    K = len(ranking)

    valores_z = []
    if test_principal == "friedman_test":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "friedman_rangos_alineados_test":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))

    p_valores = []
    for i in range(K-1):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))

    metodo_control = nombres[0]

    tabla = zip(nombres[1:],valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    n, z, p = zip(*tabla)
    nombres = list(n)
    valores_z = list(z)
    p_valores = list(p)

    return K, nombres, valores_z, p_valores, metodo_control



def bonferroni_dunn_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    alpha2 = alpha/float(K-1)

    resultado = []
    for i in range(K-1):
        resultado.append(np.asscalar(p_valores[i]<alpha2))

    p_valores_ajustados = []
    for i in range(K-1):
        v = (K-1)*p_valores[i]
        p_valores_ajustados.append(min(v,1))
    
    return {"statistics" : valores_z, "p_values" : p_valores, "control_method" : metodo_control, "names" : nombres,
            "alpha" : alpha2, "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def holm_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    alphas = []
    for i in range(1,K):
        alphas.append(alpha/float(K-i))

    resultado = [False]*(K-1)
    for i in range(K-1):
        if p_valores[i] < alphas[i]:
            resultado[i] = True
        else:
            break

    p_valores_ajustados = []
    for i in range(K-1):
        v = max([(K-(j+1))*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"statistics" : valores_z, "p_values" : p_valores, "control_method" : metodo_control, "names" : nombres,
            "alphas" : alphas, "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def hochberg_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    alphas = []
    for i in range(K-1,0,-1):
        alphas.append(alpha/float(i))

    resultado = [True]*(K-1)
    for i in range(K-2,-1,-1):
        if p_valores[i] > alphas[i]:
            resultado[i] = False
        else:
            break

    p_valores_ajustados = []
    for i in range(K-1):
        p_valores_ajustados.append(min([(K-j)*p_valores[j-1] for j in range(K-1,i,-1)]))

    return {"statistics" : valores_z, "p_values" : p_valores, "control_method" : metodo_control, "names" : nombres,
            "alphas" : alphas, "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def li_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    resultado = [True]*(K-1)
    if p_valores[K-2] > alpha:
        resultado[K-2] =  False
        valor = ((1-p_valores[K-2])/float(1-alpha))*alpha
        for i in range(K-2):
            if p_valores[i] > valor:
                resultado[i] = False

    p_valores_ajustados = []
    for i in range(K-1):
        p_valores_ajustados.append(p_valores[i]/float(p_valores[i]+1-p_valores[K-2]))

    return {"statistics" : valores_z, "p_values" : p_valores, "control_method" : metodo_control, "names" : nombres,
            "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def finner_test(K, nombres, valores_z, p_valores, metodo_control, alpha=0.05):
    alphas = []
    for i in range(1,K):
        alphas.append(1-(1-alpha)**((K-1)/float(i)))

    resultado = [False]*(K-1)
    for i in range(K-1):
        if p_valores[i] <= alphas[i]:
            resultado[i] = True
        else:
            break

    p_valores_ajustados = []
    for i in range(K-1):
        v = max([1-(1-p_valores[j])**((K-1)/float(j+1)) for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"statistics" : valores_z, "p_values" : p_valores, "control_method" : metodo_control, "names" : nombres,
            "alphas" : alphas, "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def datos_comunes_multitests(test_principal, nombres, ranking, N):
    K = len(ranking)

    m = (K*(K-1))/2

    comparaciones = []
    for i in range(K-1):
        for j in range(i+1,K):
            comparaciones.append(nombres[i] + " vs " + nombres[j])

    valores_z = []
    if test_principal == "friedman_test" or test_principal == "iman_davenport_test":
        for i in range(K-1):
            for j in range(i+1,K):
                valores_z.append((ranking[j]-ranking[i])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "friedman_rangos_alineados_test":
        for i in range(K-1):
            for j in range(i+1,K):
                valores_z.append((ranking[j]-ranking[i])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for i in range(K-1):
            for j in range(i+1,K):
                valores_z.append((ranking[j]-ranking[i])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))

    p_valores = []
    for i in range(m):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))

    tabla = zip(comparaciones,valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    c, z, p = zip(*tabla)
    comparaciones = list(c)
    valores_z = list(z)
    p_valores = list(p)

    return m, comparaciones, valores_z, p_valores



def nemenyi_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    alpha2 = alpha/float(m)

    resultado = []
    for i in range(m):
        resultado.append(np.asscalar(p_valores[i]<alpha2))

    p_valores_ajustados = []
    for i in range(m):
        v = m*p_valores[i]
        p_valores_ajustados.append(min(v,1))

    return {"statistics" : valores_z, "p_values" : p_valores, "comparisons" : comparaciones, "alpha" : alpha2,
            "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def holm_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    alphas = []
    for i in range(1,m+1):
        alphas.append(alpha/float(m+1-i))

    resultado = [False]*m
    for i in range(m):
        if p_valores[i] < alphas[i]:
            resultado[i] = True
        else:
            break

    p_valores_ajustados = []
    for i in range(m):
        v = max([(m-j)*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"statistics" : valores_z, "p_values" : p_valores, "comparisons" : comparaciones, "alphas" : alphas,
            "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def hochberg_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    alphas = []
    for i in range(m,0,-1):
        alphas.append(alpha/float(i))

    resultado = [True]*m
    for i in range(m-1,-1,-1):
        if p_valores[i] > alphas[i]:
            resultado[i] = False
        else:
            break

    p_valores_ajustados = []
    for i in range(m):
        p_valores_ajustados.append(min([(m+1-j)*p_valores[j-1] for j in range(m,i,-1)]))

    return {"statistics" : valores_z, "p_values" : p_valores, "comparisons" : comparaciones, "alphas" : alphas,
            "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def finner_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    alphas = []
    for i in range(1,m+1):
        alphas.append(1-(1-alpha)**(m/float(i)))

    resultado = [False]*m
    for i in range(m):
        if p_valores[i] <= alphas[i]:
            resultado[i] = True
        else:
            break

    p_valores_ajustados = []
    for i in range(m):
        v = max([1-(1-p_valores[j])**(m/float(j+1)) for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"statistics" : valores_z, "p_values" : p_valores, "comparisons" : comparaciones, "alphas" : alphas,
            "result" : resultado, "adjusted_p_values" : p_valores_ajustados}



def S(K):
    if K == 0 or K == 1:
        return {0}
    else:
        result = set()
        for j in reversed(range(1, K+1)):
            tmp = S(K - j)
            for s in tmp:
                result = result.union({sp.special.binom(j, 2) + s})
        return list(result)



def shaffer_multitest(m, comparaciones, valores_z, p_valores, alpha=0.05):
    K = int((1 + sp.sqrt(1+4*m*2))/2)
    A = S(K)
    t = []

    alphas = []
    for i in range(1,m+1):
        t.insert(i-1,max([a for a in A if a <= m-i+1]))
        alphas.append(alpha/float(t[i-1]))

    resultado = [False]*m
    for i in range(m):
        if p_valores[i] <= alphas[i]:
            resultado[i] = True
        else:
            break

    p_valores_ajustados = []
    for i in range(m):
        v = max([t[j]*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))

    return {"statistics" : valores_z, "p_values" : p_valores, "comparisons" : comparaciones, "alphas" : alphas,
            "result" : resultado, "adjusted_p_values" : p_valores_ajustados}

