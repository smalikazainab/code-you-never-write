# Project 3 — The Books Don't Match

## Problem
A hand-counted, known-correct total (class farewell party fund) needs to be
reconciled against a messy digital payment record with inconsistent memos
and nicknames. Generic tools can't do this because interpreting ambiguous
entries (who "Ahmed R" or an "unknown transfer" really refers to) depends
on personal knowledge only the collector has.

## AI Tool Used
Claude (Anthropic) — used to write the reconciliation script and identify
a matching bug during verification.

## Data
`books_data.json` — contains:
- The known correct total (PKR 50,000, hand-counted: 10 classmates x PKR 5,000)
- The list of 10 expected members
- Personal interpretation rules (name aliases + a special case for an
  ambiguous small transfer)
- The messy digital payment records exactly as received (nicknames,
  inconsistent formatting)

## Initial Prompt
> "Here is my expected total (hand-counted) and a messy list of digital
> payment records with inconsistent names. Here are my personal rules for
> matching ambiguous names to real people. Write a script that reconciles
> the two, finds the gap, and identifies which people still need to pay or
> are short."

## How the Script Works
- **Name resolution:** messy memos (e.g. "Ahmed R") are mapped to real
  member names using an alias dictionary supplied by the user.
- **Special-case rules:** ambiguous entries (like an unlabeled small
  transfer) are matched against user-defined rules and merged into the
  correct member's total.
- **Per-member reconciliation:** each expected member's total received is
  compared against the amount due, and classified as paid in full, short,
  overpaid, or missing entirely.
- **Gap calculation:** the known correct total is compared against the sum
  of all digital records to compute the overall shortfall.

## Verification (known facts checked against the script's output)

| Check | Known fact | Script output | Match |
|---|---|---|---|
| Digital total received | 45,000 (50,000 − 1 missing member x 5,000) | 45,000 | ✅ |
| Overall gap | 5,000 | 5,000 | ✅ |
| Missing member | Hira Yousaf (deliberately unpaid) | Hira Yousaf | ✅ |
| Sana Iqbal's status | Paid in full (4,500 + 500 remaining transfer) | Paid in full | ✅ |

## What Worked
- Name-alias resolution correctly matched all messy nicknames to real
  members.
- The overall gap calculation (5,000) matched the known fact exactly on
  the first run.

## What Didn't / Challenges
- **A real bug was caught during verification:** the first version of the
  script failed to match the "unknown transfer" special-case rule to Sana
  Iqbal (due to an exact-string-match bug), which incorrectly flagged her
  as underpaid instead of paid in full. The overall total was still
  correct by coincidence, but the per-member breakdown was wrong. This was
  only caught by checking the output against what was already known about
  Sana's payment — a direct example of the assignment's core rule: never
  trust output you cannot check, even when the headline number looks right.
- The fix: matching special-case rules by substring instead of exact
  string equality.

## Final Result
- **Gap identified:** PKR 5,000 unaccounted for.
- **Person to follow up with:** Hira Yousaf — no payment recorded at all.
- All other 9 members confirmed paid in full once the ambiguous transfer
  was correctly attributed.

## Files in This Folder
- `reconcile.py` — the final, corrected reconciliation script
- `books_data.json` — known total, member list, interpretation rules, and
  digital payment records
- `README.md` — this file
