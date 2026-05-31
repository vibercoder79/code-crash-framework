#!/usr/bin/env python3
# dpo/scripts/dpo-audit.py — deterministischer Kontrollkatalog-Audit (BOO-87)
#
# Arbeitet die YAML-Kataloge unter dpo/controls/ (Framework) + .claude/dpo/controls/
# (Projekt-Overlay) ab und erzeugt ein reproduzierbares Report-Paar:
#   <projekt>/dpo/reports/<date>_audit.md   (menschenlesbar)
#   <projekt>/dpo/reports/<date>_audit.json (maschinenlesbar)
#
# Ehrlicher Determinismus: mechanische Checks -> PASS/GAP (reproduzierbar),
# Urteils-Checks -> REVIEW-NEEDED (Mensch bestaetigt). KEINE Rechtsberatung.
# Dependency-frei (python3-Stdlib, flacher YAML-Mini-Parser — kein PyYAML).
# KEINE Datenbank: Determinismus + Versionierung kommen aus den Git-YAML-Katalogen.
#
# Env:
#   DPO_PROJECT_ROOT  Projekt-Wurzel (Default: cwd)
#   DPO_AUDIT_DATE    Report-Datum (Default: heute) — fuer reproduzierbare Tests
import sys, os, re, json, glob, datetime

SOURCE_EXT = (".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".py", ".java",
              ".c", ".cc", ".cpp", ".h", ".hpp", ".go", ".rb", ".php")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "coverage", "__pycache__"}


def parse_catalog(path):
    """Flacher YAML-Subset: Liste von Mappings (- name: ... key: value)."""
    out, cur = [], None
    if not os.path.isfile(path):
        return out
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        if s.lstrip().startswith("- "):
            if cur:
                out.append(cur)
            cur, s = {}, s.lstrip()[2:]
        if ":" in s and cur is not None:
            k, v = s.split(":", 1)
            cur[k.strip()] = v.strip().strip("'\"")
    if cur:
        out.append(cur)
    return out


def _iter_source_files(root):
    for dp, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.endswith(SOURCE_EXT):
                yield os.path.join(dp, fn)


def _check_file_exists(arg, root):
    return ("PASS", "Datei vorhanden") if os.path.isfile(os.path.join(root, arg)) \
        else ("GAP", "Datei fehlt: " + arg)


def _check_file_contains(arg, root):
    f, _, needle = arg.partition("::")
    if not os.path.isfile(os.path.join(root, f)):
        return "GAP", "Datei fehlt: " + f
    txt = open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
    found = bool(needle) and needle.lower() in txt.lower()  # case-insensitiv, robuster
    return ("PASS", "'%s' gefunden" % needle) if found \
        else ("GAP", "'%s' fehlt in %s" % (needle, f))


def _check_grep_absent(arg, root):
    try:
        rx = re.compile(arg)
    except re.error:
        return "REVIEW-NEEDED", "ungueltiges Muster: " + arg
    hits = []
    for fp in _iter_source_files(root):
        try:
            if rx.search(open(fp, encoding="utf-8", errors="ignore").read()):
                hits.append(os.path.relpath(fp, root))
        except Exception:
            pass
    return ("GAP", "Treffer: " + ", ".join(sorted(hits)[:5])) if hits \
        else ("PASS", "kein Treffer")


_CHECKS = {
    "file-exists": _check_file_exists,
    "file-contains": _check_file_contains,
    "grep-absent": _check_grep_absent,
}


def run_check(ctrl, root):
    typ = (ctrl.get("check_typ") or "review").lower()
    if typ == "review":
        return "REVIEW-NEEDED", "Urteils-Check — Operator bestaetigt"
    fn = _CHECKS.get(typ)
    if not fn:
        return "REVIEW-NEEDED", "unbekannter check_typ: " + typ
    return fn(ctrl.get("check_arg") or "", root)


def load_controls(script_dir, root):
    cat_files = sorted(glob.glob(os.path.join(script_dir, "..", "controls", "*.yml")))
    overlay = os.path.join(root, ".claude", "dpo", "controls")
    cat_files += sorted(glob.glob(os.path.join(overlay, "**", "*.yml"), recursive=True))
    json_overlay = sorted(glob.glob(os.path.join(overlay, "**", "*.json"), recursive=True))
    controls = []
    for cf in cat_files:
        for c in parse_catalog(cf):
            c["_katalog"] = os.path.basename(cf)
            controls.append(c)
    for cf in json_overlay:
        try:
            data = json.load(open(cf, encoding="utf-8"))
        except Exception:
            continue
        items = data if isinstance(data, list) else data.get("controls", [])
        for c in items:
            c["_katalog"] = os.path.basename(cf)
            controls.append(c)
    return controls


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.environ.get("DPO_PROJECT_ROOT") or os.getcwd()
    date = os.environ.get("DPO_AUDIT_DATE") or datetime.date.today().isoformat()

    controls = load_controls(script_dir, root)
    results = []
    for c in controls:
        status, detail = run_check(c, root)
        results.append({
            "id": c.get("id", "?"), "titel": c.get("titel", ""),
            "katalog": c.get("_katalog", ""), "quelle": c.get("quelle", ""),
            "status": status, "detail": detail,
            "evidenz": c.get("evidenz", ""), "mapsTo": c.get("mapsTo", ""),
        })
    results.sort(key=lambda r: (r["katalog"], r["id"]))  # deterministische Reihenfolge
    summary = {s: sum(1 for r in results if r["status"] == s)
               for s in ("PASS", "GAP", "REVIEW-NEEDED")}

    reports = os.path.join(root, "dpo", "reports")
    os.makedirs(reports, exist_ok=True)
    kataloge = ", ".join(sorted({r["katalog"] for r in results})) or "(keine)"

    md = ["# DPO Compliance-Audit — " + date, "",
          "**Kataloge:** " + kataloge,
          "**Ergebnis:** %d PASS · %d GAP · %d REVIEW-NEEDED"
          % (summary["PASS"], summary["GAP"], summary["REVIEW-NEEDED"]),
          "", "| Control | Titel | Quelle | Status | Detail |",
          "|---|---|---|---|---|"]
    for r in results:
        md.append("| %s | %s | %s | %s | %s |"
                  % (r["id"], r["titel"], r["quelle"], r["status"], r["detail"]))
    gaps = [r for r in results if r["status"] == "GAP"]
    if gaps:
        md += ["", "## Offene GAPs — was zu tun ist", ""]
        for r in gaps:
            md.append("- **%s** (%s): %s → siehe %s"
                      % (r["id"], r["quelle"], r["evidenz"], r["mapsTo"]))
    reviews = [r for r in results if r["status"] == "REVIEW-NEEDED"]
    if reviews:
        md += ["", "## REVIEW-NEEDED — Mensch bestaetigt (kein Auto-Urteil)", ""]
        for r in reviews:
            md.append("- **%s** (%s): %s → %s"
                      % (r["id"], r["quelle"], r["titel"], r["mapsTo"]))
    md += ["", "_Deterministisch erzeugt: gleicher Projektstand = gleiches Ergebnis. "
           "OSCAL-Export ist eine spaetere Ausbaustufe._", ""]

    open(os.path.join(reports, date + "_audit.md"), "w", encoding="utf-8").write("\n".join(md))
    json.dump({"date": date, "summary": summary, "controls": results},
              open(os.path.join(reports, date + "_audit.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    print("[DPO-AUDIT] %d PASS / %d GAP / %d REVIEW-NEEDED"
          % (summary["PASS"], summary["GAP"], summary["REVIEW-NEEDED"]))
    print("[DPO-AUDIT] Report: dpo/reports/%s_audit.md (+ .json)" % date)
    # Exit-Code: 0 (Audit ist Bericht, kein Gate). GAP/REVIEW stehen im Report.
    return 0


if __name__ == "__main__":
    sys.exit(main())
