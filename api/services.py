# -*- coding: utf-8 -*-
import sys, os
sys.path = [os.path.dirname(__file__), os.path.dirname(os.path.dirname(__file__))] + sys.path
from bottle import route, run, response, request, hook
import scipy.stats as st
import numpy as np
from stac import nonparametric_tests as npt
from stac import parametric_tests as pt
from utils import clean_missing_values, evaluate_test
import json
import traceback

def headers(func):
    def func_wrapper(*args, **kwargs):
        response.content_type = "application/json"
        try:
            if request.method == "OPTIONS":
                return {}
            else:
                return json.dumps(func(*args, **kwargs))
        except Exception as e:
            response.status = 400
            return json.dumps({"error": str(e), "stack": str(traceback.format_exc())})
        
    return func_wrapper

@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
 

@route('/assistant', method=["POST", "OPTIONS"])
@headers
def asssistant():
    values = request.json
    data = {'n': len(values.values()[0]), 'k': len(values.keys())}
    
    # Paired?     
    values_clean = clean_missing_values(request.json)
    data['paired'] = True if data['n'] == len(values_clean.values()[0]) else False
    
    # Normality?
    alpha = 0.1
    values_clean = clean_missing_values(request.json, delete_row=False)
    _, p_values = map(list, zip(*[st.shapiro(v) for v in values_clean.values()]))
    data['normality'] = int(reduce(lambda x,y: x and y, [p_value < alpha for p_value in p_values]))
    
    # Homocedasticity?
    _, p_value = st.levene(*values_clean.values())
    data['homocedasticity'] = int(p_value < alpha)
    
    data.update(evaluate_test(data))
    
    return data

@route('/binomialsign', method=["POST", "OPTIONS"])
@route('/binomialsign/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def binomialsign(alpha=0.05):
    values = clean_missing_values(request.json)
    statistic, p_value = npt.binomial_sign_test(values.values()[0], values.values()[1])
    result = int(p_value<alpha)
    return {"result" : result, "statistic" : statistic, "p_value" : p_value}

@route('/wilcoxon', method=["POST", "OPTIONS"])
@route('/wilcoxon/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def wilcoxon(alpha=0.05):
    values = clean_missing_values(request.json)
    statistic, p_value = st.wilcoxon(values.values()[0], values.values()[1])
    result = int(p_value<alpha)
    return {"result" : result, "statistic" : statistic, "p_value" : p_value}
    
	
@route('/mannwhitneyu', method=["POST", "OPTIONS"])
@route('/mannwhitneyu/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def mannwhitneyu(alpha=0.05):
    values = clean_missing_values(request.json, delete_row=False)
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

@route('/friedman', method=["POST", "OPTIONS"])
@route('/friedman/<alpha:float>', method=["POST", "OPTIONS"])
@route('/friedman/<post_hoc>', method=["POST", "OPTIONS"])
@route('/friedman/<post_hoc>/<control>', method=["POST", "OPTIONS"])
@route('/friedman/<post_hoc>/<alpha:float>', method=["POST", "OPTIONS"])
@route('/friedman/<post_hoc>/<control>/<alpha:float>', method=["POST", "OPTIONS"])
@headers
@ranking
def friedman(alpha=0.05, post_hoc="bonferroni_dunn_test", control=None):
    values = clean_missing_values(request.json)
    statistic, p_value, rankings, ranking_cmp = npt.friedman_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    if post_hoc.split('_')[-1] == "test":
        comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks, control)
    else:
        comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values
    

@route('/friedman-aligned-ranks', method=["POST", "OPTIONS"])
@route('/friedman-aligned-ranks/<alpha:float>', method=["POST", "OPTIONS"])
@route('/friedman-aligned-ranks/<post_hoc>', method=["POST", "OPTIONS"])
@route('/friedman-aligned-ranks/<post_hoc>/<control>', method=["POST", "OPTIONS"])
@route('/friedman-aligned-ranks/<post_hoc>/<alpha:float>', method=["POST", "OPTIONS"])
@route('/friedman-aligned-ranks/<post_hoc>/<control>/<alpha:float>', method=["POST", "OPTIONS"])
@headers
@ranking
def friedman_aligned_ranks(alpha=0.05, post_hoc="bonferroni_dunn_test", control=None):
    values = clean_missing_values(request.json)
    statistic, p_value, rankings, ranking_cmp = npt.friedman_aligned_ranks_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    if post_hoc.split('_')[-1] == "test":
        comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks, control)
    else:
        comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values
    
@route('/quade', method=["POST", "OPTIONS"])
@route('/quade/<alpha:float>', method=["POST", "OPTIONS"])
@route('/quade/<post_hoc>', method=["POST", "OPTIONS"])
@route('/quade/<post_hoc>/<control>', method=["POST", "OPTIONS"])
@route('/quade/<post_hoc>/<alpha:float>', method=["POST", "OPTIONS"])
@route('/quade/<post_hoc>/<control>/<alpha:float>', method=["POST", "OPTIONS"])
@headers
@ranking
def quade(alpha=0.05, post_hoc="bonferroni_dunn_test", control=None):
    values = clean_missing_values(request.json)
    statistic, p_value, rankings, ranking_cmp = npt.quade_test(*values.values())
    rankings, names = map(list, zip(*sorted(zip(rankings, values.keys()), key=lambda t: t[0])))
    ranks = {key: ranking_cmp[i] for i,key in enumerate(values.keys())}
    if post_hoc.split('_')[-1] == "test":
        comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks, control)
    else:
        comparisons, z_values, _, adj_p_values = getattr(npt, post_hoc)(ranks)
    return statistic, p_value, rankings, names, comparisons, z_values, adj_p_values


@route('/shapiro', method=["POST", "OPTIONS"])
@route('/shapiro/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def shapiro(alpha=0.05):
    values = clean_missing_values(request.json, delete_row=False)
    statistics, p_values = map(list, zip(*[st.shapiro(v) for v in values.values()]))
    result = [int(p_value < alpha) for p_value in p_values]
    return {"statistic": statistics, "p_value": p_values, "result": result}
    
@route('/kolmogorov', method=["POST", "OPTIONS"])
@route('/kolmogorov/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def kolmogorov(alpha=0.05):
    values = clean_missing_values(request.json, delete_row=False)
    statistics, p_values = map(list, zip(*[st.kstest(v, 'norm') for v in values.values()]))
    result = [int(p_value < alpha) for p_value in p_values]
    return {"statistic": statistics, "p_value": p_values, "result": result}
    
@route('/agostino', method=["POST", "OPTIONS"])
@route('/agostino/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def agostino(alpha=0.05):
    values = clean_missing_values(request.json, delete_row=False)
    statistics, p_values = map(list, zip(*[st.normaltest(v) for v in values.values()]))
    result = [int(p_value < alpha) for p_value in p_values]
    return {"statistic": statistics, "p_value": p_values, "result": result}

@route('/levene', method=["POST", "OPTIONS"])
@route('/levene/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def levene(alpha=0.05):
    values = clean_missing_values(request.json, delete_row=False)
    statistic, p_value = st.levene(*values.values())
    result = int(p_value < alpha)
    return {"statistic": statistic, "p_value": p_value, "result": result}


@route('/ttest', method=["POST", "OPTIONS"])
@route('/ttest/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def ttest(alpha=0.05):
    values = clean_missing_values(request.json)
    statistic, p_value = st.ttest_rel(values.values()[0], values.values()[1])
    result = int(p_value < alpha)
    return {"statistic": statistic.tolist(), "p_value": p_value, "result": result}
    
@route('/ttest-ind', method=["POST", "OPTIONS"])
@route('/ttest-ind/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def ttest_ind(alpha=0.05):
    values = clean_missing_values(request.json)
    statistic, p_value = st.ttest_ind(values.values()[0], values.values()[1])
    result = int(p_value < alpha)
    return {"statistic": statistic.tolist(), "p_value": p_value, "result": result}


@route('/anova', method=["POST", "OPTIONS"])
@route('/anova/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def anova(alpha=0.05):
    values = clean_missing_values(request.json)
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
        
@route('/anova-within', method=["POST", "OPTIONS"])
@route('/anova-within/<alpha:float>', method=["POST", "OPTIONS"])
@headers
def anova(alpha=0.05):
    values = clean_missing_values(request.json)
    statistic, p_value, pivots = pt.anova_within_test(*values.values())
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

