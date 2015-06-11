# -*- coding: utf-8 -*-
"""
Created on Tue Api 22 16:05:31 2014

@author: Adrián
"""

import networkx as nx

color = "#adadad"
fillcolor = "#ebebeb"

G = nx.DiGraph()

# Nodes
G.add_node("parametric_conditions", label="Normality AND\nHomocedasticity?", shape="diamond")
G.add_node("parametric", label="Parametric test")
G.add_node("groups_parametric", label="Number of\ngroups (k)?", shape="diamond")
G.add_node("paired_ttest", label="Paired\nsamples?", shape="diamond")
G.add_node("ttest_rel", label="t-test\npaired samples", shape="box", style="rounded")
G.add_node("ttest_ind", label="t-test\nunpaired samples", shape="box", style="rounded")
G.add_node("paired_anova", label="Paired\nsamples?", shape="diamond")
G.add_node("anova", label="ANOVA\nbetween cases", shape="box", style="rounded")
G.add_node("anova_within", label="ANOVA\nwithin cases", shape="box", style="rounded")
G.add_node("nonparametric", label="Non Parametric test")
G.add_node("groups_nonparametric", label="Number of\ngroups (k)?", shape="diamond")
G.add_node("paired_wilcoxon", label="Paired\nsamples?", shape="diamond")
G.add_node("wilcoxon_test", label="Wilcoxon", shape="box", style="rounded")
G.add_node("mannwhitneyu_test", label="Mann Whitney U", shape="box", style="rounded")
G.add_node("sample_ranking", label="Sample\nsize (n)?", shape="diamond")
G.add_node("friedman_test", label="Friedman", shape="box", style="rounded")
G.add_node("aligned_ranks_test", label="Aligned Ranks", shape="box", style="rounded")
for node in G.nodes(): G.node[node].update({'color': color, 'style': G.node[node].get('style', "")+",filled", 'fillcolor': 'white'})

# Edges
G.add_edge("parametric_conditions", "parametric", label="yes")
G.add_edge("parametric_conditions", "nonparametric", label="no")
G.add_edge("parametric", "groups_parametric")
G.add_edge("groups_parametric", "paired_ttest", label="k = 2")
G.add_edge("paired_ttest", "ttest_rel", label="paired")
G.add_edge("paired_ttest", "ttest_ind", label="unpaired")
G.add_edge("groups_parametric", "paired_anova", label="k > 2")
G.add_edge("paired_anova", "anova_within", label="paired")
G.add_edge("paired_anova", "anova", label="unpaired")
G.add_edge("nonparametric", "groups_nonparametric")
G.add_edge("groups_nonparametric", "paired_wilcoxon", label="k = 2")
G.add_edge("paired_wilcoxon", "wilcoxon_test", label="paired")
G.add_edge("paired_wilcoxon", "mannwhitneyu_test", label="unpaired")
G.add_edge("groups_nonparametric", "sample_ranking", label="k > 2")
G.add_edge("sample_ranking", "friedman_test", label="k > 4\n and n >= 2k")
G.add_edge("sample_ranking", "aligned_ranks_test", label="k < 5\nor n < 2k")
for edge in G.edges(): G.edge[edge[0]][edge[1]].update({'label': " " + G.edge[edge[0]][edge[1]].get('label', "") + " ", 'style': G.edge[edge[0]][edge[1]].get('style', "")+",filled", 'fillcolor': 'white'})

def evaluate_test(data):
    gl = G.copy()
    selection = []
    # Tree logic
    if data['normality'] and data['homocedasticity']:
        selection.extend([
            gl.node["parametric_conditions"],
            gl.edge["parametric_conditions"]["parametric"],
            gl.node["parametric"],
            gl.edge["parametric"]["groups_parametric"],
            gl.node["groups_parametric"]
        ])
        
        if data['k'] > 2:
            selection.extend([
                gl.edge["groups_parametric"]["anova"],
                gl.node["anova"]
            ])
            test = 'anova'
        else:
            selection.extend([
                gl.edge["groups_parametric"]["paired_ttest"],
                gl.node["paired_ttest"]
            ])
            if data['paired']:
                selection.extend([
                    gl.edge["paired_ttest"]["ttest_rel"],
                    gl.node["ttest_rel"]
                ])
                test = 'ttest'
            else:
                selection.extend([
                    gl.edge["paired_ttest"]["ttest_ind"],
                    gl.node["ttest_ind"]
                ])
                test = 'ttest_ind'
    else:
        selection.extend([
            gl.node["parametric_conditions"],
            gl.edge["parametric_conditions"]["nonparametric"],
            gl.node["nonparametric"],
            gl.edge["nonparametric"]["groups_nonparametric"],
            gl.node["groups_nonparametric"]
        ])
        if data['k'] > 2:
            selection.extend([
                gl.edge["groups_nonparametric"]["sample_ranking"],
                gl.node["sample_ranking"]
            ])
            
            if data['k'] < 5 or data['n'] < 2*data['k']:
                selection.extend([
                    gl.edge["sample_ranking"]["aligned_ranks_test"],
                    gl.node["aligned_ranks_test"]
                ])
                test = 'aligned_ranks'
            else:
                selection.extend([
                    gl.edge["sample_ranking"]["friedman_test"],
                    gl.node["friedman_test"]
                ])
                test = 'friedman'
        else:
            selection.extend([
                gl.edge["groups_nonparametric"]["paired_wilcoxon"],
                gl.node["paired_wilcoxon"]
            ])
            if data['paired']:
                selection.extend([
                    gl.edge["paired_wilcoxon"]["wilcoxon_test"],
                    gl.node["wilcoxon_test"]
                ])
                test = 'wilcoxon'
            else:
                selection.extend([
                    gl.edge["paired_wilcoxon"]["mannwhitneyu_test"],
                    gl.node["mannwhitneyu_test"]
                ])
                test = 'mannwhitneyu'
           
    for v in selection: v.update({"fillcolor": fillcolor})
        
    return {'test': test, 'graph': str(nx.to_agraph(gl))}

    
def clean_missing_values(values, delete_row=True):
    n = len(values.values()[0])
    names = values.keys()
    p = len(names)
    if delete_row:
        for i in range(n):
            for j in range(p):
                try:
                    float(values[names[j]][i])
                except:
                    for k in names:
                        values[k][i] = float('nan')
                    break
    for k in names:
        values[k] = [v for v in values[k] if str(v) != 'nan']
        
    return values
                
