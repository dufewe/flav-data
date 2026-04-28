# This file contains all the lepton experimental measurements from flavio

Sindrum II Ti 1993:
  experiment: SINDRUM II
  inspire: Dohmen:1993mp
  url: https://doi.org/10.1016/0370-2693(93)91383-X
  values:
    CR(mu->e, Ti): < 4.3e-12 @ 90% CL

Sindrum II Au 2006:
  experiment: SINDRUM II
  inspire: Bertl:2006up
  url: https://link.springer.com/article/10.1140%2Fepjc%2Fs2006-02582-x
  values:
    CR(mu->e, Au): < 7e-13 @ 90% CL

PDG 2017 tau:
  experiment: PDG
  inspire: Patrignani:2016xqp
  values:
    BR(tau->mununu): 17.39(4)e-2
    BR(tau->enunu):  17.82(4)e-2
    BR(tau->pinu):   10.82(5)e-2
    BR(tau->Knu):    6.96(10)e-3

PDG 2017 tau LFV:
  experiment: PDG
  inspire: Patrignani:2016xqp
  values:
    BR(tau->egamma):  < 3.3e-8 @ 90% CL
    BR(tau->mugamma): < 4.4e-8 @ 90% CL
    BR(tau->rhoe):    < 1.8e-8 @ 90% CL
    BR(tau->rhomu):   < 1.2e-8 @ 90% CL
    BR(tau->phimu):   < 8.4e-8 @ 90% CL
    BR(tau->phie):    < 3.1e-8 @ 90% CL

Belle 2010 tau->lll:
  experiment: Belle
  inspire: Hayasaka:2010np
  values:
    BR(tau->eee):
        distribution: general_gamma_upper_limit
        limit: 2.7e-8
        confidence_level: 0.9
        counts_total: 0
        counts_background: 0.21
        background_std: 0.15
    BR(tau->mumumu):
        distribution: general_gamma_upper_limit
        limit: 2.1e-8
        confidence_level: 0.9
        counts_total: 0
        counts_background: 0.13
        background_std: 0.06
    BR(tau->emumu):
        distribution: general_gamma_upper_limit
        limit: 2.7e-8
        confidence_level: 0.9
        counts_total: 0
        counts_background: 0.10
        background_std: 0.04
    BR(tau->muee):
        distribution: general_gamma_upper_limit
        limit: 1.8e-8
        confidence_level: 0.9
        counts_total: 0
        counts_background: 0.04
        background_std: 0.04
    BR(tau->muemu):
        distribution: general_gamma_upper_limit
        limit: 1.7e-8
        confidence_level: 0.9
        counts_total: 0
        counts_background: 0.02
        background_std: 0.02
    BR(tau->emue):
        distribution: general_gamma_upper_limit
        limit: 1.5e-8
        confidence_level: 0.9
        counts_total: 0
        counts_background: 0.01
        background_std: 0.01

PDG 2017 mu LFV:
  experiment: PDG
  inspire: Patrignani:2016xqp
  values:
    BR(mu->egamma): < 4.2e-13 @ 90% CL
    BR(mu->eee):    < 1.0e-12 @ 90% CL

CHARM-II neutrino trident:
  experiment: CHARM-II
  inspire: Geiregat:1990gz
  values:
    R_trident: 1.58 ± 0.57

CCFR neutrino trident:
  experiment: CCFR
  inspire: Mishra:1991bv
  values:
    R_trident: 0.82 ± 0.28

PDG g-2 e tau:
  experiment: PDG
  inspire: Tanabashi:2018oca
  values:
    a_e: 1159652180.91(26) e-12
    a_tau: -0.018 ± 0.017

PDG g-2 mu:
  experiment: PDG
  inspire: Tanabashi:2018oca
  values:
    a_mu: 11659208.9 ± 5.4 ± 3.3 e-10

FNAL g-2:
  experiment: Muon g-2
  values:
    a_mu: 116592040(54) e-11

FNAL g-2 combination:
  experiment: Muon g-2
  values:
    a_mu: 116592061(41) e-11

LEP ee->WW:
  experiment: LEP
  inspire: Schael:2013ita
  description: >
    Combined LEP result from table E.5 with the correlation matrix
    from table E.3.
  values:
    - name: R(ee->WW)
      E: 182.7
      value: 1.036 ± 0.022
    - name: R(ee->WW)
      E: 188.6
      value: 0.988 ± 0.013
    - name: R(ee->WW)
      E: 191.6
      value: 0.994 ± 0.028
    - name: R(ee->WW)
      E: 195.5
      value: 1.011 ± 0.018
    - name: R(ee->WW)
      E: 199.5
      value: 0.987 ± 0.017
    - name: R(ee->WW)
      E: 201.6
      value: 0.997 ± 0.024
    - name: R(ee->WW)
      E: 204.9
      value: 0.984 ± 0.017
    - name: R(ee->WW)
      E: 206.6
      value: 1.007 ± 0.014
  correlation:
    [[1.000, 0.145, 0.065, 0.104, 0.105, 0.076, 0.104, 0.130],
     [0.145, 1.000, 0.093, 0.148, 0.149, 0.108, 0.148, 0.186],
     [0.065, 0.093, 1.000, 0.066, 0.067, 0.048, 0.066, 0.083],
     [0.104, 0.148, 0.066, 1.000, 0.107, 0.077, 0.106, 0.133],
     [0.105, 0.149, 0.067, 0.107, 1.000, 0.078, 0.106, 0.134],
     [0.076, 0.108, 0.048, 0.077, 0.078, 1.000, 0.077, 0.097],
     [0.104, 0.148, 0.066, 0.106, 0.106, 0.077, 1.000, 0.132],
     [0.130, 0.186, 0.083, 0.133, 0.134, 0.097, 0.132, 1.000]]

LEP ee->WW angular:
  experiment: LEP
  inspire: Schael:2013ita
  description: >
    Combined LEP result from table XX. Correlations are neglected.
  values:
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: -1.0
      thetamax: -0.8
      value: 0.502 ± 0.114
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: -0.8
      thetamax: -0.6
      value: 0.705 ± 0.129
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: -0.6
      thetamax: -0.4
      value: 0.868 ± 0.143
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: -0.4
      thetamax: -0.2
      value: 1.281 ± 0.203
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: -0.2
      thetamax: 0.0
      value: 1.529 ± 0.195
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: 0.0
      thetamax: 0.2
      value: 2.15 ± 0.244
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: 0.2
      thetamax: 0.4
      value: 2.583 ± 0.27
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: 0.4
      thetamax: 0.6
      value: 2.602 ± 0.254
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: 0.6
      thetamax: 0.8
      value: 4.245 ± 0.367
    - name: <dR/dtheta>(ee->WW)
      E: 182.66
      thetamin: 0.8
      thetamax: 1.0
      value: 5.372 ± 0.419
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: -1.0
      thetamax: -0.8
      value: 0.718 ± 0.074
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: -0.8
      thetamax: -0.6
      value: 0.856 ± 0.079
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: -0.6
      thetamax: -0.4
      value: 1.009 ± 0.086
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: -0.4
      thetamax: -0.2
      value: 1.101 ± 0.088
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: -0.2
      thetamax: 0.0
      value: 1.277 ± 0.094
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: 0.0
      thetamax: 0.2
      value: 1.801 ± 0.123
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: 0.2
      thetamax: 0.4
      value: 2.215 ± 0.14
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: 0.4
      thetamax: 0.6
      value: 2.823 ± 0.151
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: 0.6
      thetamax: 0.8
      value: 4.001 ± 0.179
    - name: <dR/dtheta>(ee->WW)
      E: 189.09
      thetamin: 0.8
      thetamax: 1.0
      value: 5.762 ± 0.223
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: -1.0
      thetamax: -0.8
      value: 0.679 ± 0.079
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: -0.8
      thetamax: -0.6
      value: 0.635 ± 0.065
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: -0.6
      thetamax: -0.4
      value: 0.991 ± 0.084
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: -0.4
      thetamax: -0.2
      value: 1.087 ± 0.088
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: -0.2
      thetamax: 0.0
      value: 1.275 ± 0.096
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: 0.0
      thetamax: 0.2
      value: 1.71 ± 0.116
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: 0.2
      thetamax: 0.4
      value: 2.072 ± 0.126
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: 0.4
      thetamax: 0.6
      value: 2.866 ± 0.158
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: 0.6
      thetamax: 0.8
      value: 4.1 ± 0.185
    - name: <dR/dtheta>(ee->WW)
      E: 198.38
      thetamin: 0.8
      thetamax: 1.0
      value: 6.535 ± 0.236
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: -1.0
      thetamax: -0.8
      value: 0.495 ± 0.058
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: -0.8
      thetamax: -0.6
      value: 0.602 ± 0.066
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: -0.6
      thetamax: -0.4
      value: 0.653 ± 0.069
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: -0.4
      thetamax: -0.2
      value: 1.057 ± 0.094
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: -0.2
      thetamax: 0.0
      value: 1.24 ± 0.093
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: 0.0
      thetamax: 0.2
      value: 1.707 ± 0.115
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: 0.2
      thetamax: 0.4
      value: 2.294 ± 0.14
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: 0.4
      thetamax: 0.6
      value: 2.797 ± 0.143
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: 0.6
      thetamax: 0.8
      value: 4.481 ± 0.187
    - name: <dR/dtheta>(ee->WW)
      E: 205.92
      thetamin: 0.8
      thetamax: 1.0
      value: 7.584 ± 0.26