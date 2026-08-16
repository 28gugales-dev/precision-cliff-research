# Wave 7c kernel generator — mechanical substitution from the wave-7b template
# (sec3_artifacts/runners/kaggle_wave7b_phi4_14b.py), same pattern 7b used from
# the 14B fresh runner. Usage:
#   python wave7c_make_runner.py <family> <prereg_sha256>
# Families and their verified GGUF configs live in CONFIGS (see wave7c_prep.md).
# Emits sec3_artifacts/runners/kaggle_wave7c_<family>.py. Generation only —
# nothing here samples.
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "sec3_artifacts/runners/kaggle_wave7b_phi4_14b.py"

CONFIGS = {
    "gemma4_31b": {
        "repo": "mradermacher/gemma-4-31B-it-GGUF",
        "q4": "gemma-4-31B-it.Q4_K_M.gguf",
        "q2": "gemma-4-31B-it.Q2_K.gguf",
        "seeds": [7501, 7502, 7503, 7504, 7505],
        "proposer": "gemma-4-31b",
        "size_note": "31B",
    },
    "nemotron_nano_30b": {
        "repo": "bartowski/nvidia_Nemotron-3-Nano-30B-A3B-GGUF",
        "q4": "nvidia_Nemotron-3-Nano-30B-A3B-Q4_K_M.gguf",
        "q2": "nvidia_Nemotron-3-Nano-30B-A3B-Q2_K.gguf",
        "seeds": [7601, 7602, 7603, 7604, 7605],
        "proposer": "nemotron-3-nano-30b-a3b",
        "size_note": "30B MoE A3B",
    },
    "gpt_oss_20b": {
        "repo": "unsloth/gpt-oss-20b-GGUF",
        "q4": "gpt-oss-20b-Q4_K_M.gguf",
        "q2": "gpt-oss-20b-Q2_K.gguf",
        "seeds": [7701, 7702, 7703, 7704, 7705],
        "proposer": "gpt-oss-20b",
        "size_note": "20B MoE (MXFP4-native parent; community GGUF conversion, disclosed in prereg)",
    },
    "north_mini_code": {
        "repo": "bartowski/North-Mini-Code-1.0-GGUF",
        "q4": "North-Mini-Code-1.0-Q4_K_M.gguf",
        "q2": "North-Mini-Code-1.0-Q2_K.gguf",
        "seeds": [7801, 7802, 7803, 7804, 7805],
        "proposer": "north-mini-code-1.0",
        "size_note": "Cohere North code model",
    },
}


def make(family, prereg_sha):
    cfg = CONFIGS[family]
    src = TEMPLATE.read_text(encoding="utf-8")
    old = "wave7b_phi4_14b"
    new = f"wave7c_{family}"
    subs = [
        # config block
        ('REPO = "bartowski/phi-4-GGUF"', f'REPO = "{cfg["repo"]}"'),
        ('("q4_k_m", "phi-4-Q4_K_M.gguf", 1)', f'("q4_k_m", "{cfg["q4"]}", 1)'),
        ('("q2_k",   "phi-4-Q2_K.gguf",   1)', f'("q2_k",   "{cfg["q2"]}",   1)'),
        ("SEEDS = [7301, 7302, 7303, 7304, 7305]", f"SEEDS = {cfg['seeds']}"),
        (f'RUNNER_VERSION = "{old}_v1"', f'RUNNER_VERSION = "{new}_v1"'),
        # labels and paths (covers WORK/ZIP_BASE/logs/arm/results strings)
        (old, new),
        # proposer label
        ('f"phi-4-14b-{quant}"', f'f"{cfg["proposer"]}-{{quant}}"'),
        # provenance purpose
        ("wave 7b competence-matched family generality: phi4_14b, prereg sha cd043d63ce0cfc0e",
         f"wave 7c screened family generality: {family} ({cfg['size_note']}), prereg sha {prereg_sha[:16]}"),
        # header registration block
        ("wave7b_prereg_families_14b.md, SHA-256\n# cd043d63ce0cfc0eef8ec3bc587b314014451709090d6f95467493731c002cd9",
         f"wave7c_prereg_screened_families.md, SHA-256\n# {prereg_sha}"),
        ("WAVE 7b — FAMILY GENERALITY, COMPETENCE-MATCHED",
         "WAVE 7c — FAMILY GENERALITY, SCREEN-SELECTED"),
    ]
    for a, b in subs:
        if a not in src:
            sys.exit(f"substitution anchor missing: {a[:60]!r}")
        src = src.replace(a, b)
    out = HERE / f"sec3_artifacts/runners/kaggle_wave7c_{family}.py"
    out.write_text(src, encoding="utf-8", newline="\n")
    print(f"wrote {out.name} ({len(src)} bytes)")
    return out


if __name__ == "__main__":
    fam = sys.argv[1]
    sha = sys.argv[2] if len(sys.argv) > 2 else "PLACEHOLDER_PREREG_SHA"
    if fam == "all":
        for f in CONFIGS:
            make(f, sha)
    else:
        make(fam, sha)
