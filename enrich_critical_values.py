"""
Enriches the highest-priority existing Lab Info tests with two new fields:
critical_values_en (life-threatening thresholds requiring immediate notification)
and interfering_factors_en (things that can cause a false high/low result).

Primary critical-value source: ARUP Laboratories official Critical Values list
(https://www.aruplab.com/files/resources/testing/ARUP_Critical_Values.pdf, adult
values, accessed 2026-07-14) plus acutecaretesting.org's peer-reviewed review of
critical-value practice for cross-checking which analytes are near-universally
included on critical-value lists.

Run once: python3 enrich_critical_values.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "potassium": {
        "critical": "Adult critical range: <3.0 mmol/L or >6.1 mmol/L (ARUP Laboratories). Severe hypo- or hyperkalemia can cause life-threatening cardiac arrhythmias and requires immediate physician notification and, often, emergency treatment (e.g., IV calcium, insulin/glucose, or potassium replacement depending on direction).",
        "interfering": "Hemolysis during or after collection (e.g., difficult draw, prolonged tourniquet time, vigorous mixing) releases intracellular potassium and is the most common cause of a falsely elevated result -- a hemolyzed sample should prompt a repeat draw before acting on an unexpectedly high value. Fist clenching during venipuncture can also transiently raise results. Marked leukocytosis or thrombocytosis can cause pseudohyperkalemia in vitro from cell lysis in the tube after collection, without reflecting the true in-vivo level."
    },
    "sodium": {
        "critical": "Adult critical range: <120 mmol/L or >160 mmol/L (ARUP Laboratories). Severe hypo- or hypernatremia, especially if of rapid onset, can cause seizures, cerebral edema, or altered consciousness and requires urgent clinical correlation -- correction rate must be carefully controlled to avoid osmotic demyelination syndrome when correcting chronic hyponatremia.",
        "interfering": "Severe hyperlipidemia or hyperproteinemia can cause spuriously low sodium on older indirect ion-selective electrode methods (pseudohyponatremia) -- less of an issue with modern direct ISE methods, but worth considering if the result doesn't fit the clinical picture. Drawing from an arm receiving IV fluids can dilute or skew the result."
    },
    "calcium": {
        "critical": "Adult critical range for total calcium: <6.0 mg/dL or >13.0 mg/dL (ARUP Laboratories). Severe hypocalcemia can cause tetany, seizures, or cardiac arrhythmia (prolonged QT); severe hypercalcemia can cause altered mental status, cardiac arrhythmia, and is a medical emergency.",
        "interfering": "Total calcium result is significantly affected by serum albumin, since roughly 40% of calcium is protein-bound -- a low albumin can make total calcium appear falsely low even when the physiologically active ionized calcium is normal (a 'corrected calcium' calculation, or a direct ionized calcium measurement, should be used when albumin is abnormal). Prolonged tourniquet time and drawing above an IV line with calcium-containing fluids can also skew results."
    },
    "magnesium": {
        "critical": "Adult critical range: <1.0 mg/dL or >9.0 mg/dL (ARUP Laboratories). Severe hypomagnesemia can cause seizures and cardiac arrhythmias (including torsades de pointes); severe hypermagnesemia (usually from renal failure plus magnesium administration, e.g., in eclampsia treatment) can cause respiratory depression and cardiac arrest.",
        "interfering": "Hemolysis falsely raises results, since intracellular magnesium concentration is higher than serum. Serum magnesium reflects only about 1% of total body stores, so a normal result does not rule out significant intracellular/total body depletion."
    },
    "phosphorus": {
        "critical": "Adult critical range: <1.0 mg/dL or >9.0 mg/dL (ARUP Laboratories). Severe hypophosphatemia can cause muscle weakness, respiratory failure, and cardiac dysfunction (classically seen in refeeding syndrome); severe hyperphosphatemia (usually in renal failure or tumor lysis syndrome) contributes to hypocalcemia and metastatic calcification risk.",
        "interfering": "Hemolysis falsely raises results. Recent meals (phosphorus has diurnal variation and is affected by carbohydrate intake, which shifts phosphate intracellularly) can lower results -- a fasting morning sample is preferred for accurate interpretation."
    },
    "fasting-glucose": {
        "critical": "Adult critical range: <55 mg/dL or >450 mg/dL (ARUP Laboratories; neonatal thresholds differ and are higher-risk at even less extreme values). Severe hypoglycemia can cause seizures, coma, and permanent neurologic injury if untreated; severe hyperglycemia raises concern for diabetic ketoacidosis or hyperosmolar hyperglycemic state.",
        "interfering": "Delayed sample processing allows ongoing glycolysis by red and white blood cells, which can falsely lower results if the tube isn't a glycolysis-inhibitor (gray-top/fluoride) tube or isn't processed promptly. Recent food/drink intake invalidates a 'fasting' result -- confirm true fasting status before acting on a borderline value."
    },
    "cbc": {
        "critical": "Adult critical ranges (ARUP Laboratories): Hemoglobin <7.0 g/dL; Platelet count \u226420,000/\u00b5L or \u22651,000,000/\u00b5L; White blood cell count \u22642,000/\u00b5L or \u226540,000/\u00b5L. Severe anemia, severe thrombocytopenia (bleeding risk) or extreme thrombocytosis, and marked leukopenia (infection risk) or leukocytosis (possible leukemia/severe infection) all warrant urgent clinical correlation and often same-day physician notification.",
        "interfering": "Cold agglutinins or red cell clumping can cause a falsely low automated RBC/platelet count and falsely high MCV -- warming the sample or manual review can correct this. Platelet clumping (often EDTA-induced pseudothrombocytopenia) can cause a falsely low automated platelet count; a citrate-tube repeat or peripheral smear review confirms the true count. Marked leukocytosis can interfere with automated hemoglobin/hematocrit measurement on some analyzers."
    },
    "troponin": {
        "critical": "ARUP Laboratories lists a high-sensitivity troponin I critical value of \u2265200 ng/L; local critical-value thresholds vary by assay generation and institution -- always use the reporting lab's own critical-value policy for high-sensitivity assays, which are far more sensitive than older-generation troponin tests.",
        "interfering": "Skeletal muscle injury, strenuous exercise, renal failure (reduced clearance), and tachyarrhythmias can all cause troponin elevation without acute coronary syndrome -- the pattern of rise and fall on serial testing, not a single value, is what distinguishes acute myocardial injury from chronically elevated troponin (e.g., in chronic kidney disease)."
    },
    "pt-inr": {
        "critical": "ARUP Laboratories critical values: Prothrombin Time \u226546.4 seconds; INR \u22655.0. A markedly elevated INR substantially increases spontaneous bleeding risk, particularly in warfarin-treated patients, and requires urgent clinical correlation and possible reversal therapy.",
        "interfering": "Under-filled citrate tubes (wrong blood-to-anticoagulant ratio) falsely prolong PT/INR -- this is one of the most common preanalytical errors in coagulation testing. Traumatic or difficult venipuncture can activate clotting factors in the sample and give a falsely shortened or unreliable result."
    },
    "aptt": {
        "critical": "ARUP Laboratories critical value: aPTT \u226585 seconds. A markedly prolonged aPTT increases bleeding risk and, in a patient on unfractionated heparin, may indicate the dose is well above the therapeutic target.",
        "interfering": "Under-filled citrate tubes (wrong blood-to-anticoagulant ratio) falsely prolong the result -- a common and important preanalytical error. Drawing the sample from or near a heparinized IV line/catheter can contaminate the sample and falsely prolong the result even when the patient is not therapeutically anticoagulated."
    }
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated, missing = 0, []
    for slug, data in ENRICHMENT.items():
        row = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (slug,)).fetchone()
        if not row:
            missing.append(slug)
            continue
        conn.execute(
            "UPDATE lab_tests SET critical_values_en = ?, interfering_factors_en = ? WHERE slug = ?",
            (data["critical"], data["interfering"], slug)
        )
        updated += 1
    conn.commit()
    conn.close()
    print(f"Updated: {updated}")
    if missing:
        print(f"Not found in DB (skipped): {missing}")

if __name__ == "__main__":
    main()
