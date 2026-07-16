"""
Seed script for MedForsa GCC's Order Sets ("مجموعات التحاليل") -- curated
panels of commonly co-ordered tests, built entirely from tests already in
the Lab Info library. No new lab test data is fabricated here; each order
set is simply a named grouping of existing, already-sourced tests.

Run once: python3 seed_order_sets.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ORDER_SETS = [
    {
        "slug": "anemia-workup", "name_en": "Anemia Workup Panel",
        "category": "Hematology",
        "description_en": "Core panel for the initial evaluation of unexplained anemia -- assesses cell counts, iron stores, and the two most common nutritional causes of macrocytic anemia.",
        "tests": ["cbc", "ferritin", "serum-iron", "tibc-transferrin-saturation", "vitamin-b12", "folate", "reticulocyte-count"]
    },
    {
        "slug": "thyroid-function-panel", "name_en": "Thyroid Function Panel",
        "category": "Endocrinology",
        "description_en": "Standard panel for evaluating thyroid function and screening for autoimmune thyroid disease.",
        "tests": ["tsh", "free-t4", "free-t3", "anti-tpo"]
    },
    {
        "slug": "liver-function-panel", "name_en": "Liver Function Panel",
        "category": "Hepatology",
        "description_en": "Core liver enzyme and synthetic function panel used to screen for and characterize liver injury.",
        "tests": ["alt-ast", "alkaline-phosphatase", "ggt", "total-bilirubin", "albumin", "total-protein"]
    },
    {
        "slug": "cardiovascular-risk-panel", "name_en": "Cardiovascular Risk Panel",
        "category": "Cardiology",
        "description_en": "Extended lipid and inflammation panel used to refine cardiovascular risk assessment beyond a standard lipid panel.",
        "tests": ["lipid-panel", "hba1c", "crp", "homocysteine", "lipoprotein-a"]
    },
    {
        "slug": "acute-coronary-syndrome-panel", "name_en": "Acute Coronary Syndrome / Chest Pain Panel",
        "category": "Cardiology",
        "description_en": "Cardiac biomarker panel for the initial evaluation of suspected acute coronary syndrome.",
        "tests": ["troponin", "ck-mb", "myoglobin", "bnp"]
    },
    {
        "slug": "autoimmune-screening-panel", "name_en": "Autoimmune / Connective Tissue Disease Screening Panel",
        "category": "Rheumatology",
        "description_en": "First-line screening panel for suspected autoimmune/connective tissue disease, with reflex-style specific antibody tests included for a complete workup.",
        "tests": ["ana", "ena-panel", "anti-dsdna", "rheumatoid-factor", "anti-ccp", "complement-c3", "complement-c4", "esr", "crp"]
    },
    {
        "slug": "preoperative-coagulation-panel", "name_en": "Pre-Operative / Bleeding Risk Coagulation Panel",
        "category": "Hematology / Coagulation",
        "description_en": "Baseline coagulation screening panel used before surgery or to investigate unexplained bleeding.",
        "tests": ["pt-inr", "aptt", "fibrinogen", "cbc"]
    },
    {
        "slug": "thrombophilia-workup", "name_en": "Thrombophilia Workup Panel",
        "category": "Hematology / Coagulation",
        "description_en": "Panel for investigating a hereditary or acquired clotting tendency after unprovoked or recurrent venous thromboembolism.",
        "tests": ["factor-v-leiden", "prothrombin-g20210a", "protein-c", "protein-s", "antithrombin-iii", "d-dimer"]
    },
    {
        "slug": "sepsis-workup-panel", "name_en": "Sepsis / Severe Infection Workup Panel",
        "category": "Critical Care",
        "description_en": "Core panel for evaluating suspected sepsis or severe systemic infection in the emergency or critical care setting.",
        "tests": ["cbc", "procalcitonin", "lactate", "crp", "blood-culture", "creatinine", "bun"]
    },
    {
        "slug": "female-fertility-hormone-panel", "name_en": "Female Fertility / Reproductive Hormone Panel",
        "category": "Reproductive Endocrinology",
        "description_en": "Core hormone panel for the initial evaluation of female fertility and ovarian reserve.",
        "tests": ["fsh", "lh", "estradiol", "amh", "prolactin", "tsh"]
    },
    {
        "slug": "male-fertility-panel", "name_en": "Male Fertility / Andrology Panel",
        "category": "Andrology",
        "description_en": "Core panel for the initial evaluation of male infertility, combining semen quality assessment with the relevant hormone workup.",
        "tests": ["semen-analysis", "total-testosterone", "free-testosterone", "fsh", "lh", "prolactin"]
    },
    {
        "slug": "bone-mineral-panel", "name_en": "Bone & Mineral Metabolism Panel",
        "category": "Endocrinology",
        "description_en": "Panel for evaluating calcium/bone metabolism disorders, including suspected parathyroid or vitamin D-related disease.",
        "tests": ["calcium", "phosphorus", "magnesium", "pth", "vitamin-d", "albumin", "alkaline-phosphatase"]
    },
    {
        "slug": "prenatal-first-visit-panel", "name_en": "Prenatal (First Antenatal Visit) Panel",
        "category": "Obstetrics",
        "description_en": "Core screening panel typically performed at the first prenatal visit.",
        "tests": ["abo-rh-typing", "antibody-screen", "cbc", "rubella-igg", "hbsag", "hiv-ag-ab-combo", "syphilis-screening", "urinalysis", "toxoplasma-igg-igm"]
    },
    {
        "slug": "pretransfusion-panel", "name_en": "Pretransfusion Compatibility Panel",
        "category": "Blood Bank / Immunohematology",
        "description_en": "Standard pretransfusion 'type and screen' plus crossmatch workflow for safely issuing blood products.",
        "tests": ["abo-rh-typing", "antibody-screen", "crossmatch", "antibody-identification", "dat-coombs"]
    },
    {
        "slug": "diabetes-monitoring-panel", "name_en": "Diabetes Diagnosis & Monitoring Panel",
        "category": "Endocrinology",
        "description_en": "Core panel for diagnosing diabetes and monitoring glycemic control and related risk, including kidney screening.",
        "tests": ["fasting-glucose", "hba1c", "microalbumin", "lipid-panel", "creatinine"]
    }
]

def main():
    conn = sqlite3.connect(DB_PATH)
    existing_slugs = {r[0] for r in conn.execute("SELECT slug FROM lab_tests").fetchall()}
    inserted, skipped = 0, 0
    for s in ORDER_SETS:
        existing = conn.execute("SELECT id FROM order_sets WHERE slug = ?", (s["slug"],)).fetchone()
        if existing:
            print(f"SKIP (already exists): {s['slug']}")
            skipped += 1
            continue
        valid_tests = [t for t in s["tests"] if t in existing_slugs]
        missing = [t for t in s["tests"] if t not in existing_slugs]
        if missing:
            print(f"  NOTE: {s['slug']} references missing test slugs (skipped from set): {missing}")
        conn.execute(
            "INSERT INTO order_sets (slug, name_en, description_en, category, test_slugs_json, is_published) VALUES (?,?,?,?,?,?)",
            (s["slug"], s["name_en"], s["description_en"], s["category"], json.dumps(valid_tests), 1)
        )
        print(f"INSERTED: {s['slug']} ({s['name_en']}) -- {len(valid_tests)} tests")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
