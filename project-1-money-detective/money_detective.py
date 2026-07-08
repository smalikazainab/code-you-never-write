"""
Money Detective
----------------
Analyzes a personal transaction history (CSV: Date, Description, Amount)
to find:
  1. Recurring charges (subscriptions/regular bills)
  2. Duplicate payments (same description + same amount + same date)
  3. Possible forgotten subscriptions (appeared only once, never repeated)

Usage:
    python money_detective.py sample_transactions.csv
"""

import sys
import pandas as pd


def load_data(path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    amount_col = [c for c in df.columns if "Amount" in c][0]
    df = df.rename(columns={amount_col: "Amount"})
    return df


def find_duplicates(df):
    """Same description + same amount + same date = likely duplicate charge."""
    dup_mask = df.duplicated(subset=["Date", "Description", "Amount"], keep=False)
    return df[dup_mask].sort_values(["Date", "Description"])


def find_recurring(df, min_occurrences=2):
    """Descriptions that appear 2+ times with the same amount = recurring."""
    grouped = df.groupby(["Description", "Amount"]).size().reset_index(name="Occurrences")
    recurring = grouped[grouped["Occurrences"] >= min_occurrences]
    return recurring.sort_values("Occurrences", ascending=False)


def find_forgotten_subscriptions(df, recurring_df):
    """
    Charges that appear only ONCE but have subscription-like keywords
    (Subscription, Premium, Membership, Prime, Plan) are flagged as
    possible forgotten subscriptions worth double-checking.
    """
    keywords = ["subscription", "premium", "membership", "prime", "plan"]
    counts = df.groupby("Description").size()
    single_occurrence = counts[counts == 1].index

    flagged = df[
        df["Description"].isin(single_occurrence)
        & df["Description"].str.lower().str.contains("|".join(keywords))
    ]
    return flagged


def main(path):
    df = load_data(path)

    print("=" * 60)
    print("MONEY DETECTIVE REPORT")
    print("=" * 60)

    total = df["Amount"].sum()
    print(f"\nTotal transactions: {len(df)}")
    print(f"Total spend: {total:,.0f}")

    # Monthly breakdown (for verification against known baseline)
    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Amount"].sum()
    print("\n--- Monthly Totals (verify these against your own records) ---")
    for month, amt in monthly.items():
        print(f"  {month}: {amt:,.0f}")

    # Duplicates
    dups = find_duplicates(df)
    print(f"\n--- Possible Duplicate Charges ({len(dups)} rows) ---")
    if dups.empty:
        print("  None found.")
    else:
        print(dups[["Date", "Description", "Amount"]].to_string(index=False))
        dup_cost = dups["Amount"].sum() / 2  # each duplicate pair counted twice
        print(f"  Estimated wasted amount from duplicates: {dup_cost:,.0f}")

    # Recurring charges
    recurring = find_recurring(df)
    print(f"\n--- Recurring Charges / Subscriptions ({len(recurring)} found) ---")
    print(recurring.to_string(index=False))

    # Forgotten subscriptions
    forgotten = find_forgotten_subscriptions(df, recurring)
    print(f"\n--- Possible Forgotten Subscriptions ({len(forgotten)} found) ---")
    if forgotten.empty:
        print("  None found.")
    else:
        print(forgotten[["Date", "Description", "Amount"]].to_string(index=False))

    print("\n" + "=" * 60)
    print("End of report.")
    print("=" * 60)


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "sample_transactions.csv"
    main(file_path)
