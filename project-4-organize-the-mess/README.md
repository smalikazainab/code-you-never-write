# Project 4 — Organize the Mess (The Files You Forgot)

## Problem
A real, years-accumulated Downloads folder (18,550 files) had grown into
digital clutter — duplicate downloads, forgotten installers, and files
saved in multiple copies. Unlike the other three projects, this one
involves real file operations, where a careless script could delete or
rename the wrong files, so safety discipline was the core requirement.

## AI Tool Used
Claude (Anthropic) — used to write the scanning/reporting scripts and to
redesign the approach twice after real failures (disk space, encoding).

## Data
A real personal Downloads folder on Windows, containing 18,550 files
accumulated over roughly a year (documents, presentations, installers,
videos, images, code, and more).

## Initial Prompt
> "Here is my messy Downloads folder. Write a script that finds duplicate
> files (by content, not just filename), flags very large files (>100MB),
> and groups files by type. Show me a full dry-run plan first — every
> operation you would perform — and don't touch anything until I approve
> it. Never delete or overwrite my original files."

## Safety Steps Followed (per assignment requirement)

1. **Copy first** — the entire Downloads folder was copied to
   `Downloads_COPY` before any script touched it. All operations ran
   against the copy, never the original.
2. **Wrote the brief** — "clean" was defined as: find duplicates (by file
   content hash), flag files over 100MB, and group everything by type
   (Documents, Images, Installers, Code, Videos, etc.).
3. **Demanded a dry run** — `scan_mess.py` only reads and analyzes; it
   never moves, renames, or deletes anything. It writes a full plan to
   `plan.json` listing every proposed operation.
4. **Reviewed the plan** — the plan was inspected before any execution
   step ran.
5. **Approved and executed** — `execute_plan.py` only ran after typing
   "YES" to an explicit confirmation prompt, and results were written to
   new locations, never overwriting originals.
6. **Verified and kept** — the final organized structure and reports were
   spot-checked against the original folder to confirm nothing was lost
   or altered.

## How the Scripts Work
- **`scan_mess.py`**: walks the folder recursively, computes a content
  hash (MD5) for each file to detect true duplicates (not just similar
  names), flags files over 100MB, and assigns each file to a type group.
  Outputs everything to `plan.json` — no files are touched.
- **`execute_plan.py`**: reads the approved plan and copies files into a
  new `Organized/` folder structure (Documents, Images, Installers, etc.).
  Files over 200MB are intentionally **not** copied (to avoid duplicating
  huge installers/videos) — their location is recorded instead in
  `large_files_not_copied.txt`. Duplicate candidates are written to
  `duplicates_report.txt` for manual review rather than being
  auto-deleted.

## What Worked
- Content-hash duplicate detection correctly found genuine duplicates,
  including a video file (`DEMO CLASS.mp4`) saved under three different
  names, totaling roughly 750MB of wasted space.
- The dry-run plan gave a complete, reviewable list before any action.
- Final verification confirmed the original folder was untouched and the
  organized copy was structured correctly.

## What Didn't / Challenges (and how they were fixed)
- **Disk space errors:** the first execution attempt tried to physically
  copy every file — including multi-gigabyte installers and ISOs — which
  ran the disk out of space mid-run. Fixed by skipping the physical copy
  for any file over 200MB and only recording its location instead.
- **Unicode encoding errors:** some filenames contained special/emoji
  characters that Windows' default text encoding (cp1252) couldn't write
  to report files. Fixed by explicitly opening all report files with
  UTF-8 encoding.
- These were genuine bugs caught by actually running the script against
  real data — exactly the kind of verification this assignment is
  designed to teach.

## Final Result
- **18,550 files scanned**
- **9,727 duplicate files found**, representing **~4.3 GB** of wasted
  space
- **40 large files** (>100MB) identified, including several 400MB–1.4GB
  installers
- Files organized into 9 type-based folders (Archives, Audio, Code,
  Documents, Images, Installers, Other, Presentations, Spreadsheets,
  Videos) — as copies, with the original folder completely untouched
- **Action:** review `duplicates_report.txt` to reclaim ~4.3 GB of disk
  space by deleting confirmed duplicates (e.g. redundant copies of
  "DEMO CLASS.mp4")

## Files in This Folder
- `scan_mess.py` — dry-run scanner (read-only, generates `plan.json`)
- `execute_plan.py` — executes the approved plan into an organized copy
- `README.md` — this file

Note: `plan.json` and the generated reports (`duplicates_report.txt`,
`large_files_report.txt`, `large_files_not_copied.txt`) are specific to
the real Downloads folder and were not committed here to avoid exposing
personal file names/paths — sample output is documented above instead.
