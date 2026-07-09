# Project 1 — Money Detective

## Problem
Instead of tracking spending going forward, this project hunts for money leaks
hidden in past transaction history — recurring charges, duplicate payments,
and subscriptions that may have been forgotten. These are personal patterns
that no generic budgeting app can detect, because the rules for what counts
as a "leak" depend on the individual's own spending habits.

## AI Tool Used
Claude (Anthropic) — used to write the Python script, explain its logic, and
help verify the results.

## Data
`sample_transactions.csv` — two months (May–June 2026) of transaction data
containing Date, Description, and Amount (PKR). Real bank details were not
used; this is representative sample data with realistic categories
(groceries, rides, subscriptions, bills, food delivery, doctor visits).

## Initial Prompt
> "Here is my transaction history (date, description, amount). Write a
> Python script that finds: (1) recurring/subscription charges, (2)
> duplicate or repeated payments on the same day, (3) possible forgotten
> subscriptions (charged once, never seen again). Output a clear summary
> report."

## How the Script Works
- **Duplicate detection:** flags transactions with the same description,
  amount, and date appearing more than once — the signature of an
  accidental double-charge.
- **Recurring charges:** groups transactions by description + amount and
  counts occurrences; anything appearing 2+ times is treated as a
  subscription or regular bill.
- **Forgotten subscriptions:** flags charges that occurred only once but
  contain subscription-like keywords (Subscription, Premium, Membership,
  Prime, Plan) — a possible sign of a subscription started and forgotten.

## Verification (known facts checked against the script's output)

| Check | Known baseline | Script output | Match |
|---|---|---|---|
| May total spend | 32,850 | 32,850 | ✅ |
| June total spend | 39,740 | 39,740 | ✅ |
| Duplicate charge | Netflix charged twice on 21 May | Netflix, 21 May, 2× 1500 | ✅ |

Because both monthly totals matched exactly and the known duplicate was
correctly caught, the rest of the script's output (recurring charges list)
was trusted without further manual checking — per the assignment rule:
*never trust output you cannot check.*

## What Worked
- The script correctly identified all 5 recurring charges (Netflix, Mobile
  Balance, Doctor Appointment, Electricity Bill, Spotify).
- It correctly caught the one planted duplicate charge (Netflix, 21 May).
- Monthly totals matched known figures exactly.

## What Didn't / Challenges
- Setting up Python on Windows required installing Python from
  python.org (not the Microsoft Store alias) and separately installing
  the `pandas` library with `pip install pandas`.
- No forgotten subscriptions were found in this dataset — a legitimate
  result, not a script failure.

## Final Result
- **Found:** one duplicate charge (Netflix, PKR 1,500 wasted) and a clear
  list of 5 recurring monthly charges totaling PKR 13,150/month.
- **Action:** review the Netflix duplicate with the payment provider, and
  keep an eye on the "Doctor Appointment" recurring cost.

## Files in This Folder
- `money_detective.py` — the final script (re-runnable monthly on fresh data)
- `sample_transactions.csv` — the transaction data used
- `README.md` — this file
