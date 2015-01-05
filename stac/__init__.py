from .tests_parametricos import anova_test, bonferroni_test
from .nonparametric_tests import *

__all__ = ['anova_test',
           'bonferroni_test',
           'wilcoxon_test',
           'test_ranking',
           'friedman_test',
           'iman_davenport_test',
           'friedman_rangos_alineados_test',
           'quade_test',
           'bonferroni_dunn_test',
           'holm_test',
           'hochberg_test',
           'li_test',
           'finner_test',
           'nemenyi_multitest',
           'holm_multitest',
           'hochberg_multitest',
           'finner_multitest',
           'shaffer_multitest']
