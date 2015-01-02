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
    if k < 3: raise ValueError('Less than 3 levels')
    n = len(args[0])
    if len(set([len(v) for v in args])) != 1: raise ValueError('Unequal number of samples')
    

    rankings = []
    for i in range(N):
        row = [col[i] for col in data.items()]
        row_sort = sorted(tmp, reverse=objective)
        rankings.append([row_sort.index(v) + (row_sort.count(v)-1)/2. for v in row])

    rankings_avg = [sp.mean([row[i] for row in rankings]) for i in range(K)]

    chi2 = ((12*N)/float((K*(K+1))))*((sp.sum(r**2 for r in rankings_avg))-((K*(K+1)**2)/float(4)))
    iman_davenport = ((N-1)*chi2)/float((N*(K-1)-chi2))

    p_value = 1 - st.f.cdf(iman_davenport, K-1, (K-1)*(N-1))

    return iman_davenport, p_value, rankings_avg



def friedman_rangos_alineados_test(nombres_algoritmos, matriz_datos, alpha=0.05, tipo=0):
    K = len(nombres_algoritmos)

    N = len(matriz_datos)

    observaciones_alineadas = []
    for conj_datos in matriz_datos:
        fila_observaciones = []
        valor_localizacion = sp.mean(conj_datos)
        for dato in conj_datos:
            fila_observaciones.append(dato-valor_localizacion)
        observaciones_alineadas.append(fila_observaciones)

    tabla_a_lista = []
    for fila in observaciones_alineadas:
        for dato in fila:
            tabla_a_lista.append(dato)

    tabla_a_lista.sort(reverse=tipo)

    rankings = []
    for fila in observaciones_alineadas:
        ranking_conj = []
        for dato in fila:
            ranking_conj.append((tabla_a_lista.count(dato)+tabla_a_lista.index(dato)*2+1)/float(2))
        rankings.append(ranking_conj)

    rankings_medios = []
    totales_algoritmos = []
    for i in range(K):
        rankings_medios.append(sp.mean([fila[i] for fila in rankings]))
        totales_algoritmos.append(sp.sum([fila[i] for fila in rankings]))

    totales_conjuntos = []
    for i in rankings:
        totales_conjuntos.append(sp.sum(i))

    T = (K-1)*(sp.sum(total**2 for total in totales_algoritmos)-(K*N**2/float(4))*(K*N+1)**2)/float(((K*N*(K*N+1)*(2*K*N+1))/float(6))-(1/float(K))*sp.sum(total**2 for total in totales_conjuntos))

    p_valor = 1 - st.chi2.cdf(T, K-1)

    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

    rankings_medios.sort()

    return {"result" : np.asscalar(p_valor < alpha), "p_value" : p_valor, "statistic" : T,
    "names" : ranking_nombres, "ranking" : rankings_medios}



def quade_test(nombres_algoritmos, matriz_datos, alpha=0.05, tipo=0):
    K = len(nombres_algoritmos)

    N = len(matriz_datos)

    rankings_resultados = []
    for conj_datos in matriz_datos:
        ranking_conj = []
        copia = list(conj_datos)

        copia.sort(reverse=tipo)
        for dato in conj_datos:
            ranking_conj.append((copia.count(dato)+copia.index(dato)*2+1)/float(2))
        rankings_resultados.append(ranking_conj)

    rankings_problemas = []
    rangos = []
    for conj_datos in matriz_datos:
        rangos.append(max(conj_datos)-min(conj_datos))
    copia = list(rangos)
    copia.sort()
    for rango in rangos:
        rankings_problemas.append((copia.count(rango)+copia.index(rango)*2+1)/float(2))

    S = []
    W = []
    ranking_medio = (K+1)/float(2)
    contador_problemas = 0
    for ranking_conj in rankings_resultados:
        fila_s = []
        fila_w = []
        for i in range(K):
            fila_s.append(rankings_problemas[contador_problemas]*(ranking_conj[i]-ranking_medio))
            fila_w.append(rankings_problemas[contador_problemas]*ranking_conj[i])
        contador_problemas+=1
        S.append(fila_s)
        W.append(fila_w)

    Sj = []
    Wj = []
    for i in range(K):
        Sj.append(sp.sum(fila[i] for fila in S))
        Wj.append(sp.sum(fila[i] for fila in W))

    rankings_medios = []
    for i in range(K):
        rankings_medios.append(Wj[i]/float((N*(N+1))/float(2)))

    A = N*(N+1)*(2*N+1)*K*(K+1)*(K-1)/float(72)
    B = sp.sum(x**2 for x in Sj)/float(N)

    T = (N-1)*B/float(A-B)

    p_valor = 1 - st.f.cdf(T, K-1, (K-1)*(N-1))

    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

    rankings_medios.sort()

    return {"result" : np.asscalar(p_valor < alpha), "p_value" : p_valor, "statistic" : T,
    "names" : ranking_nombres, "ranking" : rankings_medios}



def datos_comunes_tests(test_principal, nombres, ranking, N):
    K = len(ranking)

    valores_z = []
    if test_principal == "friedman_test" or test_principal == "iman_davenport_test":
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

