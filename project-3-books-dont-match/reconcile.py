"""
The Books Don't Match
-----------------------
Reconciles a known, hand-counted total against a messy digital payment
record with inconsistent memos, using the user's own rules for
interpreting ambiguous entries.

Usage:
    python reconcile.py books_data.json
"""

import sys
import json


def resolve_name(memo, aliases):
    """Return the real member name for a messy memo, using alias rules."""
    return aliases.get(memo, memo)


def main(path):
    with open(path) as f:
        data = json.load(f)

    known_total = data["known_correct_total"]
    due_per_member = data["amount_due_per_member"]
    expected_members = data["expected_members"]
    aliases = data["interpretation_rules"]["name_aliases"]
    special_cases = data["interpretation_rules"]["special_cases"]
    records = data["digital_payment_records"]

    print("=" * 60)
    print("BOOKS RECONCILIATION REPORT")
    print("=" * 60)
    print(f"\nExpected total (hand-counted): PKR {known_total:,}")
    print(f"Expected members: {len(expected_members)} x PKR {due_per_member:,} each")

    # Step 1: apply special-case rules (e.g. the "unknown transfer")
    # by merging them into the matching member's total.
    resolved_payments = {}  # member -> total received
    unresolved = []

    for r in records:
        memo, amount = r["memo"], r["amount"]

        # Special-case rule matching: memo text may not exactly match the
        # rule's key, so match on the core phrase instead of full equality.
        matched_special = None
        for rule_key in special_cases:
            if memo.strip().lower() in rule_key.lower():
                matched_special = rule_key
                break

        if matched_special:
            resolved_payments["Sana Iqbal"] = resolved_payments.get("Sana Iqbal", 0) + amount
            continue

        real_name = resolve_name(memo, aliases)
        if real_name in expected_members:
            resolved_payments[real_name] = resolved_payments.get(real_name, 0) + amount
        else:
            unresolved.append(r)

    # Step 2: totals
    digital_total = sum(resolved_payments.values()) + sum(r["amount"] for r in unresolved)
    gap = known_total - digital_total

    print(f"\nDigital records total (after applying rules): PKR {digital_total:,}")
    print(f"GAP (expected - received): PKR {gap:,}")

    # Step 3: per-member breakdown
    print("\n--- Per-Member Status ---")
    missing_members = []
    short_members = []
    for member in expected_members:
        received = resolved_payments.get(member, 0)
        if received == 0:
            print(f"  {member}: PKR 0  -> MISSING, needs follow-up")
            missing_members.append(member)
        elif received < due_per_member:
            print(f"  {member}: PKR {received:,} -> SHORT by PKR {due_per_member - received:,}")
            short_members.append(member)
        elif received > due_per_member:
            print(f"  {member}: PKR {received:,} -> OVERPAID by PKR {received - due_per_member:,}")
        else:
            print(f"  {member}: PKR {received:,} -> paid in full")

    if unresolved:
        print("\n--- Unresolved / Unmatched Entries (need manual review) ---")
        for r in unresolved:
            print(f"  memo='{r['memo']}', amount=PKR {r['amount']:,}")

    print("\n" + "-" * 60)
    print("SUMMARY")
    print("-" * 60)
    if missing_members:
        print(f"Members with no payment recorded: {', '.join(missing_members)}")
    if short_members:
        print(f"Members who paid short: {', '.join(short_members)}")
    if not missing_members and not short_members:
        print("All members accounted for in full.")

    print(f"\nTotal gap to follow up on: PKR {gap:,}")
    print("=" * 60)


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "books_data.json"
    main(file_path)
