# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:33:54 2014

@author: Adrián
"""

import scipy as sp
import scipy.stats as st

#Para cuando el tamaño muestral N sea menor o igual a 25, se puede hacer el test de Wilcoxon
#examinando la tabla que nos da los valores críticos (el intervalo) para cada valor de N y
#nivel de significancia (0.10,0.05,0.02,0.01,0.005,0.001) dado. Si tenemos en cuenta que T
#será el valor mínimo de (suma rangos positivos, suma rangos negativos), se utilizan los límites
#inferiores de los intervalos y el contraste será estadísticamente significativo si: T <= límite
#inferior correspondiente.
tabla_wilcoxon = {0.10:{5:0,6:2,7:3,8:5,9:8,10:10,11:13,12:17,13:21,14:25,15:30,16:35,17:41,
                    18:47,19:53,20:60,21:67,22:75,23:83,24:91,25:100},
                  0.05:{6:0,7:2,8:3,9:5,10:8,11:10,12:13,13:17,14:21,15:25,16:29,17:34,18:40,
                    19:46,20:52,21:58,22:65,23:73,24:81,25:89},
                  0.02:{7:0,8:1,9:3,10:5,11:7,12:9,13:12,14:15,15:19,16:23,17:27,18:32,19:37,
                    20:43,21:49,22:55,23:62,24:69,25:76},
                  0.01:{8:0,9:1,10:3,11:5,12:7,13:9,14:12,15:15,16:19,17:23,18:27,19:32,20:37,
                    21:42,22:48,23:54,24:61,25:68},
                  0.005:{9:0,10:1,11:3,12:5,13:7,14:9,15:12,16:15,17:19,18:23,19:27,20:32,
                    21:37,22:42,23:48,24:54,25:60},
                  0.001:{11:0,12:1,13:2,14:4,15:6,16:8,17:11,18:14,19:18,20:21,21:25,22:30,
                    23:35,24:40,25:45}}

"""Test de los Rangos Signados de Wilcoxon."""
def wilcoxon_test(matriz_datos, alpha):

    #El test de Wilcoxon compara dos algoritmos.
    if len(matriz_datos[0]) != 2:
        return {"fallo" : "Test de Wilcoxon solo aplicable a dos algoritmos"}
    
    #Paso de una matriz de conjuntos de datos a dos listas: lista "a", que contiene
    #los resultados de aplicar el primer algoritmo a los datos y una lista "b" que
    #contiene los resultados de aplicar el segundo algoritmo sobre los mismos datos.
    a = []
    b = []
    for lista_datos in matriz_datos:
        a.append(lista_datos[0])
        b.append(lista_datos[1])
    
    #Cálculo del número de veces que se aplican los dos algoritmos, es decir,
    #el número de individuos o datos sobre los que se aplican los algoritmos. El
    #tamaño de a y b deben ser iguales. Se conoce como tamaño muestral. Hay
    #dos muestras: a y b.
    N = len(a)
    
    #Cálculo de las diferencias sin signos y con signos. Se excluye el 0.
    diferencias = []
    signos = []
    for i in range(N):
        diferencia = a[i]-b[i]
        if diferencia != 0:
            diferencias.append(abs(diferencia))
            signos.append(diferencia)
    
    #Tamaño muestral después de eliminar las diferencias 0.
    N = len(diferencias)

    #El tamaño de la muestra  (sin ligaduras) debe ser al menos de 5.
    if N < 5:
        return {"fallo" : "Menos de 5 conjuntos de datos sin ligaduras"}

    #Rangos de orden 1,2,...,N. Cada elemento de copia tiene un rango asociado:
    #indice(elemento) + 1. Si hay empates se calcula la media del rango de cada
    #uno de los elementos repetidos.
    copia = list(diferencias)
    copia.sort()
    rangos = []
    for i in diferencias:
        rangos.append((copia.count(i)+copia.index(i)*2+1)/float(2))
    
    #Sumas de los rangos de las Di mayores que 0 y menores que 0.
    mayor0 = []
    menor0 = []
    for i in range(N):
        if signos[i] > 0:
            mayor0.append(rangos[i])
        else:
            menor0.append(rangos[i])
    T_Mas = sp.sum(mayor0)
    T_Men = sp.sum(menor0)

    #T es el valor mínimo de T_Mas y T_Men.
    T = min(T_Mas,T_Men)
    
    print "N (sin ceros):" , N
    print "Suma de rangos positivos:" , T_Mas
    print "Suma de rangos negativos:" , T_Men
    print "Valor T:" , T
    
    #Para tamaños muestrales pequeños, se puede determinar el test de Wilcoxon mediante la comparación
    #de T con el valor crítico de la tabla de Wilcoxon. Para tamaños muestrales grandes, el test se puede
    #aproximar con la distribución normal.
    if N <= 25:
        #Límite inferior del intervalo de aceptación.
        punto_critico = tabla_wilcoxon[alpha][N]
        return {"resultado" : str(T <= punto_critico), "estadistico" : T, "suma rangos pos" : T_Mas, "suma rangos neg" : T_Men ,
        "punto critico" : punto_critico}
    else:
        #Cálculo del valor Z
        Z = (T-((N*(N+1))/float(4)))/float(sp.sqrt((N*(N+1)*(2*N+1))/float(24)))
        #Cálculo del punto critico de la distribución Normal (Para alpha = 0.05
        #es -1.96 en el caso de dos colas, es decir 0.025 a cada lado).
        Z_alphaDiv2 = st.norm.ppf(alpha/float(2))
        #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo
        #como el estadístico Z.
        p_valor = 2*(1-st.norm.cdf(abs(Z)))
		
        print "Valor Z:" , Z
        print "Valor Z_alphaDiv2:" , Z_alphaDiv2
        print "p_valor:" , p_valor
        
        #Si p_valor < alpha => contraste estadísticamente significativo. Otra 
        #forma de saber si el estadístico Z cae en la región de rechazo es:
        #if Z <= Z_alphaDiv2 or Z >= -Z_alphaDiv2:
            #print "Se rechaza H0."
        #else:
            #print "Se acepta HO."
        
        return {"resultado" : str(p_valor < alpha), "p_valor" : round(p_valor,6), "estadistico" : round(Z,3),
        "suma rangos pos" : T_Mas, "suma rangos neg" : T_Men, "puntos criticos" : [round(Z_alphaDiv2,2),round(-Z_alphaDiv2,2)]}
  


"""Test de Friedman."""      
def friedman_test(nombres_algoritmos, matriz_datos, alpha, tipo):
    
    #Número de algoritmos.
    K = len(nombres_algoritmos)
    
    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)
    
    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema.
    #Cada fila representa un conjunto de datos compuesto por los valores (rankings) asignados.
    #Los valores se asignan de forma ascencente: 1 al mejor resultado, 2 al segundo, etc. En
    #caso de empates, se asignan valores medios.
    rankings = []
    for conj_datos in matriz_datos:
        ranking_conj = []
        copia = list(conj_datos)
        #Ordenamos según el problema se tratase de maximizar o minimizar.
        copia.sort(reverse=tipo)
        for dato in conj_datos:
            ranking_conj.append((copia.count(dato)+copia.index(dato)*2+1)/float(2))
        rankings.append(ranking_conj)
        
    #Cálculo de los rankings medios de los algoritmos sobre los N problemas.
    rankings_medios = []
    for i in range(K):
        rankings_medios.append(sp.mean([fila[i] for fila in rankings]))
        
    #Cálculo del estadístico de Friedman, que se distribuye como una distribución chi-cuadrado
    #con K-1 grados de libertad, siendo K el número de variables relacionadas (o número de algoritmos).
    chi2 = ((12*N)/float((K*(K+1))))*((sp.sum(r**2 for r in rankings_medios))-((K*(K+1)**2)/float(4)))
    
    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico 
    #chi2.
    p_valor = 1 - st.chi2.cdf(chi2, K-1)
    
    #Cálculo del ranking de los nombres de los algoritmos (de acuerdo a los rankings medios obtenidos).
    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

	#Ordenamiento de menor a mayor de los rankings medios obtenidos y redondeo de sus datos.
    rankings_medios.sort()
    for i in range(K):
        rankings_medios[i] = round(rankings_medios[i],3)

    return {"resultado" : str(p_valor < alpha), "p_valor": round(p_valor,6), "estadistico" : round(chi2,3), 
    "nombres" : ranking_nombres, "ranking" : rankings_medios}



"""Test de Iman-Davenport."""
def iman_davenport_test(nombres_algoritmos, matriz_datos, alpha, tipo):

    #Número de algoritmos.
    K = len(nombres_algoritmos)
    
    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)
    
    # Cálculo del estadistico de Friedman.
    friedman = friedman_test(nombres_algoritmos, matriz_datos, alpha, tipo)
    chi2 = friedman["estadistico"]

    # Cálculo del estadistico de Iman-Davenport, que se distribuye de acuerdo a una distribución
    #f con (K-1) y (K-1)(N-1) grados de libertad.
    iman_davenport = ((N-1)*chi2)/float((N*(K-1)-chi2))
    
    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico 
    #iman_davenport.
    p_valor = 1 - st.f.cdf(iman_davenport, K-1, (K-1)*(N-1))

    return {"resultado" : str(p_valor < alpha), "p_valor": round(p_valor,6), "estadistico" : round(iman_davenport,3), 
    "nombres": friedman["nombres"], "ranking": friedman["ranking"]}



"""Test de los Rangos Alineados de Friedman."""
def friedman_rangos_alineados_test(nombres_algoritmos, matriz_datos, alpha, tipo):

    #Número de algoritmos.
    K = len(nombres_algoritmos)
    
    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)
    
    #Cálculo de las observaciones alienadas: Primero se halla el valor de localización, que es el
    #rendimiento medio alcanzado por cada algoritmo en cada conjunto de datos. Luego, se calculan
	#las diferencias entre el rendimiento obtenido por cada algoritmo con respecto al valor de localización.
    #Se repite para todos los algoritmos y conjuntos de datos.
    observaciones_alineadas = []
    for conj_datos in matriz_datos:
        fila_observaciones = []
        valor_localizacion = sp.mean(conj_datos)
        for dato in conj_datos:
            fila_observaciones.append(dato-valor_localizacion)
        observaciones_alineadas.append(fila_observaciones)
        
    # Creación de una lista a partir de la tabla observaciones_alineadas.
    tabla_a_lista = []
    for fila in observaciones_alineadas:
        for dato in fila:
            tabla_a_lista.append(dato)
    
    # Ordenación de la lista.
    tabla_a_lista.sort(reverse=tipo)
    
    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema.
    #Cada fila representa un conjunto de datos compuesto por los rankings asignados. Los
    #rankings se asignan de forma ascencente: 1 al mejor resultado, 2 al segundo, ... hasta
    #K*N. En caso de empates, se asignan valores medios.
    rankings = []
    for fila in observaciones_alineadas:
        ranking_conj = []
        for dato in fila:
            ranking_conj.append((tabla_a_lista.count(dato)+tabla_a_lista.index(dato)*2+1)/float(2))
        rankings.append(ranking_conj)
    
    #Cálculo de los rankings medios de los algoritmos sobre los N problemas y de la suma de los
    #ranking obtenidos por cada algoritmo.
    rankings_medios = []
    totales_algoritmos = []
    for i in range(K):
        rankings_medios.append(sp.mean([fila[i] for fila in rankings]))
        totales_algoritmos.append(sp.sum([fila[i] for fila in rankings]))
        
    #Cálculo de suma de los rankings obtenidos para cada conjunto de datos.
    totales_conjuntos = []
    for i in rankings:
        totales_conjuntos.append(sp.sum(i))
        
    #Cálculo del estadístico de los Rangos Alineados de Friedman.
    T = (K-1)*(sp.sum(total**2 for total in totales_algoritmos)-(K*N**2/float(4))*(K*N+1)**2)/float(((K*N*(K*N+1)*(2*K*N+1))/float(6))-(1/float(K))*sp.sum(total**2 for total in totales_conjuntos))

    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico T.
    p_valor = 1 - st.chi2.cdf(T, K-1)
    
    #Cálculo del ranking de los nombres de los algoritmos (de acuerdo a los rankings medios obtenidos).
    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

	#Ordenamiento de menor a mayor de los rankings medios obtenidos y redondeo de sus datos.
    rankings_medios.sort()
    for i in range(K):
        rankings_medios[i] = round(rankings_medios[i],3)
        
    return {"resultado" : str(p_valor < alpha), "p_valor": round(p_valor,6), "estadistico" : round(T,3), 
    "nombres" : ranking_nombres, "ranking" : rankings_medios}



"""Test de Quade."""
def quade_test(nombres_algoritmos, matriz_datos, alpha, tipo):
    
    #Número de algoritmos.
    K = len(nombres_algoritmos)
    
    #Número de conjuntos de datos (Número de veces que se aplican los algoritmos o número de
    #problemas).
    N = len(matriz_datos)
    
    #Asignación de rankings a los resultados obtenidos por cada algoritmo en cada problema de forma
    #similar al test de Friedman: cada fila representa un conjunto de datos compuesto por los 
    #valores (rankings) asignados. Los valores se asignan de forma ascencente: 1 al mejor resultado,
    #2 al segundo, etc. En caso de empates, se asignan valores medios.
    rankings_resultados = []
    for conj_datos in matriz_datos:
        ranking_conj = []
        copia = list(conj_datos)
        #Ordenamos según el problema se tratase de maximizar o minimizar.
        copia.sort(reverse=tipo)
        for dato in conj_datos:
            ranking_conj.append((copia.count(dato)+copia.index(dato)*2+1)/float(2))
        rankings_resultados.append(ranking_conj)

    #Los rankings se asignan a los problemas de acuerdo al tamaño del rango de la muestra en cada
    #uno. El rango de la muestra en un problema es la diferencia entre la observación más alta y
    #la más baja en dicho problema. Se asigna el ranking 1 al conjunto con el menor rango, el 2 al
    #segundo con menor rango, etc. Se utilizan rankings medios en caso de empate.
    rankings_problemas = []
    rangos = []
    for conj_datos in matriz_datos:
        rangos.append(max(conj_datos)-min(conj_datos))
    copia = list(rangos)
    copia.sort()
    for rango in rangos:
        rankings_problemas.append((copia.count(rango)+copia.index(rango)*2+1)/float(2))
    
    #S, W.
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
      
    #Sj, Wj.
    Sj = []
    Wj = []
    for i in range(K):
        Sj.append(sp.sum(fila[i] for fila in S))
        Wj.append(sp.sum(fila[i] for fila in W))
    
    #Rankings medios.
    rankings_medios = []
    for i in range(K):
        rankings_medios.append(Wj[i]/float((N*(N+1))/float(2)))
    
    #Términos A, B.
    A = N*(N+1)*(2*N+1)*K*(K+1)*(K-1)/float(72)
    B = sp.sum(x**2 for x in Sj)/float(N)
    
    #Cáculo del estadístico.
    T = (N-1)*B/float(A-B)
    
    #Cálculo del p_valor: Probabilidad de obtener un valor al menos tan extremo como el estadístico T.
    p_valor = 1 - st.f.cdf(T, K-1, (K-1)*(N-1))
    
    #Cálculo del ranking de los nombres de los algoritmos (de acuerdo a los rankings medios obtenidos).
    ranking_nombres = []
    for i in sorted({nombres_algoritmos[i] : rankings_medios[i] for i in range(K)}.items(), key = lambda t:t[1]):
        ranking_nombres.append(i[0])

    #Ordenamiento de menor a mayor de los rankings medios obtenidos y redondeo de sus datos.
    rankings_medios.sort()
    for i in range(K):
        rankings_medios[i] = round(rankings_medios[i],3)
            
    return {"resultado" : str(p_valor < alpha), "p_valor": round(p_valor,6), "estadistico" : round(T,3), 
    "nombres" : ranking_nombres, "ranking" : rankings_medios}



"""Test de Bonferroni Dunn."""
def bonferroni_dunn_test(test_principal, nombres, ranking, N, alpha):
    
    #Número de algoritmos K (incluyendo método de control).
    K = len(ranking)
    
    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman" or test_principal == "iman-davenport":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "rangos-alineados":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))
    
    #Cálculo de los p_valores.
    p_valores = []
    for i in range(K-1):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))
        
    #Método de control (Primero del ranking).
    metodo_control = nombres[0]
    
    #Ordenamiento de los nombres, valores_z y p_valores segun el p_valor.
    tabla = zip(nombres[1:],valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    n, z, p = zip(*tabla)
    nombres = list(n)
    valores_z = list(z)
    p_valores = list(p)
    
    #Nuevo alpha.
    alpha2 = alpha/float(K-1)

    #Cálculo de los resultados.
    resultado = []
    for i in range(K-1):
        resultado.append(p_valores[i]<alpha2)
        
    #Cálculo de los p_valores ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        v = (K-1)*p_valores[i]
        p_valores_ajustados.append(min(v,1))
    
    return {"valores z" : valores_z, "p_valores" : p_valores, "metodo de control" : metodo_control,
            "nombres" : nombres, "alpha" : alpha2, "resultado" : resultado, "p_valores ajustados" : p_valores_ajustados}



"""Test de Holm."""
def holm_test(test_principal, nombres, ranking, N, alpha):
    
    #Número de algoritmos K (incluyendo método de control).
    K = len(ranking)
    
    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman" or test_principal == "iman-davenport":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "rangos-alineados":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))
    
    #Cálculo de los p_valores.
    p_valores = []
    for i in range(K-1):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))
        
    #Método de control (Primero del ranking).
    metodo_control = nombres[0]
    
    #Ordenamiento de los nombres, valores_z y p_valores segun el p_valor.
    tabla = zip(nombres[1:],valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    n, z, p = zip(*tabla)
    nombres = list(n)
    valores_z = list(z)
    p_valores = list(p)
    
    #Valores alphas.
    alphas = []
    for i in range(1,K):
        alphas.append(alpha/float(K-i))
    
    #Cálculo de los resultados.
    resultado = [False]*(K-1)
    for i in range(K-1):
        if p_valores[i] < alphas[i]:
            resultado[i] = True
        else:
            break
    
    #Cálculo de los p_valores ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        v = max([(K-(j+1))*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))
        
    return {"valores z" : valores_z, "p_valores" : p_valores, "metodo de control" : metodo_control,
            "nombres" : nombres, "alphas" : alphas, "resultado" : resultado, "p_valores ajustados" : p_valores_ajustados}



"""Test de Hochberg."""
def hochberg_test(test_principal, nombres, ranking, N, alpha):
    
    #Número de algoritmos K (incluyendo método de control).
    K = len(ranking)
    
    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman" or test_principal == "iman-davenport":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "rangos-alineados":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))
    
    #Cálculo de los p_valores.
    p_valores = []
    for i in range(K-1):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))
        
    #Método de control (Primero del ranking).
    metodo_control = nombres[0]
    
    #Ordenamiento de los nombres, valores_z y p_valores segun el p_valor.
    tabla = zip(nombres[1:],valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    n, z, p = zip(*tabla)
    nombres = list(n)
    valores_z = list(z)
    p_valores = list(p)
    
    #Valores alphas.
    alphas = []
    for i in range(K-1,0,-1):
        alphas.append(alpha/float(i))
    
    #Cálculo de los resultados.
    resultado = [True]*(K-1)
    for i in range(K-2,-1,-1):
        if p_valores[i] > alphas[i]:
            resultado[i] = False
        else:
            break
    
    #Cálculo de los p_valores ajustados (no da lo mismo que la pág. 142).
    p_valores_ajustados = []
    for i in range(K-1):
        p_valores_ajustados.append(max([(K-j)*p_valores[j-1] for j in range(K-1,i,-1)]))
        
    return {"valores z" : valores_z, "p_valores" : p_valores, "metodo de control" : metodo_control,
            "nombres" : nombres, "alphas" : alphas, "resultado" : resultado, "p_valores ajustados" : p_valores_ajustados}



"""Test de Li."""
def li_test(test_principal, nombres, ranking, N, alpha):
    
    #Número de algoritmos K (incluyendo método de control).
    K = len(ranking)
    
    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman" or test_principal == "iman-davenport":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "rangos-alineados":
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for j in range(1,K):
            valores_z.append((ranking[0]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))
    
    #Cálculo de los p_valores.
    p_valores = []
    for i in range(K-1):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))
        
    #Método de control (Primero del ranking).
    metodo_control = nombres[0]
    
    #Ordenamiento de los nombres, valores_z y p_valores segun el p_valor.
    tabla = zip(nombres[1:],valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    n, z, p = zip(*tabla)
    nombres = list(n)
    valores_z = list(z)
    p_valores = list(p)
    
    #Cálculo de los resultados.
    resultado = [True]*(K-1)
    if p_valores[K-2] > alpha:
        resultado[K-2] =  False
        valor = (1-p_valores[K-2])/float((1-alpha)*alpha)
        for i in range(K-2):
            if p_valores[i] > valor:
                resultado[i] = False

    #Cálculo de los p_valores ajustados.
    p_valores_ajustados = []
    for i in range(K-1):
        p_valores_ajustados.append(p_valores[i]/float(p_valores[i]+1-p_valores[K-2]))
        
    return {"valores z" : valores_z, "p_valores" : p_valores, "metodo de control" : metodo_control,
            "nombres" : nombres, "resultado" : resultado, "p_valores ajustados" : p_valores_ajustados}



"""Test de Shaffer."""
def shaffer_test(test_principal, nombres, ranking, N, alpha):
    
    #Número de algoritmos K (incluyendo método de control).
    K = len(ranking)

    #Número posible de comparaciones.
    m = (K*(K-1))/2

    #Nombres de las coparaciones.
    comparaciones = []
    for i in range(K-1):
        for j in range(1,K):
            comparaciones.append(nombres[i] + " vs " + nombres[j])
    
    #Cálculo del estadístico Z (distribución normal). El valor cambia en función de si el
    #test principal es Friedman o Iman-Davenport, Rangos Alineados de Friedman o Quade.
    valores_z = []
    if test_principal == "friedman" or test_principal == "iman-davenport":
        for i in range(K-1):
            for j in range(1,K):
                valores_z.append((ranking[i]-ranking[j])/sp.sqrt((K*(K+1))/float(6*N)))
    elif test_principal == "rangos-alineados":
        for i in range(K-1):
            for j in range(1,K):
                valores_z.append((ranking[i]-ranking[j])/sp.sqrt((K*(N+1))/float(6)))
    else:
        for i in range(K-1):
            for j in range(1,K):
                valores_z.append((ranking[i]-ranking[j])/sp.sqrt((K*(K+1)*((2*N)+1)*(K-1))/float(18*N*(N+1))))

    #Cálculo de los p_valores.
    p_valores = []
    for i in range(m):
        p_valores.append(2*(1-st.norm.cdf(abs(valores_z[i]))))
    
    #Ordenamiento de las comparaciones, valores_z y p_valores segun el p_valor.
    tabla = zip(comparaciones,valores_z,p_valores)
    tabla.sort(key=lambda valor: valor[2])
    c, z, p = zip(*tabla)
    comparaciones = list(c)
    valores_z = list(z)
    p_valores = list(p)
    
    #Valores alphas (Esto no usa la fórmula de la pág. 150 Lo hace igual que Holm. Hay que revisar).
    alphas = []
    for i in range(1,m+1):
        alphas.append(alpha/float(m+1-i))
    
    #Cálculo de los resultados.
    resultado = [False]*m
    for i in range(m):
        if p_valores[i] < alphas[i]:
            resultado[i] = True
        else:
            break
    
    #Cálculo de los p_valores ajustados (Esto no usa la fórmula de la pág. 150 El tj que usa sería
    #el j de la lista de alphas. Hay que revisar).
    p_valores_ajustados = []
    for i in range(m):
        v = max([alphas[j]*p_valores[j] for j in range(i+1)])
        p_valores_ajustados.append(min(v,1))
        
    return {"valores z" : valores_z, "p_valores" : p_valores, "comparaciones" : comparaciones, "alphas" : alphas,
            "resultado" : resultado, "p_valores ajustados" : p_valores_ajustados}