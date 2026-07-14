"""
Seed script (batch 9) for MedForsa GCC's Lab Info reference library.
Adds Arterial Blood Gas, Ammonia, Lactate, and Urine Microalbumin/Creatinine Ratio.
English-only content per platform policy.

Run once: python3 seed_lab_tests_batch9.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "abg", "name_en": "Arterial Blood Gas (ABG)",
        "aliases": "ABG, Blood Gas Analysis",
        "category": "Clinical Chemistry / Point of Care",
        "purpose_en": "Assesses acid-base status, oxygenation, and ventilation; essential in respiratory failure, critical illness, and metabolic derangements (e.g., DKA, sepsis) where rapid bedside results guide immediate management.",
        "specimen_type": "Arterial whole blood (heparinized syringe), typically from the radial, brachial, or femoral artery",
        "collection_notes_en": "Sample must be free of air bubbles and analyzed promptly (or kept on ice if delayed) since gas exchange with air or ongoing cellular metabolism in the syringe can alter pH, pCO2, and pO2 results within minutes.",
        "methodology_en": "Ion-selective electrodes measure pH and pCO2 directly; pO2 is measured by an amperometric (Clark-type) electrode; bicarbonate (HCO3) and base excess are calculated from the measured pH and pCO2 using the Henderson-Hasselbalch equation, not measured directly.",
        "reference_ranges": [
            {"parameter": "pH", "population": "Adult, arterial", "range": "7.35-7.45"},
            {"parameter": "pCO2 (PaCO2)", "population": "Adult, arterial", "range": "35-45 mmHg"},
            {"parameter": "HCO3 (bicarbonate, calculated)", "population": "Adult, arterial", "range": "22-26 mEq/L"},
            {"parameter": "pO2 (PaO2)", "population": "Adult, arterial, room air", "range": "80-100 mmHg"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Interpretation follows a stepwise approach: (1) check pH to determine acidemia (<7.35) or alkalemia (>7.45); (2) check pCO2 -- a change in the same direction as the pH abnormality (e.g., low pH with high pCO2) indicates a respiratory cause, while a change in the opposite direction suggests metabolic compensation; (3) check HCO3 similarly for a primary metabolic process versus renal compensation. A normal pH with abnormal pCO2 and HCO3 suggests a fully compensated disorder or a mixed disorder, and should be interpreted alongside the clinical picture. pO2 assesses oxygenation but is not used to classify the acid-base disorder itself.",
        "critical_values_en": "There is no single universal ABG panic-value list, but markedly abnormal values (e.g., pH <7.20 or >7.60, pCO2 >70 mmHg, pO2 <40 mmHg) generally represent a medical emergency requiring immediate intervention. Always follow the reporting lab/point-of-care device's own critical-value policy.",
        "interfering_factors_en": "Air bubbles in the syringe cause the sample to equilibrate toward room air, falsely raising pO2 and lowering pCO2. Delayed analysis allows continued cellular metabolism (glycolysis, oxygen consumption) in the sample, falsely lowering pH and pO2 and raising pCO2 -- icing the sample slows this if analysis will be delayed. Venous contamination of an arterial sample falsely lowers pO2 and raises pCO2.",
        "associated_conditions": [
            {"condition": "Respiratory acidosis (e.g., COPD exacerbation, respiratory depression)", "direction": "low pH, high pCO2"},
            {"condition": "Respiratory alkalosis (e.g., hyperventilation, anxiety, PE)", "direction": "high pH, low pCO2"},
            {"condition": "Metabolic acidosis (e.g., DKA, lactic acidosis, renal failure)", "direction": "low pH, low HCO3"},
            {"condition": "Metabolic alkalosis (e.g., prolonged vomiting, diuretic use)", "direction": "high pH, high HCO3"},
            {"condition": "Hypoxemic respiratory failure", "direction": "low pO2"}
        ],
        "sources": [
            {"name": "Nurse.org - Arterial Blood Gas (ABG) Analysis: Values & Interpretation", "url": "https://nurse.org/articles/arterial-blood-gas-test/", "accessed": "2026-07-14"},
            {"name": "Respiratory Therapy Zone - ABG Interpretation Made Easy", "url": "https://www.respiratorytherapyzone.com/abg-interpretation/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "ammonia", "name_en": "Ammonia, Blood",
        "aliases": "NH3, Serum Ammonia",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected hepatic encephalopathy in patients with liver disease and altered mental status, and investigates suspected inherited urea cycle disorders, particularly in neonates/children with unexplained encephalopathy.",
        "specimen_type": "Venous whole blood, EDTA (lavender top) or heparin (green top) tube, drawn without a tourniquet if possible",
        "collection_notes_en": "Critical preanalytical requirements: draw without prolonged tourniquet time or fist clenching, transport on ice, and have the lab analyze it within about 15-20 minutes (or centrifuge and freeze the plasma promptly if immediate analysis isn't possible) -- delayed or improper handling is the most common cause of a falsely elevated result.",
        "methodology_en": "Enzymatic (glutamate dehydrogenase-based) assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Ammonia", "population": "Adult", "range": "\u226435 \u00b5mol/L (\u226460 \u00b5g/dL)", "notes": "Neonatal and pediatric reference ranges are substantially different and higher"}],
        "reference_ranges_verified": True,
        "critical_values_en": "Levels >200 \u00b5mol/L are associated with poor neurological outcomes; severe hyperammonemia (>400 \u00b5mol/L) may require urgent dialysis/kidney replacement therapy, particularly in neonates with suspected urea cycle disorders. Rapidly rising or markedly elevated ammonia warrants urgent clinical correlation and consideration of emergency treatment.",
        "interfering_factors_en": "Hemolysis releases ammonia from red blood cells and is a major cause of falsely elevated results. Prolonged tourniquet application, fist clenching during the draw, and delayed sample processing/transport all falsely raise results -- an unexpectedly high ammonia in a clinically well-appearing patient should prompt review of collection technique before acting on the result.",
        "associated_conditions": [
            {"condition": "Hepatic encephalopathy (cirrhosis, acute liver failure)", "direction": "high"},
            {"condition": "Inherited urea cycle disorders (neonates/children)", "direction": "high"},
            {"condition": "Reye syndrome", "direction": "high"}
        ],
        "sources": [{"name": "droracle.ai - What is the normal serum ammonia concentration in adults? (clinical reference synthesis)", "url": "https://www.droracle.ai/articles/853651/what-is-the-normal-serum-ammonia-concentration-in-adults", "accessed": "2026-07-14"}]
    },
    {
        "slug": "lactate", "name_en": "Lactate, Blood",
        "aliases": "Lactic Acid, Serum Lactate",
        "category": "Clinical Chemistry / Point of Care",
        "purpose_en": "Marker of tissue hypoperfusion and anaerobic metabolism; used to identify and risk-stratify sepsis/septic shock, assess the severity of shock states generally, and guide resuscitation (serial lactate clearance).",
        "specimen_type": "Arterial or venous whole blood (point-of-care) or plasma (central lab); often measured on the same sample as an ABG",
        "collection_notes_en": "Avoid prolonged tourniquet use and fist clenching, which can falsely raise results through local muscle anaerobic metabolism; process promptly, as ongoing glycolysis in an unprocessed sample raises lactate over time (a fluoride-oxalate tube or rapid processing minimizes this).",
        "methodology_en": "Enzymatic (lactate oxidase or lactate dehydrogenase-based) assay on point-of-care blood gas analyzers or central laboratory chemistry analyzers.",
        "reference_ranges": [{"parameter": "Lactate", "population": "Normal, unstressed adult", "range": "~0.5-1.5 mmol/L", "notes": "Critically ill patients are generally considered to have a 'normal' lactate below 2 mmol/L; even lactate levels within the traditional reference range have been associated with increased mortality risk in critically ill populations in some studies"}],
        "reference_ranges_verified": True,
        "critical_values_en": "Lactate \u22654 mmol/L is a key criterion supporting a diagnosis of septic shock (per Sepsis-3 criteria, alongside vasopressor requirement) and is generally treated as a value requiring urgent clinical attention and aggressive resuscitation.",
        "interfering_factors_en": "Tourniquet use and muscle activity (fist clenching, struggling) during the draw cause local anaerobic metabolism that falsely raises the result. Delayed processing of the sample allows continued glycolysis by blood cells, also falsely raising the result -- use of a lactate-stabilizing (fluoride) tube or prompt analysis minimizes this artifact.",
        "associated_conditions": [
            {"condition": "Septic shock / severe sepsis", "direction": "high, \u22654 mmol/L"},
            {"condition": "Any shock state (cardiogenic, hypovolemic, obstructive)", "direction": "high"},
            {"condition": "Tissue hypoxia / severe exertion / seizure", "direction": "high, transiently"}
        ],
        "sources": [
            {"name": "PMC - Even Mild Hyperlactatemia Is Associated with Increased Mortality in Critically Ill Patients", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4056896/", "accessed": "2026-07-14"},
            {"name": "PMC - Relative hyperlactatemia and hospital mortality in critically ill patients", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2875540/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "microalbumin", "name_en": "Urine Albumin-to-Creatinine Ratio (ACR / Microalbumin)",
        "aliases": "ACR, Microalbumin, uACR, Urine Microalbumin/Creatinine Ratio",
        "category": "Clinical Chemistry / Urinalysis",
        "purpose_en": "Early screening test for diabetic and hypertensive kidney disease -- detects small amounts of albumin in urine below the detection threshold of a standard urine dipstick, before overt proteinuria or a drop in eGFR develops.",
        "specimen_type": "Spot (random) urine sample, ideally first-morning; 24-hour urine collection is the historical gold standard but a spot ACR is now considered sufficient for screening and monitoring",
        "collection_notes_en": "Avoid testing during a urinary tract infection, after heavy exercise, or during acute illness/fever, as these can all cause a transient false elevation; a positive result should be confirmed with a repeat test, ideally first-morning, before diagnosing microalbuminuria.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay for urine albumin, paired with a urine creatinine measurement (Jaffe or enzymatic method) to calculate the ratio, which corrects for variation in urine concentration.",
        "reference_ranges": [
            {"parameter": "Albumin-to-creatinine ratio", "population": "Normal", "range": "<30 mg/g creatinine"},
            {"parameter": "Albumin-to-creatinine ratio", "population": "Microalbuminuria (moderately increased albuminuria)", "range": "30-299 mg/g creatinine"},
            {"parameter": "Albumin-to-creatinine ratio", "population": "Macroalbuminuria (severely increased albuminuria)", "range": "\u2265300 mg/g creatinine"}
        ],
        "reference_ranges_verified": True,
        "interfering_factors_en": "Urinary tract infection, fever/acute illness, heavy exercise before collection, marked hyperglycemia, and menstrual blood contamination can all cause a transient false elevation -- clinically significant microalbuminuria should be confirmed on a repeat sample under standard conditions (2 of 3 samples over 3-6 months per ADA guidance) before being treated as a persistent finding.",
        "clinical_significance_en": "Microalbuminuria is an early, reversible marker of diabetic nephropathy and is also an independent marker of generalized cardiovascular risk, associated with increased risk of stroke and heart disease even outside of diabetes. The American Diabetes Association recommends annual screening in type 1 diabetics with disease duration >5 years and in all type 2 diabetics from diagnosis. Detecting microalbuminuria prompts intensified blood pressure control (typically with an ACE inhibitor or ARB) and glycemic control, which can slow or reverse progression to macroalbuminuria and kidney failure.",
        "associated_conditions": [
            {"condition": "Diabetic nephropathy (early stage)", "direction": "high (30-299 mg/g)"},
            {"condition": "Hypertensive nephrosclerosis", "direction": "high"},
            {"condition": "Generalized cardiovascular risk marker", "direction": "high, even at levels below the microalbuminuria threshold in some studies"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Microalbumin: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2088184-overview", "accessed": "2026-07-14"},
            {"name": "MLabs (University of Michigan) - Urine Albumin Creatinine Ratio (ACR), citing ADA interpretation guidelines", "url": "https://mlabs.umich.edu/tests/microalbumin-urine", "accessed": "2026-07-14"}
        ]
    }
]

def main():
    conn = sqlite3.connect(DB_PATH)
    inserted, skipped = 0, 0
    for t in TESTS:
        existing = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (t["slug"],)).fetchone()
        if existing:
            print(f"SKIP (already exists): {t['slug']}")
            skipped += 1
            continue
        conn.execute(
            """INSERT INTO lab_tests
            (slug, name_en, name_ar, aliases, category, purpose_en, purpose_ar, specimen_type,
             collection_notes_en, collection_notes_ar, methodology_en, methodology_ar,
             reference_ranges_json, reference_ranges_verified, clinical_significance_en, clinical_significance_ar,
             critical_values_en, interfering_factors_en,
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("critical_values_en"), t.get("interfering_factors_en"),
             json.dumps(t.get("associated_conditions", [])), json.dumps(t["sources"]),
             1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
