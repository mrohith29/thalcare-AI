import random
import pandas as pd

INPUT = r"e:\non github files\Techolution Interview\synthetic_blood_banks_1100.csv"
OUTPUT = r"e:\non github files\Techolution Interview\synthetic_blood_banks_1100_augmented.csv"

random.seed(42)

blood_types = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]

df = pd.read_csv(INPUT, dtype=str)

# Ensure column exists
if "Blood_Group" not in df.columns:
    raise SystemExit("Blood_Group column not found")

all_prob = 0.06   # ~6% of rows will get ALL types
min_types = 2     # ensure multiple types per bank

new_groups = []
for _ in range(len(df)):
    if random.random() < all_prob:
        types = blood_types[:]  # all types
    else:
        k = random.randint(min_types, len(blood_types))
        types = random.sample(blood_types, k)
    new_groups.append("|".join(sorted(types)))  # sorted for consistency

df["Blood_Group"] = new_groups

# Guarantee that every blood type appears at least once in dataset
present = set()
for cell in df["Blood_Group"]:
    present.update(cell.split("|"))
missing = [t for t in blood_types if t not in present]
if missing:
    # add missing types to random rows (append if not already present)
    rows = list(df.index)
    random.shuffle(rows)
    i = 0
    for m in missing:
        while i < len(rows):
            idx = rows[i]
            current = set(df.at[idx, "Blood_Group"].split("|"))
            if m not in current:
                current.add(m)
                df.at[idx, "Blood_Group"] = "|".join(sorted(current))
                i += 1
                break
            i += 1

df.to_csv(OUTPUT, index=False)
print(f"Written augmented CSV to: {OUTPUT}")