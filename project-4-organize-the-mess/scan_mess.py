"""
Organize the Mess — Step 1: SCAN (dry run only)
--------------------------------------------------
This script ONLY reads and analyzes your folder. It does not move, rename,
or delete anything. It produces a plan (plan.json) listing every proposed
operation. You must review that plan before anything is executed.

SAFETY: Point this at a COPY of your folder, never the original.

Usage:
    python scan_mess.py "C:\\Users\\H P\\Downloads_COPY"
"""

import sys
import os
import hashlib
import json
from collections import defaultdict

LARGE_FILE_THRESHOLD_MB = 100

TYPE_GROUPS = {
    "Documents": [".docx", ".doc", ".pdf", ".txt", ".md"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
    "Presentations": [".pptx", ".ppt"],
    "Images": [".png", ".jpg", ".jpeg", ".jfif", ".gif", ".webp"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
    "Installers": [".exe", ".msi", ".msix", ".apk"],
    "Code": [".py", ".js", ".html", ".css", ".php", ".ipynb", ".sql"],
}


def get_type_group(ext):
    ext = ext.lower()
    for group, extensions in TYPE_GROUPS.items():
        if ext in extensions:
            return group
    return "Other"


def file_hash(path, block_size=65536):
    """Compute a content hash so we can detect true duplicates
    (not just similar names)."""
    hasher = hashlib.md5()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(block_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def scan_folder(root):
    files_info = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                continue
            ext = os.path.splitext(name)[1]
            files_info.append({
                "path": full_path,
                "name": name,
                "ext": ext,
                "size_mb": round(size / (1024 * 1024), 2),
                "group": get_type_group(ext),
            })
    return files_info


def find_duplicates_by_content(files_info):
    """Group files by content hash to find true duplicates
    (only hash files under 200MB to keep this fast)."""
    hash_map = defaultdict(list)
    for f in files_info:
        if f["size_mb"] > 200:
            continue  # skip hashing huge installers, too slow
        h = file_hash(f["path"])
        if h:
            hash_map[h].append(f["path"])

    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}


def build_plan(root, files_info):
    plan = {
        "source_folder": root,
        "total_files_scanned": len(files_info),
        "proposed_operations": [],
    }

    # 1. Duplicate detection (by content)
    dup_groups = find_duplicates_by_content(files_info)
    dup_wasted_mb = 0
    for h, paths in dup_groups.items():
        # keep the first (oldest-looking) file, propose removing the rest
        keep = paths[0]
        for extra in paths[1:]:
            size = next(f["size_mb"] for f in files_info if f["path"] == extra)
            dup_wasted_mb += size
            plan["proposed_operations"].append({
                "action": "flag_duplicate",
                "file": extra,
                "duplicate_of": keep,
                "size_mb": size,
            })

    # 2. Large file flags
    for f in files_info:
        if f["size_mb"] > LARGE_FILE_THRESHOLD_MB:
            plan["proposed_operations"].append({
                "action": "flag_large_file",
                "file": f["path"],
                "size_mb": f["size_mb"],
            })

    # 3. Group-by-type proposal (copy destination, never move original)
    for f in files_info:
        plan["proposed_operations"].append({
            "action": "copy_to_group_folder",
            "file": f["path"],
            "destination_group": f["group"],
        })

    plan["summary"] = {
        "duplicate_files_found": sum(len(p) - 1 for p in dup_groups.values()),
        "estimated_space_wasted_mb": round(dup_wasted_mb, 2),
        "large_files_found": sum(
            1 for op in plan["proposed_operations"]
            if op["action"] == "flag_large_file"
        ),
    }
    return plan


def main(root):
    print(f"Scanning: {root}")
    files_info = scan_folder(root)
    plan = build_plan(root, files_info)

    with open("plan.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    print("\n" + "=" * 60)
    print("DRY RUN COMPLETE — NO FILES WERE CHANGED")
    print("=" * 60)
    print(f"Total files scanned: {plan['total_files_scanned']}")
    print(f"Duplicate files found: {plan['summary']['duplicate_files_found']}")
    print(f"Space wasted on duplicates: {plan['summary']['estimated_space_wasted_mb']} MB")
    print(f"Large files (>{LARGE_FILE_THRESHOLD_MB}MB) found: {plan['summary']['large_files_found']}")
    print("\nFull plan saved to plan.json — REVIEW IT before running execute_plan.py")
    print("=" * 60)


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    main(folder)
