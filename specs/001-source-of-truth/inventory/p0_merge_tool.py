#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0 merge-safety tool (Source of Truth, Feature 001).

Modes (run from repo root):
  analyze : inventory/state.json + overlap-analysis.md + overlap-hashes.csv
  stage   : COPY->VERIFY->REMOVE every overlapping untracked file to
            C:/Users/co0ob/Projects/p0_merge_stage/<localhash8>/<relpath>
            + inventory/stage-receipt.md
  audit   : inventory/survival-audit.md + survival-summary.json

Discipline: NEVER git clean; nothing is removed without a verified copy + receipt.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))  # inventory -> feature -> feature(+1): root
INV = os.path.join(HERE)
STAGE_ROOT = r"C:\Users\co0ob\Projects\p0_merge_stage"

def git(args, check=False):
    p = subprocess.run(["git"] + args, cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        sys.exit("FATAL git rc=%d stderr=%s" % (p.returncode,
                 p.stderr[:300].decode("utf-8", "replace")))
    return p.returncode, p.stdout

def git_text(args):
    rc, out = git(args)
    return rc, out.decode("utf-8", "replace")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def win_long(path):
    p = os.path.abspath(path)
    return ("\\\\?\\" + p) if len(p) > 240 and not p.startswith("\\\\?\\") else p

def status_entries():
    rc, out = git(["-c", "core.quotepath=false", "status", "--porcelain=v1",
                   "--untracked-files=all", "-z"])
    entries = [e.decode("utf-8", "replace") for e in out.split(b"\0") if e]
    branch, untracked, modified = "", [], []
    for e in entries:
        if e.startswith("## "):
            branch = e[3:].strip()
            continue
        st, path = e[:2], e[3:].lstrip()
        if st == "??":
            untracked.append(path)
        elif st in (" M", "M "):
            modified.append(path)
    return branch, untracked, modified

def origin_tracked(head):
    rc, out = git_text(["-c", "core.quotepath=false", "ls-tree", "-r",
                        "--name-only", head])
    if rc != 0:
        sys.exit("FATAL ls-tree rc=%d stderr=%s" % (rc, out[:200]))
    return set(x for x in out.splitlines() if x)

def origin_blob(head, path):
    try:
        rc, out = git(["cat-file", "blob", "%s:%s" % (head, path)])
        return rc, out
    except Exception:
        return 1, b""

def load_state():
    p = os.path.join(INV, "state.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def save_state(s):
    p = os.path.join(INV, "state.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)

def analyze():
    head = git_text(["rev-parse", "origin/master"])[1].strip()
    branch, untracked, modified = status_entries()
    tracked = origin_tracked(head)
    overlap = sorted(p for p in untracked if p in tracked)
    # Windows case-folding collisions: same on-disk path with different letter case
    fold = {t.lower(): t for t in tracked}
    case_overlap = sorted(p for p in untracked
                          if p not in tracked and p.lower() in fold)
    non_overlap = sorted(p for p in untracked
                         if p not in tracked and p.lower() not in fold)
    rows = []
    for path in overlap + case_overlap:
        local = os.path.join(REPO, path.replace("/", os.sep))
        if not os.path.isfile(win_long(local)):
            rows.append(dict(path=path, local_sha256=None, remote_sha256=None,
                             equal=None, bytes_local=None, bytes_remote=None,
                             error="local file missing"))
            continue
        local_abs = win_long(local)
        lh = sha256_file(local_abs)
        rc, blob = origin_blob(head, path)
        if rc != 0 and path.lower() in fold:
            rc, blob = origin_blob(head, fold[path.lower()])
            path_cmp = fold[path.lower()]
        else:
            path_cmp = path
        if rc != 0:
            rows.append(dict(path=path, local_sha256=lh, remote_sha256=None,
                             equal=None,
                             bytes_local=os.path.getsize(local_abs),
                             bytes_remote=None,
                             error="cat-file rc=%d" % rc))
            continue
        rh = hashlib.sha256(blob).hexdigest()
        rows.append(dict(path=path, local_sha256=lh, remote_sha256=rh,
                         equal=(lh == rh),
                         bytes_local=os.path.getsize(local_abs),
                         bytes_remote=len(blob), error=None))
    state = {
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "head": head,
        "branch_line": branch,
        "untracked": untracked,
        "modified": modified,
        "origin_tracked_count": len(tracked),
        "premerge_origin_tracked": sorted(tracked),
        "overlap": overlap,
        "non_overlap_untracked": non_overlap,
        "hash_rows": rows,
        "staged": [],
        "wip_commit": None,
    }
    save_state(state)
    with open(os.path.join(INV, "overlap-analysis.md"), "w", encoding="utf-8") as f:
        f.write("# Overlap Analysis (T004)\n\n")
        f.write("- head: `%s` @ %s\n" % (head, state["captured_at"]))
        f.write("- branch line: `%s`\n" % branch)
        f.write("- untracked files: **%d** | modified tracked: **%d** | "
                "origin tracked: **%d**\n" % (len(untracked), len(modified), len(tracked)))
        f.write("- OVERLAP (untracked AND tracked@origin): **%d** files\n\n" % len(overlap))
        for r in rows:
            eq = "IDENTICAL" if r["equal"] else ("DIFFERENT" if r["equal"] is False else "ERROR")
            f.write("- %s -> %s\n" % (r["path"], eq))
    with open(os.path.join(INV, "overlap-hashes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "local_sha256", "remote_sha256", "equal",
                    "bytes_local", "bytes_remote", "error"])
        for r in rows:
            w.writerow([r["path"], r["local_sha256"], r["remote_sha256"],
                        r["equal"], r["bytes_local"], r["bytes_remote"], r["error"]])
    n_eq = sum(1 for r in rows if r["equal"])
    n_diff = sum(1 for r in rows if r["equal"] is False)
    n_err = sum(1 for r in rows if r["equal"] is None)
    print("ANALYZE OK head=%s overlap=%d identical=%d different=%d errors=%d non_overlap=%d"
          % (head[:7], len(overlap), n_eq, n_diff, n_err, len(non_overlap)))

def stage():
    s = load_state()
    staged = []
    for r in s["hash_rows"]:
        if r["equal"] is None:
            print("SKIP-ERROR %s (%s)" % (r["path"], r.get("error")))
            continue
        path = r["path"]
        local = os.path.join(REPO, path.replace("/", os.sep))
        if not os.path.isfile(win_long(local)):
            print("SKIP-MISSING %s" % path)
            continue
        dest = win_long(os.path.join(STAGE_ROOT, r["local_sha256"][:8],
                                     path.replace("/", os.sep)))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(win_long(local), dest)
        if sha256_file(dest) != r["local_sha256"]:
            sys.exit("ABORT copy-verify mismatch %s" % path)
        os.remove(win_long(local))
        staged.append(dict(path=path, staged_as=dest, sha256=r["local_sha256"],
                           equal_at_capture=r["equal"], removed_local=True,
                           when=time.strftime("%Y-%m-%dT%H:%M:%S")))
    s["staged"] = staged
    save_state(s)
    with open(os.path.join(INV, "stage-receipt.md"), "w", encoding="utf-8") as f:
        f.write("# Move-Aside Receipt (T006)\n\n")
        f.write("Stage root: `%s` | staged %d files\n\n" % (STAGE_ROOT, len(staged)))
        for e in staged:
            f.write("- `%s` -> `%s` sha256=%s... identical-at-capture=%s "
                    "(local copy removed AFTER verified twin)\n"
                    % (e["path"], e["staged_as"], e["sha256"][:12],
                       e["equal_at_capture"]))
    print("STAGE OK files=%d" % len(staged))

def audit():
    s = load_state()
    head_now = git_text(["rev-parse", "HEAD"])[1].strip()
    head_tracked = origin_tracked(head_now)
    branch, untracked_now, modified_now = status_entries()
    staged_by_path = {e["path"]: e for e in s.get("staged", [])}
    classes = {}
    vanished = []
    for p in s["untracked"]:
        if p in untracked_now:
            c = "kept-untracked"
        elif p in head_tracked:
            e = staged_by_path.get(p)
            if e and e["equal_at_capture"]:
                c = "replaced-by-tracked-identical"
            elif e:
                c = "variant-preserved-aside"
            else:
                c = "now-tracked(see-log)"
        elif p in staged_by_path:
            c = "moved-aside(staged)"
        else:
            c = "VANISHED"
            vanished.append(p)
        classes[c] = classes.get(c, 0) + 1
    lost_tracked = [p for p in s.get("premerge_origin_tracked", [])
                    if p not in head_tracked]
    order = ["replaced-by-tracked-identical", "variant-preserved-aside",
             "moved-aside(staged)", "kept-untracked", "now-tracked(see-log)"]
    lines = ["# Survival Audit (T011)", "",
             "- audit at: `%s`" % time.strftime("%Y-%m-%dT%H:%M:%S"),
             "- HEAD: `%s`" % head_now, "",
             "## Untracked-material outcomes", ""]
    for k in order:
        if classes.get(k):
            lines.append("- **%s**: %d" % (k, classes[k]))
    lines.append("- **VANISHED**: %d (MUST be 0)" % len(vanished))
    lines.append("")
    if vanished:
        lines.append("### VANISHED (phase fails!)")
        lines.extend("- %s" % p for p in vanished)
        lines.append("")
    lines.append("## Tracked-set integrity (vs pre-merge origin tree)")
    lines.append("")
    lines.append("- pre-merge origin-tracked: %d" % len(s.get("premerge_origin_tracked", [])))
    lines.append("- lost-tracked paths: %d (must be 0 unless documented)" % len(lost_tracked))
    if lost_tracked:
        lines.extend("- %s" % p for p in lost_tracked[:50])
    lines.append("")
    lines.append("- current untracked: %d" % len(untracked_now))
    lines.append("- current modified tracked: %d" % len(modified_now))
    with open(os.path.join(INV, "survival-audit.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(INV, "survival-summary.json"), "w", encoding="utf-8") as f:
        json.dump(dict(classes=classes, vanished=vanished,
                       lost_tracked=lost_tracked,
                       untracked_now=len(untracked_now),
                       modified_now=modified_now, head=head_now),
                  f, ensure_ascii=False, indent=1)
    print("AUDIT OK vanished=%d lost_tracked=%d untracked_now=%d modified_now=%d"
          % (len(vanished), len(lost_tracked), len(untracked_now), len(modified_now)))

def relink():
    """Rebuild state['staged'] from STAGE_ROOT + current head blob hashes (TRUTH rebuild)."""
    s = load_state()
    head = git_text(["rev-parse", "origin/master"])[1].strip()
    head_tracked = origin_tracked(head)
    head_fold = {t.lower(): t for t in head_tracked}
    staged = []
    for root, dirs, files in os.walk(STAGE_ROOT):
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, STAGE_ROOT)
            parts = rel.split(os.sep)
            if len(parts) < 2:
                continue  # skip stray top-level helpers
            path = "/".join(parts[1:])
            h = sha256_file(win_long(full))
            res = path if path in head_tracked else head_fold.get(path.lower())
            if res is not None:
                rc, blob = origin_blob(head, res)
                eq = (rc == 0 and hashlib.sha256(blob).hexdigest() == h)
            else:
                eq = False
            staged.append(dict(path=path, staged_as=full, sha256=h,
                               equal_at_capture=eq, removed_local=True,
                               head=head, when=s.get("captured_at", "")))
    s["staged"] = staged
    s["wip_commit"] = s.get("wip_commit") or "4b6a2c8"
    s["relink_head"] = head
    save_state(s)
    n_eq = sum(1 for e in staged if e["equal_at_capture"])
    print("RELINK OK staged=%d identical-vs-head=%s variants=%d" % (len(staged), n_eq, len(staged) - n_eq))

if __name__ == "__main__":
    import csv
    mode = sys.argv[1] if len(sys.argv) > 1 else "analyze"
    print("TOOL paths repo=%s" % REPO)
    if mode == "analyze":
        analyze()
    elif mode == "stage":
        stage()
    elif mode == "relink":
        relink()
    elif mode == "audit":
        audit()
    else:
        sys.exit("usage: analyze|stage|audit")
