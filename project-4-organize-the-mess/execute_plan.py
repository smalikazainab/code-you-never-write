"""
Organize the Mess — Step 2: EXECUTE (only after you approve plan.json)
------------------------------------------------------------------------
Reads plan.json (produced by scan_mess.py) and creates a NEW organized
folder structure by COPYING files into type-based subfolders.

SAFETY GUARANTEES:
  - Original files are never modified, moved, or deleted.
  - Duplicate files are NOT deleted automatically — they are listed in
    duplicates_report.txt for you to review and delete yourself.
  - Only files grouped under "copy_to_group_folder" are copied, into a
    new "Organized" folder next to your source.

Usage:
    python execute_plan.py plan.json
"""

import sys
import os
import json
import shutil


def main(plan_path):
    with open(plan_path, encoding="utf-8") as f:
        plan = json.load(f)

    source = plan["source_folder"]
    organized_root = os.path.join(os.path.dirname(source.rstrip("\\/")), "Organized")

    print(f"Source (untouched): {source}")
    print(f"New organized copy will be created at: {organized_root}")

    confirm = input(
        "\nType YES to proceed with copying files into the organized "
        "folder (originals will NOT be touched): "
    )
    if confirm.strip().upper() != "YES":
        print("Aborted. No files were copied.")
        return

    os.makedirs(organized_root, exist_ok=True)

    copied = 0
    skipped_large = 0
    large_file_locations = []

    for op in plan["proposed_operations"]:
        if op["action"] != "copy_to_group_folder":
            continue
        src = op["file"]
        group = op["destination_group"]

        try:
            size_mb = os.path.getsize(src) / (1024 * 1024)
        except OSError:
            size_mb = 0

        # Don't physically copy very large files (installers, ISOs, videos).
        # They stay where they are; we just record where they'd be grouped.
        if size_mb > 200:
            skipped_large += 1
            large_file_locations.append(f"{src}  ({size_mb:.1f} MB) -> would belong in '{group}'")
            continue

        dest_dir = os.path.join(organized_root, group)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, os.path.basename(src))

        # Avoid overwriting if a same-named file already exists in dest
        base, ext = os.path.splitext(dest_path)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = f"{base}_{counter}{ext}"
            counter += 1

        try:
            shutil.copy2(src, dest_path)
            copied += 1
        except (PermissionError, FileNotFoundError, OSError) as e:
            print(f"  Skipped (error): {src} -> {e}")

    if large_file_locations:
        with open("large_files_not_copied.txt", "w", encoding="utf-8") as f:
            f.write("These files were NOT physically copied (too large — left in original location):\n\n")
            f.write("\n".join(large_file_locations))

    # Write duplicate report (for manual review, nothing auto-deleted)
    dup_ops = [op for op in plan["proposed_operations"] if op["action"] == "flag_duplicate"]
    with open("duplicates_report.txt", "w", encoding="utf-8") as f:
        f.write("Possible duplicate files (NOT deleted — review manually):\n\n")
        for op in dup_ops:
            f.write(f"  {op['file']}  (duplicate of {op['duplicate_of']}, {op['size_mb']} MB)\n")

    large_ops = [op for op in plan["proposed_operations"] if op["action"] == "flag_large_file"]
    with open("large_files_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Large files (>100MB):\n\n")
        for op in large_ops:
            f.write(f"  {op['file']}  ({op['size_mb']} MB)\n")

    print("\n" + "=" * 60)
    print("EXECUTION COMPLETE")
    print("=" * 60)
    print(f"Files copied into organized structure: {copied}")
    print(f"Large files NOT copied (left in place, see large_files_not_copied.txt): {skipped_large}")
    print(f"Duplicate candidates listed in: duplicates_report.txt ({len(dup_ops)} found)")
    print(f"Large files listed in: large_files_report.txt ({len(large_ops)} found)")
    print(f"\nYour original folder was NOT modified: {source}")
    print("=" * 60)


if __name__ == "__main__":
    plan_file = sys.argv[1] if len(sys.argv) > 1 else "plan.json"
    main(plan_file)
