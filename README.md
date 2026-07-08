# Code You Never Write — Real-World AI Coding Projects

**Name:** Syeda Malika Zainab Kazmi

## Summary

This repository contains four real-world projects completed for the
"Code You Never Write" assignment (Panaversity Agent Factory — Lecture 7).
In each project, I acted as the client rather than the programmer:
describing a real personal problem to an AI tool, having it write the
code, and verifying every result against facts I already knew to be true
before trusting it.

## AI Tools Used

Claude (Anthropic) — used across all four projects to write scripts,
explain their logic in plain English, and help debug real issues that
came up when running the code against real data.

## Projects

| # | Project | Problem Solved |
|---|---|---|
| 1 | [Money Detective](project-1-money-detective/) | Found a duplicate charge and mapped recurring subscriptions in personal transaction history |
| 2 | [What's My Grade, Really](project-2-whats-my-grade/) | Calculated true current grade using the teacher's actual weighted grading policy, and the score needed on the Final to hit target grades |
| 3 | [The Books Don't Match](project-3-books-dont-match/) | Reconciled a hand-counted fund total against messy digital payment records, finding a PKR 5,000 gap and the exact person to follow up with |
| 4 | [Organize the Mess](project-4-organize-the-mess/) | Scanned a real 18,550-file Downloads folder, found 9,727 duplicate files (~4.3 GB wasted), and safely organized it without touching any original files |

Each project folder contains the final script(s), the data used, the
prompts given to the AI, and a README explaining the problem, the AI tool
used, and how the result was verified.

## Core Principle Followed

Per the assignment's rule — **never trust output you cannot check** —
every project's result was verified against a fact already known before
being trusted:
- Project 1: monthly totals matched known baselines exactly
- Project 2: one category average was recalculated by hand and matched
- Project 3: the overall gap matched the known missing amount exactly,
  and a real matching bug was caught and fixed during verification
- Project 4: the dry-run plan was reviewed before any file operation ran,
  and the original folder was confirmed untouched afterward
