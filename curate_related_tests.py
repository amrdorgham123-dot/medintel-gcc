"""
Curates related_tests_json for MedForsa GCC's Lab Info tests, linking tests that
are clinically related (commonly ordered together or relevant to the same workup),
not just tests that happen to share a database category. Falls back to same-category
suggestions automatically for any test not curated here (see _resolve_related_tests
in app.py).

Run once (safe to re-run -- it overwrites related_tests_json for the slugs listed
below only): python3 curate_related_tests.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

# slug -> list of related slugs (clinically relevant, cross-category where useful)
RELATIONS = {
    "cbc": ["ferritin", "serum-iron", "tibc-transferrin-saturation", "vitamin-b12", "folate", "reticulocyte-count", "g6pd"],
    "fasting-glucose": ["hba1c", "lipid-panel", "creatinine"],
    "hba1c": ["fasting-glucose", "lipid-panel", "creatinine"],
    "lipid-panel": ["hba1c", "fasting-glucose", "homocysteine", "lipoprotein-a", "crp", "alt-ast"],
    "creatinine": ["bun", "sodium", "potassium", "uric-acid"],
    "bun": ["creatinine", "sodium", "potassium", "albumin"],
    "sodium": ["potassium", "chloride", "bicarbonate-co2", "creatinine", "bun"],
    "potassium": ["sodium", "chloride", "bicarbonate-co2", "creatinine"],
    "chloride": ["sodium", "potassium", "bicarbonate-co2"],
    "bicarbonate-co2": ["sodium", "potassium", "chloride"],
    "calcium": ["phosphorus", "magnesium", "albumin", "pth", "vitamin-d"],
    "magnesium": ["calcium", "phosphorus", "potassium"],
    "phosphorus": ["calcium", "magnesium", "pth", "vitamin-d"],
    "alt-ast": ["alkaline-phosphatase", "ggt", "total-bilirubin", "albumin", "total-protein", "pt-inr"],
    "alkaline-phosphatase": ["ggt", "alt-ast", "total-bilirubin", "calcium", "phosphorus"],
    "ggt": ["alkaline-phosphatase", "alt-ast", "total-bilirubin"],
    "total-bilirubin": ["alt-ast", "alkaline-phosphatase", "ggt", "cbc"],
    "albumin": ["total-protein", "alt-ast"],
    "total-protein": ["albumin", "alt-ast"],
    "uric-acid": ["creatinine", "bun", "lipid-panel"],
    "ferritin": ["serum-iron", "tibc-transferrin-saturation", "cbc", "vitamin-b12", "folate", "crp"],
    "serum-iron": ["ferritin", "tibc-transferrin-saturation", "cbc"],
    "tibc-transferrin-saturation": ["ferritin", "serum-iron", "cbc"],
    "vitamin-d": ["calcium", "phosphorus", "pth", "tsh"],
    "vitamin-b12": ["folate", "cbc", "reticulocyte-count", "homocysteine"],
    "folate": ["vitamin-b12", "cbc", "reticulocyte-count"],
    "tsh": ["free-t4", "free-t3", "vitamin-d", "prolactin"],
    "free-t4": ["tsh", "free-t3"],
    "free-t3": ["tsh", "free-t4"],
    "pth": ["calcium", "phosphorus", "vitamin-d"],
    "cortisol": ["tsh", "prolactin"],
    "crp": ["esr", "cbc", "lipid-panel", "ferritin"],
    "esr": ["crp", "cbc", "rheumatoid-factor", "anti-ccp"],
    "rheumatoid-factor": ["anti-ccp", "esr", "crp", "ana"],
    "anti-ccp": ["rheumatoid-factor", "esr", "crp"],
    "ana": ["anti-dsdna", "complement-c3", "complement-c4", "rheumatoid-factor"],
    "anti-dsdna": ["ana", "complement-c3", "complement-c4"],
    "complement-c3": ["complement-c4", "ana", "anti-dsdna"],
    "complement-c4": ["complement-c3", "ana", "anti-dsdna"],
    "anca": ["creatinine", "urinalysis"],
    "pt-inr": ["aptt", "fibrinogen", "d-dimer", "alt-ast"],
    "aptt": ["pt-inr", "fibrinogen", "d-dimer"],
    "fibrinogen": ["pt-inr", "aptt", "d-dimer"],
    "d-dimer": ["pt-inr", "aptt", "fibrinogen"],
    "antithrombin-iii": ["protein-c", "protein-s", "pt-inr", "aptt"],
    "protein-c": ["protein-s", "antithrombin-iii", "pt-inr"],
    "protein-s": ["protein-c", "antithrombin-iii", "pt-inr"],
    "homocysteine": ["vitamin-b12", "folate", "lipid-panel", "lipoprotein-a"],
    "lipoprotein-a": ["lipid-panel", "homocysteine", "crp"],
    "troponin": ["ck-mb", "bnp"],
    "ck-mb": ["troponin", "bnp"],
    "bnp": ["troponin", "ck-mb", "creatinine"],
    "psa": ["psa", "urinalysis"],
    "afp": ["beta-hcg", "ca-125"],
    "beta-hcg": ["afp", "urinalysis"],
    "ca-125": ["afp", "cea"],
    "ca19-9": ["cea", "afp"],
    "cea": ["ca19-9", "ca-125", "afp"],
    "ca15-3": ["cea"],
    "total-testosterone": ["free-testosterone", "prolactin", "tsh"],
    "free-testosterone": ["total-testosterone", "prolactin"],
    "prolactin": ["tsh", "total-testosterone", "free-testosterone"],
    "semen-analysis": ["total-testosterone", "free-testosterone", "prolactin"],
    "hbsag": ["hbsab", "alt-ast", "total-bilirubin"],
    "hbsab": ["hbsag", "alt-ast"],
    "hiv-ag-ab-combo": ["cbc", "hbsag"],
    "abo-rh-typing": ["antibody-screen", "crossmatch", "dat-coombs"],
    "antibody-screen": ["abo-rh-typing", "crossmatch", "antibody-identification"],
    "dat-coombs": ["abo-rh-typing", "cbc", "total-bilirubin"],
    "crossmatch": ["abo-rh-typing", "antibody-screen"],
    "antibody-identification": ["antibody-screen", "crossmatch"],
    "kleihauer-betke": ["abo-rh-typing", "antibody-screen"],
    "blood-culture": ["crp", "cbc", "esr"],
    "urine-culture": ["urinalysis", "creatinine"],
    "h-pylori-testing": ["alt-ast"],
    "urinalysis": ["creatinine", "urine-culture"],
    "g6pd": ["cbc", "reticulocyte-count", "total-bilirubin"],
    "reticulocyte-count": ["cbc", "ferritin", "vitamin-b12", "folate"],
}

def main():
    conn = sqlite3.connect(DB_PATH)
    existing_slugs = {r[0] for r in conn.execute("SELECT slug FROM lab_tests").fetchall()}
    updated, skipped_missing_self, skipped_no_valid_targets = 0, 0, 0
    for slug, related in RELATIONS.items():
        if slug not in existing_slugs:
            skipped_missing_self += 1
            continue
        valid_related = [r for r in related if r in existing_slugs]
        if not valid_related:
            skipped_no_valid_targets += 1
            continue
        conn.execute(
            "UPDATE lab_tests SET related_tests_json = ? WHERE slug = ?",
            (json.dumps(valid_related), slug)
        )
        updated += 1
    conn.commit()
    conn.close()
    print(f"Updated: {updated}")
    print(f"Skipped (test itself not in DB yet): {skipped_missing_self}")
    print(f"Skipped (no valid related targets in DB yet): {skipped_no_valid_targets}")

if __name__ == "__main__":
    main()
