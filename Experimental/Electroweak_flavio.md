# This file contains all the electroweak experimental measurements from flavio

LEP-SLD:
  experiment: LEP, SLD
  inspire: Janot:2019oyi
  description: Table B.13 of arXiv:1912.02067
  values:
    GammaZ: 2.4955 ± 0.0023
    sigma_had: 1065.14 ± 0.84 e-7 # 41.4742 ± 0.0326 nb
    R_e: 20.8038 ± 0.0497
    R_mu: 20.7842 ± 0.0335
    R_tau: 20.7644 ± 0.0448
    AFB(Z->ee): 0.0145 ± 0.0025
    AFB(Z->mumu): 0.0169 ± 0.0013
    AFB(Z->tautau): 0.0188 ± 0.0017
  correlation: [[1.0000, -0.3238, -0.0110, 0.0079, 0.0059, 0.0071, 0.0020, 0.0013],
                [1.0000, 0.1134, 0.1387, 0.0984, 0.0015, 0.0035, 0.0018],
                [1.0000, 0.0694, 0.0464, -0.3704, 0.0197, 0.0132],
                [1.0000, 0.0696, 0.0013, 0.0121, -0.0030],
                [1.0000, 0.0029, 0.0012, 0.0093],
                [1.0000, -0.0242, -0.0202],
                [1.0000, 0.0464],
                [1.0000]]

LEP-SLD cb:
  experiment: LEP, SLD
  inspire: ALEPH:2005ab
  description: Tables 5.10 and 5.11 of arXiv:hep-ex/0509008
  values:
    R_b: 0.21629 ± 0.00066
    R_c: 0.1721 ± 0.0030
    AFB(Z->bb): 0.0992 ± 0.0016
    AFB(Z->cc): 0.0707 ± 0.0035
    A(Z->bb): 0.923 ± 0.020
    A(Z->cc): 0.670 ± 0.027
  correlation: [[1.00, -0.18, -0.10, 0.07, -0.08, 0.04],
                [1.00, 0.04, -0.06, 0.04, -0.06],
                [1.00, 0.15, 0.06, 0.01],
                [1.00, -0.02, 0.04],
                [1.00, 0.11],
                [1.00]]

A_s SLD:
  experiment: SLD
  inspire: Abe:2000uc
  values:
    A(Z->ss): 0.895 ± 0.066 ± 0.062


PDG Rc:
  experiment: PDG
  inspire: Tanabashi:2018oca
  values:
    R_uc: 0.166 ± 0.009
    R(W->cX): 0.49 ± 0.04

A_l LEP:
  experiment: LEP
  inspire: ALEPH:2005ab
  description: >
    Leptonic asymmetry parameters extracted from tau polarization measurements.
    Equations (4.9) and (4.10) of arXiv:hep-ex/0509008
  values:
    A(Z->ee): 0.1498±0.0049
    A(Z->tautau): 0.1439±0.0043

A_l SLD:
  experiment: SLD
  inspire: ALEPH:2005ab
  description: Table 3.6 of arXiv:hep-ex/0509008
  values:
    A(Z->ee): 0.1516 ± 0.0021
    A(Z->mumu): 0.142 ± 0.015
    A(Z->tautau): 0.136 ± 0.015
  correlation: [[1.0, 0.038, 0.033],
                [1.0, 0.007],
                [1.0]]

LEP Z leptonic decay:
  experiment: LEP
  inspire: ALEPH:2005ab
  description: Table 7.1
  values:
    Gamma(Z->nunu): 165.8 +- 0.8 e-3 # Width per neutrino species without assuming LFU
    Gamma(Z->ee): 83.92 +- 0.12 e-3
    Gamma(Z->mumu): 83.99 +- 0.18 e-3
    Gamma(Z->tautau): 84.08 +- 0.22 e-3

ATLAS W->taunu 2020:
  experiment: ATLAS
  inspire: Aad:2020ayz
  values:
    Rtaumu(W->lnu): 0.992 ± 0.007 ± 0.011

LHCb W->lnu 2016:
  experiment: LHCb
  inspire: Aaij:2016qqz
  description: The inverse of the ratio quoted in the abstact
  values:
    Rmue(W->lnu): 0.980 ± 0.002 ± 0.018

D0 W->taunu 1999:
  experiment: D0
  inspire: Abbott:1999pk
  description: The square of the ratio quoted in the abstact (cf. eq. (1))
  values:
    Rtaue(W->lnu): 0.960 ± 0.062

m_W Tevatron:
  experiment: CDF, D0
  inspire: Aaltonen:2013iut
  values:
    m_W: 80.387 ± 0.016

m_W ATLAS 2017:
  experiment: CDF, D0
  inspire: Aaboud:2017svj
  values:
    m_W: 80.3695 ± 0.0185

DELPHI Z LFV:
  experiment: DELPHI
  inspire: Abreu:1996mj
  values:
    # Low background: assuming zero expected and observed counts for simplicity
    BR(Z->mutau):
      distribution: gamma_upper_limit
      limit: 1.2e-5
      confidence_level: 0.95
      counts_total: 0
      counts_background: 0
    BR(Z->etau):
      distribution: gamma_upper_limit
      limit: 2.2e-5
      confidence_level: 0.95
      counts_total: 0
      counts_background: 0
    BR(Z->emu):
      distribution: gamma_upper_limit
      limit: 0.25e-5
      confidence_level: 0.95
      counts_total: 0
      counts_background: 0

ATLAS Z->taul 2020:
  experiment: ATLAS
  inspire: Aad:2020gkd
  values:
    # High background: assuming half-Gaussian for simplicity
    BR(Z->etau): < 8.1e-6 @ 95% CL
    BR(Z->mutau): < 9.5e-6 @ 95% CL

ATLAS Z LFV 2014:
  experiment: ATLAS
  inspire: Aad:2014bca
  values:
    # High background: assuming half-Gaussian for simplicity
    BR(Z->emu): < 7.5e-7 @ 95% CL

OPAL Z LFV:
  experiment: OPAL
  inspire: Akers:1995gz
  values:
  # Low background: assuming zero expected and observed counts for simplicity
    BR(Z->emu):
      distribution: gamma_upper_limit
      limit: 1.7e-6
      confidence_level: 0.95
      counts_total: 0
      counts_background: 0
    BR(Z->etau):
      distribution: gamma_upper_limit
      limit: 9.8e-6
      confidence_level: 0.95
      counts_total: 0
      counts_background: 0
    BR(Z->mutau):
      distribution: gamma_upper_limit
      limit: 17.0e-6
      confidence_level: 0.95
      counts_total: 0
      counts_background: 0

LEP W->leptons:
  experiment: LEP
  inspire: Schael:2013ita
  description: Table 5.5
  values:
    BR(W->enu): 10.71 ± 0.16 e-2
    BR(W->munu): 10.63 ± 0.15 e-2
    BR(W->taunu): 11.38 ± 0.21 e-2

LEP W->leptons ratios:
  experiment: LEP
  inspire: Schael:2013ita
  description: Equations (5.2)-(5.4)
  values:
    Rmue(W->lnu): 0.993 +- 0.019
    Rtaue(W->lnu): 1.063 +- 0.027
    Rtaumu(W->lnu): 1.070 +- 0.026

PDG W width:
  inspire: Patrignani:2016xqp
  values:
    GammaW: 2.085 ± 0.042

