Tests no Paramétricos
=====================

Cuando los datos proporcionados **no** cumplen los criterios paramétricos de (independencia, normalidad y homocedasticidad) podemos realizar contrastes sobre datos con los siguientes tests no paramétricos:

* :mod:`Test de Wilcoxon <tests_no_parametricos.wilcoxon_test>`
* :mod:`Test de Friedman <tests_no_parametricos.friedman_test>`
* :mod:`Test de Iman-Davenport <tests_no_parametricos.iman_davenport_test>`
* :mod:`Test de los Rangos Alineados de Friedman <tests_no_parametricos.friedman_rangos_alineados_test>`
* :mod:`Test de Quade <tests_no_parametricos.quade_test>`
* :mod:`Test de Bonferroni-Dunn <tests_no_parametricos.bonferroni_dunn_test>`
* :mod:`Test de Holm <tests_no_parametricos.holm_test>`
* :mod:`Test de Hochberg <tests_no_parametricos.hochberg_test>`
* :mod:`Test de Li <tests_no_parametricos.li_test>`
* :mod:`Test de Finner <tests_no_parametricos.finner_test>`
* :mod:`Multitest de Bonferroni-Dunn <tests_no_parametricos.nemenyi_multitest>`
* :mod:`Multitest de Holm <tests_no_parametricos.holm_multitest>`
* :mod:`Multitest de Hochberg <tests_no_parametricos.hochberg_multitest>`
* :mod:`Multitest de Finner <tests_no_parametricos.finner_multitest>`
* :mod:`Multitest de Shaffer <tests_no_parametricos.shaffer_multitest>`

Funciones auxialiares:

* :mod:`Datos comunes tests POST-HOC <tests_no_parametricos.datos_comunes_tests>`
* :mod:`Datos comunes multitests POST-HOC <tests_no_parametricos.datos_comunes_multitests>`
* :mod:`S para Shaffer <tests_no_parametricos.S>`

.. automodule:: tests_no_parametricos
   :members: wilcoxon_test, friedman_test, iman_davenport_test, friedman_rangos_alineados_test, quade_test, bonferroni_dunn_test, holm_test, hochberg_test, li_test, finner_test, nemenyi_multitest, holm_multitest, hochberg_multitest, finner_multitest, shaffer_multitest, datos_comunes_tests, datos_comunes_multitests, S
