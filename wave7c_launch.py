# Wave 7c launch orchestration. Run AFTER the prereg is locked (tally inserted,
# committed). Steps per invocation:
#   python wave7c_launch.py dataset          -> push prereg as public Kaggle dataset
#   python wave7c_launch.py kernel <family>  -> generate runner w/ real SHA, push public kernel
#   python wave7c_launch.py status           -> list kernel statuses
#   python wave7c_launch.py fetch <family>   -> download kernel output into wave7c_output/
# Requires kaggle CLI authenticated (verified this session).
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREREG = HERE / "wave7c_prereg_screened_families.md"
STAGE = HERE / "_wave7c_stage"
OWNER = "sohamgugalet"
DS_SLUG = "wave7c-prereg-screened-families"

FAMILY_TITLES = {
    "gemma4_31b": "precision-sweep-gemma4-31b-wave7c",
    "nemotron_nano_30b": "precision-sweep-nemotron-nano30b-wave7c",
    "gpt_oss_20b": "precision-sweep-gptoss-20b-wave7c",
    "north_mini_code": "precision-sweep-northmini-wave7c",
}


def sha():
    return hashlib.sha256(PREREG.read_bytes()).hexdigest()


def run(cmd, **kw):
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode != 0:
        sys.exit(f"command failed rc={r.returncode}")
    return r.stdout


def push_dataset():
    if "PLACEHOLDER" in PREREG.read_text(encoding="utf-8"):
        sys.exit("prereg still has placeholders; refusing to push")
    d = STAGE / "dataset"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(PREREG, d / PREREG.name)
    (d / "dataset-metadata.json").write_text(json.dumps({
        "title": "wave7c-prereg-screened-families",
        "id": f"{OWNER}/{DS_SLUG}",
        "licenses": [{"name": "CC0-1.0"}],
    }, indent=1))
    run(["kaggle", "datasets", "create", "-p", str(d), "--public"])
    print("prereg sha256:", sha())


def push_kernel(family):
    if "PLACEHOLDER" in PREREG.read_text(encoding="utf-8"):
        sys.exit("prereg still has placeholders; refusing to push")
    run([sys.executable, str(HERE / "wave7c_make_runner.py"), family, sha()])
    src = HERE / f"sec3_artifacts/runners/kaggle_wave7c_{family}.py"
    k = STAGE / f"kernel_{family}"
    k.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, k / src.name)
    slug = FAMILY_TITLES[family]
    (k / "kernel-metadata.json").write_text(json.dumps({
        "id": f"{OWNER}/{slug}",
        "title": slug,
        "code_file": src.name,
        "language": "python",
        "kernel_type": "script",
        "is_private": "false",
        "enable_gpu": "true",
        "enable_tpu": "false",
        "enable_internet": "true",
        "machine_shape": "NvidiaTeslaT4",
        "dataset_sources": [], "competition_sources": [],
        "kernel_sources": [], "model_sources": [],
    }, indent=1))
    run(["kaggle", "kernels", "push", "-p", str(k)])


def status():
    for fam, slug in FAMILY_TITLES.items():
        r = subprocess.run(["kaggle", "kernels", "status", f"{OWNER}/{slug}"],
                           capture_output=True, text=True)
        print(f"{fam:20s} {(r.stdout or r.stderr).strip()}")


def fetch(family):
    slug = FAMILY_TITLES[family]
    out = HERE / "wave7c_output" / f"wave7c_{family}_kernel_output"
    out.mkdir(parents=True, exist_ok=True)
    run(["kaggle", "kernels", "output", f"{OWNER}/{slug}", "-p", str(out)])
    # unpack the runner's partial zip into the analysis layout if present
    for z in out.glob("*.zip"):
        tgt = HERE / "wave7c_output" / f"wave7c_{family}"
        shutil.unpack_archive(str(z), str(tgt))
        print(f"unpacked {z.name} -> {tgt}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dataset":
        push_dataset()
    elif cmd == "kernel":
        push_kernel(sys.argv[2])
    elif cmd == "status":
        status()
    elif cmd == "fetch":
        fetch(sys.argv[2])
    else:
        sys.exit("usage: dataset | kernel <family> | status | fetch <family>")
