# Corrections ledger (revision 1 -> reviewed revision)

Itemized ledger of every claim that changed between the reviewed draft
(revision 1) and the revised paper, with the internal-check finding that
forced each change. This is the LaTeX source of the table formerly shipped
as Appendix C of the anchoring paper; the paper now carries a summary
paragraph and points here. Source abbreviations: stats / R2 / GECCO are the
three internal adversarial-check reports; council is the arbitration record.

```latex
\section{Corrections ledger}

\begingroup
\footnotesize
\begin{longtable}{@{}p{0.02\textwidth}p{0.05\textwidth}p{0.27\textwidth}p{0.38\textwidth}p{0.13\textwidth}@{}}
\caption{Corrections to revision 1. Every claim that changed between the reviewed
draft and this one, with the finding that forced it. \texttt{stats} =
\texttt{p4\_review\_stats.md}, \texttt{R2} = \texttt{p4\_review\_reviewer2.md}, \texttt{GECCO} =
\texttt{p4\_review\_gecco.md}, \texttt{council} = \texttt{p6\_cruxes.md}.}\label{tab:corrections}\\
\toprule
\textbf{\#} & \textbf{\S} & \textbf{Revision-1 claim} & \textbf{Corrected} & \textbf{Source} \\
\midrule
\endfirsthead
\toprule
\textbf{\#} & \textbf{\S} & \textbf{Revision-1 claim} & \textbf{Corrected} & \textbf{Source} \\
\midrule
\endhead
\midrule
\multicolumn{5}{r}{\emph{continued on next page}} \\
\endfoot
\bottomrule
\endlastfoot
1 & Abs, 1 & ``recall'' a template; ``template memorizer'' & behavioral vocabulary only: emits / concentrates / modal output & R2 \#2; R-E \\
2 & 2.3 & $\mathrm{round}(\sqrt{N})$ an empirical discovery; ``zero free parameters'' & a definition --- two formalizations of ``nearest'' coincide on the integers; weakly identified selection among four & GECCO M8; R2 \#24 \\
3 & 1.1, F1 & penalty ``hits exactly zero at the top of each zone'' & zero at $N = 14$, 15, 35, 48; \textbf{0.59\% residual at $N = 24$}; 4 of 22 trap $N$ cost nothing, so branch $\ne$ penalty & GECCO M14; R2 \#19 \\
4 & 1.1, 7 & ``published bounds sit above all of them'' & withdrawn: the $N = 26$ bound (2.63598) \emph{is} ShinkaEvolve's, so the LLM systems are the record; table stops at $N = 30$, leaving the LP abort gate unchecked above it & GECCO M3; R2 \#20--21 \\
5 & 3.3 & cap exclusions ``understated validity by 17\%'' & 77.8\% vs 70.0\% --- 7.8 points, 10\% relative; exclusion unregistered, both rates reported & R2 \#13; GECCO m15 \\
6 & 3.3, 6 & ``two parse failures''; ``two fraction-literal samples'' & three in each case & stats F14, F15 \\
7 & Abs, 1, 3.2 & ``predicts the exact sum-of-radii the model will emit'' & predicts the \textbf{empirical modal output} at 7/7 $N$; per-sample rate = modal frequency, 56--86\% by cell, 46\% pooled; round-number baseline 2/69 & R2 \#15; R-E \\
8 & 4.1 & one $a = 3$ sample left the family; rectangle ``confirmed'' & two (3.45, 3.5); all 11 valid samples characterized; partial support, CI $[21\%, 72\%]$, null stated & stats F16; R2 \#17; GECCO M9c \\
9 & Abs, 1, 5 & $32/45 = 71\%$; inversion 71 $\rightarrow$ 100 $\rightarrow$ 13 & \textbf{$35/45 = 77.8\%$} at $10^{-6}$, 64.4\% at $10^{-9}$; inversion 78 $\rightarrow$ 100 $\rightarrow$ 13 (64 $\rightarrow$ 90 $\rightarrow$ 13 strict); matched-cell 83 $\rightarrow$ 100 $\rightarrow$ 13 given separately & stats F1; R2 \#3; R-F \\
10 & 5 & Sonnet rival 6/30, 3/10 at $N = 31$ & 5/30 and 2/10 --- the 2.75 escape sits $1.47\times10^{-3}$ from the rival, inside the window; categorical claims now structural or at $10^{-6}$ & stats F12; R2 \#14 \\
11 & 1 & ``a monotone inversion'' & monotone in ambition only; validity rises then collapses & GECCO m21 \\
12 & 6.2 & P-T2 ``not confirmed'' ($p = 0.48$); P-T3 ``confirmed'' ($p = 0.0325$) & one rule applied symmetrically: P-T2 \textbf{confirmed as registered} (1/53 vs 2/50, no inferential weight); P-T3 met as registered but fragile & stats F7; R-C \\
13 & Abs, 1, 6.2 & ``leaving validity unchanged'' & no \emph{detectable} change ($p = 0.30$, $n = 60$/arm, underpowered); the P-T1 direction is entirely parse compliance --- 3 vs 0 parse failures, 7 vs 7 geometric & R2 \#7--8 \\
14 & 6.3 & ``the registered falsifier was not triggered'' & \textbf{triggered at 2 of 3 $N$} under the registered \texttt{<=}; not under the code's strict \texttt{<}; both reported, registered reading authoritative; pilot validity effect attributed to the bundled rewording & stats F8; R-B \\
15 & 6.4 & pilot produced two effects, both died at scale & a third ran in the P-T3 direction at the same cell (9/10 vs 4/7, $p = 0.16$): P-T3 replicated a pilot signal & stats F18 \\
16 & 6.5 & 12 claims excluded as ``no numeric content'' & regex coverage gaps; 9 of 12 carry checkable dimensions, quoted verbatim in \S6.5; worst case $38/53 = 72\%$ & stats F9 \\
17 & 6.5 & the three mismatches ``are all the same case'' & one of three; all three score MATCH under blind adjudication; the two remaining mismatches are alternation mis-descriptions (rows 11, 33) & stats F10; R-D \\
18 & 1, 7 & SeaEvo (2604.24372) reports a $\sim$2.636 packing value & removed: SeaEvo does not evaluate circle packing & GECCO M4 \\
19 & 7 & 2605.29268 reports asymmetric proposal mass in program space & deleted --- that paper is on bandit compute allocation; removing it leaves no cited evidence that the anchoring survives the code channel & GECCO M5 \\
20 & 7 & 2606.13603, 2605.29087 estimate faithfulness by perturbation / probing & both are causal-decoupling results; only 2503.08679 is an estimator & GECCO M6 \\
21 & 7, 8 & 2407.10873 and 2604.19440 filed as loop skepticism & 2407.10873 grounds the \emph{importance} of evolutionary search --- evidence against our substitution, engaged in \S8; 2604.19440 recites as ``local refiner'' & GECCO M7, m5 \\
22 & 1, 7 & AlphaEvolve ``2.635''; FunSearch \emph{Nature} 2023; LMX TELO 2023; AlphaEvolve/ShinkaEvolve unidentified & 2.63586276; \emph{Nature} 625(7995):468--475, 2024; arXiv 2023 / TELO 2024; both systems identified & GECCO M3c, m2, m3 \\
23 & 1, 7 & ThetaEvolve ``in the same band''; HELIX ordering unremarked & ThetaEvolve claims new best-known bounds; HELIX sits below ShinkaEvolve while claiming SOTA & GECCO m10, m11 \\
24 & 7 & ``EvoDiverse (2606.10587)''; 2505.15392 as numeric anchoring & cited by title, method name unverified; 2505.15392 is general anchoring & GECCO m4, m9 \\
25 & 7 & HindsightBench freezes ``under SHA-256''; 2607.07184 ``files OSF preregistrations'' & both unsupported by the sources; restated as frozen preregistrations and registered outcome-blinded predictions & GECCO m7, m8 \\
26 & 7 & ``Mutation Without Variation'': 87\% of chains and 93\% of mutations & nested, not parallel: in 87\% of chains, over 93\% of mutations revisit a prior form & GECCO m1 \\
27 & Abs, 6.1 & ``hundreds of invocations''; corpus arithmetic unreconcilable & 231 invocations, itemized in \S6.1 & R2 \#30; GECCO M11c \\
28 & 3.3, 6 & 18/23 and 35/50 given without stating they are nested subsets & subsets defined in \S3.3 and Table 1; full-ledger 41/57 and 2/57 alongside & stats F13; R2 \#4; GECCO M11b \\
29 & 5 & Sonnet multi-radius ``against a Haiku baseline of 13/35'' & dropped; that baseline reproduces at no denominator & R2 \#23a \\
30 & 5 & ``no Haiku sample did [this] in 101 invocations'' & 155 weak-tier rows; two exceeded the family best, both by $\sim$$10^{-7}$ & stats F17; R2 \#23b \\
31 & 3.1, 9 & dual-tolerance reporting promised, never delivered; ``cryptographic prompt hashes'' & both tolerances in every validity figure; hashes restated as prompt-fragment hashes with coverage gaps itemized above & stats F21; GECCO M12 \\
32 & all & five HTML working comments and a merge-provenance header shipped & removed; the two load-bearing ones ($k = 8$ clipping, $p$-value convention) promoted into \S1.1, Fig 1 and \S6 & stats F22; R2 \#29; GECCO NIT-1--2 \\
33 & 2.2 & item 30's magnitude gloss ``both by $\sim$$10^{-7}$'' & independent re-audit (2026-08-27): the two exceedances are $+3.0\times10^{-7}$ ($N=17$) and $+3.5\times10^{-9}$ ($N=21$); both remain below the $10^{-6}$ bar, count unchanged & fresh-eyes audit \\
\end{longtable}
\endgroup
```
