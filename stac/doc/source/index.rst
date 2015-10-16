.. STAC documentation master file, created by
   sphinx-quickstart on Thu Jan 29 13:09:17 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

STAC Python Library
============================
Through this library you can verify the results obtained from the learning algorithms applying the statistic tests to the experiments, which, among other uses, support the decision making process (the election of the most suitable algorithm, for example).
   
Normality tests
============================
.. currentmodule:: scipy.stats
.. autosummary::
    shapiro
    normaltest
    kstest
    
Homoscedasticity tests
============================
.. currentmodule:: scipy.stats
.. autosummary::
    levene

Parametric two group comparison tests
============================
.. currentmodule:: scipy.stats
.. autosummary::
    ttest_ind
    ttest_rel
    
Non-parametric two group comparison tests
============================
.. currentmodule:: scipy.stats
.. autosummary::
    wilcoxon
    mannwhitneyu

.. currentmodule:: stac.nonparametric_tests
.. autosummary::
    binomial_sign_test
    
Parametric multiple comparison tests
============================
ANOVA tests
-------------------
.. currentmodule:: stac.parametric_tests
.. autosummary::
    anova_test
    anova_within_test
    
Post-hoc tests
-------------------
.. currentmodule:: stac.parametric_tests
.. autosummary::
    bonferroni_test


Non-Parametric multiple comparison tests
============================
Ranking tests
-------------------
.. currentmodule:: stac.nonparametric_tests
.. autosummary::
    friedman_test
    friedman_aligned_ranks_test
    quade_test
    
Post-hoc 1 vs all tests
-------------------
.. currentmodule:: stac.nonparametric_tests
.. autosummary::
    bonferroni_dunn_test
    holm_test
    finner_test
    hochberg_test
    li_test
    
Post-hoc all vs all tests
-------------------
.. currentmodule:: stac.nonparametric_tests
.. autosummary::
    nemenyi_multitest
    holm_multitest
    finner_multitest
    hochberg_multitest
    shaffer_multitest

