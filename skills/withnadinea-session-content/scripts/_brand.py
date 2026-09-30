"""Find the withnadinea-brand skill's render.py wherever the skills are installed."""
import os, glob, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent


def find_render():
    env = os.environ.get("WITHNADINEA_BRAND")
    cands = []
    if env:
        cands.append(pathlib.Path(env) / "scripts" / "render.py")
    for base in [HERE.parent.parent, pathlib.Path("/mnt/skills/user"), pathlib.Path("/mnt/skills"),
                 pathlib.Path.home() / ".claude" / "skills", pathlib.Path("/home/claude")]:
        cands.append(base / "withnadinea-brand" / "scripts" / "render.py")
    for c in cands:
        if c.exists():
            return c
    for pat in ["/mnt/**/withnadinea-brand/scripts/render.py", "/home/**/withnadinea-brand/scripts/render.py",
                "/tmp/**/withnadinea-brand/scripts/render.py"]:
        hits = glob.glob(pat, recursive=True)
        if hits:
            return pathlib.Path(hits[0])
    sys.exit("ERROR: the withnadinea-brand skill was not found. Install it (withnadinea-brand.skill) "
             "or set WITHNADINEA_BRAND=/path/to/withnadinea-brand")


def render(spec_path, out_dir):
    r = subprocess.run([sys.executable, str(find_render()), str(spec_path), str(out_dir)],
                       capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        sys.exit(f"render failed for {spec_path}:\n{out}")
    return out
