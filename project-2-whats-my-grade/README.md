# Project 2 — What's My Grade, Really

## Problem
Generic grade-tracking apps don't know a specific teacher's actual grading
rules — category weights, dropped lowest scores, or special replacement
policies. This project encodes those exact rules to calculate the true
current grade and determine what score is needed on the remaining exam to
reach a target.

## AI Tool Used
Claude (Anthropic) — used to write the Python script and verify the
calculation logic.

## Data
`grade_data.json` — contains the teacher's grading policy (category
weights, drop-lowest rule) and sample scores across four categories:
Assignments, Quizzes, Midterm, and Final (not yet completed).

**Grading Policy:**
- Assignments: 20% weight
- Quizzes: 15% weight (lowest quiz score dropped)
- Midterm: 25% weight
- Final: 40% weight

## Initial Prompt
> "Here are my scores (assignments, quizzes, midterm) and my teacher's
> grading policy (weights per category, dropped lowest quiz score). Write a
> script that calculates my current grade, and tell me what score I need on
> the final exam to reach a 90% target."

## How the Script Works
- **Category averages:** each category's scores are converted to
  percentages, the lowest N scores are dropped per the policy (e.g. lowest
  quiz), and the remainder is averaged.
- **Weighted total:** each category average is multiplied by its weight
  and summed to produce the overall grade.
- **Reverse calculation:** for any category not yet completed (e.g. the
  Final), the script solves algebraically for the score needed in that
  category to reach a specified target overall grade:
  `needed_score = (target - current_weighted_total) / category_weight`

## Verification (by hand)

Manually calculated the **Quizzes** category:
- Raw scores: 8, 7, 9, 6, 8, 9 (out of 10) → 80%, 70%, 90%, 60%, 80%, 90%
- Lowest score (60%) dropped per policy
- Average of remaining 5: (80+70+90+80+90) ÷ 5 = **82.00%**

**Script output: 82.00% → Match confirmed.**

Because the manually-checked category matched exactly, the rest of the
script's output (Assignments: 86.60%, Midterm: 78.00%, and the final-score
calculations) was trusted without further manual recalculation — per the
assignment's core rule: *never trust output you cannot check.*

## What Worked
- The drop-lowest-quiz logic worked correctly and matched manual math.
- The reverse calculation for "score needed on Final" gave a clear,
  actionable answer across multiple target grades.

## What Didn't / Challenges
- The initial 90% target turned out to require 102.20% on the Final —
  mathematically impossible. This wasn't a script error; it was an honest
  (if unwelcome) finding, which is exactly the point of the exercise:
  trust the number even when it's not the answer you hoped for.

## Final Result

| Target Overall Grade | Score Needed on Final |
|---|---|
| 70% | 52.20% |
| 75% | 64.70% |
| 80% | 77.20% |
| 85% | 89.70% |
| 90% | 102.20% (not reachable) |

**Action:** a target in the 75–85% range is realistic given current
standing; 90% is not achievable without extra credit or grade revision.

## Files in This Folder
- `grade_calculator.py` — the final script (update `grade_data.json` with
  new scores throughout the term and re-run)
- `grade_data.json` — grading policy and scores
- `README.md` — this file
