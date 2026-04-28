# This file contains all the nuclear experimental measurements from flavio

Ft(0+) Hardy/Towner 2014:
  experiment: various
  inspire: Hardy:2014qxa
  values:
    Ft(10C): 4.6763 ± 0.0068 1e+27  # 3078.0 ± 4.5 s
    Ft(14O): 4.6663 ± 0.0049 1e+27  # 3071.4 ± 3.2 s
    Ft(22Mg): 4.6762 ± 0.0111 1e+27  # 3077.9 ± 7.3 s
    Ft(26mAl): 4.6686 ± 0.0015 1e+27  # 3072.9 ± 1.0 s
    Ft(34Cl): 4.6652 ± 0.0027 1e+27  # 3070.7 ± 1.8 s
    Ft(34Ar): 4.6575 ± 0.0128 1e+27  # 3065.6 ± 8.4 s
    Ft(38mK): 4.6666 ± 0.003 1e+27  # 3071.6 ± 2.0 s
    Ft(38Ca): 4.6739 ± 0.0109 1e+27  # 3076.4 ± 7.2 s
    Ft(42Sc): 4.6678 ± 0.0035 1e+27  # 3072.4 ± 2.3 s
    Ft(46V): 4.6704 ± 0.003 1e+27  # 3074.1 ± 2.0 s
    Ft(50Mn): 4.666 ± 0.0032 1e+27  # 3071.2 ± 2.1 s
    Ft(54Co): 4.6638 ± 0.004 1e+27  # 3069.8 ± 2.6 s
    Ft(62Ga): 4.6664 ± 0.0102 1e+27  # 3071.5 ± 6.7 s
    Ft(74Rb): 4.6733 ± 0.0167 1e+27  # 3076.0 ± 11.0 s

Ft(0+) Hardy/Towner 2020:
  experiment: various
  inspire: Hardy:2020qwl
  values:
    Ft(10C): 4.6728 ± 0.0067 1e+27  # 3075.7 ± 4.4 s
    Ft(14O): 4.6645 ± 0.0029 1e+27  # 3070.2 ± 1.9 s
    Ft(22Mg): 4.6736 ± 0.0106 1e+27  # 3076.2 ± 7.0 s
    Ft(26mAl): 4.6678 ± 0.0017 1e+27  # 3072.4 ± 1.1 s
    Ft(34Cl): 4.6666 ± 0.0027 1e+27  # 3071.6 ± 1.8 s
    Ft(34Ar): 4.6719 ± 0.0047 1e+27  # 3075.1 ± 3.1 s
    Ft(38mK): 4.6686 ± 0.003 1e+27  # 3072.9 ± 2.0 s
    Ft(38Ca): 4.6760 ± 0.0094 1e+27  # 3077.8 ± 6.2 s
    Ft(42Sc): 4.6667 ± 0.0030 1e+27  # 3071.7 ± 2.0 s
    Ft(46V): 4.6707 ± 0.003 1e+27  # 3074.3 ± 2.0 s
    Ft(50Mn): 4.6658 ± 0.0024 1e+27  # 3071.1 ± 1.6 s
    Ft(54Co): 4.6648 ± 0.0036 1e+27  # 3070.4 ± 2.5 s
    Ft(62Ga): 4.6678 ± 0.0102 1e+27  # 3072.4 ± 6.7 s
    Ft(74Rb): 4.6748 ± 0.0167 1e+27  # 3077.0 ± 11.0 s

Neutron averages GACS 2018 1:
  inspire: Gonzalez-Alonso:2018omy
  description: Averages in table 7 of the paper by Gonzalez-Alonso et al.
  values:
    - name: tau_n
      me_E: 0.655
      value: 1.3366(12) 1e+27 # 879.75(76) s
    - name: Btilde_n
      me_E: 0.591
      value: 0.9805(30)

Neutron A parameter PERKEO II 2012:
  inspire: Mund:2012fq
  values:
    - name: Atilde_n
      me_E: 0.559
      value: -0.11926(31)(42)

Neutron A parameter PERKEO III 2018:
  inspire: Markisch:2018ndu
  values:
    - name: Atilde_n
      me_E: 0.559
      value: -0.11985(17)(12)

Neutron A parameter UCNA 2017:
  inspire: Brown:2017mhw
  values:
    - name: Atilde_n
      me_E: 0.586
      value: -0.12015(34)(63)

Neutron averages GACS 2018 2:
  inspire: Gonzalez-Alonso:2018omy
  description: Averages in table 7 of the paper by Gonzalez-Alonso et al.
  values:
    a_n: -0.1034(37)
    D_n: -0.00012(20)

aCORN atilde_n 2017:
  experiment: aCORN
  inspire: Darius:2017arh
  values:
    - name: atilde_n
      me_E: 0.695
      value: -0.1090(41)

nTRV R_n 2011:
  experiment: nTRV
  inspire: Kozela:2011mc
  values:
    R_n: 0.004(13)

Mostovoi lambda_n 2001:
  experiment: Mostovoi et al.
  inspire: Mostovoi:2001ye
  values:
    - name: lambdaAB_n
      me_E: 0.581
      value: -1.2686(47)
    
ATLAS pp->ee 2016:
  experiment: ATLAS
  inspire: ATLAS:2017fih
  values:
  - name: R_13(pp->ee)
    qmax: 85.54876
    qmin: 80.0
    value:
      background_std: 69401.5708
      counts_background: 10974.128946591254
      counts_total: 1176847.0
      distribution: general_gamma_counting_process
      scale_factor: 9.079216742641075e-07
  - name: R_13(pp->ee)
    qmax: 91.48239
    qmin: 85.54876
    value:
      background_std: 362245.73273
      counts_background: 20197.544340420172
      counts_total: 6608874.0
      distribution: general_gamma_counting_process
      scale_factor: 1.578288016852957e-07
  - name: R_13(pp->ee)
    qmax: 97.82756
    qmin: 91.48239
    value:
      background_std: 236917.40941
      counts_background: 14758.751538861532
      counts_total: 3928394.0
      distribution: general_gamma_counting_process
      scale_factor: 2.6643422884378354e-07
  - name: R_13(pp->ee)
    qmax: 104.61284
    qmin: 97.82756
    value:
      background_std: 25907.27369
      counts_background: 8303.474996545438
      counts_total: 432217.0
      distribution: general_gamma_counting_process
      scale_factor: 2.433985942583826e-06
  - name: R_13(pp->ee)
    qmax: 111.86874
    qmin: 104.61284
    value:
      background_std: 8629.47379
      counts_background: 7744.303026077903
      counts_total: 162962.0
      distribution: general_gamma_counting_process
      scale_factor: 6.658077258351981e-06
  - name: R_13(pp->ee)
    qmax: 119.6279
    qmin: 111.86874
    value:
      background_std: 4855.99299
      counts_background: 7479.00056482295
      counts_total: 93773.0
      distribution: general_gamma_counting_process
      scale_factor: 1.2056724982029082e-05
  - name: R_13(pp->ee)
    qmax: 127.92524
    qmin: 119.6279
    value:
      background_std: 3290.32109
      counts_background: 7349.777298742665
      counts_total: 63446.0
      distribution: general_gamma_counting_process
      scale_factor: 1.806483692003574e-05
  - name: R_13(pp->ee)
    qmax: 136.79808
    qmin: 127.92524
    value:
      background_std: 2472.545
      counts_background: 7097.990404497162
      counts_total: 47190.0
      distribution: general_gamma_counting_process
      scale_factor: 2.529845178476055e-05
  - name: R_13(pp->ee)
    qmax: 146.28633
    qmin: 136.79808
    value:
      background_std: 1906.07197
      counts_background: 6619.998084113988
      counts_total: 36539.0
      distribution: general_gamma_counting_process
      scale_factor: 3.415359516648235e-05
  - name: R_13(pp->ee)
    qmax: 156.43268
    qmin: 146.28633
    value:
      background_std: 1531.96354
      counts_background: 6282.7489410602875
      counts_total: 29267.0
      distribution: general_gamma_counting_process
      scale_factor: 4.3779840768871884e-05
  - name: R_13(pp->ee)
    qmax: 167.28278
    qmin: 156.43268
    value:
      background_std: 1260.16032
      counts_background: 5859.656548202215
      counts_total: 23874.0
      distribution: general_gamma_counting_process
      scale_factor: 5.628054175473133e-05
  - name: R_13(pp->ee)
    qmax: 178.88544
    qmin: 167.28278
    value:
      background_std: 1052.39276
      counts_background: 5277.835442619564
      counts_total: 19689.0
      distribution: general_gamma_counting_process
      scale_factor: 7.028500277716987e-05
  - name: R_13(pp->ee)
    qmax: 191.29285
    qmin: 178.88544
    value:
      background_std: 883.33112
      counts_background: 4837.365635368392
      counts_total: 16548.0
      distribution: general_gamma_counting_process
      scale_factor: 8.65923086594022e-05
  - name: R_13(pp->ee)
    qmax: 204.56084
    qmin: 191.29285
    value:
      background_std: 742.04396
      counts_background: 4281.768795274276
      counts_total: 13671.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001081634337384418
  - name: R_13(pp->ee)
    qmax: 218.74908
    qmin: 204.56084
    value:
      background_std: 627.82514
      counts_background: 3856.6204211634854
      counts_total: 11337.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001297591712669735
  - name: R_13(pp->ee)
    qmax: 233.92142
    qmin: 218.74908
    value:
      background_std: 525.82479
      counts_background: 3296.722728086122
      counts_total: 9358.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001600221396184068
  - name: R_13(pp->ee)
    qmax: 250.1461
    qmin: 233.92142
    value:
      background_std: 444.71135
      counts_background: 2818.1100442860775
      counts_total: 7877.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001975366089958675
  - name: R_13(pp->ee)
    qmax: 267.49612
    qmin: 250.1461
    value:
      background_std: 367.66547
      counts_background: 2408.9815482652252
      counts_total: 6434.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00023747235174379153
  - name: R_13(pp->ee)
    qmax: 286.04953
    qmin: 267.49612
    value:
      background_std: 314.24861
      counts_background: 2059.2496420247057
      counts_total: 5500.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0002936162223584367
  - name: R_13(pp->ee)
    qmax: 305.8898
    qmin: 286.04953
    value:
      background_std: 258.88905
      counts_background: 1699.9875967186451
      counts_total: 4445.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003556667718937045
  - name: R_13(pp->ee)
    qmax: 327.10617
    qmin: 305.8898
    value:
      background_std: 217.35737
      counts_background: 1428.07788026321
      counts_total: 3648.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0004480144439399666
  - name: R_13(pp->ee)
    qmax: 349.79411
    qmin: 327.10617
    value:
      background_std: 181.52639
      counts_background: 1138.5441438965217
      counts_total: 2981.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0005310545963681227
  - name: R_13(pp->ee)
    qmax: 374.05567
    qmin: 349.79411
    value:
      background_std: 155.1601
      counts_background: 907.7115369661385
      counts_total: 2431.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0006661026947009184
  - name: R_13(pp->ee)
    qmax: 400.0
    qmin: 374.05567
    value:
      background_std: 128.64381
      counts_background: 736.4024468642822
      counts_total: 1964.0
      distribution: general_gamma_counting_process
      scale_factor: 0.000821057973610578
  - name: R_13(pp->ee)
    qmax: 427.74382
    qmin: 400.0
    value:
      background_std: 103.29922
      counts_background: 576.9574935153886
      counts_total: 1606.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0010192069080174118
  - name: R_13(pp->ee)
    qmax: 457.41193
    qmin: 427.74382
    value:
      background_std: 85.46347
      counts_background: 459.98301955218915
      counts_total: 1231.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0012436687644054158
  - name: R_13(pp->ee)
    qmax: 489.13782
    qmin: 457.41193
    value:
      background_std: 73.72079
      counts_background: 366.72437857973097
      counts_total: 1013.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0015599358727921824
  - name: R_13(pp->ee)
    qmax: 523.06419
    qmin: 489.13782
    value:
      background_std: 55.19929
      counts_background: 282.35728074374333
      counts_total: 776.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0019190218064174967
  - name: R_13(pp->ee)
    qmax: 559.34369
    qmin: 523.06419
    value:
      background_std: 48.80979
      counts_background: 209.95171574856192
      counts_total: 622.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0023835569428771767
  - name: R_13(pp->ee)
    qmax: 598.13951
    qmin: 559.34369
    value:
      background_std: 35.32162
      counts_background: 167.3853364513252
      counts_total: 464.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00306926940947003
  - name: R_13(pp->ee)
    qmax: 639.6262
    qmin: 598.13951
    value:
      background_std: 30.02474
      counts_background: 128.87735639450338
      counts_total: 403.0
      distribution: general_gamma_counting_process
      scale_factor: 0.003783205685801885
  - name: R_13(pp->ee)
    qmax: 683.99038
    qmin: 639.6262
    value:
      background_std: 24.61983
      counts_background: 95.82902209885535
      counts_total: 300.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0048328867938694006
  - name: R_13(pp->ee)
    qmax: 731.43164
    qmin: 683.99038
    value:
      background_std: 18.49127
      counts_background: 71.25535263396021
      counts_total: 219.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0061788985279947065
  - name: R_13(pp->ee)
    qmax: 782.16341
    qmin: 731.43164
    value:
      background_std: 14.79304
      counts_background: 52.98316906283727
      counts_total: 202.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00771345682841781
  - name: R_13(pp->ee)
    qmax: 836.4139
    qmin: 782.16341
    value:
      background_std: 11.664
      counts_background: 42.24116744281099
      counts_total: 133.0
      distribution: general_gamma_counting_process
      scale_factor: 0.010165575952204128
  - name: R_13(pp->ee)
    qmax: 894.42719
    qmin: 836.4139
    value:
      background_std: 9.52662
      counts_background: 25.929437974046724
      counts_total: 107.0
      distribution: general_gamma_counting_process
      scale_factor: 0.01242797370580426
  - name: R_13(pp->ee)
    qmax: 956.46425
    qmin: 894.42719
    value:
      background_std: 7.02936
      counts_background: 22.951305889412726
      counts_total: 82.0
      distribution: general_gamma_counting_process
      scale_factor: 0.016162595737660334
  - name: R_13(pp->ee)
    qmax: 1022.80418
    qmin: 956.46425
    value:
      background_std: 6.42159
      counts_background: 16.196444247816817
      counts_total: 57.0
      distribution: general_gamma_counting_process
      scale_factor: 0.020840379028760656
  - name: R_13(pp->ee)
    qmax: 1093.74541
    qmin: 1022.80418
    value:
      background_std: 4.58922
      counts_background: 11.835067295194715
      counts_total: 43.0
      distribution: general_gamma_counting_process
      scale_factor: 0.027865041812088247
  - name: R_13(pp->ee)
    qmax: 1169.6071
    qmin: 1093.74541
    value:
      background_std: 4.072
      counts_background: 10.116872048488071
      counts_total: 27.0
      distribution: general_gamma_counting_process
      scale_factor: 0.035803723505292595
  - name: R_13(pp->ee)
    qmax: 1250.73051
    qmin: 1169.6071
    value:
      background_std: 3.55774
      counts_background: 7.015993056428879
      counts_total: 24.0
      distribution: general_gamma_counting_process
      scale_factor: 0.04593082843097357
  - name: R_13(pp->ee)
    qmax: 1337.48061
    qmin: 1250.73051
    value:
      background_std: 2.4616
      counts_background: 4.698868287883057
      counts_total: 12.0
      distribution: general_gamma_counting_process
      scale_factor: 0.06403541056796183
  - name: R_13(pp->ee)
    qmax: 1430.24766
    qmin: 1337.48061
    value:
      background_std: 1.81931
      counts_background: 3.3159315038208375
      counts_total: 13.0
      distribution: general_gamma_counting_process
      scale_factor: 0.08673919266016257
  - name: R_13(pp->ee)
    qmax: 1529.44898
    qmin: 1430.24766
    value:
      background_std: 1.46459
      counts_background: 2.259847110480091
      counts_total: 11.0
      distribution: general_gamma_counting_process
      scale_factor: 0.11145420943657515
  - name: R_13(pp->ee)
    qmax: 1635.53087
    qmin: 1529.44898
    value:
      background_std: 1.08804
      counts_background: 1.898388951473906
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.15849963717169402
  - name: R_13(pp->ee)
    qmax: 1748.97054
    qmin: 1635.53087
    value:
      background_std: 0.93005
      counts_background: 1.3632228684915886
      counts_total: 7.0
      distribution: general_gamma_counting_process
      scale_factor: 0.21578697195602808
  - name: R_13(pp->ee)
    qmax: 1870.27835
    qmin: 1748.97054
    value:
      background_std: 0.63117
      counts_background: 0.7406931897077118
      counts_total: 4.0
      distribution: general_gamma_counting_process
      scale_factor: 0.29880872349382903
  - name: R_13(pp->ee)
    qmax: 2000.0
    qmin: 1870.27835
    value:
      background_std: 0.48462
      counts_background: 0.5507554316034936
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.42852039805782594
  - name: R_13(pp->ee)
    qmax: 2138.71909
    qmin: 2000.0
    value:
      background_std: 0.36813
      counts_background: 0.40244806183924986
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 0.6123650966362543
  - name: R_13(pp->ee)
    qmax: 2287.05967
    qmin: 2138.71909
    value:
      background_std: 0.28204
      counts_background: 0.2840024714771532
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 0.8677570480195347
  - name: R_13(pp->ee)
    qmax: 2445.68909
    qmin: 2287.05967
    value:
      background_std: 0.21388
      counts_background: 0.20394064320970548
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 1.2903519721722103
  - name: R_13(pp->ee)
    qmax: 2615.32097
    qmin: 2445.68909
    value:
      background_std: 0.16619
      counts_background: 0.1365865406765846
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 1.926655509892617
  - name: R_13(pp->ee)
    qmax: 2796.71844
    qmin: 2615.32097
    value:
      background_std: 0.13146
      counts_background: 0.09808205828100346
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.9324549932851895
  - name: R_13(pp->ee)
    qmax: 2990.69756
    qmin: 2796.71844
    value:
      background_std: 0.10401
      counts_background: 0.06343879426969366
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 4.533838085494976
  - name: R_13(pp->ee)
    qmax: 3198.13098
    qmin: 2990.69756
    value:
      background_std: 0.08242
      counts_background: 0.0424872909961412
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 7.081975644121295
  - name: R_13(pp->ee)
    qmax: 3419.95189
    qmin: 3198.13098
    value:
      background_std: 0.06515
      counts_background: 0.027480484808533566
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 11.46009601807493
  - name: R_13(pp->ee)
    qmax: 3657.1582
    qmin: 3419.95189
    value:
      background_std: 0.05132
      counts_background: 0.016290814897373034
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 19.33169068048448
  - name: R_13(pp->ee)
    qmax: 3910.81703
    qmin: 3657.1582
    value:
      background_std: 0.03987
      counts_background: 0.010175819294691284
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 32.40865776788391
  - name: R_13(pp->ee)
    qmax: 4182.06952
    qmin: 3910.81703
    value:
      background_std: 0.03073
      counts_background: 0.005626136448385503
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 57.27738321032179
  - name: R_13(pp->ee)
    qmax: 4472.13595
    qmin: 4182.06952
    value:
      background_std: 0.02337
      counts_background: 0.0032209939381416005
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 104.79375109828433
  - name: R_13(pp->ee)
    qmax: 4782.32127
    qmin: 4472.13595
    value:
      background_std: 0.01745
      counts_background: 0.0018764583977886877
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 207.42976237268493
  - name: R_13(pp->ee)
    qmax: 5114.0209
    qmin: 4782.32127
    value:
      background_std: 0.01197
      counts_background: 0.0019430219749753776
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 393.32125134990633

ATLAS pp->ee 2019:
  experiment: ATLAS
  inspire: ATLAS:2019erb
  values:
  - name: R_13(pp->ee)
    qmax: 135.0803
    qmin: 130.0015
    value:
      background_std: 5000.588854114147
      counts_background: 13446.903379204288
      counts_total: 97949.09608780447
      distribution: general_gamma_counting_process
      scale_factor: 1.2332693238148677e-05
  - name: R_13(pp->ee)
    qmax: 140.3576
    qmin: 135.0803
    value:
      background_std: 4357.6509582467115
      counts_background: 13228.252576729941
      counts_total: 84590.46700920945
      distribution: general_gamma_counting_process
      scale_factor: 1.4446251442417394e-05
  - name: R_13(pp->ee)
    qmax: 145.841
    qmin: 140.3576
    value:
      background_std: 3809.8769400757465
      counts_background: 12880.255464655524
      counts_total: 73677.58736496375
      distribution: general_gamma_counting_process
      scale_factor: 1.687832468956729e-05
  - name: R_13(pp->ee)
    qmax: 151.5373
    qmin: 145.841
    value:
      background_std: 3357.8139815115555
      counts_background: 12377.245762429153
      counts_total: 65298.2717265786
      distribution: general_gamma_counting_process
      scale_factor: 1.95402439647497e-05
  - name: R_13(pp->ee)
    qmax: 157.4575
    qmin: 151.5373
    value:
      background_std: 2993.0645235757147
      counts_background: 11990.855921203432
      counts_total: 57173.48475062844
      distribution: general_gamma_counting_process
      scale_factor: 2.2433067165504817e-05
  - name: R_13(pp->ee)
    qmax: 163.609
    qmin: 157.4575
    value:
      background_std: 2656.6060408763883
      counts_background: 11430.266588630146
      counts_total: 51011.969305676175
      distribution: general_gamma_counting_process
      scale_factor: 2.5872912924585207e-05
  - name: R_13(pp->ee)
    qmax: 170.0008
    qmin: 163.609
    value:
      background_std: 2412.4247016848776
      counts_background: 10905.906649282797
      counts_total: 45817.07724602184
      distribution: general_gamma_counting_process
      scale_factor: 2.9184567585936974e-05
  - name: R_13(pp->ee)
    qmax: 176.6408
    qmin: 170.0008
    value:
      background_std: 2181.797292029745
      counts_background: 10287.502279210825
      counts_total: 41014.31123306121
      distribution: general_gamma_counting_process
      scale_factor: 3.306245838643729e-05
  - name: R_13(pp->ee)
    qmax: 183.5417
    qmin: 176.6408
    value:
      background_std: 1954.1188631227808
      counts_background: 9757.089561424931
      counts_total: 37157.82096625343
      distribution: general_gamma_counting_process
      scale_factor: 3.768318673487399e-05
  - name: R_13(pp->ee)
    qmax: 190.7122
    qmin: 183.5417
    value:
      background_std: 1760.8803060321534
      counts_background: 9231.366523721455
      counts_total: 33242.380659475326
      distribution: general_gamma_counting_process
      scale_factor: 4.2741138263125134e-05
  - name: R_13(pp->ee)
    qmax: 198.1629
    qmin: 190.7122
    value:
      background_std: 1602.9072476828815
      counts_background: 8643.446763401971
      counts_total: 30091.30081059541
      distribution: general_gamma_counting_process
      scale_factor: 4.80112479990445e-05
  - name: R_13(pp->ee)
    qmax: 205.9028
    qmin: 198.1629
    value:
      background_std: 1453.4497184562108
      counts_background: 8112.2121914010795
      counts_total: 26905.019843905644
      distribution: general_gamma_counting_process
      scale_factor: 5.4099701415806044e-05
  - name: R_13(pp->ee)
    qmax: 213.9394
    qmin: 205.9028
    value:
      background_std: 1312.0100412543106
      counts_background: 7545.11334688143
      counts_total: 24242.977217540498
      distribution: general_gamma_counting_process
      scale_factor: 6.0928725802191565e-05
  - name: R_13(pp->ee)
    qmax: 222.2975
    qmin: 213.9394
    value:
      background_std: 1190.0446190750324
      counts_background: 7003.694784802399
      counts_total: 21812.55089957259
      distribution: general_gamma_counting_process
      scale_factor: 6.84071111037318e-05
  - name: R_13(pp->ee)
    qmax: 230.9902
    qmin: 222.2975
    value:
      background_std: 1078.9245274849386
      counts_background: 6400.317969534015
      counts_total: 19791.862964624223
      distribution: general_gamma_counting_process
      scale_factor: 7.643854201559559e-05
  - name: R_13(pp->ee)
    qmax: 240.0039
    qmin: 230.9902
    value:
      background_std: 981.7354664069255
      counts_background: 5924.685059029112
      counts_total: 17807.673308411715
      distribution: general_gamma_counting_process
      scale_factor: 8.62407749068593e-05
  - name: R_13(pp->ee)
    qmax: 249.3802
    qmin: 240.0039
    value:
      background_std: 889.2823126646324
      counts_background: 5395.220298379147
      counts_total: 16295.976158627765
      distribution: general_gamma_counting_process
      scale_factor: 9.649122883371949e-05
  - name: R_13(pp->ee)
    qmax: 259.1229
    qmin: 249.3802
    value:
      background_std: 793.7255297662615
      counts_background: 4950.853869576408
      counts_total: 14289.667537147046
      distribution: general_gamma_counting_process
      scale_factor: 0.0001087606655189842
  - name: R_13(pp->ee)
    qmax: 269.2462
    qmin: 259.1229
    value:
      background_std: 719.3740771806467
      counts_background: 4512.562837037432
      counts_total: 13037.604152525233
      distribution: general_gamma_counting_process
      scale_factor: 0.00012179109660095017
  - name: R_13(pp->ee)
    qmax: 279.7625
    qmin: 269.2462
    value:
      background_std: 653.7372273056299
      counts_background: 4052.707722521289
      counts_total: 11562.813282279834
      distribution: general_gamma_counting_process
      scale_factor: 0.00013724979684923984
  - name: R_13(pp->ee)
    qmax: 290.6922
    qmin: 279.7625
    value:
      background_std: 589.656565522517
      counts_background: 3686.0131077455826
      counts_total: 10185.167926541993
      distribution: general_gamma_counting_process
      scale_factor: 0.0001537646079277784
  - name: R_13(pp->ee)
    qmax: 302.0488
    qmin: 290.6922
    value:
      background_std: 524.1327408624023
      counts_background: 3270.059670600919
      counts_total: 9218.998992379236
      distribution: general_gamma_counting_process
      scale_factor: 0.00017274238659341256
  - name: R_13(pp->ee)
    qmax: 313.8491
    qmin: 302.0488
    value:
      background_std: 474.78876252421395
      counts_background: 2949.4485567879747
      counts_total: 8103.516491866462
      distribution: general_gamma_counting_process
      scale_factor: 0.00019444276945669583
  - name: R_13(pp->ee)
    qmax: 326.1076
    qmin: 313.8491
    value:
      background_std: 428.2289459608986
      counts_background: 2609.607391708814
      counts_total: 7413.335254694742
      distribution: general_gamma_counting_process
      scale_factor: 0.00021789453569040658
  - name: R_13(pp->ee)
    qmax: 338.8478
    qmin: 326.1076
    value:
      background_std: 387.2323019446182
      counts_background: 2338.114749738156
      counts_total: 6526.826468444991
      distribution: general_gamma_counting_process
      scale_factor: 0.00024454498308601225
  - name: R_13(pp->ee)
    qmax: 352.0857
    qmin: 338.8478
    value:
      background_std: 352.7944835921638
      counts_background: 2088.1376517856006
      counts_total: 5785.420059023196
      distribution: general_gamma_counting_process
      scale_factor: 0.00027617480881406836
  - name: R_13(pp->ee)
    qmax: 365.8409
    qmin: 352.0857
    value:
      background_std: 322.01254487850343
      counts_background: 1833.8603924256438
      counts_total: 5116.656467932042
      distribution: general_gamma_counting_process
      scale_factor: 0.00031329384990679563
  - name: R_13(pp->ee)
    qmax: 380.13
    qmin: 365.8409
    value:
      background_std: 290.83285495135436
      counts_background: 1603.7754477699277
      counts_total: 4611.286134228489
      distribution: general_gamma_counting_process
      scale_factor: 0.00034911174867409173
  - name: R_13(pp->ee)
    qmax: 394.9808
    qmin: 380.13
    value:
      background_std: 259.7009761921493
      counts_background: 1417.6814840612915
      counts_total: 4047.8983410975466
      distribution: general_gamma_counting_process
      scale_factor: 0.0003949383957866019
  - name: R_13(pp->ee)
    qmax: 410.3972
    qmin: 394.9808
    value:
      background_std: 229.65524036567348
      counts_background: 1250.3041429155573
      counts_total: 3590.8323511844733
      distribution: general_gamma_counting_process
      scale_factor: 0.0004474341452706121
  - name: R_13(pp->ee)
    qmax: 426.4304
    qmin: 410.3972
    value:
      background_std: 203.68384695271632
      counts_background: 1084.2595270085908
      counts_total: 3139.3471197369486
      distribution: general_gamma_counting_process
      scale_factor: 0.000502394652969665
  - name: R_13(pp->ee)
    qmax: 443.0861
    qmin: 426.4304
    value:
      background_std: 180.46309211601982
      counts_background: 929.1673801481127
      counts_total: 2714.309586232467
      distribution: general_gamma_counting_process
      scale_factor: 0.0005685160282425192
  - name: R_13(pp->ee)
    qmax: 460.3964
    qmin: 443.0861
    value:
      background_std: 164.0562520677799
      counts_background: 817.4596293316953
      counts_total: 2413.180160272831
      distribution: general_gamma_counting_process
      scale_factor: 0.0006441667284197498
  - name: R_13(pp->ee)
    qmax: 478.383
    qmin: 460.3964
    value:
      background_std: 151.21565368258194
      counts_background: 713.584028297956
      counts_total: 1996.6996376866573
      distribution: general_gamma_counting_process
      scale_factor: 0.0007278476711879326
  - name: R_13(pp->ee)
    qmax: 497.0722
    qmin: 478.383
    value:
      background_std: 129.85622039100267
      counts_background: 613.1550127653774
      counts_total: 1818.8200490770755
      distribution: general_gamma_counting_process
      scale_factor: 0.000824405810877622
  - name: R_13(pp->ee)
    qmax: 516.4871
    qmin: 497.0722
    value:
      background_std: 109.71058270193336
      counts_background: 523.2001554980269
      counts_total: 1631.0963731925158
      distribution: general_gamma_counting_process
      scale_factor: 0.0009312442275077185
  - name: R_13(pp->ee)
    qmax: 536.665
    qmin: 516.4871
    value:
      background_std: 103.53297658059545
      counts_background: 454.5871906281341
      counts_total: 1367.4928859180989
      distribution: general_gamma_counting_process
      scale_factor: 0.0010553631282144097
  - name: R_13(pp->ee)
    qmax: 557.6312
    qmin: 536.665
    value:
      background_std: 93.88784842155745
      counts_background: 397.187198322839
      counts_total: 1269.26775976893
      distribution: general_gamma_counting_process
      scale_factor: 0.0012095248020111693
  - name: R_13(pp->ee)
    qmax: 579.4164
    qmin: 557.6312
    value:
      background_std: 77.65934727626819
      counts_background: 330.5066667843718
      counts_total: 1080.5695533549847
      distribution: general_gamma_counting_process
      scale_factor: 0.0013733533694863858
  - name: R_13(pp->ee)
    qmax: 602.0475
    qmin: 579.4164
    value:
      background_std: 68.49151428413838
      counts_background: 294.8093172874121
      counts_total: 937.1021583413152
      distribution: general_gamma_counting_process
      scale_factor: 0.001559360967585762
  - name: R_13(pp->ee)
    qmax: 625.568
    qmin: 602.0475
    value:
      background_std: 61.58781286671711
      counts_background: 249.33282193224875
      counts_total: 813.1811647654824
      distribution: general_gamma_counting_process
      scale_factor: 0.0017785323319468057
  - name: R_13(pp->ee)
    qmax: 650.0075
    qmin: 625.568
    value:
      background_std: 54.91632379110085
      counts_background: 208.28654226082028
      counts_total: 706.1610340728728
      distribution: general_gamma_counting_process
      scale_factor: 0.0020326209745027937
  - name: R_13(pp->ee)
    qmax: 675.4017
    qmin: 650.0075
    value:
      background_std: 49.24721937606607
      counts_background: 177.74281816292327
      counts_total: 555.9057477934142
      distribution: general_gamma_counting_process
      scale_factor: 0.002318110242712648
  - name: R_13(pp->ee)
    qmax: 701.7818
    qmin: 675.4017
    value:
      background_std: 41.95765059011334
      counts_background: 150.85535618677892
      counts_total: 506.8087793638034
      distribution: general_gamma_counting_process
      scale_factor: 0.0026641125124107945
  - name: R_13(pp->ee)
    qmax: 729.1987
    qmin: 701.7818
    value:
      background_std: 36.232091025653396
      counts_background: 128.3887976607438
      counts_total: 435.21427396152177
      distribution: general_gamma_counting_process
      scale_factor: 0.003038931703603945
  - name: R_13(pp->ee)
    qmax: 757.6867
    qmin: 729.1987
    value:
      background_std: 31.448674177937836
      counts_background: 105.81648927530459
      counts_total: 423.3756607856382
      distribution: general_gamma_counting_process
      scale_factor: 0.003495874956877871
  - name: R_13(pp->ee)
    qmax: 787.2599
    qmin: 757.6867
    value:
      background_std: 27.980615771797872
      counts_background: 94.25018192276096
      counts_total: 398.84895995789265
      distribution: general_gamma_counting_process
      scale_factor: 0.004013458350225681
  - name: R_13(pp->ee)
    qmax: 818.0378
    qmin: 787.2599
    value:
      background_std: 24.220760425686688
      counts_background: 75.90914641038265
      counts_total: 299.7511245694044
      distribution: general_gamma_counting_process
      scale_factor: 0.0046219449602098025
  - name: R_13(pp->ee)
    qmax: 849.9666
    qmin: 818.0378
    value:
      background_std: 21.780938810526123
      counts_background: 65.42094372808647
      counts_total: 236.00694123573948
      distribution: general_gamma_counting_process
      scale_factor: 0.005300675309648257
  - name: R_13(pp->ee)
    qmax: 883.1727
    qmin: 849.9666
    value:
      background_std: 19.215492334610015
      counts_background: 52.8355751984345
      counts_total: 215.41871361748014
      distribution: general_gamma_counting_process
      scale_factor: 0.0061180313214885314
  - name: R_13(pp->ee)
    qmax: 917.6761
    qmin: 883.1727
    value:
      background_std: 16.20071279217406
      counts_background: 48.63267629643907
      counts_total: 221.29819689281416
      distribution: general_gamma_counting_process
      scale_factor: 0.0070704917637696586
  - name: R_13(pp->ee)
    qmax: 953.5275
    qmin: 917.6761
    value:
      background_std: 13.811881132488796
      counts_background: 39.524460869806795
      counts_total: 159.51371038435036
      distribution: general_gamma_counting_process
      scale_factor: 0.008185107986076986
  - name: R_13(pp->ee)
    qmax: 990.7707
    qmin: 953.5275
    value:
      background_std: 13.175902417516886
      counts_background: 32.7632843122609
      counts_total: 129.13353082330747
      distribution: general_gamma_counting_process
      scale_factor: 0.009525662259813395
  - name: R_13(pp->ee)
    qmax: 1029.4777
    qmin: 990.7707
    value:
      background_std: 11.659037470077081
      counts_background: 27.223269349649232
      counts_total: 112.49576532027582
      distribution: general_gamma_counting_process
      scale_factor: 0.01106394894571722
  - name: R_13(pp->ee)
    qmax: 1069.6969
    qmin: 1029.4777
    value:
      background_std: 9.87136032601964
      counts_background: 24.514709760773517
      counts_total: 92.90250290773875
      distribution: general_gamma_counting_process
      scale_factor: 0.012840152490616673
  - name: R_13(pp->ee)
    qmax: 1111.4873
    qmin: 1069.6969
    value:
      background_std: 8.705970941275497
      counts_background: 19.941773635240168
      counts_total: 88.01472671768623
      distribution: general_gamma_counting_process
      scale_factor: 0.015031760330856996
  - name: R_13(pp->ee)
    qmax: 1154.9002
    qmin: 1111.4873
    value:
      background_std: 7.842767814625907
      counts_background: 16.67930161035911
      counts_total: 75.27792938634673
      distribution: general_gamma_counting_process
      scale_factor: 0.017709511586387495
  - name: R_13(pp->ee)
    qmax: 1200.0193
    qmin: 1154.9002
    value:
      background_std: 7.314831606268497
      counts_background: 13.649286751347637
      counts_total: 56.67417863502218
      distribution: general_gamma_counting_process
      scale_factor: 0.020425979352369422
  - name: R_13(pp->ee)
    qmax: 1246.9012
    qmin: 1200.0193
    value:
      background_std: 6.513418863069771
      counts_background: 11.710345740689903
      counts_total: 63.539075129751424
      distribution: general_gamma_counting_process
      scale_factor: 0.0243830964409557
  - name: R_13(pp->ee)
    qmax: 1295.6146
    qmin: 1246.9012
    value:
      background_std: 5.521353708896579
      counts_background: 9.80053893636672
      counts_total: 38.09018848604091
      distribution: general_gamma_counting_process
      scale_factor: 0.028231052442424482
  - name: R_13(pp->ee)
    qmax: 1346.2192
    qmin: 1295.6146
    value:
      background_std: 4.694009268181746
      counts_background: 9.156707931912937
      counts_total: 40.04102995107373
      distribution: general_gamma_counting_process
      scale_factor: 0.033909257162614614
  - name: R_13(pp->ee)
    qmax: 1398.8127
    qmin: 1346.2192
    value:
      background_std: 3.8574711625114353
      counts_background: 6.790775188931913
      counts_total: 28.3155164256166
      distribution: general_gamma_counting_process
      scale_factor: 0.04009624995790919
  - name: R_13(pp->ee)
    qmax: 1453.4609
    qmin: 1398.8127
    value:
      background_std: 3.378377788764045
      counts_background: 5.6222286920611175
      counts_total: 22.44740373150197
      distribution: general_gamma_counting_process
      scale_factor: 0.0471070903104401
  - name: R_13(pp->ee)
    qmax: 1510.244
    qmin: 1453.4609
    value:
      background_std: 3.1048366619791468
      counts_background: 5.824330789885145
      counts_total: 21.468559635362947
      distribution: general_gamma_counting_process
      scale_factor: 0.05605466718315075
  - name: R_13(pp->ee)
    qmax: 1569.2317
    qmin: 1510.244
    value:
      background_std: 2.5393736037251857
      counts_background: 4.426622246863116
      counts_total: 17.562457567401644
      distribution: general_gamma_counting_process
      scale_factor: 0.06717407775091293
  - name: R_13(pp->ee)
    qmax: 1630.4802
    qmin: 1569.2317
    value:
      background_std: 2.113991020963491
      counts_background: 3.1974777594226738
      counts_total: 9.749244343870092
      distribution: general_gamma_counting_process
      scale_factor: 0.08051811110941567
  - name: R_13(pp->ee)
    qmax: 1694.1791
    qmin: 1630.4802
    value:
      background_std: 1.9315240978219659
      counts_background: 2.521951325381498
      counts_total: 13.652946963709823
      distribution: general_gamma_counting_process
      scale_factor: 0.0954448321661011
  - name: R_13(pp->ee)
    qmax: 1760.3666
    qmin: 1694.1791
    value:
      background_std: 1.6926221911321264
      counts_background: 2.291654014912636
      counts_total: 16.58183914474875
      distribution: general_gamma_counting_process
      scale_factor: 0.11570464057085542
  - name: R_13(pp->ee)
    qmax: 1829.1236
    qmin: 1760.3666
    value:
      background_std: 1.361682821855043
      counts_background: 1.6702317082582852
      counts_total: 8.771855311944638
      distribution: general_gamma_counting_process
      scale_factor: 0.14006243288425288
  - name: R_13(pp->ee)
    qmax: 1900.583
    qmin: 1829.1236
    value:
      background_std: 1.3526428282999017
      counts_background: 2.588502215943407
      counts_total: 5.8442199558327825
      distribution: general_gamma_counting_process
      scale_factor: 0.171541450134859
  - name: R_13(pp->ee)
    qmax: 1974.8342
    qmin: 1900.583
    value:
      background_std: 1.0166440219119595
      counts_background: 1.2453333652849015
      counts_total: 0.9715693367457594
      distribution: general_gamma_counting_process
      scale_factor: 0.2092432338426458
  - name: R_13(pp->ee)
    qmax: 2051.9861
    qmin: 1974.8342
    value:
      background_std: 0.8758447738018891
      counts_background: 1.0690832979944493
      counts_total: 1.945364105403084
      distribution: general_gamma_counting_process
      scale_factor: 0.2540206377272894
  - name: R_13(pp->ee)
    qmax: 2132.1334
    qmin: 2051.9861
    value:
      background_std: 0.7323076989773978
      counts_background: 0.8432196384712763
      counts_total: 8.771855311944638
      distribution: general_gamma_counting_process
      scale_factor: 0.3151573602388245
  - name: R_13(pp->ee)
    qmax: 2215.4306
    qmin: 2132.1334
    value:
      background_std: 0.6225672579529163
      counts_background: 0.6383669088289287
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.3848308840456396
  - name: R_13(pp->ee)
    qmax: 2301.9821
    qmin: 2215.4306
    value:
      background_std: 0.5353327260232467
      counts_background: 0.5473485414495267
      counts_total: 4.869045766105319
      distribution: general_gamma_counting_process
      scale_factor: 0.4803713478452193
  - name: R_13(pp->ee)
    qmax: 2391.9149
    qmin: 2301.9821
    value:
      background_std: 0.44779220779209794
      counts_background: 0.40168531051194534
      counts_total: 2.9193262317623336
      distribution: general_gamma_counting_process
      scale_factor: 0.5987878305366042
  - name: R_13(pp->ee)
    qmax: 2485.3393
    qmin: 2391.9149
    value:
      background_std: 0.39094696744595075
      counts_background: 0.3327677765713436
      counts_total: 4.869045766105319
      distribution: general_gamma_counting_process
      scale_factor: 0.7482562094872316
  - name: R_13(pp->ee)
    qmax: 2582.4354
    qmin: 2485.3393
    value:
      background_std: 0.33759452477562935
      counts_background: 0.26659839919840733
      counts_total: 1.9453641054030664
      distribution: general_gamma_counting_process
      scale_factor: 0.9435029816259038
  - name: R_13(pp->ee)
    qmax: 2683.3248
    qmin: 2582.4354
    value:
      background_std: 0.2924475697391959
      counts_background: 0.21531147314498952
      counts_total: 1.9453641054030664
      distribution: general_gamma_counting_process
      scale_factor: 1.1988471147431752
  - name: R_13(pp->ee)
    qmax: 2788.1558
    qmin: 2683.3248
    value:
      background_std: 0.2551134283132255
      counts_background: 0.17073605744979936
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.5175353554380437
  - name: R_13(pp->ee)
    qmax: 2897.0567
    qmin: 2788.1558
    value:
      background_std: 0.22443486979462815
      counts_background: 0.13491272038044805
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.952669252351545
  - name: R_13(pp->ee)
    qmax: 3010.2376
    qmin: 2897.0567
    value:
      background_std: 0.1977807518255459
      counts_background: 0.10584081101112268
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.5023129756161775
  - name: R_13(pp->ee)
    qmax: 3127.7298
    qmin: 3010.2376
    value:
      background_std: 0.1714685821113244
      counts_background: 0.08107242078289494
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.2447259310769816
  - name: R_13(pp->ee)
    qmax: 3249.9226
    qmin: 3127.7298
    value:
      background_std: 0.1495995914919013
      counts_background: 0.06217161870903482
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 4.26158294106928
  - name: R_13(pp->ee)
    qmax: 3376.8593
    qmin: 3249.9226
    value:
      background_std: 0.12989764614730645
      counts_background: 0.04783456444454831
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 5.610273061459661
  - name: R_13(pp->ee)
    qmax: 3508.785
    qmin: 3376.8593
    value:
      background_std: 0.11563780858998697
      counts_background: 0.036053033371854636
      counts_total: 0.9715693367457524
      distribution: general_gamma_counting_process
      scale_factor: 7.455924738202726
  - name: R_13(pp->ee)
    qmax: 3645.8646
    qmin: 3508.785
    value:
      background_std: 0.09999023273953724
      counts_background: 0.026236390256353926
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 9.99546044140827
  - name: R_13(pp->ee)
    qmax: 3788.2997
    qmin: 3645.8646
    value:
      background_std: 0.08561484210451817
      counts_background: 0.0197865569730545
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 13.585420837517379
  - name: R_13(pp->ee)
    qmax: 3936.2646
    qmin: 3788.2997
    value:
      background_std: 0.07388368415465373
      counts_background: 0.014347254625227372
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 18.459757051860073
  - name: R_13(pp->ee)
    qmax: 4090.0448
    qmin: 3936.2646
    value:
      background_std: 0.06302461460316248
      counts_background: 0.010466361273598884
      counts_total: 0.9715693367457524
      distribution: general_gamma_counting_process
      scale_factor: 25.650681230111875
  - name: R_13(pp->ee)
    qmax: 4249.8329
    qmin: 4090.0448
    value:
      background_std: 0.05481290833416443
      counts_background: 0.0073878230583136195
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 35.51063091958176
  - name: R_13(pp->ee)
    qmax: 4415.8634
    qmin: 4249.8329
    value:
      background_std: 0.04643474045611447
      counts_background: 0.005513465057972382
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 50.76076976105406
  - name: R_13(pp->ee)
    qmax: 4588.34
    qmin: 4415.8634
    value:
      background_std: 0.038981639480376584
      counts_background: 0.003516379596285951
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 73.10315047448637
  - name: R_13(pp->ee)
    qmax: 4767.5952
    qmin: 4588.34
    value:
      background_std: 0.031000561796046447
      counts_background: 0.0025468025477199596
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 106.42394209196908
  - name: R_13(pp->ee)
    qmax: 4953.8535
    qmin: 4767.5952
    value:
      background_std: 0.021350088623077475
      counts_background: 0.0016877241333322882
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 156.8038424677342
  - name: R_13(pp->ee)
    qmax: 5147.3884
    qmin: 4953.8535
    value:
      background_std: 0.018518244451196132
      counts_background: 0.0011031105137100342
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 234.69830154908252
  - name: R_13(pp->ee)
    qmax: 5348.4372
    qmin: 5147.3884
    value:
      background_std: 0.017332008085563434
      counts_background: 0.0007122186928155025
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 359.02069531801953
  - name: R_13(pp->ee)
    qmax: 5557.3875
    qmin: 5348.4372
    value:
      background_std: 0.014476023761680524
      counts_background: 0.0004371690750339727
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 559.0543679036756
  - name: R_13(pp->ee)
    qmax: 5774.5011
    qmin: 5557.3875
    value:
      background_std: 0.011412766098604794
      counts_background: 0.0002667414011898086
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 880.2572239137857
  - name: R_13(pp->ee)
    qmax: 5999.885
    qmin: 5774.5011
    value:
      background_std: 0.019660699632794803
      counts_background: 0.00021127565301545443
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 609.1436469323086

ATLAS pp->enu 2019:
  experiment: ATLAS
  inspire: ATLAS:2019lsy
  values:
  - mTmax: 138.982
    mTmin: 130.0
    name: R_13(pp->enu)
    value:
      background_std: 49484.8419359949
      counts_background: 129820.73135913502
      counts_total: 563230.0
      distribution: general_gamma_counting_process
      scale_factor: 2.6383035029286187e-06
  - mTmax: 148.585
    mTmin: 138.982
    name: R_13(pp->enu)
    value:
      background_std: 55498.444905803444
      counts_background: 150819.18570542432
      counts_total: 673665.0
      distribution: general_gamma_counting_process
      scale_factor: 2.1721793318498923e-06
  - mTmax: 158.852
    mTmin: 148.585
    name: R_13(pp->enu)
    value:
      background_std: 43770.02692843129
      counts_background: 141096.9691326152
      counts_total: 560331.0
      distribution: general_gamma_counting_process
      scale_factor: 2.657433241379074e-06
  - mTmax: 169.828
    mTmin: 158.852
    name: R_13(pp->enu)
    value:
      background_std: 31092.242263884735
      counts_background: 123492.29775385726
      counts_total: 431950.0
      distribution: general_gamma_counting_process
      scale_factor: 3.4931113488836114e-06
  - mTmax: 181.562
    mTmin: 169.828
    name: R_13(pp->enu)
    value:
      background_std: 21906.70777115767
      counts_background: 104542.43332579503
      counts_total: 324635.0
      distribution: general_gamma_counting_process
      scale_factor: 4.776628421187213e-06
  - mTmax: 194.107
    mTmin: 181.562
    name: R_13(pp->enu)
    value:
      background_std: 15640.847197926973
      counts_background: 85600.41777043986
      counts_total: 243844.0
      distribution: general_gamma_counting_process
      scale_factor: 6.627806912223095e-06
  - mTmax: 207.519
    mTmin: 194.107
    name: R_13(pp->enu)
    value:
      background_std: 10898.031044212757
      counts_background: 68932.5647278195
      counts_total: 184520.0
      distribution: general_gamma_counting_process
      scale_factor: 9.15542720466144e-06
  - mTmax: 221.857
    mTmin: 207.519
    name: R_13(pp->enu)
    value:
      background_std: 7745.417400963231
      counts_background: 53691.25271654329
      counts_total: 140146.0
      distribution: general_gamma_counting_process
      scale_factor: 1.2079889169497448e-05
  - mTmax: 237.186
    mTmin: 221.857
    name: R_13(pp->enu)
    value:
      background_std: 5584.0849060870305
      counts_background: 41819.8659755992
      counts_total: 107018.0
      distribution: general_gamma_counting_process
      scale_factor: 1.5943224938748905e-05
  - mTmax: 253.575
    mTmin: 237.186
    name: R_13(pp->enu)
    value:
      background_std: 4156.766259887125
      counts_background: 32573.29828846043
      counts_total: 82526.0
      distribution: general_gamma_counting_process
      scale_factor: 2.104860673441654e-05
  - mTmax: 271.095
    mTmin: 253.575
    name: R_13(pp->enu)
    value:
      background_std: 3174.1290373266174
      counts_background: 24539.820553266094
      counts_total: 62571.0
      distribution: general_gamma_counting_process
      scale_factor: 2.6429874692013637e-05
  - mTmax: 289.827
    mTmin: 271.095
    name: R_13(pp->enu)
    value:
      background_std: 2384.8306572215984
      counts_background: 18487.620978801562
      counts_total: 48409.0
      distribution: general_gamma_counting_process
      scale_factor: 3.413673825960676e-05
  - mTmax: 309.852
    mTmin: 289.827
    name: R_13(pp->enu)
    value:
      background_std: 1873.7928281696456
      counts_background: 14162.026474743869
      counts_total: 37169.0
      distribution: general_gamma_counting_process
      scale_factor: 4.3374881191144686e-05
  - mTmax: 331.261
    mTmin: 309.852
    name: R_13(pp->enu)
    value:
      background_std: 1439.4149123862792
      counts_background: 10319.66489379555
      counts_total: 28815.0
      distribution: general_gamma_counting_process
      scale_factor: 5.4976886015863484e-05
  - mTmax: 354.15
    mTmin: 331.261
    name: R_13(pp->enu)
    value:
      background_std: 1124.7987219360627
      counts_background: 7519.791303183718
      counts_total: 21919.0
      distribution: general_gamma_counting_process
      scale_factor: 6.983735327425578e-05
  - mTmax: 378.62
    mTmin: 354.15
    name: R_13(pp->enu)
    value:
      background_std: 860.1626882944936
      counts_background: 5479.563709228112
      counts_total: 16774.0
      distribution: general_gamma_counting_process
      scale_factor: 9.113140840083532e-05
  - mTmax: 404.781
    mTmin: 378.62
    name: R_13(pp->enu)
    value:
      background_std: 682.617048645322
      counts_background: 3992.8792213658303
      counts_total: 12897.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00011335202408318016
  - mTmax: 432.749
    mTmin: 404.781
    name: R_13(pp->enu)
    value:
      background_std: 536.8088063004928
      counts_background: 2861.4860951082856
      counts_total: 9953.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00014377894804630837
  - mTmax: 462.65
    mTmin: 432.749
    name: R_13(pp->enu)
    value:
      background_std: 415.87036813854627
      counts_background: 2016.7978951875964
      counts_total: 7535.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00018591638603231064
  - mTmax: 494.616
    mTmin: 462.65
    name: R_13(pp->enu)
    value:
      background_std: 327.4099326139175
      counts_background: 1445.3327570847223
      counts_total: 5773.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00023697414219574304
  - mTmax: 528.792
    mTmin: 494.616
    name: R_13(pp->enu)
    value:
      background_std: 259.82819288145004
      counts_background: 1035.7938114110407
      counts_total: 4547.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003026719415244498
  - mTmax: 565.329
    mTmin: 528.792
    name: R_13(pp->enu)
    value:
      background_std: 209.6449560187175
      counts_background: 754.7680448057165
      counts_total: 3389.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00038917133148512646
  - mTmax: 604.39
    mTmin: 565.329
    name: R_13(pp->enu)
    value:
      background_std: 161.85673331239573
      counts_background: 506.03442716518185
      counts_total: 2610.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0005003943116325671
  - mTmax: 646.15
    mTmin: 604.39
    name: R_13(pp->enu)
    value:
      background_std: 124.83452342124754
      counts_background: 344.9700173072118
      counts_total: 2012.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0006485843183333087
  - mTmax: 690.796
    mTmin: 646.15
    name: R_13(pp->enu)
    value:
      background_std: 100.70386611247854
      counts_background: 292.0344482181367
      counts_total: 1457.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0008317641822735494
  - mTmax: 738.526
    mTmin: 690.796
    name: R_13(pp->enu)
    value:
      background_std: 76.50435062982301
      counts_background: 189.37872560617632
      counts_total: 1127.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0010895786829861827
  - mTmax: 789.555
    mTmin: 738.526
    name: R_13(pp->enu)
    value:
      background_std: 59.719265267352384
      counts_background: 140.31564899455563
      counts_total: 843.0
      distribution: general_gamma_counting_process
      scale_factor: 0.001412822577146357
  - mTmax: 844.109
    mTmin: 789.555
    name: R_13(pp->enu)
    value:
      background_std: 50.140722564398686
      counts_background: 98.8955724921642
      counts_total: 623.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0017803096161370174
  - mTmax: 902.433
    mTmin: 844.109
    name: R_13(pp->enu)
    value:
      background_std: 35.256962054222704
      counts_background: 67.41835243374094
      counts_total: 518.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0024157613670345063
  - mTmax: 964.786
    mTmin: 902.433
    name: R_13(pp->enu)
    value:
      background_std: 27.023343874576295
      counts_background: 48.31517993631411
      counts_total: 337.0
      distribution: general_gamma_counting_process
      scale_factor: 0.003181339294922784
  - mTmax: 1031.45
    mTmin: 964.786
    name: R_13(pp->enu)
    value:
      background_std: 20.610596523538565
      counts_background: 34.05291864522614
      counts_total: 294.0
      distribution: general_gamma_counting_process
      scale_factor: 0.004261800410656309
  - mTmax: 1102.72
    mTmin: 1031.45
    name: R_13(pp->enu)
    value:
      background_std: 15.801791187298008
      counts_background: 24.40393204977451
      counts_total: 232.0
      distribution: general_gamma_counting_process
      scale_factor: 0.005617225180407488
  - mTmax: 1178.91
    mTmin: 1102.72
    name: R_13(pp->enu)
    value:
      background_std: 12.092075309739018
      counts_background: 17.20008315833659
      counts_total: 141.0
      distribution: general_gamma_counting_process
      scale_factor: 0.007531030901164063
  - mTmax: 1260.36
    mTmin: 1178.91
    name: R_13(pp->enu)
    value:
      background_std: 9.236083822588933
      counts_background: 12.122753827141004
      counts_total: 94.0
      distribution: general_gamma_counting_process
      scale_factor: 0.010291406333570428
  - mTmax: 1347.45
    mTmin: 1260.36
    name: R_13(pp->enu)
    value:
      background_std: 7.050629700264793
      counts_background: 8.982065252640252
      counts_total: 85.0
      distribution: general_gamma_counting_process
      scale_factor: 0.013889921973154359
  - mTmax: 1440.55
    mTmin: 1347.45
    name: R_13(pp->enu)
    value:
      background_std: 5.313931243968536
      counts_background: 6.022027927865022
      counts_total: 62.0
      distribution: general_gamma_counting_process
      scale_factor: 0.019227178040903105
  - mTmax: 1540.09
    mTmin: 1440.55
    name: R_13(pp->enu)
    value:
      background_std: 4.012313219170332
      counts_background: 4.244372625273755
      counts_total: 39.0
      distribution: general_gamma_counting_process
      scale_factor: 0.026286375406568627
  - mTmax: 1646.5
    mTmin: 1540.09
    name: R_13(pp->enu)
    value:
      background_std: 2.9664130688494814
      counts_background: 2.991467193105486
      counts_total: 19.0
      distribution: general_gamma_counting_process
      scale_factor: 0.03661217167018156
  - mTmax: 1760.26
    mTmin: 1646.5
    name: R_13(pp->enu)
    value:
      background_std: 2.221664521030124
      counts_background: 2.1084095948925303
      counts_total: 16.0
      distribution: general_gamma_counting_process
      scale_factor: 0.051946315689801466
  - mTmax: 1881.89
    mTmin: 1760.26
    name: R_13(pp->enu)
    value:
      background_std: 1.6642557842663488
      counts_background: 1.4860236575819088
      counts_total: 16.0
      distribution: general_gamma_counting_process
      scale_factor: 0.07370280403066642
  - mTmax: 2011.92
    mTmin: 1881.89
    name: R_13(pp->enu)
    value:
      background_std: 1.2408557038083075
      counts_background: 1.0473611561256748
      counts_total: 6.0
      distribution: general_gamma_counting_process
      scale_factor: 0.10652406912436779
  - mTmax: 2150.93
    mTmin: 2011.92
    name: R_13(pp->enu)
    value:
      background_std: 0.9175441203948996
      counts_background: 0.7381883765874365
      counts_total: 9.0
      distribution: general_gamma_counting_process
      scale_factor: 0.15685237916048003
  - mTmax: 2299.55
    mTmin: 2150.93
    name: R_13(pp->enu)
    value:
      background_std: 0.6699226658253623
      counts_background: 0.5202809710305953
      counts_total: 7.0
      distribution: general_gamma_counting_process
      scale_factor: 0.23099190742964934
  - mTmax: 2458.43
    mTmin: 2299.55
    name: R_13(pp->enu)
    value:
      background_std: 0.49062532661644165
      counts_background: 0.3606400503373748
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 0.35249089583406584
  - mTmax: 2628.3
    mTmin: 2458.43
    name: R_13(pp->enu)
    value:
      background_std: 0.36196939444447523
      counts_background: 0.25418194262210525
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.5393081042532946
  - mTmax: 2809.9
    mTmin: 2628.3
    name: R_13(pp->enu)
    value:
      background_std: 0.2642369584530569
      counts_background: 0.17618977761286764
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.8395788818133482
  - mTmax: 3004.05
    mTmin: 2809.9
    name: R_13(pp->enu)
    value:
      background_std: 0.19233013273004337
      counts_background: 0.12417994036408388
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.3372273163550168
  - mTmax: 3211.62
    mTmin: 3004.05
    name: R_13(pp->enu)
    value:
      background_std: 0.13940468020741487
      counts_background: 0.08607706688769459
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.213220904042899
  - mTmax: 3433.52
    mTmin: 3211.62
    name: R_13(pp->enu)
    value:
      background_std: 0.10465906608625981
      counts_background: 0.060667793430760786
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.6879888136360206
  - mTmax: 3670.76
    mTmin: 3433.52
    name: R_13(pp->enu)
    value:
      background_std: 0.08095785152351652
      counts_background: 0.04205273168724137
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 6.413200058277911
  - mTmax: 3924.39
    mTmin: 3670.76
    name: R_13(pp->enu)
    value:
      background_std: 0.06416177941570102
      counts_background: 0.029149440623341485
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 11.490881994271946
  - mTmax: 4195.55
    mTmin: 3924.39
    name: R_13(pp->enu)
    value:
      background_std: 0.050197835211499
      counts_background: 0.020205343495236155
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 21.349419121997073
  - mTmax: 4485.44
    mTmin: 4195.55
    name: R_13(pp->enu)
    value:
      background_std: 0.0390590161901452
      counts_background: 0.01987153935881761
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 53.13381329287313
  - mTmax: 4795.36
    mTmin: 4485.44
    name: R_13(pp->enu)
    value:
      background_std: 0.030206657901604487
      counts_background: 0.01987153935881761
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 478.7342235134824

ATLAS pp->mumu 2016:
  experiment: ATLAS
  inspire: ATLAS:2017fih
  values:
  - name: R_13(pp->mumu)
    qmax: 85.54876
    qmin: 80.0
    value:
      background_std: 47159.54161
      counts_background: 6764.512232812854
      counts_total: 826504.0
      distribution: general_gamma_counting_process
      scale_factor: 1.2762305970254551e-06
  - name: R_13(pp->mumu)
    qmax: 91.48239
    qmin: 85.54876
    value:
      background_std: 317634.55716
      counts_background: 14108.902856458606
      counts_total: 5730639.0
      distribution: general_gamma_counting_process
      scale_factor: 1.8178514613498493e-07
  - name: R_13(pp->mumu)
    qmax: 97.82756
    qmin: 91.48239
    value:
      background_std: 221426.46149
      counts_background: 11237.65450078062
      counts_total: 4062661.0
      distribution: general_gamma_counting_process
      scale_factor: 2.580659037125757e-07
  - name: R_13(pp->mumu)
    qmax: 104.61284
    qmin: 97.82756
    value:
      background_std: 23673.1391
      counts_background: 5387.892461379928
      counts_total: 430822.0
      distribution: general_gamma_counting_process
      scale_factor: 2.4936960922852982e-06
  - name: R_13(pp->mumu)
    qmax: 111.86874
    qmin: 104.61284
    value:
      background_std: 8035.54464
      counts_background: 5023.582206650105
      counts_total: 149927.0
      distribution: general_gamma_counting_process
      scale_factor: 7.290369522877894e-06
  - name: R_13(pp->mumu)
    qmax: 119.6279
    qmin: 111.86874
    value:
      background_std: 4269.74216
      counts_background: 5023.582206650105
      counts_total: 82971.0
      distribution: general_gamma_counting_process
      scale_factor: 1.3372407014959593e-05
  - name: R_13(pp->mumu)
    qmax: 127.92524
    qmin: 119.6279
    value:
      background_std: 2723.04212
      counts_background: 4936.420670223463
      counts_total: 54641.0
      distribution: general_gamma_counting_process
      scale_factor: 2.1054688970870164e-05
  - name: R_13(pp->mumu)
    qmax: 136.79808
    qmin: 127.92524
    value:
      background_std: 1948.58465
      counts_background: 4766.608240471557
      counts_total: 39501.0
      distribution: general_gamma_counting_process
      scale_factor: 2.9854648690468575e-05
  - name: R_13(pp->mumu)
    qmax: 146.28633
    qmin: 136.79808
    value:
      background_std: 1473.90656
      counts_background: 4602.637343122306
      counts_total: 29742.0
      distribution: general_gamma_counting_process
      scale_factor: 4.112847100734332e-05
  - name: R_13(pp->mumu)
    qmax: 156.43268
    qmin: 146.28633
    value:
      background_std: 1174.61412
      counts_background: 4291.423265461886
      counts_total: 23871.0
      distribution: general_gamma_counting_process
      scale_factor: 5.222690831812434e-05
  - name: R_13(pp->mumu)
    qmax: 167.28278
    qmin: 156.43268
    value:
      background_std: 929.80497
      counts_background: 4071.901814092623
      counts_total: 18942.0
      distribution: general_gamma_counting_process
      scale_factor: 6.850801569289413e-05
  - name: R_13(pp->mumu)
    qmax: 178.88544
    qmin: 167.28278
    value:
      background_std: 758.69868
      counts_background: 3665.972384998197
      counts_total: 15482.0
      distribution: general_gamma_counting_process
      scale_factor: 8.721354907837495e-05
  - name: R_13(pp->mumu)
    qmax: 191.29285
    qmin: 178.88544
    value:
      background_std: 614.04569
      counts_background: 3300.510213938981
      counts_total: 12495.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00011154601639580714
  - name: R_13(pp->mumu)
    qmax: 204.56084
    qmin: 191.29285
    value:
      background_std: 515.5105
      counts_background: 3023.9480388959396
      counts_total: 10462.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00013751259618992973
  - name: R_13(pp->mumu)
    qmax: 218.74908
    qmin: 204.56084
    value:
      background_std: 419.80357
      counts_background: 2583.224566423371
      counts_total: 8583.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001735423572841351
  - name: R_13(pp->mumu)
    qmax: 233.92142
    qmin: 218.74908
    value:
      background_std: 354.93752
      counts_background: 2245.697995539776
      counts_total: 6868.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00021559836611425865
  - name: R_13(pp->mumu)
    qmax: 250.1461
    qmin: 233.92142
    value:
      background_std: 290.98522
      counts_background: 1918.4001035163626
      counts_total: 5649.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0002731167148073568
  - name: R_13(pp->mumu)
    qmax: 267.49612
    qmin: 250.1461
    value:
      background_std: 247.43115
      counts_background: 1638.8040442129902
      counts_total: 4723.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003374008924078145
  - name: R_13(pp->mumu)
    qmax: 286.04953
    qmin: 267.49612
    value:
      background_std: 201.90089
      counts_background: 1351.799128632837
      counts_total: 3762.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0004203618744570092
  - name: R_13(pp->mumu)
    qmax: 305.8898
    qmin: 286.04953
    value:
      background_std: 167.21174
      counts_background: 1154.7819846894593
      counts_total: 3064.0
      distribution: general_gamma_counting_process
      scale_factor: 0.000505843637474153
  - name: R_13(pp->mumu)
    qmax: 327.10617
    qmin: 305.8898
    value:
      background_std: 140.17541
      counts_background: 952.5441959802893
      counts_total: 2471.0
      distribution: general_gamma_counting_process
      scale_factor: 0.000613240962561096
  - name: R_13(pp->mumu)
    qmax: 349.79411
    qmin: 327.10617
    value:
      background_std: 111.28163
      counts_background: 732.5965428215242
      counts_total: 2031.0
      distribution: general_gamma_counting_process
      scale_factor: 0.000797354458396957
  - name: R_13(pp->mumu)
    qmax: 374.05567
    qmin: 349.79411
    value:
      background_std: 93.29852
      counts_background: 614.9663483614243
      counts_total: 1595.0
      distribution: general_gamma_counting_process
      scale_factor: 0.000976717309835189
  - name: R_13(pp->mumu)
    qmax: 400.0
    qmin: 374.05567
    value:
      background_std: 77.70347
      counts_background: 498.465534451482
      counts_total: 1333.0
      distribution: general_gamma_counting_process
      scale_factor: 0.001204994600221865
  - name: R_13(pp->mumu)
    qmax: 427.74382
    qmin: 400.0
    value:
      background_std: 61.74306
      counts_background: 370.1793275429616
      counts_total: 1018.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0015350528063604598
  - name: R_13(pp->mumu)
    qmax: 457.41193
    qmin: 427.74382
    value:
      background_std: 51.3044
      counts_background: 300.0515993082377
      counts_total: 819.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0018938236520369333
  - name: R_13(pp->mumu)
    qmax: 489.13782
    qmin: 457.41193
    value:
      background_std: 41.50204
      counts_background: 230.76804756031794
      counts_total: 675.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0023960593888305657
  - name: R_13(pp->mumu)
    qmax: 523.06419
    qmin: 489.13782
    value:
      background_std: 33.75002
      counts_background: 168.40359227647843
      counts_total: 508.0
      distribution: general_gamma_counting_process
      scale_factor: 0.002875050419527591
  - name: R_13(pp->mumu)
    qmax: 559.34369
    qmin: 523.06419
    value:
      background_std: 27.85797
      counts_background: 136.50078065460167
      counts_total: 397.0
      distribution: general_gamma_counting_process
      scale_factor: 0.003640757290227692
  - name: R_13(pp->mumu)
    qmax: 598.13951
    qmin: 559.34369
    value:
      background_std: 21.3442
      counts_background: 92.87640686917166
      counts_total: 306.0
      distribution: general_gamma_counting_process
      scale_factor: 0.004706476979947758
  - name: R_13(pp->mumu)
    qmax: 639.6262
    qmin: 598.13951
    value:
      background_std: 17.55967
      counts_background: 79.34019129282822
      counts_total: 252.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0059466057209445556
  - name: R_13(pp->mumu)
    qmax: 683.99038
    qmin: 639.6262
    value:
      background_std: 14.07663
      counts_background: 57.89871417152278
      counts_total: 188.0
      distribution: general_gamma_counting_process
      scale_factor: 0.007549747471335277
  - name: R_13(pp->mumu)
    qmax: 731.43164
    qmin: 683.99038
    value:
      background_std: 10.86199
      counts_background: 39.39482623328838
      counts_total: 129.0
      distribution: general_gamma_counting_process
      scale_factor: 0.009806916300293492
  - name: R_13(pp->mumu)
    qmax: 782.16341
    qmin: 731.43164
    value:
      background_std: 8.62141
      counts_background: 28.249678752902835
      counts_total: 97.0
      distribution: general_gamma_counting_process
      scale_factor: 0.012426627758492669
  - name: R_13(pp->mumu)
    qmax: 836.4139
    qmin: 782.16341
    value:
      background_std: 6.86123
      counts_background: 21.72667376225719
      counts_total: 78.0
      distribution: general_gamma_counting_process
      scale_factor: 0.016545321809072172
  - name: R_13(pp->mumu)
    qmax: 894.42719
    qmin: 836.4139
    value:
      background_std: 5.52516
      counts_background: 14.526539259467864
      counts_total: 57.0
      distribution: general_gamma_counting_process
      scale_factor: 0.02008708102951275
  - name: R_13(pp->mumu)
    qmax: 956.46425
    qmin: 894.42719
    value:
      background_std: 4.55665
      counts_background: 12.851466920699988
      counts_total: 51.0
      distribution: general_gamma_counting_process
      scale_factor: 0.025461293341897798
  - name: R_13(pp->mumu)
    qmax: 1022.80418
    qmin: 956.46425
    value:
      background_std: 3.47985
      counts_background: 9.54398459640824
      counts_total: 39.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0334998929733532
  - name: R_13(pp->mumu)
    qmax: 1093.74541
    qmin: 1022.80418
    value:
      background_std: 2.75975
      counts_background: 7.469831593577929
      counts_total: 29.0
      distribution: general_gamma_counting_process
      scale_factor: 0.044837372096784914
  - name: R_13(pp->mumu)
    qmax: 1169.6071
    qmin: 1093.74541
    value:
      background_std: 2.17145
      counts_background: 4.822553197387249
      counts_total: 18.0
      distribution: general_gamma_counting_process
      scale_factor: 0.05915717390694639
  - name: R_13(pp->mumu)
    qmax: 1250.73051
    qmin: 1169.6071
    value:
      background_std: 1.68286
      counts_background: 3.168433486401449
      counts_total: 18.0
      distribution: general_gamma_counting_process
      scale_factor: 0.07712113092077916
  - name: R_13(pp->mumu)
    qmax: 1337.48061
    qmin: 1250.73051
    value:
      background_std: 1.32923
      counts_background: 3.2243779751696438
      counts_total: 14.0
      distribution: general_gamma_counting_process
      scale_factor: 0.10633648600532984
  - name: R_13(pp->mumu)
    qmax: 1430.24766
    qmin: 1337.48061
    value:
      background_std: 0.87866
      counts_background: 1.0156796632709002
      counts_total: 12.0
      distribution: general_gamma_counting_process
      scale_factor: 0.14294159630178704
  - name: R_13(pp->mumu)
    qmax: 1529.44898
    qmin: 1430.24766
    value:
      background_std: 0.66988
      counts_background: 0.6910779352492378
      counts_total: 5.0
      distribution: general_gamma_counting_process
      scale_factor: 0.1939725971420614
  - name: R_13(pp->mumu)
    qmax: 1635.53087
    qmin: 1529.44898
    value:
      background_std: 0.55593
      counts_background: 0.7542820691954563
      counts_total: 4.0
      distribution: general_gamma_counting_process
      scale_factor: 0.2562541562784672
  - name: R_13(pp->mumu)
    qmax: 1748.97054
    qmin: 1635.53087
    value:
      background_std: 0.40035
      counts_background: 0.5043159487171365
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 0.3676386752489595
  - name: R_13(pp->mumu)
    qmax: 1870.27835
    qmin: 1748.97054
    value:
      background_std: 0.27387
      counts_background: 0.16451905877536685
      counts_total: 4.0
      distribution: general_gamma_counting_process
      scale_factor: 0.5117948254787213
  - name: R_13(pp->mumu)
    qmax: 2000.0
    qmin: 1870.27835
    value:
      background_std: 0.22103
      counts_background: 0.2417942372278825
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 0.7060929175913717
  - name: R_13(pp->mumu)
    qmax: 2138.71909
    qmin: 2000.0
    value:
      background_std: 0.15372
      counts_background: 0.0802713950670074
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.9724792218029669
  - name: R_13(pp->mumu)
    qmax: 2287.05967
    qmin: 2138.71909
    value:
      background_std: 0.11179
      counts_background: 0.05756190191731741
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.4083745391102105
  - name: R_13(pp->mumu)
    qmax: 2445.68909
    qmin: 2287.05967
    value:
      background_std: 0.08209
      counts_background: 0.042005949972813435
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.0044780091476864
  - name: R_13(pp->mumu)
    qmax: 2615.32097
    qmin: 2445.68909
    value:
      background_std: 0.05988
      counts_background: 0.031746012958316444
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.91733963386076
  - name: R_13(pp->mumu)
    qmax: 2796.71844
    qmin: 2615.32097
    value:
      background_std: 0.0421
      counts_background: 0.01781741085520469
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 4.2993953037780495
  - name: R_13(pp->mumu)
    qmax: 2990.69756
    qmin: 2796.71844
    value:
      background_std: 0.02913
      counts_background: 0.010914573172176702
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 6.510226547571808
  - name: R_13(pp->mumu)
    qmax: 3198.13098
    qmin: 2990.69756
    value:
      background_std: 0.02102
      counts_background: 0.007426377591989643
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 9.568102771607448
  - name: R_13(pp->mumu)
    qmax: 3419.95189
    qmin: 3198.13098
    value:
      background_std: 0.01555
      counts_background: 0.004316533692595911
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 13.662409300684185
  - name: R_13(pp->mumu)
    qmax: 3657.1582
    qmin: 3419.95189
    value:
      background_std: 0.01023
      counts_background: 0.002553257372458486
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 21.850209058054062
  - name: R_13(pp->mumu)
    qmax: 3910.81703
    qmin: 3657.1582
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 34.656276448131415
  - name: R_13(pp->mumu)
    qmax: 4182.06952
    qmin: 3910.81703
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 49.54781272142746
  - name: R_13(pp->mumu)
    qmax: 4472.13595
    qmin: 4182.06952
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 87.46816282633966
  - name: R_13(pp->mumu)
    qmax: 4782.32127
    qmin: 4472.13595
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 121.93859151255853
  - name: R_13(pp->mumu)
    qmax: 5114.0209
    qmin: 4782.32127
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 262.2375145176054
  - name: R_13(pp->mumu)
    qmax: 5468.72706
    qmin: 5114.0209
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 343.38755161998483
  - name: R_13(pp->mumu)
    qmax: 5848.03548
    qmin: 5468.72706
    value:
      counts_background: 0.001799150805370723
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2617.913300405422

ATLAS pp->mumu 2019:
  experiment: ATLAS
  inspire: ATLAS:2019erb
  values:
  - name: R_13(pp->mumu)
    qmax: 135.0803
    qmin: 130.0015
    value:
      background_std: 4367.714595558474
      counts_background: 10153.696651035758
      counts_total: 88900.72505429288
      distribution: general_gamma_counting_process
      scale_factor: 1.3369345962892415e-05
  - name: R_13(pp->mumu)
    qmax: 140.3576
    qmin: 135.0803
    value:
      background_std: 3723.6485839727693
      counts_background: 9920.127401610305
      counts_total: 76010.57790325048
      distribution: general_gamma_counting_process
      scale_factor: 1.5898981787757855e-05
  - name: R_13(pp->mumu)
    qmax: 145.841
    qmin: 140.3576
    value:
      background_std: 3236.9080720913894
      counts_background: 9683.799805626148
      counts_total: 65457.24010408282
      distribution: general_gamma_counting_process
      scale_factor: 1.8539400928576078e-05
  - name: R_13(pp->mumu)
    qmax: 151.5373
    qmin: 145.841
    value:
      background_std: 2806.1162240248427
      counts_background: 9324.157636961534
      counts_total: 57192.287720319844
      distribution: general_gamma_counting_process
      scale_factor: 2.1715730499541426e-05
  - name: R_13(pp->mumu)
    qmax: 157.4575
    qmin: 151.5373
    value:
      background_std: 2450.637008789551
      counts_background: 8977.872052703644
      counts_total: 50650.36549548864
      distribution: general_gamma_counting_process
      scale_factor: 2.527844696386039e-05
  - name: R_13(pp->mumu)
    qmax: 163.609
    qmin: 157.4575
    value:
      background_std: 2164.498903030556
      counts_background: 8610.873404427524
      counts_total: 44624.60130125474
      distribution: general_gamma_counting_process
      scale_factor: 2.906361503952766e-05
  - name: R_13(pp->mumu)
    qmax: 170.0008
    qmin: 163.609
    value:
      background_std: 1920.222298832865
      counts_background: 8258.876975724814
      counts_total: 39180.94686790684
      distribution: general_gamma_counting_process
      scale_factor: 3.334107023836068e-05
  - name: R_13(pp->mumu)
    qmax: 176.6408
    qmin: 170.0008
    value:
      background_std: 1705.1502447211092
      counts_background: 7853.265009112155
      counts_total: 35224.766877306836
      distribution: general_gamma_counting_process
      scale_factor: 3.819525942378966e-05
  - name: R_13(pp->mumu)
    qmax: 183.5417
    qmin: 176.6408
    value:
      background_std: 1545.617453400506
      counts_background: 7424.961349684826
      counts_total: 31434.531451849627
      distribution: general_gamma_counting_process
      scale_factor: 4.271296549700928e-05
  - name: R_13(pp->mumu)
    qmax: 190.7122
    qmin: 183.5417
    value:
      background_std: 1361.6390035916802
      counts_background: 6991.151557647795
      counts_total: 28236.813106458783
      distribution: general_gamma_counting_process
      scale_factor: 4.964223066989248e-05
  - name: R_13(pp->mumu)
    qmax: 198.1629
    qmin: 190.7122
    value:
      background_std: 1253.7405021521731
      counts_background: 6573.151233593104
      counts_total: 25356.64657165797
      distribution: general_gamma_counting_process
      scale_factor: 5.453267356084372e-05
  - name: R_13(pp->mumu)
    qmax: 205.9028
    qmin: 198.1629
    value:
      background_std: 1098.3565690535725
      counts_background: 6075.875574996823
      counts_total: 22526.59594090615
      distribution: general_gamma_counting_process
      scale_factor: 6.384475962493046e-05
  - name: R_13(pp->mumu)
    qmax: 213.9394
    qmin: 205.9028
    value:
      background_std: 992.7290459400999
      counts_background: 5695.190813520244
      counts_total: 20180.31199254282
      distribution: general_gamma_counting_process
      scale_factor: 7.214698475492765e-05
  - name: R_13(pp->mumu)
    qmax: 222.2975
    qmin: 213.9394
    value:
      background_std: 896.1748902043114
      counts_background: 5283.247892779931
      counts_total: 17982.10623060412
      distribution: general_gamma_counting_process
      scale_factor: 8.169694585037675e-05
  - name: R_13(pp->mumu)
    qmax: 230.9902
    qmin: 222.2975
    value:
      background_std: 809.212231286829
      counts_background: 4847.175690441768
      counts_total: 15899.124773315576
      distribution: general_gamma_counting_process
      scale_factor: 9.223170235446104e-05
  - name: R_13(pp->mumu)
    qmax: 240.0039
    qmin: 230.9902
    value:
      background_std: 730.8420363763416
      counts_background: 4424.41975182121
      counts_total: 14358.798423966993
      distribution: general_gamma_counting_process
      scale_factor: 0.00010455881400980028
  - name: R_13(pp->mumu)
    qmax: 249.3802
    qmin: 240.0039
    value:
      background_std: 664.432089671552
      counts_background: 4088.453093853648
      counts_total: 12706.672555008621
      distribution: general_gamma_counting_process
      scale_factor: 0.00011802003228863011
  - name: R_13(pp->mumu)
    qmax: 259.1229
    qmin: 249.3802
    value:
      background_std: 600.9116491230056
      counts_background: 3744.4206371814294
      counts_total: 11581.632690063301
      distribution: general_gamma_counting_process
      scale_factor: 0.0001333523043133782
  - name: R_13(pp->mumu)
    qmax: 269.2462
    qmin: 259.1229
    value:
      background_std: 539.5037438901195
      counts_background: 3366.338860568191
      counts_total: 10445.632978001702
      distribution: general_gamma_counting_process
      scale_factor: 0.00014984999260907078
  - name: R_13(pp->mumu)
    qmax: 279.7625
    qmin: 269.2462
    value:
      background_std: 481.7766655760301
      counts_background: 3059.168629698733
      counts_total: 9214.883837706684
      distribution: general_gamma_counting_process
      scale_factor: 0.00016956358618142945
  - name: R_13(pp->mumu)
    qmax: 290.6922
    qmin: 279.7625
    value:
      background_std: 430.5313825812963
      counts_background: 2760.3694805902355
      counts_total: 8289.496742318039
      distribution: general_gamma_counting_process
      scale_factor: 0.00019086688158066704
  - name: R_13(pp->mumu)
    qmax: 302.0488
    qmin: 290.6922
    value:
      background_std: 382.42825286878207
      counts_background: 2464.6658255028965
      counts_total: 7120.62776904233
      distribution: general_gamma_counting_process
      scale_factor: 0.00021569582037502934
  - name: R_13(pp->mumu)
    qmax: 313.8491
    qmin: 302.0488
    value:
      background_std: 342.57338424915906
      counts_background: 2201.4790502153915
      counts_total: 6484.727335344805
      distribution: general_gamma_counting_process
      scale_factor: 0.00024349719192928918
  - name: R_13(pp->mumu)
    qmax: 326.1076
    qmin: 313.8491
    value:
      background_std: 306.1004050678098
      counts_background: 1973.3103565915962
      counts_total: 5623.509795073417
      distribution: general_gamma_counting_process
      scale_factor: 0.0002770729480361409
  - name: R_13(pp->mumu)
    qmax: 338.8478
    qmin: 326.1076
    value:
      background_std: 274.4678706684229
      counts_background: 1738.0193631550799
      counts_total: 5011.715548434577
      distribution: general_gamma_counting_process
      scale_factor: 0.0003121084865743795
  - name: R_13(pp->mumu)
    qmax: 352.0857
    qmin: 338.8478
    value:
      background_std: 246.51840584259045
      counts_background: 1541.8025161604032
      counts_total: 4362.237611319943
      distribution: general_gamma_counting_process
      scale_factor: 0.0003524922041136547
  - name: R_13(pp->mumu)
    qmax: 365.8409
    qmin: 352.0857
    value:
      background_std: 218.9502659152475
      counts_background: 1359.5182059940296
      counts_total: 3844.4448328256917
      distribution: general_gamma_counting_process
      scale_factor: 0.00040421316902894167
  - name: R_13(pp->mumu)
    qmax: 380.13
    qmin: 365.8409
    value:
      background_std: 198.62327140570002
      counts_background: 1216.8477789335761
      counts_total: 3373.409872220816
      distribution: general_gamma_counting_process
      scale_factor: 0.00045262155049093436
  - name: R_13(pp->mumu)
    qmax: 394.9808
    qmin: 380.13
    value:
      background_std: 175.62174603822345
      counts_background: 1043.1137252969772
      counts_total: 3075.199782381399
      distribution: general_gamma_counting_process
      scale_factor: 0.000515346199953781
  - name: R_13(pp->mumu)
    qmax: 410.3972
    qmin: 394.9808
    value:
      background_std: 157.82332196945347
      counts_background: 922.5295789032424
      counts_total: 2715.0409331261626
      distribution: general_gamma_counting_process
      scale_factor: 0.0005820924460894944
  - name: R_13(pp->mumu)
    qmax: 426.4304
    qmin: 410.3972
    value:
      background_std: 139.44109301019662
      counts_background: 785.8839723326984
      counts_total: 2332.826720881545
      distribution: general_gamma_counting_process
      scale_factor: 0.0006613531407923803
  - name: R_13(pp->mumu)
    qmax: 443.0861
    qmin: 426.4304
    value:
      background_std: 124.04574505049224
      counts_background: 681.5390372117919
      counts_total: 2039.7505842876824
      distribution: general_gamma_counting_process
      scale_factor: 0.0007495824096508766
  - name: R_13(pp->mumu)
    qmax: 460.3964
    qmin: 443.0861
    value:
      background_std: 111.28258332313048
      counts_background: 610.0170339986892
      counts_total: 1788.8091733167446
      distribution: general_gamma_counting_process
      scale_factor: 0.0008536029653024192
  - name: R_13(pp->mumu)
    qmax: 478.383
    qmin: 460.3964
    value:
      background_std: 97.82425788700547
      counts_background: 511.9471693577202
      counts_total: 1591.9518481111725
      distribution: general_gamma_counting_process
      scale_factor: 0.0009710101550714133
  - name: R_13(pp->mumu)
    qmax: 497.0722
    qmin: 478.383
    value:
      background_std: 86.22812946786841
      counts_background: 425.82508654016516
      counts_total: 1382.6905097402805
      distribution: general_gamma_counting_process
      scale_factor: 0.001099342257951573
  - name: R_13(pp->mumu)
    qmax: 516.4871
    qmin: 497.0722
    value:
      background_std: 77.02205107162364
      counts_background: 371.91640457090034
      counts_total: 1222.3381474622556
      distribution: general_gamma_counting_process
      scale_factor: 0.0012509665545845244
  - name: R_13(pp->mumu)
    qmax: 536.665
    qmin: 516.4871
    value:
      background_std: 68.00617861258111
      counts_background: 316.1517695027948
      counts_total: 1035.5403586009006
      distribution: general_gamma_counting_process
      scale_factor: 0.0014293298020503268
  - name: R_13(pp->mumu)
    qmax: 557.6312
    qmin: 536.665
    value:
      background_std: 60.25531747065475
      counts_background: 272.38180747053616
      counts_total: 862.5866633691002
      distribution: general_gamma_counting_process
      scale_factor: 0.001634083003692843
  - name: R_13(pp->mumu)
    qmax: 579.4164
    qmin: 557.6312
    value:
      background_std: 52.793463587154974
      counts_background: 228.33065305467525
      counts_total: 747.601121084075
      distribution: general_gamma_counting_process
      scale_factor: 0.0018718853685534508
  - name: R_13(pp->mumu)
    qmax: 602.0475
    qmin: 579.4164
    value:
      background_std: 46.77168397340796
      counts_background: 196.7191772412662
      counts_total: 657.3050925583041
      distribution: general_gamma_counting_process
      scale_factor: 0.00213247365713196
  - name: R_13(pp->mumu)
    qmax: 625.568
    qmin: 602.0475
    value:
      background_std: 41.17478142754923
      counts_background: 165.58547765970255
      counts_total: 589.5395359110807
      distribution: general_gamma_counting_process
      scale_factor: 0.0024248550694873027
  - name: R_13(pp->mumu)
    qmax: 650.0075
    qmin: 625.568
    value:
      background_std: 35.59135332143866
      counts_background: 134.43853087762895
      counts_total: 518.7695788389075
      distribution: general_gamma_counting_process
      scale_factor: 0.0027999949465572094
  - name: R_13(pp->mumu)
    qmax: 675.4017
    qmin: 650.0075
    value:
      background_std: 31.50592338622992
      counts_background: 116.90036706652529
      counts_total: 433.31443806054205
      distribution: general_gamma_counting_process
      scale_factor: 0.0032173646200448825
  - name: R_13(pp->mumu)
    qmax: 701.7818
    qmin: 675.4017
    value:
      background_std: 27.701379510691396
      counts_background: 96.68738128971845
      counts_total: 381.29817398945477
      distribution: general_gamma_counting_process
      scale_factor: 0.0036835961056184263
  - name: R_13(pp->mumu)
    qmax: 729.1987
    qmin: 701.7818
    value:
      background_std: 24.413852558671156
      counts_background: 80.78505166867615
      counts_total: 320.4749513348551
      distribution: general_gamma_counting_process
      scale_factor: 0.004224823661838057
  - name: R_13(pp->mumu)
    qmax: 757.6867
    qmin: 729.1987
    value:
      background_std: 21.289903046275185
      counts_background: 65.68939614857862
      counts_total: 242.93407215642299
      distribution: general_gamma_counting_process
      scale_factor: 0.0048782033266619364
  - name: R_13(pp->mumu)
    qmax: 787.2599
    qmin: 757.6867
    value:
      background_std: 18.6305451577818
      counts_background: 55.191921686106184
      counts_total: 210.5823218507958
      distribution: general_gamma_counting_process
      scale_factor: 0.005685927149368299
  - name: R_13(pp->mumu)
    qmax: 818.0378
    qmin: 787.2599
    value:
      background_std: 16.536662591150815
      counts_background: 46.44635626445527
      counts_total: 188.9874425158228
      distribution: general_gamma_counting_process
      scale_factor: 0.006526492268644452
  - name: R_13(pp->mumu)
    qmax: 849.9666
    qmin: 818.0378
    value:
      background_std: 14.505819605441038
      counts_background: 38.80428814755235
      counts_total: 159.5758369534162
      distribution: general_gamma_counting_process
      scale_factor: 0.007561327447535445
  - name: R_13(pp->mumu)
    qmax: 883.1727
    qmin: 849.9666
    value:
      background_std: 12.69398206148668
      counts_background: 31.799772094128638
      counts_total: 132.1149124444831
      distribution: general_gamma_counting_process
      scale_factor: 0.008728608670103418
  - name: R_13(pp->mumu)
    qmax: 917.6761
    qmin: 883.1727
    value:
      background_std: 10.96013593066989
      counts_background: 26.36362907327209
      counts_total: 130.16374355967136
      distribution: general_gamma_counting_process
      scale_factor: 0.010091307273161725
  - name: R_13(pp->mumu)
    qmax: 953.5275
    qmin: 917.6761
    value:
      background_std: 9.558654105300288
      counts_background: 23.380122492950765
      counts_total: 97.83393914976413
      distribution: general_gamma_counting_process
      scale_factor: 0.011737486789007353
  - name: R_13(pp->mumu)
    qmax: 990.7707
    qmin: 953.5275
    value:
      background_std: 8.116619876003165
      counts_background: 18.38640506850625
      counts_total: 98.80166798124685
      distribution: general_gamma_counting_process
      scale_factor: 0.013692105390868953
  - name: R_13(pp->mumu)
    qmax: 1029.4777
    qmin: 990.7707
    value:
      background_std: 6.987043676362929
      counts_background: 15.21189421824547
      counts_total: 81.18051581971463
      distribution: general_gamma_counting_process
      scale_factor: 0.0160710899719232
  - name: R_13(pp->mumu)
    qmax: 1069.6969
    qmin: 1029.4777
    value:
      background_std: 6.10507820981051
      counts_background: 12.588360806599598
      counts_total: 55.71446901078137
      distribution: general_gamma_counting_process
      scale_factor: 0.018679890606014583
  - name: R_13(pp->mumu)
    qmax: 1111.4873
    qmin: 1069.6969
    value:
      background_std: 5.299848780346374
      counts_background: 10.187765038978078
      counts_total: 59.63166441063757
      distribution: general_gamma_counting_process
      scale_factor: 0.02213925417038206
  - name: R_13(pp->mumu)
    qmax: 1154.9002
    qmin: 1111.4873
    value:
      background_std: 4.704235571766579
      counts_background: 8.771953096827428
      counts_total: 36.14199722366014
      distribution: general_gamma_counting_process
      scale_factor: 0.025995727241749172
  - name: R_13(pp->mumu)
    qmax: 1200.0193
    qmin: 1154.9002
    value:
      background_std: 4.109596900305143
      counts_background: 6.286152008579877
      counts_total: 24.408232244793
      distribution: general_gamma_counting_process
      scale_factor: 0.029524140097346323
  - name: R_13(pp->mumu)
    qmax: 1246.9012
    qmin: 1200.0193
    value:
      background_std: 3.5014741416758075
      counts_background: 5.241049219066606
      counts_total: 36.14199722366014
      distribution: general_gamma_counting_process
      scale_factor: 0.035347463724205386
  - name: R_13(pp->mumu)
    qmax: 1295.6146
    qmin: 1246.9012
    value:
      background_std: 2.923171595185668
      counts_background: 4.2503303733331395
      counts_total: 31.25014888621801
      distribution: general_gamma_counting_process
      scale_factor: 0.04219771056355407
  - name: R_13(pp->mumu)
    qmax: 1346.2192
    qmin: 1295.6146
    value:
      background_std: 2.512368538459842
      counts_background: 3.8819983776243974
      counts_total: 20.49594947779133
      distribution: general_gamma_counting_process
      scale_factor: 0.05045499969815339
  - name: R_13(pp->mumu)
    qmax: 1398.8127
    qmin: 1346.2192
    value:
      background_std: 2.1871160372659273
      counts_background: 3.1071352035118855
      counts_total: 25.38742792567412
      distribution: general_gamma_counting_process
      scale_factor: 0.058682989749848556
  - name: R_13(pp->mumu)
    qmax: 1453.4609
    qmin: 1398.8127
    value:
      background_std: 1.9142288225378918
      counts_background: 2.9117906481200126
      counts_total: 11.704138361564704
      distribution: general_gamma_counting_process
      scale_factor: 0.07044473007349586
  - name: R_13(pp->mumu)
    qmax: 1510.244
    qmin: 1453.4609
    value:
      background_std: 1.6109747804279697
      counts_background: 1.9734458718273507
      counts_total: 16.58737946413429
      distribution: general_gamma_counting_process
      scale_factor: 0.08351175322357265
  - name: R_13(pp->mumu)
    qmax: 1569.2317
    qmin: 1510.244
    value:
      background_std: 1.3596667617093998
      counts_background: 1.5622776588617944
      counts_total: 10.726629870436735
      distribution: general_gamma_counting_process
      scale_factor: 0.09998835035230029
  - name: R_13(pp->mumu)
    qmax: 1630.4802
    qmin: 1569.2317
    value:
      background_std: 1.1753244807757732
      counts_background: 1.487705918173613
      counts_total: 9.749338664649121
      distribution: general_gamma_counting_process
      scale_factor: 0.12016774811866186
  - name: R_13(pp->mumu)
    qmax: 1694.1791
    qmin: 1630.4802
    value:
      background_std: 0.9528937034579805
      counts_background: 0.8356622771025878
      counts_total: 2.91991134349133
      distribution: general_gamma_counting_process
      scale_factor: 0.14378400198027075
  - name: R_13(pp->mumu)
    qmax: 1760.3666
    qmin: 1694.1791
    value:
      background_std: 0.8251118128615457
      counts_background: 0.8674311841250307
      counts_total: 4.869751887632895
      distribution: general_gamma_counting_process
      scale_factor: 0.17429670890943472
  - name: R_13(pp->mumu)
    qmax: 1829.1236
    qmin: 1760.3666
    value:
      background_std: 0.6958565863982882
      counts_background: 0.6821581505907652
      counts_total: 3.8954990733880965
      distribution: general_gamma_counting_process
      scale_factor: 0.20969017935423678
  - name: R_13(pp->mumu)
    qmax: 1900.583
    qmin: 1829.1236
    value:
      background_std: 0.5899493142426738
      counts_background: 0.5239969594953287
      counts_total: 6.821945865342037
      distribution: general_gamma_counting_process
      scale_factor: 0.24977990391086993
  - name: R_13(pp->mumu)
    qmax: 1974.8342
    qmin: 1900.583
    value:
      background_std: 0.49092823052342044
      counts_background: 0.43885114767648925
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 0.30756292961115134
  - name: R_13(pp->mumu)
    qmax: 2051.9861
    qmin: 1974.8342
    value:
      background_std: 0.4291881334049234
      counts_background: 0.48162812476032607
      counts_total: 3.8954990733880965
      distribution: general_gamma_counting_process
      scale_factor: 0.37647180044702155
  - name: R_13(pp->mumu)
    qmax: 2132.1334
    qmin: 2051.9861
    value:
      background_std: 0.3343365638196021
      counts_background: 0.19462746985675
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 0.4582338738034427
  - name: R_13(pp->mumu)
    qmax: 2215.4306
    qmin: 2132.1334
    value:
      background_std: 0.2857824733113037
      counts_background: 0.19526708767209217
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 0.5618019999396292
  - name: R_13(pp->mumu)
    qmax: 2301.9821
    qmin: 2215.4306
    value:
      background_std: 0.23116537164941736
      counts_background: 0.12643808270036044
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 0.6987736111706894
  - name: R_13(pp->mumu)
    qmax: 2391.9149
    qmin: 2301.9821
    value:
      background_std: 0.20089826500598856
      counts_background: 0.1576924633211208
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 0.8585327857157209
  - name: R_13(pp->mumu)
    qmax: 2485.3393
    qmin: 2391.9149
    value:
      background_std: 0.15887986626290038
      counts_background: 0.08480789327041269
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 1.069515278976801
  - name: R_13(pp->mumu)
    qmax: 2582.4354
    qmin: 2485.3393
    value:
      background_std: 0.1410858145400934
      counts_background: 0.11418425270635946
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.301972263055654
  - name: R_13(pp->mumu)
    qmax: 2683.3248
    qmin: 2582.4354
    value:
      background_std: 0.1068676666450574
      counts_background: 0.04961113093891317
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.668772913396739
  - name: R_13(pp->mumu)
    qmax: 2788.1558
    qmin: 2683.3248
    value:
      background_std: 0.09165593554507097
      counts_background: 0.04562408445467029
      counts_total: 0.9718367624821219
      distribution: general_gamma_counting_process
      scale_factor: 2.0212804689349286
  - name: R_13(pp->mumu)
    qmax: 2897.0567
    qmin: 2788.1558
    value:
      background_std: 0.07266099936407698
      counts_background: 0.029852647397427517
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.5884432174257777
  - name: R_13(pp->mumu)
    qmax: 3010.2376
    qmin: 2897.0567
    value:
      background_std: 0.05937261374480347
      counts_background: 0.02305575282997262
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.2616513664606708
  - name: R_13(pp->mumu)
    qmax: 3127.7298
    qmin: 3010.2376
    value:
      background_std: 0.048897651723779155
      counts_background: 0.021533828672332694
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 4.14712944045477
  - name: R_13(pp->mumu)
    qmax: 3249.9226
    qmin: 3127.7298
    value:
      background_std: 0.04053363372415464
      counts_background: 0.014452558190829348
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 5.109370450736852
  - name: R_13(pp->mumu)
    qmax: 3376.8593
    qmin: 3249.9226
    value:
      background_std: 0.032884110998414366
      counts_background: 0.011636818292003148
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 6.541208558341123
  - name: R_13(pp->mumu)
    qmax: 3508.785
    qmin: 3376.8593
    value:
      background_std: 0.02567529578701084
      counts_background: 0.00767366729706161
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 8.535774507148146
  - name: R_13(pp->mumu)
    qmax: 3645.8646
    qmin: 3508.785
    value:
      background_std: 0.021258406573862562
      counts_background: 0.006780896151680328
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 10.678887754304286
  - name: R_13(pp->mumu)
    qmax: 3788.2997
    qmin: 3645.8646
    value:
      background_std: 0.017022424340037038
      counts_background: 0.005546717917897577
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 13.776294316278825
  - name: R_13(pp->mumu)
    qmax: 3936.2646
    qmin: 3788.2997
    value:
      background_std: 0.013641616891697666
      counts_background: 0.003463470453841179
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 17.526333510275986
  - name: R_13(pp->mumu)
    qmax: 4090.0448
    qmin: 3936.2646
    value:
      background_std: 0.011398526264329106
      counts_background: 0.0031503203861262606
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 21.973882965269826
  - name: R_13(pp->mumu)
    qmax: 4249.8329
    qmin: 4090.0448
    value:
      counts_background: 0.002082335478877652
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 29.205209784669062
  - name: R_13(pp->mumu)
    qmax: 4415.8634
    qmin: 4249.8329
    value:
      counts_background: 0.0017217578499394992
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 38.16374407614321
  - name: R_13(pp->mumu)
    qmax: 4588.34
    qmin: 4415.8634
    value:
      counts_background: 0.0012556895280845621
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 46.82189531633008
  - name: R_13(pp->mumu)
    qmax: 4767.5952
    qmin: 4588.34
    value:
      counts_background: 0.0010416661644099543
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 64.27197320998265
  - name: R_13(pp->mumu)
    qmax: 4953.8535
    qmin: 4767.5952
    value:
      counts_background: 0.0011258892192544847
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 81.1673764868627
  - name: R_13(pp->mumu)
    qmax: 5147.3884
    qmin: 4953.8535
    value:
      counts_background: 0.0005170426780294539
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 99.92773150300667
  - name: R_13(pp->mumu)
    qmax: 5348.4372
    qmin: 5147.3884
    value:
      counts_background: 0.0005607270986205246
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 132.74348458839472
  - name: R_13(pp->mumu)
    qmax: 5557.3875
    qmin: 5348.4372
    value:
      counts_background: 0.00027014231729417554
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 162.634233307347
  - name: R_13(pp->mumu)
    qmax: 5774.5011
    qmin: 5557.3875
    value:
      counts_background: 0.00021044257812091968
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 217.6082875120953
  - name: R_13(pp->mumu)
    qmax: 5999.885
    qmin: 5774.5011
    value:
      counts_background: 0.0009004009617230382
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 55.02608893905476

ATLAS pp->munu 2019:
  experiment: ATLAS
  inspire: ATLAS:2019lsy
  values:
  - mTmax: 119.581
    mTmin: 110.0
    name: R_13(pp->munu)
    value:
      background_std: 173393.2448460692
      counts_background: 311864.19556950964
      counts_total: 2194000.0
      distribution: general_gamma_counting_process
      scale_factor: 6.183558551333135e-07
  - mTmax: 129.997
    mTmin: 119.581
    name: R_13(pp->munu)
    value:
      background_std: 185347.68842526848
      counts_background: 334965.4391578278
      counts_total: 2235920.0
      distribution: general_gamma_counting_process
      scale_factor: 6.139253383650937e-07
  - mTmax: 141.32
    mTmin: 129.997
    name: R_13(pp->munu)
    value:
      background_std: 137086.69374739804
      counts_background: 275204.2727846906
      counts_total: 1532830.0
      distribution: general_gamma_counting_process
      scale_factor: 9.30843667032931e-07
  - mTmax: 153.63
    mTmin: 141.32
    name: R_13(pp->munu)
    value:
      background_std: 90970.90353681444
      counts_background: 210511.51756797262
      counts_total: 980250.0
      distribution: general_gamma_counting_process
      scale_factor: 1.4960178814318527e-06
  - mTmax: 167.011
    mTmin: 153.63
    name: R_13(pp->munu)
    value:
      background_std: 55187.39413924524
      counts_background: 158175.03201538566
      counts_total: 612905.0
      distribution: general_gamma_counting_process
      scale_factor: 2.5367232855516335e-06
  - mTmax: 181.558
    mTmin: 167.011
    name: R_13(pp->munu)
    value:
      background_std: 32400.733223956522
      counts_background: 116745.83059004245
      counts_total: 389728.0
      distribution: general_gamma_counting_process
      scale_factor: 4.11468330741908e-06
  - mTmax: 197.372
    mTmin: 181.558
    name: R_13(pp->munu)
    value:
      background_std: 18816.999329162023
      counts_background: 86167.76482670868
      counts_total: 256420.0
      distribution: general_gamma_counting_process
      scale_factor: 6.562284233727933e-06
  - mTmax: 214.564
    mTmin: 197.372
    name: R_13(pp->munu)
    value:
      background_std: 11001.560721747801
      counts_background: 62472.61068447967
      counts_total: 172285.0
      distribution: general_gamma_counting_process
      scale_factor: 9.856474323178904e-06
  - mTmax: 233.253
    mTmin: 214.564
    name: R_13(pp->munu)
    value:
      background_std: 6787.890162959327
      counts_background: 45293.354116629445
      counts_total: 119462.0
      distribution: general_gamma_counting_process
      scale_factor: 1.4412265253190765e-05
  - mTmax: 253.57
    mTmin: 233.253
    name: R_13(pp->munu)
    value:
      background_std: 4482.559073112255
      counts_background: 32256.75604219662
      counts_total: 83461.0
      distribution: general_gamma_counting_process
      scale_factor: 2.0236995712824706e-05
  - mTmax: 275.657
    mTmin: 253.57
    name: R_13(pp->munu)
    value:
      background_std: 3092.594300793429
      counts_background: 22565.672240758515
      counts_total: 59443.0
      distribution: general_gamma_counting_process
      scale_factor: 2.8091111352459282e-05
  - mTmax: 299.667
    mTmin: 275.657
    name: R_13(pp->munu)
    value:
      background_std: 2144.445723415727
      counts_background: 15786.136802201023
      counts_total: 42137.0
      distribution: general_gamma_counting_process
      scale_factor: 4.0155157629817596e-05
  - mTmax: 325.769
    mTmin: 299.667
    name: R_13(pp->munu)
    value:
      background_std: 1511.5214055146557
      counts_background: 10847.878881784714
      counts_total: 30145.0
      distribution: general_gamma_counting_process
      scale_factor: 5.361211781724731e-05
  - mTmax: 354.144
    mTmin: 325.769
    name: R_13(pp->munu)
    value:
      background_std: 1062.6283559947005
      counts_background: 7322.429051619332
      counts_total: 21500.0
      distribution: general_gamma_counting_process
      scale_factor: 7.30621477165014e-05
  - mTmax: 384.991
    mTmin: 354.144
    name: R_13(pp->munu)
    value:
      background_std: 748.9523747775957
      counts_background: 4942.71440530476
      counts_total: 15241.0
      distribution: general_gamma_counting_process
      scale_factor: 9.980396350154575e-05
  - mTmax: 418.524
    mTmin: 384.991
    name: R_13(pp->munu)
    value:
      background_std: 559.2949933845287
      counts_background: 3336.382711281383
      counts_total: 10752.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00013312926976211077
  - mTmax: 454.979
    mTmin: 418.524
    name: R_13(pp->munu)
    value:
      background_std: 421.42780851011713
      counts_background: 2212.21629107045
      counts_total: 7843.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001859921295859557
  - mTmax: 494.609
    mTmin: 454.979
    name: R_13(pp->munu)
    value:
      background_std: 321.7383409908742
      counts_background: 1440.856366006565
      counts_total: 5457.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00024623862733648454
  - mTmax: 537.69
    mTmin: 494.609
    name: R_13(pp->munu)
    value:
      background_std: 239.9465672188081
      counts_background: 938.4557359249345
      counts_total: 4013.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00034358157741364064
  - mTmax: 584.525
    mTmin: 537.69
    name: R_13(pp->munu)
    value:
      background_std: 183.88702799447276
      counts_background: 611.2331451408502
      counts_total: 2761.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0004695043536296467
  - mTmax: 635.438
    mTmin: 584.525
    name: R_13(pp->munu)
    value:
      background_std: 138.2081337259135
      counts_background: 412.5886164536204
      counts_total: 2050.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0006495279550335438
  - mTmax: 690.786
    mTmin: 635.438
    name: R_13(pp->munu)
    value:
      background_std: 104.31690520855189
      counts_background: 259.2943797404666
      counts_total: 1401.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0008841816038939344
  - mTmax: 750.956
    mTmin: 690.786
    name: R_13(pp->munu)
    value:
      background_std: 81.90443651622297
      counts_background: 175.02635490532282
      counts_total: 1056.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0012005591743499255
  - mTmax: 816.366
    mTmin: 750.956
    name: R_13(pp->munu)
    value:
      background_std: 63.05459775821269
      counts_background: 111.97934711011833
      counts_total: 673.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0016858815516968251
  - mTmax: 887.473
    mTmin: 816.366
    name: R_13(pp->munu)
    value:
      background_std: 47.85252681781809
      counts_background: 72.93416823487914
      counts_total: 531.0
      distribution: general_gamma_counting_process
      scale_factor: 0.002378929594384112
  - mTmax: 964.775
    mTmin: 887.473
    name: R_13(pp->munu)
    value:
      background_std: 29.884772152050953
      counts_background: 51.02213419686935
      counts_total: 339.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0037000395697988574
  - mTmax: 1048.81
    mTmin: 964.775
    name: R_13(pp->munu)
    value:
      background_std: 21.73445316870199
      counts_background: 31.49748386037507
      counts_total: 237.0
      distribution: general_gamma_counting_process
      scale_factor: 0.005174238254625601
  - mTmax: 1140.16
    mTmin: 1048.81
    name: R_13(pp->munu)
    value:
      background_std: 15.61168559953998
      counts_background: 20.514879271343897
      counts_total: 150.0
      distribution: general_gamma_counting_process
      scale_factor: 0.007466198646398077
  - mTmax: 1239.47
    mTmin: 1140.16
    name: R_13(pp->munu)
    value:
      background_std: 11.187807123760404
      counts_background: 13.36171083961638
      counts_total: 105.0
      distribution: general_gamma_counting_process
      scale_factor: 0.01100172185890467
  - mTmax: 1347.44
    mTmin: 1239.47
    name: R_13(pp->munu)
    value:
      background_std: 8.090867417412117
      counts_background: 8.702723238099091
      counts_total: 96.0
      distribution: general_gamma_counting_process
      scale_factor: 0.016214937698075395
  - mTmax: 1464.8
    mTmin: 1347.44
    name: R_13(pp->munu)
    value:
      background_std: 5.861732064721911
      counts_background: 5.668240591945363
      counts_total: 53.0
      distribution: general_gamma_counting_process
      scale_factor: 0.02390337386688388
  - mTmax: 1592.39
    mTmin: 1464.8
    name: R_13(pp->munu)
    value:
      background_std: 4.239721806470444
      counts_background: 3.6918273199269356
      counts_total: 36.0
      distribution: general_gamma_counting_process
      scale_factor: 0.035244263449434175
  - mTmax: 1731.09
    mTmin: 1592.39
    name: R_13(pp->munu)
    value:
      background_std: 3.061547949508712
      counts_background: 2.404553712756417
      counts_total: 29.0
      distribution: general_gamma_counting_process
      scale_factor: 0.05303191512672773
  - mTmax: 1881.87
    mTmin: 1731.09
    name: R_13(pp->munu)
    value:
      background_std: 2.218979709424131
      counts_background: 1.5943593275816659
      counts_total: 18.0
      distribution: general_gamma_counting_process
      scale_factor: 0.07838762242210882
  - mTmax: 2045.79
    mTmin: 1881.87
    name: R_13(pp->munu)
    value:
      background_std: 1.6094064148303902
      counts_background: 1.03843498310755
      counts_total: 9.0
      distribution: general_gamma_counting_process
      scale_factor: 0.12035229841895172
  - mTmax: 2223.98
    mTmin: 2045.79
    name: R_13(pp->munu)
    value:
      background_std: 1.1798660461214443
      counts_background: 0.6885429477500506
      counts_total: 5.0
      distribution: general_gamma_counting_process
      scale_factor: 0.18151088088844602
  - mTmax: 2417.69
    mTmin: 2223.98
    name: R_13(pp->munu)
    value:
      background_std: 0.86915070607508
      counts_background: 0.4484604392161544
      counts_total: 8.0
      distribution: general_gamma_counting_process
      scale_factor: 0.27868241219689954
  - mTmax: 2628.28
    mTmin: 2417.69
    name: R_13(pp->munu)
    value:
      background_std: 0.6397040443261947
      counts_background: 0.29735542214027355
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.4288406362148017
  - mTmax: 2857.21
    mTmin: 2628.28
    name: R_13(pp->munu)
    value:
      background_std: 0.4678828354299824
      counts_background: 0.19716398447712893
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 0.65993662594304
  - mTmax: 3106.08
    mTmin: 2857.21
    name: R_13(pp->munu)
    value:
      background_std: 0.3384261768295841
      counts_background: 0.12841645879193278
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 1.0339214268125256
  - mTmax: 3376.63
    mTmin: 3106.08
    name: R_13(pp->munu)
    value:
      background_std: 0.24192533758888526
      counts_background: 0.0851476004897484
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.6238864069933419
  - mTmax: 3670.74
    mTmin: 3376.63
    name: R_13(pp->munu)
    value:
      background_std: 0.17058236546210775
      counts_background: 0.056457824311358915
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 2.551003391247446
  - mTmax: 3990.47
    mTmin: 3670.74
    name: R_13(pp->munu)
    value:
      background_std: 0.11914494667660731
      counts_background: 0.037434829726717155
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 4.091595045707155
  - mTmax: 4338.05
    mTmin: 3990.47
    name: R_13(pp->munu)
    value:
      background_std: 0.0820679904624702
      counts_background: 0.024821475034884872
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 6.565906566219575
  - mTmax: 4715.91
    mTmin: 4338.05
    name: R_13(pp->munu)
    value:
      background_std: 0.055953621511592076
      counts_background: 0.019677300467498864
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 10.912599350193446
  - mTmax: 5126.68
    mTmin: 4715.91
    name: R_13(pp->munu)
    value:
      background_std: 0.037750974048514296
      counts_background: 0.019677300467498864
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 19.88897136882155
  - mTmax: 5573.22
    mTmin: 5126.68
    name: R_13(pp->munu)
    value:
      background_std: 0.02523328957856268
      counts_background: 0.019677300467498864
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 42.53711207391964
  - mTmax: 6058.67
    mTmin: 5573.22
    name: R_13(pp->munu)
    value:
      background_std: 0.01671618330130428
      counts_background: 0.019677300467498864
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 143.20866623927168

CMS pp->ee 2021:
  experiment: CMS
  inspire: CMS:2021ctt
  values:
  - name: R_13(pp->ee)
    qmax: 65.0
    qmin: 60.0
    value:
      background_std: 831.0
      counts_background: 5701.878980308002
      counts_total: 15452.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00012185527470961339
  - name: R_13(pp->ee)
    qmax: 70.0
    qmin: 65.0
    value:
      background_std: 1023.3
      counts_background: 6455.043606542603
      counts_total: 22003.0
      distribution: general_gamma_counting_process
      scale_factor: 8.041585490665783e-05
  - name: R_13(pp->ee)
    qmax: 75.0
    qmin: 70.0
    value:
      background_std: 2692.9500000000003
      counts_background: 7865.872675685383
      counts_total: 69945.0
      distribution: general_gamma_counting_process
      scale_factor: 1.648513703714104e-05
  - name: R_13(pp->ee)
    qmax: 80.0
    qmin: 75.0
    value:
      background_std: 10302.0
      counts_background: 9370.536765396653
      counts_total: 304020.0
      distribution: general_gamma_counting_process
      scale_factor: 3.460285251233667e-06
  - name: R_13(pp->ee)
    qmax: 85.0
    qmin: 80.0
    value:
      background_std: 50005.0
      counts_background: 12020.799408359051
      counts_total: 1522250.0
      distribution: general_gamma_counting_process
      scale_factor: 6.690077527158101e-07
  - name: R_13(pp->ee)
    qmax: 90.0
    qmin: 85.0
    value:
      background_std: 321280.0
      counts_background: 25138.417113316355
      counts_total: 9638500.0
      distribution: general_gamma_counting_process
      scale_factor: 1.0426141482073915e-07
  - name: R_13(pp->ee)
    qmax: 95.0
    qmin: 90.0
    value:
      background_std: 429800.0
      counts_background: 32226.353364161692
      counts_total: 13100500.0
      distribution: general_gamma_counting_process
      scale_factor: 7.666763265989404e-08
  - name: R_13(pp->ee)
    qmax: 100.0
    qmin: 95.0
    value:
      background_std: 72980.0
      counts_background: 14817.334342045522
      counts_total: 2188450.0
      distribution: general_gamma_counting_process
      scale_factor: 4.4704648764652155e-07
  - name: R_13(pp->ee)
    qmax: 105.0
    qmin: 100.0
    value:
      background_std: 21565.0
      counts_background: 12540.078528575195
      counts_total: 634750.0
      distribution: general_gamma_counting_process
      scale_factor: 1.5807013446331753e-06
  - name: R_13(pp->ee)
    qmax: 110.0
    qmin: 105.0
    value:
      background_std: 11210.0
      counts_background: 12533.67770365131
      counts_total: 330785.0
      distribution: general_gamma_counting_process
      scale_factor: 3.1060510844567983e-06
  - name: R_13(pp->ee)
    qmax: 115.0
    qmin: 110.0
    value:
      background_std: 7552.0
      counts_background: 12382.087819132976
      counts_total: 213745.0
      distribution: general_gamma_counting_process
      scale_factor: 4.863852620007929e-06
  - name: R_13(pp->ee)
    qmax: 120.0
    qmin: 115.0
    value:
      background_std: 5501.0
      counts_background: 12095.702732163982
      counts_total: 153970.0
      distribution: general_gamma_counting_process
      scale_factor: 6.893179328721299e-06
  - name: R_13(pp->ee)
    qmax: 125.0
    qmin: 120.0
    value:
      background_std: 5257.0
      counts_background: 11728.78965062577
      counts_total: 118255.0
      distribution: general_gamma_counting_process
      scale_factor: 8.931757380176736e-06
  - name: R_13(pp->ee)
    qmax: 130.0
    qmin: 125.0
    value:
      background_std: 5197.0
      counts_background: 11292.004025812214
      counts_total: 94995.0
      distribution: general_gamma_counting_process
      scale_factor: 1.1384475528590407e-05
  - name: R_13(pp->ee)
    qmax: 135.0
    qmin: 130.0
    value:
      background_std: 5180.5
      counts_background: 10912.264773388133
      counts_total: 78355.0
      distribution: general_gamma_counting_process
      scale_factor: 1.4125836791104324e-05
  - name: R_13(pp->ee)
    qmax: 140.0
    qmin: 135.0
    value:
      background_std: 3200.1499999999996
      counts_background: 10471.079468496435
      counts_total: 65250.0
      distribution: general_gamma_counting_process
      scale_factor: 1.7088844016926783e-05
  - name: R_13(pp->ee)
    qmax: 145.0
    qmin: 140.0
    value:
      background_std: 2400.1
      counts_background: 9969.37898459165
      counts_total: 56545.0
      distribution: general_gamma_counting_process
      scale_factor: 2.0407827461011443e-05
  - name: R_13(pp->ee)
    qmax: 150.0
    qmin: 145.0
    value:
      background_std: 2193.7
      counts_background: 9432.135822344337
      counts_total: 48691.0
      distribution: general_gamma_counting_process
      scale_factor: 2.47663159105068e-05
  - name: R_13(pp->ee)
    qmax: 160.0
    qmin: 150.0
    value:
      background_std: 4317.799999999999
      counts_background: 17254.827825832945
      counts_total: 79345.0
      distribution: general_gamma_counting_process
      scale_factor: 1.5416384324049313e-05
  - name: R_13(pp->ee)
    qmax: 170.0
    qmin: 160.0
    value:
      background_std: 2478.0
      counts_background: 15315.666857844357
      counts_total: 62263.0
      distribution: general_gamma_counting_process
      scale_factor: 2.021551726016375e-05
  - name: R_13(pp->ee)
    qmax: 180.0
    qmin: 170.0
    value:
      background_std: 2020.1
      counts_background: 13603.693439102217
      counts_total: 50152.0
      distribution: general_gamma_counting_process
      scale_factor: 2.6749392802316055e-05
  - name: R_13(pp->ee)
    qmax: 190.0
    qmin: 180.0
    value:
      background_std: 1637.2
      counts_background: 11834.791436535725
      counts_total: 40918.0
      distribution: general_gamma_counting_process
      scale_factor: 3.290507813517481e-05
  - name: R_13(pp->ee)
    qmax: 200.0
    qmin: 190.0
    value:
      background_std: 1438.8999999999999
      counts_background: 10420.17740612818
      counts_total: 33718.0
      distribution: general_gamma_counting_process
      scale_factor: 4.2097818026876184e-05
  - name: R_13(pp->ee)
    qmax: 220.0
    qmin: 200.0
    value:
      background_std: 2751.2
      counts_background: 17000.844251358405
      counts_total: 51164.0
      distribution: general_gamma_counting_process
      scale_factor: 2.9084933662945905e-05
  - name: R_13(pp->ee)
    qmax: 240.0
    qmin: 220.0
    value:
      background_std: 1431.14
      counts_background: 12808.032882070536
      counts_total: 36436.0
      distribution: general_gamma_counting_process
      scale_factor: 4.143221958147583e-05
  - name: R_13(pp->ee)
    qmax: 260.0
    qmin: 240.0
    value:
      background_std: 1083.64
      counts_background: 9706.08994787363
      counts_total: 26302.0
      distribution: general_gamma_counting_process
      scale_factor: 5.9588694486052555e-05
  - name: R_13(pp->ee)
    qmax: 280.0
    qmin: 260.0
    value:
      background_std: 825.0799999999999
      counts_background: 7357.276130193078
      counts_total: 19516.0
      distribution: general_gamma_counting_process
      scale_factor: 8.155766468087255e-05
  - name: R_13(pp->ee)
    qmax: 300.0
    qmin: 280.0
    value:
      background_std: 573.2
      counts_background: 5584.933994927697
      counts_total: 14567.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00011016301194453936
  - name: R_13(pp->ee)
    qmax: 320.0
    qmin: 300.0
    value:
      background_std: 503.56
      counts_background: 4209.347379552479
      counts_total: 11186.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00014385852867420914
  - name: R_13(pp->ee)
    qmax: 340.0
    qmin: 320.0
    value:
      background_std: 378.2
      counts_background: 3272.09838538474
      counts_total: 8636.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00018368143643359973
  - name: R_13(pp->ee)
    qmax: 360.0
    qmin: 340.0
    value:
      background_std: 277.65999999999997
      counts_background: 2520.9115446466994
      counts_total: 6792.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00023468800216940207
  - name: R_13(pp->ee)
    qmax: 380.0
    qmin: 360.0
    value:
      background_std: 261.12
      counts_background: 1965.7874049761576
      counts_total: 5293.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00029240951422857697
  - name: R_13(pp->ee)
    qmax: 400.0
    qmin: 380.0
    value:
      background_std: 183.15200000000002
      counts_background: 1540.8834033307726
      counts_total: 4123.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003691215976650462
  - name: R_13(pp->ee)
    qmax: 420.0
    qmin: 400.0
    value:
      background_std: 176.508
      counts_background: 1192.8079955350063
      counts_total: 3360.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00045310061385788814
  - name: R_13(pp->ee)
    qmax: 440.0
    qmin: 420.0
    value:
      background_std: 116.69800000000001
      counts_background: 949.8991571044012
      counts_total: 2759.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0005574191289649166
  - name: R_13(pp->ee)
    qmax: 460.0
    qmin: 440.0
    value:
      background_std: 102.814
      counts_background: 744.3888596458787
      counts_total: 2228.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0006851301539404938
  - name: R_13(pp->ee)
    qmax: 480.0
    qmin: 460.0
    value:
      background_std: 76.174
      counts_background: 613.8448255204651
      counts_total: 1748.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0008196203893736208
  - name: R_13(pp->ee)
    qmax: 500.0
    qmin: 480.0
    value:
      background_std: 64.512
      counts_background: 552.8919083889597
      counts_total: 1528.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0009565562876769117
  - name: R_13(pp->ee)
    qmax: 520.0
    qmin: 500.0
    value:
      background_std: 71.322
      counts_background: 410.8680174026359
      counts_total: 1234.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0011664459120967233
  - name: R_13(pp->ee)
    qmax: 540.0
    qmin: 520.0
    value:
      background_std: 47.248000000000005
      counts_background: 325.94648171940497
      counts_total: 1059.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0013481335925621426
  - name: R_13(pp->ee)
    qmax: 560.0
    qmin: 540.0
    value:
      background_std: 40.428
      counts_background: 265.285722961996
      counts_total: 864.0
      distribution: general_gamma_counting_process
      scale_factor: 0.001591944132329856
  - name: R_13(pp->ee)
    qmax: 580.0
    qmin: 560.0
    value:
      background_std: 36.858
      counts_background: 212.9764655631463
      counts_total: 751.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0018919061959419181
  - name: R_13(pp->ee)
    qmax: 600.0
    qmin: 580.0
    value:
      background_std: 31.808
      counts_background: 177.1274638240017
      counts_total: 661.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0021567037701779855
  - name: R_13(pp->ee)
    qmax: 630.0
    qmin: 600.0
    value:
      background_std: 51.794999999999995
      counts_background: 209.31038175967637
      counts_total: 792.99
      distribution: general_gamma_counting_process
      scale_factor: 0.0017529219450267489
  - name: R_13(pp->ee)
    qmax: 660.0
    qmin: 630.0
    value:
      background_std: 29.1948
      counts_background: 159.78309327380316
      counts_total: 639.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0021277297761460446
  - name: R_13(pp->ee)
    qmax: 690.0
    qmin: 660.0
    value:
      background_std: 26.3487
      counts_background: 121.75724499497386
      counts_total: 515.01
      distribution: general_gamma_counting_process
      scale_factor: 0.0025513994426335095
  - name: R_13(pp->ee)
    qmax: 720.0
    qmin: 690.0
    value:
      background_std: 23.1792
      counts_background: 95.56950371499626
      counts_total: 432.99
      distribution: general_gamma_counting_process
      scale_factor: 0.0031526945254715675
  - name: R_13(pp->ee)
    qmax: 750.0
    qmin: 720.0
    value:
      background_std: 18.7224
      counts_background: 73.36660983912986
      counts_total: 374.01
      distribution: general_gamma_counting_process
      scale_factor: 0.003894178755251911
  - name: R_13(pp->ee)
    qmax: 780.0
    qmin: 750.0
    value:
      background_std: 16.341900000000003
      counts_background: 58.42590015045859
      counts_total: 311.01000000000005
      distribution: general_gamma_counting_process
      scale_factor: 0.004796416903378421
  - name: R_13(pp->ee)
    qmax: 810.0
    qmin: 780.0
    value:
      background_std: 15.481200000000001
      counts_background: 47.350570421484804
      counts_total: 204.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0050987105983517035
  - name: R_13(pp->ee)
    qmax: 840.0
    qmin: 810.0
    value:
      background_std: 16.727700000000002
      counts_background: 36.688714089415356
      counts_total: 207.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00666658159963576
  - name: R_13(pp->ee)
    qmax: 870.0
    qmin: 840.0
    value:
      background_std: 8.4702
      counts_background: 31.132090758979373
      counts_total: 156.0
      distribution: general_gamma_counting_process
      scale_factor: 0.007763116663687077
  - name: R_13(pp->ee)
    qmax: 900.0
    qmin: 870.0
    value:
      background_std: 7.5906
      counts_background: 25.24566295052275
      counts_total: 123.99900000000001
      distribution: general_gamma_counting_process
      scale_factor: 0.00916131584214694
  - name: R_13(pp->ee)
    qmax: 950.0
    qmin: 900.0
    value:
      background_std: 13.5435
      counts_background: 31.693745296404508
      counts_total: 177.0
      distribution: general_gamma_counting_process
      scale_factor: 0.006738614100882317
  - name: R_13(pp->ee)
    qmax: 1000.0
    qmin: 950.0
    value:
      background_std: 8.2165
      counts_background: 21.460668927830792
      counts_total: 156.0
      distribution: general_gamma_counting_process
      scale_factor: 0.008662068824143233
  - name: R_13(pp->ee)
    qmax: 1050.0
    qmin: 1000.0
    value:
      background_std: 6.4415
      counts_background: 15.592370207910204
      counts_total: 86.0
      distribution: general_gamma_counting_process
      scale_factor: 0.01108553228972087
  - name: R_13(pp->ee)
    qmax: 1100.0
    qmin: 1050.0
    value:
      background_std: 6.010999999999999
      counts_background: 11.46937029942327
      counts_total: 78.0
      distribution: general_gamma_counting_process
      scale_factor: 0.014635697669161283
  - name: R_13(pp->ee)
    qmax: 1150.0
    qmin: 1100.0
    value:
      background_std: 4.5796
      counts_background: 8.285761645490192
      counts_total: 78.0
      distribution: general_gamma_counting_process
      scale_factor: 0.01788001026268359
  - name: R_13(pp->ee)
    qmax: 1200.0
    qmin: 1150.0
    value:
      background_std: 3.70115
      counts_background: 6.6757844613718555
      counts_total: 49.0
      distribution: general_gamma_counting_process
      scale_factor: 0.022008641076998608
  - name: R_13(pp->ee)
    qmax: 1250.0
    qmin: 1200.0
    value:
      background_std: 3.2655999999999996
      counts_background: 5.575763857625475
      counts_total: 41.0
      distribution: general_gamma_counting_process
      scale_factor: 0.027981768594955717
  - name: R_13(pp->ee)
    qmax: 1310.0
    qmin: 1250.0
    value:
      background_std: 3.82956
      counts_background: 3.881897282598377
      counts_total: 43.0002
      distribution: general_gamma_counting_process
      scale_factor: 0.028189579357832086
  - name: R_13(pp->ee)
    qmax: 1370.0
    qmin: 1310.0
    value:
      background_std: 2.62758
      counts_background: 3.2894898320115833
      counts_total: 31.999799999999997
      distribution: general_gamma_counting_process
      scale_factor: 0.03673021166475208
  - name: R_13(pp->ee)
    qmax: 1430.0
    qmin: 1370.0
    value:
      background_std: 2.13912
      counts_background: 2.284604311977587
      counts_total: 21.0
      distribution: general_gamma_counting_process
      scale_factor: 0.04652771203325717
  - name: R_13(pp->ee)
    qmax: 1490.0
    qmin: 1430.0
    value:
      background_std: 1.6299000000000001
      counts_background: 2.087200658059648
      counts_total: 25.0002
      distribution: general_gamma_counting_process
      scale_factor: 0.05873387586884946
  - name: R_13(pp->ee)
    qmax: 1550.0
    qmin: 1490.0
    value:
      background_std: 1.45494
      counts_background: 1.6126939070940605
      counts_total: 15.0
      distribution: general_gamma_counting_process
      scale_factor: 0.07454984333853684
  - name: R_13(pp->ee)
    qmax: 1610.0
    qmin: 1550.0
    value:
      background_std: 1.13382
      counts_background: 1.2053884468044034
      counts_total: 15.0
      distribution: general_gamma_counting_process
      scale_factor: 0.09252397592977303
  - name: R_13(pp->ee)
    qmax: 1680.0
    qmin: 1610.0
    value:
      background_std: 1.1050200000000001
      counts_background: 1.2236338923922696
      counts_total: 8.0003
      distribution: general_gamma_counting_process
      scale_factor: 0.09901519789954959
  - name: R_13(pp->ee)
    qmax: 1750.0
    qmin: 1680.0
    value:
      background_std: 0.84287
      counts_background: 0.7179398345861289
      counts_total: 10.9998
      distribution: general_gamma_counting_process
      scale_factor: 0.1285584740549172
  - name: R_13(pp->ee)
    qmax: 1820.0
    qmin: 1750.0
    value:
      background_std: 0.694645
      counts_background: 0.5992312756337012
      counts_total: 5.99998
      distribution: general_gamma_counting_process
      scale_factor: 0.1598549448996265
  - name: R_13(pp->ee)
    qmax: 1890.0
    qmin: 1820.0
    value:
      background_std: 0.542717
      counts_background: 0.4171331604714287
      counts_total: 8.0003
      distribution: general_gamma_counting_process
      scale_factor: 0.206675088252884
  - name: R_13(pp->ee)
    qmax: 1970.0
    qmin: 1890.0
    value:
      background_std: 0.5188159999999999
      counts_background: 0.4448584092905549
      counts_total: 8.0
      distribution: general_gamma_counting_process
      scale_factor: 0.23431764388882872
  - name: R_13(pp->ee)
    qmax: 2050.0
    qmin: 1970.0
    value:
      background_std: 0.38783999999999996
      counts_background: 0.2718923693807559
      counts_total: 7.0
      distribution: general_gamma_counting_process
      scale_factor: 0.3023927197023978
  - name: R_13(pp->ee)
    qmax: 2130.0
    qmin: 2050.0
    value:
      background_std: 0.318312
      counts_background: 0.19291025053987376
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.37494084989808507
  - name: R_13(pp->ee)
    qmax: 2210.0
    qmin: 2130.0
    value:
      background_std: 0.25441600000000003
      counts_background: 0.14682564442984766
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 0.4787234378231659
  - name: R_13(pp->ee)
    qmax: 2290.0
    qmin: 2210.0
    value:
      background_std: 0.20824800000000002
      counts_background: 0.12242352237028742
      counts_total: 6.0
      distribution: general_gamma_counting_process
      scale_factor: 0.6067300756920204
  - name: R_13(pp->ee)
    qmax: 2370.0
    qmin: 2290.0
    value:
      background_std: 0.15412800000000001
      counts_background: 0.03659870197119725
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.7842859691727891
  - name: R_13(pp->ee)
    qmax: 2450.0
    qmin: 2370.0
    value:
      background_std: 0.13036799999999998
      counts_background: 0.05425740153731319
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 0.9891962516528416
  - name: R_13(pp->ee)
    qmax: 2530.0
    qmin: 2450.0
    value:
      background_std: 0.11268
      counts_background: 0.08867544041149267
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.2417554789784402
  - name: R_13(pp->ee)
    qmax: 2610.0
    qmin: 2530.0
    value:
      background_std: 0.087152
      counts_background: 0.04731888189610251
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 1.5573022859798031
  - name: R_13(pp->ee)
    qmax: 2690.0
    qmin: 2610.0
    value:
      background_std: 0.0668904
      counts_background: 0.01031996049958608
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 1.9354806861329976
  - name: R_13(pp->ee)
    qmax: 2770.0
    qmin: 2690.0
    value:
      background_std: 0.0712488
      counts_background: 0.10226825556454028
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.4135367513296275
  - name: R_13(pp->ee)
    qmax: 2850.0
    qmin: 2770.0
    value:
      background_std: 0.0454984
      counts_background: 0.013600717626224529
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 3.0264910547345614
  - name: R_13(pp->ee)
    qmax: 2930.0
    qmin: 2850.0
    value:
      background_std: 0.0371568
      counts_background: 0.005193782273644783
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.691785109129273
  - name: R_13(pp->ee)
    qmax: 3010.0
    qmin: 2930.0
    value:
      background_std: 0.0305104
      counts_background: 0.007141810885623472
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 4.663887518377184
  - name: R_13(pp->ee)
    qmax: 3090.0
    qmin: 3010.0
    value:
      background_std: 0.026360799999999997
      counts_background: 0.013010919352075259
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 5.759235271238098
  - name: R_13(pp->ee)
    qmax: 3170.0
    qmin: 3090.0
    value:
      background_std: 0.0277448
      counts_background: 0.051860368262802284
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 7.009412223973501
  - name: R_13(pp->ee)
    qmax: 3250.0
    qmin: 3170.0
    value:
      background_std: 0.030994400000000002
      counts_background: 0.035416108727459886
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 8.35099988620209
  - name: R_13(pp->ee)
    qmax: 3330.0
    qmin: 3250.0
    value:
      background_std: 0.0145672
      counts_background: 0.0021522017444984046
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 10.366255158725254
  - name: R_13(pp->ee)
    qmax: 3410.0
    qmin: 3330.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 1.0
      distribution: gamma_counting_process
      scale_factor: 12.52151687913407
  - name: R_13(pp->ee)
    qmax: 3490.0
    qmin: 3410.0
    value:
      counts_background: 0.010555316363877354
      counts_total: 1.0
      distribution: gamma_counting_process
      scale_factor: 15.547386219091818
  - name: R_13(pp->ee)
    qmax: 3570.0
    qmin: 3490.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 19.54576962703109
  - name: R_13(pp->ee)
    qmax: 3650.0
    qmin: 3570.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 23.816659487454693
  - name: R_13(pp->ee)
    qmax: 3730.0
    qmin: 3650.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 29.247683290763604
  - name: R_13(pp->ee)
    qmax: 3810.0
    qmin: 3730.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 35.61698045164151
  - name: R_13(pp->ee)
    qmax: 3890.0
    qmin: 3810.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 43.46630779273621
  - name: R_13(pp->ee)
    qmax: 3970.0
    qmin: 3890.0
    value:
      counts_background: 0.0008000000000000042
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 53.23488853915603
  - name: R_13(pp->ee)
    qmax: 4070.0
    qmin: 3970.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 53.474299420776646
  - name: R_13(pp->ee)
    qmax: 4170.0
    qmin: 4070.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 67.81422641464671
  - name: R_13(pp->ee)
    qmax: 4270.0
    qmin: 4170.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 89.82037585994424
  - name: R_13(pp->ee)
    qmax: 4370.0
    qmin: 4270.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 120.95049004124854
  - name: R_13(pp->ee)
    qmax: 4470.0
    qmin: 4370.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 153.0742674834596
  - name: R_13(pp->ee)
    qmax: 4570.0
    qmin: 4470.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 206.8403584590284
  - name: R_13(pp->ee)
    qmax: 4670.0
    qmin: 4570.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 276.6606293187612
  - name: R_13(pp->ee)
    qmax: 4770.0
    qmin: 4670.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 371.59415210721096
  - name: R_13(pp->ee)
    qmax: 4870.0
    qmin: 4770.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 532.0500353532797
  - name: R_13(pp->ee)
    qmax: 4970.0
    qmin: 4870.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 759.7256104832346
  - name: R_13(pp->ee)
    qmax: 5070.0
    qmin: 4970.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1321.11117251084
  - name: R_13(pp->ee)
    qmax: 5170.0
    qmin: 5070.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2590.7112396792727
  - name: R_13(pp->ee)
    qmax: 5270.0
    qmin: 5170.0
    value:
      counts_background: 0.0010000000000000052
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 17070.97424270547

CMS pp->enu 2022:
  experiment: CMS
  inspire: CMS:2022yjm
  values:
  - mTmax: 480.0
    mTmin: 440.0
    name: R_13(pp->enu)
    value:
      background_std: 501.97
      counts_background: 685.3072038042317
      counts_total: 3134.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00040351430141328756
  - mTmax: 520.0
    mTmin: 480.0
    name: R_13(pp->enu)
    value:
      background_std: 439.23
      counts_background: 644.4853362180684
      counts_total: 3565.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003292851481636881
  - mTmax: 560.0
    mTmin: 520.0
    name: R_13(pp->enu)
    value:
      background_std: 255.4
      counts_background: 399.50539169043964
      counts_total: 3124.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003576574602018139
  - mTmax: 600.0
    mTmin: 560.0
    name: R_13(pp->enu)
    value:
      background_std: 242.31
      counts_background: 275.04985609378963
      counts_total: 2364.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00047629376353495735
  - mTmax: 640.0
    mTmin: 600.0
    name: R_13(pp->enu)
    value:
      background_std: 189.27
      counts_background: 186.2097158531025
      counts_total: 1697.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0006381973895586469
  - mTmax: 680.0
    mTmin: 640.0
    name: R_13(pp->enu)
    value:
      background_std: 170.35
      counts_background: 131.44588921082314
      counts_total: 1226.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0008572666374574982
  - mTmax: 720.0
    mTmin: 680.0
    name: R_13(pp->enu)
    value:
      background_std: 123.1
      counts_background: 99.75085725305709
      counts_total: 916.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0011387917950669679
  - mTmax: 760.0
    mTmin: 720.0
    name: R_13(pp->enu)
    value:
      background_std: 83.649
      counts_background: 67.32603352969532
      counts_total: 722.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0014857229199219265
  - mTmax: 800.0
    mTmin: 760.0
    name: R_13(pp->enu)
    value:
      background_std: 70.243
      counts_background: 45.16482953991109
      counts_total: 570.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0019496191682796162
  - mTmax: 840.0
    mTmin: 800.0
    name: R_13(pp->enu)
    value:
      background_std: 47.616
      counts_background: 33.63482142821223
      counts_total: 412.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0025113428260116377
  - mTmax: 880.0
    mTmin: 840.0
    name: R_13(pp->enu)
    value:
      background_std: 39.69
      counts_background: 22.817237186465164
      counts_total: 325.0
      distribution: general_gamma_counting_process
      scale_factor: 0.003196120193108419
  - mTmax: 920.0
    mTmin: 880.0
    name: R_13(pp->enu)
    value:
      background_std: 26.429
      counts_background: 20.14611712961653
      counts_total: 241.0
      distribution: general_gamma_counting_process
      scale_factor: 0.004015067833021666
  - mTmax: 960.0
    mTmin: 920.0
    name: R_13(pp->enu)
    value:
      background_std: 31.361
      counts_background: 21.33779422874737
      counts_total: 192.0
      distribution: general_gamma_counting_process
      scale_factor: 0.004949613109133107
  - mTmax: 1000.0
    mTmin: 960.0
    name: R_13(pp->enu)
    value:
      background_std: 31.685
      counts_background: 10.462288337266457
      counts_total: 173.0
      distribution: general_gamma_counting_process
      scale_factor: 0.006178535398397672
  - mTmax: 1040.0
    mTmin: 1000.0
    name: R_13(pp->enu)
    value:
      background_std: 22.718
      counts_background: 8.2364967337828
      counts_total: 126.0
      distribution: general_gamma_counting_process
      scale_factor: 0.007722360294691018
  - mTmax: 1080.0
    mTmin: 1040.0
    name: R_13(pp->enu)
    value:
      background_std: 16.863
      counts_background: 7.208204752796001
      counts_total: 109.0
      distribution: general_gamma_counting_process
      scale_factor: 0.00952799996465935
  - mTmax: 1120.0
    mTmin: 1080.0
    name: R_13(pp->enu)
    value:
      background_std: 13.256
      counts_background: 4.713904702816089
      counts_total: 99.0
      distribution: general_gamma_counting_process
      scale_factor: 0.011551867222248177
  - mTmax: 1160.0
    mTmin: 1120.0
    name: R_13(pp->enu)
    value:
      background_std: 15.139
      counts_background: 4.225768874893042
      counts_total: 82.0
      distribution: general_gamma_counting_process
      scale_factor: 0.013966595186166554
  - mTmax: 1200.0
    mTmin: 1160.0
    name: R_13(pp->enu)
    value:
      background_std: 11.375
      counts_background: 3.001231231747037
      counts_total: 63.0
      distribution: general_gamma_counting_process
      scale_factor: 0.016929148001889983
  - mTmax: 1240.0
    mTmin: 1200.0
    name: R_13(pp->enu)
    value:
      background_std: 10.977
      counts_background: 2.5922113788551777
      counts_total: 47.0
      distribution: general_gamma_counting_process
      scale_factor: 0.020265964296760555
  - mTmax: 1280.0
    mTmin: 1240.0
    name: R_13(pp->enu)
    value:
      background_std: 7.6228
      counts_background: 2.6190116562657138
      counts_total: 40.0
      distribution: general_gamma_counting_process
      scale_factor: 0.023939498404411515
  - mTmax: 1320.0
    mTmin: 1280.0
    name: R_13(pp->enu)
    value:
      background_std: 6.1609
      counts_background: 1.573961256203003
      counts_total: 38.0
      distribution: general_gamma_counting_process
      scale_factor: 0.028730616614956808
  - mTmax: 1360.0
    mTmin: 1320.0
    name: R_13(pp->enu)
    value:
      background_std: 5.2559
      counts_background: 0.6485946929919203
      counts_total: 32.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0340336358387083
  - mTmax: 1400.0
    mTmin: 1360.0
    name: R_13(pp->enu)
    value:
      background_std: 4.2782
      counts_background: 0.832983149755952
      counts_total: 20.0
      distribution: general_gamma_counting_process
      scale_factor: 0.040274915713912125
  - mTmax: 1440.0
    mTmin: 1400.0
    name: R_13(pp->enu)
    value:
      background_std: 5.4857
      counts_background: 1.3645868087194162
      counts_total: 25.0
      distribution: general_gamma_counting_process
      scale_factor: 0.04719625551724325
  - mTmax: 1480.0
    mTmin: 1440.0
    name: R_13(pp->enu)
    value:
      background_std: 3.49
      counts_background: 0.44300437972202733
      counts_total: 23.0
      distribution: general_gamma_counting_process
      scale_factor: 0.056233694452867626
  - mTmax: 1520.0
    mTmin: 1480.0
    name: R_13(pp->enu)
    value:
      background_std: 2.5741
      counts_background: 0.20870676586246678
      counts_total: 13.0
      distribution: general_gamma_counting_process
      scale_factor: 0.06498927776787096
  - mTmax: 1560.0
    mTmin: 1520.0
    name: R_13(pp->enu)
    value:
      background_std: 3.3212
      counts_background: 0.2564063893309645
      counts_total: 16.0
      distribution: general_gamma_counting_process
      scale_factor: 0.07583440382285062
  - mTmax: 1600.0
    mTmin: 1560.0
    name: R_13(pp->enu)
    value:
      background_std: 2.0185
      counts_background: 0.209194084111491
      counts_total: 12.0
      distribution: general_gamma_counting_process
      scale_factor: 0.08938833073551904
  - mTmax: 1640.0
    mTmin: 1600.0
    name: R_13(pp->enu)
    value:
      background_std: 1.7531
      counts_background: 0.1679213170930752
      counts_total: 15.0
      distribution: general_gamma_counting_process
      scale_factor: 0.10545901859592784
  - mTmax: 1680.0
    mTmin: 1640.0
    name: R_13(pp->enu)
    value:
      background_std: 1.5246
      counts_background: 0.13160544250175407
      counts_total: 12.0
      distribution: general_gamma_counting_process
      scale_factor: 0.12387817062794133
  - mTmax: 1720.0
    mTmin: 1680.0
    name: R_13(pp->enu)
    value:
      background_std: 1.4026
      counts_background: 0.11055903601049938
      counts_total: 8.0
      distribution: general_gamma_counting_process
      scale_factor: 0.13752768400781568
  - mTmax: 1760.0
    mTmin: 1720.0
    name: R_13(pp->enu)
    value:
      background_std: 2.5328
      counts_background: 2.5087896803124643
      counts_total: 4.0
      distribution: general_gamma_counting_process
      scale_factor: 0.1629184136167086
  - mTmax: 1800.0
    mTmin: 1760.0
    name: R_13(pp->enu)
    value:
      background_std: 1.1538
      counts_background: 0.06619339776543717
      counts_total: 6.0
      distribution: general_gamma_counting_process
      scale_factor: 0.1871574339330256
  - mTmax: 1840.0
    mTmin: 1800.0
    name: R_13(pp->enu)
    value:
      background_std: 0.92291
      counts_background: 0.053245154792676636
      counts_total: 5.0
      distribution: general_gamma_counting_process
      scale_factor: 0.2148086227331264
  - mTmax: 1880.0
    mTmin: 1840.0
    name: R_13(pp->enu)
    value:
      background_std: 1.0027
      counts_background: 0.041535780021137766
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.24684186286132442
  - mTmax: 1920.0
    mTmin: 1880.0
    name: R_13(pp->enu)
    value:
      background_std: 0.77083
      counts_background: 0.039014917536967314
      counts_total: 4.0
      distribution: general_gamma_counting_process
      scale_factor: 0.28207976992703687
  - mTmax: 1960.0
    mTmin: 1920.0
    name: R_13(pp->enu)
    value:
      background_std: 0.64178
      counts_background: 0.027335623537809647
      counts_total: 5.0
      distribution: general_gamma_counting_process
      scale_factor: 0.33256622030614635
  - mTmax: 2000.0
    mTmin: 1960.0
    name: R_13(pp->enu)
    value:
      background_std: 0.57077
      counts_background: 0.022402545517260553
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.3673999580575091
  - mTmax: 2040.0
    mTmin: 2000.0
    name: R_13(pp->enu)
    value:
      background_std: 0.48499
      counts_background: 0.0199093237708316
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.4239358581749618
  - mTmax: 2080.0
    mTmin: 2040.0
    name: R_13(pp->enu)
    value:
      background_std: 0.38061
      counts_background: 0.01965968794786311
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 0.4824559748838243
  - mTmax: 2120.0
    mTmin: 2080.0
    name: R_13(pp->enu)
    value:
      background_std: 0.38448
      counts_background: 0.011628533017902332
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.5495914693296035
  - mTmax: 2160.0
    mTmin: 2120.0
    name: R_13(pp->enu)
    value:
      background_std: 0.34595
      counts_background: 0.009579146676611621
      counts_total: 4.0
      distribution: general_gamma_counting_process
      scale_factor: 0.623955531974494
  - mTmax: 2200.0
    mTmin: 2160.0
    name: R_13(pp->enu)
    value:
      background_std: 0.28751
      counts_background: 0.008011712568570733
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 0.7074818523005214
  - mTmax: 2240.0
    mTmin: 2200.0
    name: R_13(pp->enu)
    value:
      background_std: 0.23162
      counts_background: 0.006308775741799536
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.7989192358762129
  - mTmax: 2280.0
    mTmin: 2240.0
    name: R_13(pp->enu)
    value:
      background_std: 0.20254
      counts_background: 0.0044627108367266645
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 0.9143662126858789
  - mTmax: 2320.0
    mTmin: 2280.0
    name: R_13(pp->enu)
    value:
      background_std: 0.19719
      counts_background: 0.005082597943113806
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 1.0230199000284124
  - mTmax: 2360.0
    mTmin: 2320.0
    name: R_13(pp->enu)
    value:
      background_std: 0.18762
      counts_background: 0.0037541919568823347
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.1612271443491535
  - mTmax: 2400.0
    mTmin: 2360.0
    name: R_13(pp->enu)
    value:
      background_std: 0.18722
      counts_background: 0.0028450425695979074
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 1.325232552423057
  - mTmax: 2440.0
    mTmin: 2400.0
    name: R_13(pp->enu)
    value:
      background_std: 0.17188
      counts_background: 0.0021370631189208847
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 1.4896051134189534
  - mTmax: 2480.0
    mTmin: 2440.0
    name: R_13(pp->enu)
    value:
      background_std: 0.13257
      counts_background: 0.0022211028495023053
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 1.6699196961583411
  - mTmax: 2520.0
    mTmin: 2480.0
    name: R_13(pp->enu)
    value:
      background_std: 0.13645
      counts_background: 0.0019799413836670806
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.9182667001927447
  - mTmax: 2560.0
    mTmin: 2520.0
    name: R_13(pp->enu)
    value:
      background_std: 0.10515
      counts_background: 0.0014840411935617846
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 2.1601846033228607
  - mTmax: 2600.0
    mTmin: 2560.0
    name: R_13(pp->enu)
    value:
      background_std: 0.092711
      counts_background: 0.0011834381765836062
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 2.3730181406223143
  - mTmax: 2640.0
    mTmin: 2600.0
    name: R_13(pp->enu)
    value:
      background_std: 0.08817
      counts_background: 0.0011685994725399921
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 2.7074806707651002
  - mTmax: 2680.0
    mTmin: 2640.0
    name: R_13(pp->enu)
    value:
      background_std: 0.085141
      counts_background: 0.0008704790452127665
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.0513731023759347
  - mTmax: 2720.0
    mTmin: 2680.0
    name: R_13(pp->enu)
    value:
      background_std: 0.071156
      counts_background: 0.0006357794469504392
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.409319330842205
  - mTmax: 2760.0
    mTmin: 2720.0
    name: R_13(pp->enu)
    value:
      background_std: 0.072658
      counts_background: 0.0005918956143543814
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.8955165503372227
  - mTmax: 2800.0
    mTmin: 2760.0
    name: R_13(pp->enu)
    value:
      background_std: 0.06468
      counts_background: 0.00039072955175135677
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 4.385738487000358
  - mTmax: 2840.0
    mTmin: 2800.0
    name: R_13(pp->enu)
    value:
      background_std: 0.05076
      counts_background: 0.000467508353036048
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 4.922818728757035
  - mTmax: 2880.0
    mTmin: 2840.0
    name: R_13(pp->enu)
    value:
      background_std: 0.046606
      counts_background: 0.00045938822644943643
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 5.486107009294341
  - mTmax: 2920.0
    mTmin: 2880.0
    name: R_13(pp->enu)
    value:
      background_std: 0.045623
      counts_background: 0.00042017583423266624
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 6.163594225294338
  - mTmax: 2960.0
    mTmin: 2920.0
    name: R_13(pp->enu)
    value:
      background_std: 0.038283
      counts_background: 0.0003646311259646446
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 6.734679925008108
  - mTmax: 3000.0
    mTmin: 2960.0
    name: R_13(pp->enu)
    value:
      background_std: 0.034014
      counts_background: 0.0004237336825973172
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 7.542948219632239
  - mTmax: 3040.0
    mTmin: 3000.0
    name: R_13(pp->enu)
    value:
      background_std: 0.03435
      counts_background: 0.00030318458293856663
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 8.452308090337233
  - mTmax: 3080.0
    mTmin: 3040.0
    name: R_13(pp->enu)
    value:
      background_std: 0.028267
      counts_background: 0.00014293785953370378
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 9.408209496142524
  - mTmax: 3120.0
    mTmin: 3080.0
    name: R_13(pp->enu)
    value:
      background_std: 0.0266
      counts_background: 0.00010191288807335522
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 10.397064314095664
  - mTmax: 3160.0
    mTmin: 3120.0
    name: R_13(pp->enu)
    value:
      background_std: 0.025352
      counts_background: 0.0001066642884313102
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 11.74761209882719
  - mTmax: 3200.0
    mTmin: 3160.0
    name: R_13(pp->enu)
    value:
      background_std: 0.022381
      counts_background: 0.00015515063886983884
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 12.995949212293445
  - mTmax: 3240.0
    mTmin: 3200.0
    name: R_13(pp->enu)
    value:
      background_std: 0.020585
      counts_background: 5.5808551490762533e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 14.605886754313671
  - mTmax: 3280.0
    mTmin: 3240.0
    name: R_13(pp->enu)
    value:
      background_std: 0.018963
      counts_background: 0.0001632506511005
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 16.341790746048606
  - mTmax: 3320.0
    mTmin: 3280.0
    name: R_13(pp->enu)
    value:
      background_std: 0.018016
      counts_background: 0.00010756747070226397
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 18.259238605214104
  - mTmax: 3360.0
    mTmin: 3320.0
    name: R_13(pp->enu)
    value:
      background_std: 0.016291
      counts_background: 4.9113472466873746e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 20.473452275951285
  - mTmax: 3400.0
    mTmin: 3360.0
    name: R_13(pp->enu)
    value:
      background_std: 0.015632
      counts_background: 7.388068144672712e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 22.892370082613876
  - mTmax: 3440.0
    mTmin: 3400.0
    name: R_13(pp->enu)
    value:
      background_std: 0.014362
      counts_background: 4.854408153932544e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 25.603296206579888
  - mTmax: 3480.0
    mTmin: 3440.0
    name: R_13(pp->enu)
    value:
      background_std: 0.01251
      counts_background: 9.951593682421527e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 28.943093473363724
  - mTmax: 3520.0
    mTmin: 3480.0
    name: R_13(pp->enu)
    value:
      background_std: 0.011143
      counts_background: 6.128742813172941e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 31.859729026500546
  - mTmax: 3560.0
    mTmin: 3520.0
    name: R_13(pp->enu)
    value:
      background_std: 0.011037
      counts_background: 6.457970483823947e-05
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 35.95503886561246
  - mTmax: 3600.0
    mTmin: 3560.0
    name: R_13(pp->enu)
    value:
      counts_background: 6.256125241000559e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 39.43628455173676
  - mTmax: 3640.0
    mTmin: 3600.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.7754294506719074e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 43.72361211652484
  - mTmax: 3680.0
    mTmin: 3640.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.144376967443529e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 49.396519836963265
  - mTmax: 3720.0
    mTmin: 3680.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.76667038826407e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 54.569603133326474
  - mTmax: 3760.0
    mTmin: 3720.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.4438482116017164e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 60.18933491086574
  - mTmax: 3800.0
    mTmin: 3760.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.9541190843992314e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 66.66439351398762
  - mTmax: 3840.0
    mTmin: 3800.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.3146947292629724e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 75.59575077085653
  - mTmax: 3880.0
    mTmin: 3840.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.433095589581751e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 85.04093468303768
  - mTmax: 3920.0
    mTmin: 3880.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.1029300804576948e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 95.7608380914255
  - mTmax: 3960.0
    mTmin: 3920.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.2547047458090992e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 105.34091255960409
  - mTmax: 4000.0
    mTmin: 3960.0
    name: R_13(pp->enu)
    value:
      counts_background: 8.367632438657121e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 116.65755896836576
  - mTmax: 4040.0
    mTmin: 4000.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.6837248797654785e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 130.062468100625
  - mTmax: 4080.0
    mTmin: 4040.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.188176009647675e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 145.47597794763095
  - mTmax: 4120.0
    mTmin: 4080.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.4558536757004545e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 161.8043892068633
  - mTmax: 4160.0
    mTmin: 4120.0
    name: R_13(pp->enu)
    value:
      counts_background: 6.205610359708174e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 180.56714061251841
  - mTmax: 4200.0
    mTmin: 4160.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.451282835139922e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 201.8731427183309
  - mTmax: 4240.0
    mTmin: 4200.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.3635729766936592e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 222.38462079621561
  - mTmax: 4280.0
    mTmin: 4240.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.008701554240836e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 251.33693320815155
  - mTmax: 4320.0
    mTmin: 4280.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.3414295736258857e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 279.2313394320861
  - mTmax: 4360.0
    mTmin: 4320.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.229524581534205e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 311.1327925918976
  - mTmax: 4400.0
    mTmin: 4360.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.411695270795707e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 346.99392140335146
  - mTmax: 4440.0
    mTmin: 4400.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.2732795888735984e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 387.2370369366454
  - mTmax: 4480.0
    mTmin: 4440.0
    name: R_13(pp->enu)
    value:
      counts_background: 6.864497891881006e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 423.0247210131223
  - mTmax: 4520.0
    mTmin: 4480.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.6460212003729596e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 479.26539729100654
  - mTmax: 4560.0
    mTmin: 4520.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.9778450955356363e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 529.5462239419633
  - mTmax: 4600.0
    mTmin: 4560.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.1422177389833648e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 588.4795816449404
  - mTmax: 4640.0
    mTmin: 4600.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.568658940879077e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 641.6218528299648
  - mTmax: 4680.0
    mTmin: 4640.0
    name: R_13(pp->enu)
    value:
      counts_background: 7.984791155377944e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 739.7169892646519
  - mTmax: 4720.0
    mTmin: 4680.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.933671508180186e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 817.0966718872296
  - mTmax: 4760.0
    mTmin: 4720.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.5879126959008846e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 923.052568298723
  - mTmax: 4800.0
    mTmin: 4760.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.463181630904389e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1024.921164912806
  - mTmax: 4840.0
    mTmin: 4800.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.4916616734128875e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1126.9224541487863
  - mTmax: 4880.0
    mTmin: 4840.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.1274323266335804e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1261.328656514209
  - mTmax: 4920.0
    mTmin: 4880.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.053739792937742e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1399.956650748852
  - mTmax: 4960.0
    mTmin: 4920.0
    name: R_13(pp->enu)
    value:
      counts_background: 6.437479818647312e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1556.5676804062232
  - mTmax: 5000.0
    mTmin: 4960.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.2567644552441648e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1725.0367751950323
  - mTmax: 5040.0
    mTmin: 5000.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.0649766439065436e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1926.8436826238556
  - mTmax: 5080.0
    mTmin: 5040.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.203325412649544e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2200.0798405391024
  - mTmax: 5120.0
    mTmin: 5080.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.726041742087404e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2431.632204644033
  - mTmax: 5160.0
    mTmin: 5120.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.867252783972797e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2718.112410092839
  - mTmax: 5200.0
    mTmin: 5160.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.508233519284025e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 3008.976091121458
  - mTmax: 5240.0
    mTmin: 5200.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.0779837251972395e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 3334.2145126687037
  - mTmax: 5280.0
    mTmin: 5240.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.08220717552389e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 3806.2889448599876
  - mTmax: 5320.0
    mTmin: 5280.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.056137264655654e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 4249.926131229805
  - mTmax: 5360.0
    mTmin: 5320.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.6799186385319906e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 4731.248722398351
  - mTmax: 5400.0
    mTmin: 5360.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.085987506298277e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 5383.345343434887
  - mTmax: 5440.0
    mTmin: 5400.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.8102184195864776e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 5873.857074774798
  - mTmax: 5480.0
    mTmin: 5440.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.8595231077256377e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 6747.657716416054
  - mTmax: 5520.0
    mTmin: 5480.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.394244779141172e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 7595.5462082709255
  - mTmax: 5560.0
    mTmin: 5520.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.2235001397255476e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 8458.483598060082
  - mTmax: 5600.0
    mTmin: 5560.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.850516627508042e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 9430.046128517019
  - mTmax: 5640.0
    mTmin: 5600.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.1649513034681135e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 10444.011421248497
  - mTmax: 5680.0
    mTmin: 5640.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.9345015733457527e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 12015.202010246
  - mTmax: 5720.0
    mTmin: 5680.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.162264152635207e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 14034.044059440228
  - mTmax: 5760.0
    mTmin: 5720.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.1816500531249325e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 15494.549440110264
  - mTmax: 5800.0
    mTmin: 5760.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.6000993590612424e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 18595.43125956885
  - mTmax: 5840.0
    mTmin: 5800.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.5627718461191266e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 20242.67342818032
  - mTmax: 5880.0
    mTmin: 5840.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.0161903792706209e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 23810.403295865148
  - mTmax: 5920.0
    mTmin: 5880.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.587251669707391e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 28930.870155265697
  - mTmax: 5960.0
    mTmin: 5920.0
    name: R_13(pp->enu)
    value:
      counts_background: 7.940236065855564e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 34292.65787119252
  - mTmax: 6000.0
    mTmin: 5960.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.1407201667677625e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 41917.90208558081
  - mTmax: 6040.0
    mTmin: 6000.0
    name: R_13(pp->enu)
    value:
      counts_background: 9.141031598388679e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 48730.75432539665
  - mTmax: 6080.0
    mTmin: 6040.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.8298781084494e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 61303.17657131522
  - mTmax: 6120.0
    mTmin: 6080.0
    name: R_13(pp->enu)
    value:
      counts_background: 7.301666926456176e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 71972.85379834744
  - mTmax: 6160.0
    mTmin: 6120.0
    name: R_13(pp->enu)
    value:
      counts_background: 7.822411433375862e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 84399.47027772808
  - mTmax: 6200.0
    mTmin: 6160.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.1984038714329863e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 104247.40628284871
  - mTmax: 6240.0
    mTmin: 6200.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.334706140812458e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 120654.25879817129
  - mTmax: 6280.0
    mTmin: 6240.0
    name: R_13(pp->enu)
    value:
      counts_background: 8.431783902619568e-09
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 138282.82359883687
  - mTmax: 6320.0
    mTmin: 6280.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.813155029970277e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 147160.81217761873
  - mTmax: 6360.0
    mTmin: 6320.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.8683753799690182e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 185079.06169890647
  - mTmax: 6400.0
    mTmin: 6360.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.057573799375826e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 201366.51979006067
  - mTmax: 6440.0
    mTmin: 6400.0
    name: R_13(pp->enu)
    value:
      counts_background: 5.453927004120833e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 256598.79611338233
  - mTmax: 6480.0
    mTmin: 6440.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.0671716027220986e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 290725.740290646
  - mTmax: 6520.0
    mTmin: 6480.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.2663346806840298e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 306606.1018124745
  - mTmax: 6560.0
    mTmin: 6520.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.4034117459171998e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 203881.97724314997
  - mTmax: 6600.0
    mTmin: 6560.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.014975731391466e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 380179.1236037249
  - mTmax: 6640.0
    mTmin: 6600.0
    name: R_13(pp->enu)
    value:
      counts_background: 4.845789870131363e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 434810.8763701932
  - mTmax: 6680.0
    mTmin: 6640.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.5824822650566445e-10
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 499659.12945690413
  - mTmax: 6720.0
    mTmin: 6680.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.2807492962060854e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 578459.754922838
  - mTmax: 6760.0
    mTmin: 6720.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.8269203880691544e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 607516.8058698938
  - mTmax: 6800.0
    mTmin: 6760.0
    name: R_13(pp->enu)
    value:
      counts_background: 3.5833460107032355e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 754965.9379987472
  - mTmax: 6840.0
    mTmin: 6800.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.3478336481166037e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 309643.4904872193
  - mTmax: 6880.0
    mTmin: 6840.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.8561472679585762e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 830098.0727409918
  - mTmax: 6920.0
    mTmin: 6880.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.164606019346795e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 858995.7601462529
  - mTmax: 6960.0
    mTmin: 6920.0
    name: R_13(pp->enu)
    value:
      counts_background: 1.8470459358825692e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 766507.7165064398
  - mTmax: 7000.0
    mTmin: 6960.0
    name: R_13(pp->enu)
    value:
      counts_background: 2.727124618225561e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1041350.6277935408

CMS pp->mumu 2021:
  experiment: CMS
  inspire: CMS:2021ctt
  values:
  - name: R_13(pp->mumu)
    qmax: 129.95
    qmin: 120.0
    value:
      background_std: 7121.214999999992
      counts_background: 9737.824805766377
      counts_total: 161836.74999999983
      distribution: general_gamma_counting_process
      scale_factor: 6.63886219674713e-06
  - name: R_13(pp->mumu)
    qmax: 140.74
    qmin: 129.95
    value:
      background_std: 5933.636800000011
      counts_background: 12407.694138500712
      counts_total: 148750.9400000003
      distribution: general_gamma_counting_process
      scale_factor: 7.545316742608385e-06
  - name: R_13(pp->mumu)
    qmax: 152.41
    qmin: 140.74
    value:
      background_std: 4336.571999999996
      counts_background: 13023.632672379501
      counts_total: 118462.16999999987
      distribution: general_gamma_counting_process
      scale_factor: 9.820692631382591e-06
  - name: R_13(pp->mumu)
    qmax: 165.05
    qmin: 152.41
    value:
      background_std: 4070.8384000000046
      counts_background: 15090.863954325916
      counts_total: 109457.34400000013
      distribution: general_gamma_counting_process
      scale_factor: 1.026474768552655e-05
  - name: R_13(pp->mumu)
    qmax: 178.75
    qmin: 165.05
    value:
      background_std: 2827.6799999999976
      counts_background: 15596.582516983219
      counts_total: 91418.72999999992
      distribution: general_gamma_counting_process
      scale_factor: 1.3359013205124682e-05
  - name: R_13(pp->mumu)
    qmax: 193.57
    qmin: 178.75
    value:
      background_std: 2144.157599999999
      counts_background: 15039.387246468696
      counts_total: 74643.89399999996
      distribution: general_gamma_counting_process
      scale_factor: 1.713588935538449e-05
  - name: R_13(pp->mumu)
    qmax: 209.63
    qmin: 193.57
    value:
      background_std: 1699.4692000000002
      counts_background: 14440.315894195808
      counts_total: 60618.47000000001
      distribution: general_gamma_counting_process
      scale_factor: 2.1364661053439985e-05
  - name: R_13(pp->mumu)
    qmax: 227.02
    qmin: 209.63
    value:
      background_std: 1391.0087100000012
      counts_background: 13115.370944250135
      counts_total: 49128.48900000004
      distribution: general_gamma_counting_process
      scale_factor: 2.6772501957072506e-05
  - name: R_13(pp->mumu)
    qmax: 245.86
    qmin: 227.02
    value:
      background_std: 1108.0934400000003
      counts_background: 11846.440962160255
      counts_total: 41800.308000000005
      distribution: general_gamma_counting_process
      scale_factor: 3.3343378325497194e-05
  - name: R_13(pp->mumu)
    qmax: 266.25
    qmin: 245.86
    value:
      background_std: 905.1120999999994
      counts_background: 9906.311130469863
      counts_total: 32648.46799999998
      distribution: general_gamma_counting_process
      scale_factor: 4.333015127353089e-05
  - name: R_13(pp->mumu)
    qmax: 288.34
    qmin: 266.25
    value:
      background_std: 739.9929099999993
      counts_background: 8459.131839730098
      counts_total: 26435.10299999997
      distribution: general_gamma_counting_process
      scale_factor: 5.416300782576308e-05
  - name: R_13(pp->mumu)
    qmax: 312.26
    qmin: 288.34
    value:
      background_std: 613.7872000000004
      counts_background: 6882.0943276267335
      counts_total: 21187.618400000014
      distribution: general_gamma_counting_process
      scale_factor: 6.827104799814105e-05
  - name: R_13(pp->mumu)
    qmax: 338.16
    qmin: 312.26
    value:
      background_std: 503.44420000000065
      counts_background: 5550.806232855154
      counts_total: 16796.668000000023
      distribution: general_gamma_counting_process
      scale_factor: 8.800172302419657e-05
  - name: R_13(pp->mumu)
    qmax: 366.21
    qmin: 338.16
    value:
      background_std: 396.76724999999936
      counts_background: 4372.215083799877
      counts_total: 13169.75549999998
      distribution: general_gamma_counting_process
      scale_factor: 0.00011458770545969887
  - name: R_13(pp->mumu)
    qmax: 396.59
    qmin: 366.21
    value:
      background_std: 311.09119999999996
      counts_background: 3412.248229472873
      counts_total: 10490.213999999998
      distribution: general_gamma_counting_process
      scale_factor: 0.0001445235611100018
  - name: R_13(pp->mumu)
    qmax: 429.49
    qmin: 396.59
    value:
      background_std: 242.26244000000025
      counts_background: 2479.7114595669227
      counts_total: 7649.9080000000085
      distribution: general_gamma_counting_process
      scale_factor: 0.0001890272305312742
  - name: R_13(pp->mumu)
    qmax: 465.12
    qmin: 429.49
    value:
      background_std: 193.88064499999996
      counts_background: 1987.848217691081
      counts_total: 6128.003699999999
      distribution: general_gamma_counting_process
      scale_factor: 0.0002363895586520066
  - name: R_13(pp->mumu)
    qmax: 503.71
    qmin: 465.12
    value:
      background_std: 167.36482999999987
      counts_background: 1538.0020215451727
      counts_total: 4612.662699999997
      distribution: general_gamma_counting_process
      scale_factor: 0.00031051332441116075
  - name: R_13(pp->mumu)
    qmax: 545.49
    qmin: 503.71
    value:
      background_std: 140.1510100000001
      counts_background: 997.3104239944079
      counts_total: 3456.5429600000025
      distribution: general_gamma_counting_process
      scale_factor: 0.0004196882985300517
  - name: R_13(pp->mumu)
    qmax: 590.74
    qmin: 545.49
    value:
      background_std: 112.667975
      counts_background: 738.2701471866559
      counts_total: 2634.9075
      distribution: general_gamma_counting_process
      scale_factor: 0.0005196990623977533
  - name: R_13(pp->mumu)
    qmax: 639.75
    qmin: 590.74
    value:
      background_std: 85.89492599999998
      counts_background: 505.9382896444369
      counts_total: 1979.1708299999998
      distribution: general_gamma_counting_process
      scale_factor: 0.0007040851580270638
  - name: R_13(pp->mumu)
    qmax: 692.82
    qmin: 639.75
    value:
      background_std: 64.87276800000005
      counts_background: 340.5871490233496
      counts_total: 1477.9464300000013
      distribution: general_gamma_counting_process
      scale_factor: 0.0009281468484802702
  - name: R_13(pp->mumu)
    qmax: 750.29
    qmin: 692.82
    value:
      background_std: 50.74600999999993
      counts_background: 242.94975272099649
      counts_total: 1015.9546599999985
      distribution: general_gamma_counting_process
      scale_factor: 0.0012415543238572756
  - name: R_13(pp->mumu)
    qmax: 812.54
    qmin: 750.29
    value:
      background_std: 37.176944999999996
      counts_background: 164.68857675237646
      counts_total: 759.0765
      distribution: general_gamma_counting_process
      scale_factor: 0.0016202682492240407
  - name: R_13(pp->mumu)
    qmax: 879.94
    qmin: 812.54
    value:
      background_std: 26.577842000000036
      counts_background: 103.10131781332407
      counts_total: 573.9581800000008
      distribution: general_gamma_counting_process
      scale_factor: 0.00221828186409762
  - name: R_13(pp->mumu)
    qmax: 952.94
    qmin: 879.94
    value:
      background_std: 20.075000000000003
      counts_background: 71.69678067685018
      counts_total: 389.017
      distribution: general_gamma_counting_process
      scale_factor: 0.0030160058310544184
  - name: R_13(pp->mumu)
    qmax: 1032.0
    qmin: 952.94
    value:
      background_std: 16.01834659999999
      counts_background: 48.64362460396296
      counts_total: 295.0282019999998
      distribution: general_gamma_counting_process
      scale_factor: 0.004107093994648557
  - name: R_13(pp->mumu)
    qmax: 1117.6
    qmin: 1032.0
    value:
      background_std: 10.96707199999999
      counts_background: 28.973708612553843
      counts_total: 201.9731999999998
      distribution: general_gamma_counting_process
      scale_factor: 0.0056315816930471016
  - name: R_13(pp->mumu)
    qmax: 1210.3
    qmin: 1117.6
    value:
      background_std: 7.776973800000003
      counts_background: 18.975917552292035
      counts_total: 131.98626000000007
      distribution: general_gamma_counting_process
      scale_factor: 0.007737418112646101
  - name: R_13(pp->mumu)
    qmax: 1310.7
    qmin: 1210.3
    value:
      background_std: 5.860348000000005
      counts_background: 11.777595389144965
      counts_total: 106.99628000000011
      distribution: general_gamma_counting_process
      scale_factor: 0.010670808626178873
  - name: R_13(pp->mumu)
    qmax: 1419.4
    qmin: 1310.7
    value:
      background_std: 4.029617700000002
      counts_background: 7.110327399502672
      counts_total: 70.97892600000003
      distribution: general_gamma_counting_process
      scale_factor: 0.015432354256804488
  - name: R_13(pp->mumu)
    qmax: 1537.2
    qmin: 1419.4
    value:
      background_std: 2.8347391999999987
      counts_background: 4.744557257978962
      counts_total: 59.023689999999974
      distribution: general_gamma_counting_process
      scale_factor: 0.022300989477252738
  - name: R_13(pp->mumu)
    qmax: 1664.7
    qmin: 1537.2
    value:
      background_std: 2.4225
      counts_background: 4.736851544736749
      counts_total: 26.995575
      distribution: general_gamma_counting_process
      scale_factor: 0.03226492701949835
  - name: R_13(pp->mumu)
    qmax: 1802.8
    qmin: 1664.7
    value:
      background_std: 1.349043659999999
      counts_background: 1.9522842499239974
      counts_total: 17.99995399999999
      distribution: general_gamma_counting_process
      scale_factor: 0.04763836260928834
  - name: R_13(pp->mumu)
    qmax: 1952.4
    qmin: 1802.8
    value:
      background_std: 1.137348960000001
      counts_background: 2.5046589020574546
      counts_total: 13.003980000000013
      distribution: general_gamma_counting_process
      scale_factor: 0.07099243307721687
  - name: R_13(pp->mumu)
    qmax: 2114.3
    qmin: 1952.4
    value:
      background_std: 0.6227807300000003
      counts_background: 0.5955559093625553
      counts_total: 10.995924200000006
      distribution: general_gamma_counting_process
      scale_factor: 0.10870827760983351
  - name: R_13(pp->mumu)
    qmax: 2289.7
    qmin: 2114.3
    value:
      background_std: 0.4413414799999991
      counts_background: 0.29515276868574336
      counts_total: 5.00012779999999
      distribution: general_gamma_counting_process
      scale_factor: 0.167487590606583
  - name: R_13(pp->mumu)
    qmax: 2479.7
    qmin: 2289.7
    value:
      background_std: 0.27607000000000004
      counts_background: 0.20015551084469524
      counts_total: 5.00137
      distribution: general_gamma_counting_process
      scale_factor: 0.2674513195145638
  - name: R_13(pp->mumu)
    qmax: 2685.4
    qmin: 2479.7
    value:
      background_std: 0.25381323000000033
      counts_background: 0.47702046834357753
      counts_total: 3.9998365000000056
      distribution: general_gamma_counting_process
      scale_factor: 0.4389009214653366
  - name: R_13(pp->mumu)
    qmax: 2908.1
    qmin: 2685.4
    value:
      background_std: 0.11024318099999991
      counts_background: 0.03297435038722071
      counts_total: 1.9993783299999985
      distribution: general_gamma_counting_process
      scale_factor: 0.7131174862648247
  - name: R_13(pp->mumu)
    qmax: 3149.4
    qmin: 2908.1
    value:
      background_std: 0.06986841500000006
      counts_background: 0.04458324569433998
      counts_total: 1.0002126300000007
      distribution: general_gamma_counting_process
      scale_factor: 1.2314791787980226
  - name: R_13(pp->mumu)
    qmax: 3410.7
    qmin: 3149.4
    value:
      background_std: 0.05643296099999994
      counts_background: 0.07514250176724041
      counts_total: 1.0001518799999989
      distribution: general_gamma_counting_process
      scale_factor: 2.168009269460113
  - name: R_13(pp->mumu)
    qmax: 3693.6
    qmin: 3410.7
    value:
      background_std: 0.03388293300000001
      counts_background: 0.01668698212327797
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 3.926834312717107
  - name: R_13(pp->mumu)
    qmax: 4000.0
    qmin: 3693.6
    value:
      background_std: 0.016785204800000005
      counts_background: 0.004858630873580564
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 7.4457838699106365
  - name: R_13(pp->mumu)
    qmax: 4500.0
    qmin: 4000.0
    value:
      background_std: 0.0198925
      counts_background: 0.024312284528648097
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 11.631275580400724
  - name: R_13(pp->mumu)
    qmax: 5200.0
    qmin: 4500.0
    value:
      counts_background: 0.006999999999999912
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 42.34938830898644

CMS pp->munu 2022:
  experiment: CMS
  inspire: CMS:2022yjm
  values:
  - mTmax: 218.28571428571428
    mTmin: 120.0
    name: R_13(pp->munu)
    value:
      background_std: 764326.3
      counts_background: 735456.4777480316
      counts_total: 8082423.0
      distribution: general_gamma_counting_process
      scale_factor: 1.381100504452376e-07
  - mTmax: 316.57142857142856
    mTmin: 218.28571428571428
    name: R_13(pp->munu)
    value:
      background_std: 28257.3
      counts_background: 60370.10313703723
      counts_total: 293361.0
      distribution: general_gamma_counting_process
      scale_factor: 4.5080589494231244e-06
  - mTmax: 414.8571428571429
    mTmin: 316.57142857142856
    name: R_13(pp->munu)
    value:
      background_std: 5851.09
      counts_background: 11483.256415576703
      counts_total: 59924.0
      distribution: general_gamma_counting_process
      scale_factor: 2.1202901353921295e-05
  - mTmax: 513.1428571428571
    mTmin: 414.8571428571429
    name: R_13(pp->munu)
    value:
      background_std: 1859.65
      counts_background: 2834.0427140980073
      counts_total: 18841.0
      distribution: general_gamma_counting_process
      scale_factor: 6.457148220281266e-05
  - mTmax: 611.4285714285714
    mTmin: 513.1428571428571
    name: R_13(pp->munu)
    value:
      background_std: 747.879
      counts_background: 895.805088818062
      counts_total: 7267.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0001616463699144605
  - mTmax: 709.7142857142858
    mTmin: 611.4285714285714
    name: R_13(pp->munu)
    value:
      background_std: 353.206
      counts_background: 361.61575189695833
      counts_total: 3255.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0003514780917579742
  - mTmax: 808.0
    mTmin: 709.7142857142858
    name: R_13(pp->munu)
    value:
      background_std: 179.091
      counts_background: 149.32036560618837
      counts_total: 1611.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0006984493205069298
  - mTmax: 906.2857142857143
    mTmin: 808.0
    name: R_13(pp->munu)
    value:
      background_std: 97.7124
      counts_background: 57.76185137943858
      counts_total: 876.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0012935598118303038
  - mTmax: 1004.5714285714287
    mTmin: 906.2857142857143
    name: R_13(pp->munu)
    value:
      background_std: 62.5286
      counts_background: 37.55312637975146
      counts_total: 467.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0022871572872031763
  - mTmax: 1102.857142857143
    mTmin: 1004.5714285714287
    name: R_13(pp->munu)
    value:
      background_std: 35.7788
      counts_background: 17.25852637339621
      counts_total: 282.0
      distribution: general_gamma_counting_process
      scale_factor: 0.0038788180897831002
  - mTmax: 1201.142857142857
    mTmin: 1102.857142857143
    name: R_13(pp->munu)
    value:
      background_std: 25.9187
      counts_background: 15.164570356372504
      counts_total: 178.0
      distribution: general_gamma_counting_process
      scale_factor: 0.006217144659820986
  - mTmax: 1299.4285714285716
    mTmin: 1201.142857142857
    name: R_13(pp->munu)
    value:
      background_std: 14.5396
      counts_background: 6.057353550907621
      counts_total: 115.0
      distribution: general_gamma_counting_process
      scale_factor: 0.01004697764321072
  - mTmax: 1397.7142857142858
    mTmin: 1299.4285714285716
    name: R_13(pp->munu)
    value:
      background_std: 9.55914
      counts_background: 2.7593736736576306
      counts_total: 71.0
      distribution: general_gamma_counting_process
      scale_factor: 0.01541561367084377
  - mTmax: 1496.0
    mTmin: 1397.7142857142858
    name: R_13(pp->munu)
    value:
      background_std: 6.64664
      counts_background: 1.9520955749150137
      counts_total: 40.0
      distribution: general_gamma_counting_process
      scale_factor: 0.023220193353268782
  - mTmax: 1594.2857142857144
    mTmin: 1496.0
    name: R_13(pp->munu)
    value:
      background_std: 5.7114
      counts_background: 2.9067998806677164
      counts_total: 41.0
      distribution: general_gamma_counting_process
      scale_factor: 0.03441546460678311
  - mTmax: 1692.5714285714287
    mTmin: 1594.2857142857144
    name: R_13(pp->munu)
    value:
      background_std: 3.2872
      counts_background: 0.7204998962755044
      counts_total: 33.0
      distribution: general_gamma_counting_process
      scale_factor: 0.050429467699783175
  - mTmax: 1790.857142857143
    mTmin: 1692.5714285714287
    name: R_13(pp->munu)
    value:
      background_std: 2.429
      counts_background: 0.6367605053114246
      counts_total: 10.0
      distribution: general_gamma_counting_process
      scale_factor: 0.07345482522107218
  - mTmax: 1889.1428571428573
    mTmin: 1790.857142857143
    name: R_13(pp->munu)
    value:
      background_std: 1.96496
      counts_background: 1.1195918643365383
      counts_total: 16.0
      distribution: general_gamma_counting_process
      scale_factor: 0.10214590783781516
  - mTmax: 1987.4285714285716
    mTmin: 1889.1428571428573
    name: R_13(pp->munu)
    value:
      background_std: 1.53658
      counts_background: 0.3011358874083727
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.14426901221246954
  - mTmax: 2085.714285714286
    mTmin: 1987.4285714285716
    name: R_13(pp->munu)
    value:
      background_std: 1.06203
      counts_background: 0.5289724930974729
      counts_total: 5.0
      distribution: general_gamma_counting_process
      scale_factor: 0.20042802700410473
  - mTmax: 2184.0
    mTmin: 2085.714285714286
    name: R_13(pp->munu)
    value:
      background_std: 0.789811
      counts_background: 0.25307606773948504
      counts_total: 5.0
      distribution: general_gamma_counting_process
      scale_factor: 0.2759213739465906
  - mTmax: 2282.285714285714
    mTmin: 2184.0
    name: R_13(pp->munu)
    value:
      background_std: 1.64016
      counts_background: 0.07017318305228824
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 0.2486947919892465
  - mTmax: 2380.571428571429
    mTmin: 2282.285714285714
    name: R_13(pp->munu)
    value:
      background_std: 0.532257
      counts_background: 0.18578587621395445
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.5215022051516215
  - mTmax: 2478.857142857143
    mTmin: 2380.571428571429
    name: R_13(pp->munu)
    value:
      background_std: 0.401721
      counts_background: 0.014027089270265821
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 0.7015769816918597
  - mTmax: 2577.1428571428573
    mTmin: 2478.857142857143
    name: R_13(pp->munu)
    value:
      background_std: 0.353156
      counts_background: 0.0572407434906522
      counts_total: 3.0
      distribution: general_gamma_counting_process
      scale_factor: 0.9426817545512813
  - mTmax: 2675.4285714285716
    mTmin: 2577.1428571428573
    name: R_13(pp->munu)
    value:
      background_std: 0.273798
      counts_background: 0.009280203355479627
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.2728362695780504
  - mTmax: 2773.714285714286
    mTmin: 2675.4285714285716
    name: R_13(pp->munu)
    value:
      background_std: 0.408859
      counts_background: 0.3260113188814421
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 1.7081370916365182
  - mTmax: 2872.0
    mTmin: 2773.714285714286
    name: R_13(pp->munu)
    value:
      background_std: 0.178459
      counts_background: 0.0050630557964758596
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 2.1573914897452897
  - mTmax: 2970.2857142857147
    mTmin: 2872.0
    name: R_13(pp->munu)
    value:
      background_std: 0.154555
      counts_background: 0.02354030895411082
      counts_total: 2.0
      distribution: general_gamma_counting_process
      scale_factor: 2.923616167189418
  - mTmax: 3068.571428571429
    mTmin: 2970.2857142857147
    name: R_13(pp->munu)
    value:
      background_std: 0.11898
      counts_background: 0.002754887756233705
      counts_total: 1.0
      distribution: general_gamma_counting_process
      scale_factor: 3.891484286778623
  - mTmax: 3166.857142857143
    mTmin: 3068.571428571429
    name: R_13(pp->munu)
    value:
      background_std: 0.0983986
      counts_background: 0.002418966840862466
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 5.025321423756287
  - mTmax: 3265.1428571428573
    mTmin: 3166.857142857143
    name: R_13(pp->munu)
    value:
      background_std: 0.07899
      counts_background: 0.0016655879745978085
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 6.630667669687228
  - mTmax: 3363.4285714285716
    mTmin: 3265.1428571428573
    name: R_13(pp->munu)
    value:
      background_std: 0.061663
      counts_background: 0.0010220913348152952
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 8.580794897857855
  - mTmax: 3461.714285714286
    mTmin: 3363.4285714285716
    name: R_13(pp->munu)
    value:
      background_std: 0.05249
      counts_background: 0.0012019722815964323
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 11.18786713539267
  - mTmax: 3560.0
    mTmin: 3461.714285714286
    name: R_13(pp->munu)
    value:
      background_std: 0.043518
      counts_background: 0.0005595119230388659
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 14.229179567277571
  - mTmax: 3658.2857142857147
    mTmin: 3560.0
    name: R_13(pp->munu)
    value:
      background_std: 0.035888
      counts_background: 0.0025767861577569613
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 18.633054553135672
  - mTmax: 3756.571428571429
    mTmin: 3658.2857142857147
    name: R_13(pp->munu)
    value:
      background_std: 0.02898
      counts_background: 0.00032981552772133523
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 24.00049431696484
  - mTmax: 3854.857142857143
    mTmin: 3756.571428571429
    name: R_13(pp->munu)
    value:
      background_std: 0.02309
      counts_background: 0.0002507929010435966
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 30.465794327480626
  - mTmax: 3953.1428571428573
    mTmin: 3854.857142857143
    name: R_13(pp->munu)
    value:
      background_std: 0.019
      counts_background: 0.0002074231380965868
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 39.48173087374054
  - mTmax: 4051.4285714285716
    mTmin: 3953.1428571428573
    name: R_13(pp->munu)
    value:
      background_std: 0.01527
      counts_background: 0.00010254307466266231
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 49.38721600969236
  - mTmax: 4149.714285714286
    mTmin: 4051.4285714285716
    name: R_13(pp->munu)
    value:
      background_std: 0.0123
      counts_background: 0.0001256563671538112
      counts_total: 0.0
      distribution: general_gamma_counting_process
      scale_factor: 63.077501791994194
  - mTmax: 4248.0
    mTmin: 4149.714285714286
    name: R_13(pp->munu)
    value:
      counts_background: 7.422452605320821e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 79.73851133087038
  - mTmax: 4346.285714285715
    mTmin: 4248.0
    name: R_13(pp->munu)
    value:
      counts_background: 4.5836416220864686e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 100.94154898576248
  - mTmax: 4444.571428571428
    mTmin: 4346.285714285715
    name: R_13(pp->munu)
    value:
      counts_background: 3.761930232618374e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 126.46773127308612
  - mTmax: 4542.857142857143
    mTmin: 4444.571428571428
    name: R_13(pp->munu)
    value:
      counts_background: 2.3201214556545247e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 161.447630038755
  - mTmax: 4641.142857142858
    mTmin: 4542.857142857143
    name: R_13(pp->munu)
    value:
      counts_background: 1.816860522123703e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 198.5475565878203
  - mTmax: 4739.428571428572
    mTmin: 4641.142857142858
    name: R_13(pp->munu)
    value:
      counts_background: 1.29962616478234e-05
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 243.78335597070824
  - mTmax: 4837.714285714286
    mTmin: 4739.428571428572
    name: R_13(pp->munu)
    value:
      counts_background: 8.171314021369165e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 313.00928079960136
  - mTmax: 4936.0
    mTmin: 4837.714285714286
    name: R_13(pp->munu)
    value:
      counts_background: 5.702788130690082e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 384.08487575039294
  - mTmax: 5034.285714285715
    mTmin: 4936.0
    name: R_13(pp->munu)
    value:
      counts_background: 2.655536816362048e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 465.19519783338
  - mTmax: 5132.571428571428
    mTmin: 5034.285714285715
    name: R_13(pp->munu)
    value:
      counts_background: 2.1545588755475023e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 585.2980095021534
  - mTmax: 5230.857142857143
    mTmin: 5132.571428571428
    name: R_13(pp->munu)
    value:
      counts_background: 6.715722933529167e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 712.0715988138246
  - mTmax: 5329.142857142858
    mTmin: 5230.857142857143
    name: R_13(pp->munu)
    value:
      counts_background: 1.9201839461521176e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 869.0425101085982
  - mTmax: 5427.428571428572
    mTmin: 5329.142857142858
    name: R_13(pp->munu)
    value:
      counts_background: 1.3061289602974232e-06
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 605.1382199610066
  - mTmax: 5525.714285714286
    mTmin: 5427.428571428572
    name: R_13(pp->munu)
    value:
      counts_background: 9.336466069482163e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1283.8728175198783
  - mTmax: 5624.0
    mTmin: 5525.714285714286
    name: R_13(pp->munu)
    value:
      counts_background: 7.598061149352847e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1574.479741425196
  - mTmax: 5722.285714285715
    mTmin: 5624.0
    name: R_13(pp->munu)
    value:
      counts_background: 9.628309402163802e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 1915.653134844684
  - mTmax: 5820.571428571429
    mTmin: 5722.285714285715
    name: R_13(pp->munu)
    value:
      counts_background: 6.803814408712961e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2144.379517263722
  - mTmax: 5918.857142857143
    mTmin: 5820.571428571429
    name: R_13(pp->munu)
    value:
      counts_background: 4.2377277319657177e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 2577.715998415671
  - mTmax: 6017.142857142858
    mTmin: 5918.857142857143
    name: R_13(pp->munu)
    value:
      counts_background: 6.177460889176766e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 3192.8273162849705
  - mTmax: 6115.428571428572
    mTmin: 6017.142857142858
    name: R_13(pp->munu)
    value:
      counts_background: 3.619143173349792e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 3744.6517259682723
  - mTmax: 6213.714285714286
    mTmin: 6115.428571428572
    name: R_13(pp->munu)
    value:
      counts_background: 3.155387757124606e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 4574.050044622984
  - mTmax: 6312.0
    mTmin: 6213.714285714286
    name: R_13(pp->munu)
    value:
      counts_background: 3.897156780874507e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 5338.906940974334
  - mTmax: 6410.285714285715
    mTmin: 6312.0
    name: R_13(pp->munu)
    value:
      counts_background: 2.4091380627527464e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 6319.666512062608
  - mTmax: 6508.571428571429
    mTmin: 6410.285714285715
    name: R_13(pp->munu)
    value:
      counts_background: 1.9913188557108668e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 7059.013681710888
  - mTmax: 6606.857142857143
    mTmin: 6508.571428571429
    name: R_13(pp->munu)
    value:
      counts_background: 1.4249113987876678e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 8550.36091241205
  - mTmax: 6705.142857142858
    mTmin: 6606.857142857143
    name: R_13(pp->munu)
    value:
      counts_background: 1.194606974578001e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 9635.756419654661
  - mTmax: 6803.428571428572
    mTmin: 6705.142857142858
    name: R_13(pp->munu)
    value:
      counts_background: 1.3050822275305631e-07
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 10579.458557629101
  - mTmax: 6901.714285714286
    mTmin: 6803.428571428572
    name: R_13(pp->munu)
    value:
      counts_background: 9.860600769233048e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 12759.008661759273
  - mTmax: 7000.0
    mTmin: 6901.714285714286
    name: R_13(pp->munu)
    value:
      counts_background: 5.7520370590772414e-08
      counts_total: 0.0
      distribution: gamma_counting_process
      scale_factor: 15181.392014563447