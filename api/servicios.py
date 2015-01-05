# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 12:49:31 2014

@author: Adrián
"""

import sys, os
sys.path = [os.path.dirname(__file__), os.path.dirname(os.path.dirname(__file__))] + sys.path
from bottle import route, run, response, request
import scipy.stats as st
import numpy as np
from stac import nonparametric_tests as npt
from stac import parametric_tests as pt
from utils import clean_missing_values
import json

def headers(func):
    def func_wrapper(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.content_type = "application/json"
        try:
            return json.dumps(func(*args, **kwargs))
        except Exception as e:
            return json.dumps({"error": str(e)})
        
    return func_wrapper


@route('/wilcoxon', method="POST")
@route('/wilcoxon/<alpha:float>', method="POST")
@headers
def wilcoxon(alpha=0.05):
    values = clean_missing_values(request.json['values'])
    statistic, p_value = st.wilcoxon(values.values()[0], values.values()[1])
    result = int(p_value<alpha)
    return {"result" : result, "statistic" : statistic, "p_value" : p_value}
    
	
@route('/mannwhitneyu', method="POST")
@route('/mannwhitneyu/<alpha:float>', method="POST")
@headers
def mannwhitneyu(alpha=0.05):
    values = clean_missing_values(request.json['values'], delete_row=False)
    statistic, p_value = st.mannwhitneyu(values.values()[0], values.values()[1], use_continuity="false")
    result = int(p_value*2<alpha)
    return {"result" : result, "statistic" : statistic, "p_value" : p_value*2}
    

def ranking(func):
    def func_wrapper(alpha=0.05, *args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.content_type = "application/json"
        statistic, p_value, rankings, names, comparisons, z_values, adj_p_values = func(*args, **kwargs)
        return {
            "ranking": {
                "statistic": statistic, 
                "p_value": p_value, 
                "rankings": rankings,
                "names": names,
                "result": np.asscalar(p_value < alpha)
            },
            "post_hoc": {
                "comparisons": comparisons,
                "statistic": z_values,
                "p_value": adj_p_values,
                "control": names[0],
                "result": [int(adj_p_value < alpha) for adj_p_value in adj_p_values]
            }
        }
    return func_wrapper

@route('/friedman', method="POST")
@route('/friedman/<alpha:float>', method="POST")
@route('/friedman/<post_hoc>', method="POST")
@route('/friedman/<post_hoc>/<alpha:float>', method="POST")
@headers
@ranking
def friedman(alpha=0.05, post_hoc="bonferroni_dunn_test"):
    values = clean_missing_values(request.json['values'])
    statistic, p_value, rankings, ranking_cmp = npt.friedman_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values
    

@route('/friedman-aligned-ranks', method="POST")
@route('/friedman-aligned-ranks/<alpha:float>', method="POST")
@route('/friedman-aligned-ranks/<post_hoc>', method="POST")
@route('/friedman-aligned-ranks/<post_hoc>/<alpha:float>', method="POST")
@headers
@ranking
def friedman_aligned_ranks(alpha=0.05, post_hoc="bonferroni_dunn_test"):
    values = clean_missing_values(request.json['values'])
    statistic, p_value, rankings, ranking_cmp = npt.friedman_aligned_ranks_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values
    
@route('/quade', method="POST")
@route('/quade/<alpha:float>', method="POST")
@route('/quade/<post_hoc>', method="POST")
@route('/quade/<post_hoc>/<alpha:float>', method="POST")
@headers
@ranking
def quade(alpha=0.05, post_hoc="bonferroni_dunn_test"):
    values = clean_missing_values(request.json['values'])
    statistic, p_value, rankings, ranking_cmp = npt.quade_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values


@route('/shapiro', method="POST")
@route('/shapiro/<alpha:float>', method="POST")
@headers
def shapiro(alpha=0.05):
    values = clean_missing_values(request.json['values'], delete_row=False)
    statistics, p_values = map(list, zip(*[st.shapiro(v) for v in values.values()]))
    result = [int(p_value < alpha) for p_value in p_values]
    return {"statistic": statistics, "p_value": p_values, "result": result}
    
@route('/kolmogorov', method="POST")
@route('/kolmogorov/<alpha:float>', method="POST")
@headers
def kolmogorov(alpha=0.05):
    values = clean_missing_values(request.json['values'], delete_row=False)
    statistics, p_values = map(list, zip(*[st.kstest(v, 'norm') for v in values.values()]))
    result = [int(p_value < alpha) for p_value in p_values]
    return {"statistic": statistics, "p_value": p_values, "result": result}
    
@route('/agostino', method="POST")
@route('/agostino/<alpha:float>', method="POST")
@headers
def agostino(alpha=0.05):
    values = clean_missing_values(request.json['values'], delete_row=False)
    statistics, p_values = map(list, zip(*[st.normaltest(v) for v in values.values()]))
    result = [int(p_value < alpha) for p_value in p_values]
    return {"statistic": statistics, "p_value": p_values, "result": result}

@route('/levene', method="POST")
@route('/levene/<alpha:float>', method="POST")
@headers
def levene(alpha=0.05):
    values = clean_missing_values(request.json['values'], delete_row=False)
    statistic, p_value = st.levene(*values.values())
    result = int(p_value < alpha)
    return {"statistic": statistic, "p_value": p_value, "result": result}


@route('/ttest', method="POST")
@route('/ttest/<alpha:float>', method="POST")
@headers
def ttest(alpha=0.05):
    values = clean_missing_values(request.json['values'])
    statistic, p_value = st.ttest_rel(*values.values())
    result = int(p_value < alpha)
    return {"statistic": statistic.tolist(), "p_value": p_value, "result": result}
    
@route('/ttest-ind', method="POST")
@route('/ttest-ind/<alpha:float>', method="POST")
@headers
def ttest_ind(alpha=0.05):
    values = clean_missing_values(request.json['values'])
    statistic, p_value = st.ttest_ind(*values.values())
    result = int(p_value < alpha)
    return {"statistic": statistic.tolist(), "p_value": p_value, "result": result}


@route('/anova', method="POST")
@route('/anova/<alpha:float>', method="POST")
@headers
def anova(alpha=0.05):
    values = clean_missing_values(request.json['values'])
    statistic, p_value, pivots = pt.anova_test(*values.values())
    pivots_cmp = {key: pivots[i] for i,key in enumerate(values.keys())}
    comparisons, t_values, _, adj_p_values = pt.bonferroni_test(pivots_cmp, len(values.values()[0]))
    return {
            "anova": {
                "statistic": statistic, 
                "p_value": p_value, 
                "result": np.asscalar(p_value < alpha)
            },
            "post_hoc": {
                "comparisons": comparisons,
                "statistic": t_values,
                "p_value": adj_p_values,
                "result": [int(adj_p_value < alpha) for adj_p_value in adj_p_values]
            }
        }
    

if __name__ == '__main__':
    run(reloader=True, host='localhost', port=8080, quiet=False)

