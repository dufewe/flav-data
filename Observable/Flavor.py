with open('./defs.py', 'r', encoding='utf-8') as f:
    exec(f.read())

st.sidebar.button("sss")

st.markdown('''
for charged-current beauty processes $B\\to M\\ell\\nu$, the observables include
1. forward-backward asymmetry:
            
$$A_{FB}(q^2) \\equiv \\left(\\int_0^1 \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2d\\cos\\theta} d\\cos\\theta - \\int_{-1}^0 \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2d\\cos\\theta} d\\cos\\theta \\right) \\bigg/ \\int_{-1}^1 \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2d\\cos\\theta} d\\cos\\theta$$
            
2. polarization asymmetry of lepton (left-right asymmetry?):
            
$$P_\\ell (q^2) \\equiv \\left(\\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2} \\bigg|_{\\lambda_\ell = +1/2} - \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2} \\bigg|_{\\lambda_\ell = -1/2}\\right) \\bigg/ \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2}$$
            
3. longitudinal polarization fraction of vector meson $M$: 
    
$$F_L^M (q^2) \\equiv \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2} \\bigg|_{\\lambda_M = 0} \\bigg/ \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2}$$

4. branching ratio: 
        
$$\\mathcal{B}(B\\to M\\ell\\nu) \\equiv \\Gamma(B\\to M\\ell\\nu) \\bigg/ \\Gamma_B^{\\rm tot}$$

5. lepton flavor universality violation observable with $\\ell = \\mu, e$:
            
$$R_M^{\\tau\\ell} \\equiv \\int_{m_\\tau^2}^{(m_B-m_M)^2} \\frac{d\\Gamma(B\\to M\\tau\\nu)}{dq^2} dq^2 \\bigg/ \\int_0^{(m_B^2 - m_M)^2} \\frac{d\\Gamma(B\\to M\\ell\\nu)}{dq^2} dq^2$$


for neutral-current beauty processes $B\\to M\\ell\\ell$, the observables include
1. lepton flavor universality violation observable:
            
$$R_M^{\\mu e} \\equiv \\int_0^{(m_B-m_M)^2} \\frac{d\\Gamma(B\\to M\\mu\\mu)}{dq^2} dq^2 \\bigg/ \\int_0^{(m_B-m_M)^2} \\frac{d\\Gamma(B\\to Mee)}{dq^2} dq^2$$

2. CP-averaged isospin asymmetry of $B\\to K^{(\\ast)}\\mu\\mu$:
            
$$A_I \\equiv \\frac{\\Gamma(B^0\\to K^{(\\ast)0}\\mu\\mu) - \\Gamma(B^+\\to K^{(\\ast)+}\\mu\\mu)}{\\Gamma(B^0\\to K^{(\\ast)0}\\mu\\mu) + \\Gamma(B^+\\to K^{(\\ast)+}\\mu\\mu)}$$
            
3. differential branching fraction:
            
$$\\frac{d\\mathcal{B}(B\\to M\\ell\\ell)}{dq^2}$$

4. S-wave fraction (see 1606.04731):
            
$$F_S$$
            
5. angular observable:
            
$$F_L,S_3,S_4,S_7,A_5,A_{FB},A_6,A_8,A_9$$
$$F_L,A_3,A_4,A_5,A_{6s},A_7,A_8,A_9$$
$$F_L,S_3,S_4,S_5,A_{FB},S_7,S_8,S_9$$
$$F_L,P_1,P_2,P_3,P_4^\\prime,P_5^\\prime,P_6^\\prime,P_8^\\prime$$
$$F_L,A_T^{\\rm Re},A_T^{(2)},A_T^{\\rm Im}$$ (see 2010.06011, 1501.03038)
$$A_{FB}^\\ell,A_{FB}^h,f_L,A_{FB}^{\\ell h}$$ (see 1503.07138, 1808.00264)
            
$$K_1,K_2,K_{3-34}$$ (see 1710.00746, 1808.00264)
            
$$F_H,A_{FB}$$
            
$$A_{CP}$$
            
$$\\Sigma A_{FB}, \\Delta A_{FB}$$ (2502.04013)

''')


'''
    "+,0,-"
    "heavy,light"

    
    "inspire-hep": "[LHCb:2026dan](https://inspirehep.net/literature/3144939)",
    "author": "Aaij, Roel and others",
    "collaboration": "LHCb",
    "title": "Measurement of the $W$-boson production cross-sections in $pp$ collisions at $\\sqrt{s}$ = 13 TeV in the forward region",
    "arxiv": "[hep-ex/2604.12706v1](https://arxiv.org/pdf/2604.12706)",
    "year": "2026",
    "abstract": "a precision measurement of the $W$-boson production cross-section, using the $W \\to \\mu\\nu$ decay channel, based on a sample of proton-proton collision data collected by the LHCb experiment at $\\sqrt{s} = 13$ TeV and corresponding to an integrated luminosity of 5.1 fb$^{−1}$",
    "pdf": "https://arxiv.org/pdf/2604.12706",
    "data": [
    ]
'''