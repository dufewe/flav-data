# Worked Example: LHCb:2015svh

Angular analysis of $B^0 \to K^{*0}\mu^+\mu^-$ — arXiv 1512.04442, Inspire
recid 1409497, JHEP 02 (2016) 104, HEPData 83 tables. Stored at
`expe-data/CERN-LHCb/2015/12/LHCb:2015svh.json`, indexed under month `12`.

The generic steps (discovery, metadata lookup, JSON assembly, validation,
index update, cleanup) are in SKILL.md §Workflow. This file records only
what is specific to this paper.

## HEPData table inventory
- **Tables 1–8: observables.** Table 1 has 22 observables at 2 q² bins; Table 2 has 8 CP-averaged observables (FL, S3–S9) at 8 bins; Tables 3–4 are the CP-asymmetric (A3–A9) and optimised (P1–P3, P'4/5/8) sets at 8 bins; Tables 5–7 repeat those sets with the method of moments at 15 bins; Table 8 holds zero-crossing points.
- **Tables 9–38: likelihood correlation matrices**, three 10-table sets with the same q² binning — 8 individual bins plus the merged ranges 1.1–6.0 and 15.0–19.0. Each matrix is 8×8 and belongs to one observable set; pick the set that matches the observables you imported.
- **Tables 39–53, 54–68, 69–83: bootstrap correlation matrices**, three 15-table sets using the finer q² binning (0.1–8, 11–12.5, 15–19). The 39–53 and 69–83 sets are 8×8; 54–68 is 7×7.

Classify by structure, not by description — `hepdata-ext.detect_table_type()`
inspects the YAML (a single dependent variable over 64/49 cells is a matrix;
repeated `CORR`-style independent variables confirm it).

## Choosing a matrix set

Appendices C–H provide likelihood and bootstrap matrices for the same q²
bins. Import one set — likelihood is the paper's nominal result — and keep
its binning consistent with the observable table you imported.

## Group layout

Each q² bin of the observable table becomes one element of the `data`
array, holding every observable of that bin under the channel key
`B0.2.K*0.mu+.mu-`. Table 9's matrix goes into the first (low-q²) group,
Table 10 into the second, and so on. The matrix is N×N with rows in
`obs@N` order, one row per line. Observables coupled by one source matrix
stay in that group even across channels (SKILL.md rule 6).

Canonical JSON shape: `references/json-meta.md` §"Data Entries".
