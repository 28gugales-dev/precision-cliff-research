# Build the anonymized supplementary bundle for TMLR/OpenReview upload.
#
# Copies the repro surface (scripts, ledgers, preregistrations, artifacts)
# into supplementary_anonymized/, redacts identity strings in TEXT files,
# rescans to prove zero leaks, and zips. Hash-locked preregistrations are
# redacted like everything else; BUNDLE_README.md discloses that their
# quoted SHA-256 values therefore verify against the PUBLIC Kaggle copies,
# not against the redacted copies shipped here.
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "supplementary_anonymized"
ZIP = ROOT / "supplementary_anonymized.zip"

DIRS = [
    "sec3_artifacts", "wave3_output", "wave4_artifacts", "wave5_output",
    "wave7_output", "wave7b_output", "wave7c_output", "kaggle_redetermin",
    "kaggle_wave3_manifest", "kaggle_wave4_lock", "kaggle_wave5",
    "kaggle_wave8_pilot",
]
TOP_GLOBS = [
    "sec3_*.py", "sec4_independent_rescore.py", "sec6_cv_canary_audit.py",
    "collect_raw.py",
    "echo_screen.py", "wave3_analysis.py", "wave4_analysis.py",
    "wave4_run.py", "wave5_analysis.py", "wave7_analysis.py",
    "wave7b_analysis.py", "wave7c_analysis.py", "wave7c_make_runner.py",
    "wave7c_launch.py", "opus_wave2_score.py",
    # arm surface: every runner, analysis script, prereg, amendment,
    # ledger and frozen report — arm F through arm V and the GM chain.
    "arm_*.py", "arm_*.md", "arm_*.txt", "arm_*.json", "arm_*.jsonl",
    "*prereg*", "*amendment*", "*addendum*",
    "screen_s_doc.md", "screen_s_run.py", "screen_s_raw.jsonl",
    "fig*.py", "fig*.png", "diagnostics_*.py",
    "n_sweep_forecast.py", "rect_forecast.py",
    "opus_wave2_ledger.jsonl",
    "opus_wave2_raw.json", "HOW_TO_RUN.md", "README.md", "requirements.txt",
    "corrections_ledger.md",
    # named in the papers' artifact lists (paper 1 appendix, supplement S6/S9)
    "STATE.md", "ledger_v2_corrections.md", "n_sweep_forecast.json",
    "rect_forecast.json", "p11_mode_baseline.json", "p7_blind_labels.json",
    "p7_faithfulness_rubric.md",
]
# Scripts and outputs the papers cite that live in the paper repository's
# loop/ and evidence/ directories rather than the corpus root. Shipped under
# paper_repo/ so the citations' "loop/ directory" wording resolves.
PAPER_REPO = ROOT.parent / "paper1-accept-loop"
PAPER_REPO_FILES = [
    "loop/arm_f_attempt_control.py", "loop/arm_f_attempt_uncond.py",
    "loop/arm_mu_ceiling.py", "loop/cl_lenient_reparse.py",
    "loop/extend_branch_scope.py", "loop/lp_extend_k89.py",
    "loop/recount_1e9.py", "loop/recount_cl.py",
    "evidence/cl_lenient.json", "evidence/cl_recount.json",
]
TEXT_EXT = {".py", ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml",
            ".sh", ".ipynb", ".cfg", ".toml"}

# Order matters: most specific first.
REDACTIONS = [
    (re.compile(r"[Cc]:[\\/]+Users[\\/]+(soham|\[ANON\])"), "~"),
    (re.compile(r"sohamgugalet"), "ANON-KAGGLE-OWNER"),
    (re.compile(r"Soham Shailesh Gugale"), "[ANONYMIZED AUTHOR]"),
    (re.compile(r"28gugales@gmail\.com"), "[redacted-email]"),
    # GitHub owner handles (28gugales-dev, 28gugales-zamp): whole token, before
    # the name rule below turns them into the reconstructible "28[ANON]s-dev".
    (re.compile(r"28gugales[\w-]*", re.I), "ANON-GITHUB-OWNER"),
    (re.compile(r"Soham|Gugale", re.I), "[ANON]"),
    (re.compile(r"[Cc]:[\\/]Users[\\/]soham"), "~"),
]
LEAK = re.compile(r"soham|gugale|28gugales|28\[ANON\]|github\.com/28|[Cc]:[\\/]+Users[\\/]", re.I)

README = """# Anonymized supplementary bundle

Code, ledgers and preregistrations backing every replayable figure in the
paper (see the claim-evidence map and HOW_TO_RUN.md). Built by
build_anon_bundle.py from the working corpus.

REDACTION DISCLOSURE. Identity strings (author name, e-mail, Kaggle owner
handle, local paths) were replaced throughout: the Kaggle owner handle
appears as ANON-KAGGLE-OWNER. Some preregistration files are hash-locked -
their SHA-256 digests are quoted in the paper and were computed over the
ORIGINAL bytes, so the digests do not verify against the redacted copies in
this bundle. They verify against the public Kaggle datasets named in the
paper (owner handle withheld for review) and will verify against the
de-anonymized artifact released at camera-ready. Nothing else about those
files was changed.

LAYOUT. The corpus root holds every arm's runner, ledger, preregistration,
amendment and frozen report. paper_repo/loop/ and paper_repo/evidence/ hold
the scripts and outputs the papers cite as living in the paper repository
(recount_cl.py, arm_mu_ceiling.py, cl_recount.json and the rest). This
bundle serves both companion submissions; each ships it with its own
supplement PDF and an anonymized copy of the other paper.
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    files = []
    for d in DIRS:
        for p in (ROOT / d).rglob("*"):
            if p.is_file():
                files.append(p)
    for g in TOP_GLOBS:
        files.extend(p for p in ROOT.glob(g) if p.is_file())

    pairs = [(src, src.relative_to(ROOT)) for src in sorted(set(files))]
    for rel in PAPER_REPO_FILES:
        src = PAPER_REPO / rel
        assert src.is_file(), f"paper repo file missing: {src}"
        pairs.append((src, Path("paper_repo") / rel))

    redacted = []
    for src, rel in pairs:
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix.lower() in TEXT_EXT:
            text = src.read_text(encoding="utf-8", errors="replace")
            new = text
            for pat, rep in REDACTIONS:
                new = pat.sub(rep, new)
            if new != text:
                redacted.append(str(rel))
            dst.write_text(new, encoding="utf-8")
        else:
            shutil.copy2(src, dst)

    (OUT / "BUNDLE_README.md").write_text(README, encoding="utf-8")

    leaks = []
    for p in OUT.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT:
            if LEAK.search(p.read_text(encoding="utf-8", errors="replace")):
                leaks.append(str(p.relative_to(OUT)))

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(OUT))

    print(f"bundle files: {sum(1 for p in OUT.rglob('*') if p.is_file())}")
    print(f"redacted files: {len(redacted)}")
    for r in redacted:
        print(f"  {r}")
    print(f"LEAKS AFTER REDACTION: {len(leaks)}")
    for l in leaks:
        print(f"  !! {l}")
    print(f"zip: {ZIP}  ({ZIP.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
