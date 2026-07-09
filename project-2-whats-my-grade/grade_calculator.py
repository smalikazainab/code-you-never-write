"""
What's My Grade, Really
------------------------
Calculates a student's true current grade using their teacher's actual
grading policy (category weights + dropped lowest scores), and works out
the score needed on a remaining category (e.g. the Final) to hit a target
overall grade.

Usage:
    python grade_calculator.py grade_data.json
"""

import sys
import json


def category_average(entries, drop_lowest=0):
    """Returns the average percentage for a category, after dropping the
    lowest N scores (converted to percentages first, since max can differ
    per assignment/quiz)."""
    if not entries:
        return None, []

    percentages = [(e["score"] / e["max"]) * 100 for e in entries]
    sorted_pairs = sorted(zip(percentages, entries), key=lambda x: x[0])

    dropped = sorted_pairs[:drop_lowest]
    kept = sorted_pairs[drop_lowest:]

    if not kept:
        return None, dropped

    avg = sum(p for p, _ in kept) / len(kept)
    return avg, dropped


def main(path):
    with open(path) as f:
        data = json.load(f)

    policy = data["grading_policy"]["categories"]
    scores = data["scores"]
    target = data.get("target_grade_percent")

    print("=" * 60)
    print("GRADE REPORT")
    print("=" * 60)

    category_averages = {}
    weighted_total = 0.0
    weight_accounted = 0.0
    missing_category = None

    for cat, rules in policy.items():
        entries = scores.get(cat, [])
        avg, dropped = category_average(entries, rules.get("drop_lowest", 0))

        print(f"\n--- {cat} (weight {rules['weight']*100:.0f}%) ---")
        if not entries:
            print("  No scores yet (not completed).")
            missing_category = cat
            continue

        for e in entries:
            pct = (e["score"] / e["max"]) * 100
            tag = " (dropped)" if any(e is d for _, d in dropped) else ""
            print(f"  {e['name']}: {e['score']}/{e['max']} = {pct:.1f}%{tag}")

        print(f"  Category average (after drops): {avg:.2f}%")
        category_averages[cat] = avg
        weighted_total += avg * rules["weight"]
        weight_accounted += rules["weight"]

    print("\n" + "-" * 60)
    if missing_category is None:
        print(f"CURRENT OVERALL GRADE: {weighted_total:.2f}%")
    else:
        current_partial = weighted_total
        print(f"Grade so far (excluding '{missing_category}'): "
              f"{current_partial:.2f}% out of {weight_accounted*100:.0f}% "
              f"of total weight completed")

        if target is not None:
            missing_weight = policy[missing_category]["weight"]
            needed = (target - current_partial) / missing_weight
            print(f"\nTo reach a target overall grade of {target}%, "
                  f"you need to score:")
            print(f"  >>> {needed:.2f}% on {missing_category} <<<")
            if needed > 100:
                print("  (Note: this is above 100% — target may not be "
                      "reachable with remaining work.)")
            elif needed < 0:
                print("  (Note: target is already secured regardless of "
                      f"{missing_category} score.)")

    print("=" * 60)


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "grade_data.json"
    main(file_path)
