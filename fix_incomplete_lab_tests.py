"""
Data-quality fix script. A full audit of all 220 lab_tests records found
6 pre-existing entries (from earlier sessions, not the batch 33-37 additions)
with missing clinical_significance_en, empty associated_conditions_json, or
missing questions_to_ask_en/next_steps_en. This script patches those 6
records so every published test has complete required fields.

Affected: ammonia, lactate, digoxin-level, lithium-level,
adamts13-activity, vitamin-k

Run once: python3 fix_incomplete_lab_tests.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

FIXES = {
    "ammonia": {
        "clinical_significance_en": "Elevated ammonia in a patient with liver disease and altered mental status supports hepatic encephalopathy, since the diseased/bypassed liver can no longer clear ammonia produced by gut bacterial protein metabolism, allowing it to cross the blood-brain barrier and cause neurotoxicity. The degree of elevation correlates only loosely with the severity of encephalopathy -- clinical staging (mental status, asterixis) matters more than the absolute level for grading severity or guiding treatment, though a rising level over time or a very high level can support the diagnosis when the picture is ambiguous. In neonates and children, markedly elevated ammonia without liver disease raises concern for an inherited urea cycle disorder, a pediatric emergency requiring rapid identification and treatment given the risk of irreversible neurological injury."
    },
    "lactate": {
        "clinical_significance_en": "Elevated lactate reflects tissue hypoperfusion or hypoxia driving anaerobic metabolism, and is a key marker of illness severity in sepsis and other shock states -- a level \u22654 mmol/L is part of the Sepsis-3 criteria for septic shock and is associated with higher mortality. Serial lactate measurements (lactate clearance) are used to track response to resuscitation, with a failure to clear lactate despite treatment signaling ongoing tissue hypoperfusion and prompting escalation of care. Elevation is not specific to sepsis -- any shock state (cardiogenic, hypovolemic, obstructive), severe exertion, seizure activity, or certain medications (including metformin in the setting of renal impairment) can also raise lactate, so the result is interpreted alongside the full clinical picture."
    },
    "digoxin-level": {
        "clinical_significance_en": "Digoxin has a narrow therapeutic index, and current evidence supports targeting the lower end of the traditional range (roughly 0.5-0.9 ng/mL) for heart failure, since higher levels have been associated with increased mortality without added benefit in major trials, while a somewhat higher range has traditionally been used for rate control in atrial fibrillation. Toxicity can occur even within or near the traditional therapeutic range, particularly with hypokalemia, hypomagnesemia, hypoxia, hypothyroidism, or renal impairment (digoxin is renally cleared), and classically presents with nausea, visual disturbances (yellow-green halos), confusion, and characteristic cardiac arrhythmias (including bidirectional ventricular tachycardia). Because digoxin distributes slowly into tissue, a level drawn too soon after a dose (within about 6-8 hours) can be falsely high and does not reflect true steady-state exposure.",
        "associated_conditions": [
            {"condition": "Digoxin toxicity (nausea, visual disturbance, arrhythmia)", "direction": "high, or even low-normal with hypokalemia/renal impairment/hypothyroidism"},
            {"condition": "Subtherapeutic digoxin (inadequate rate control or heart failure benefit)", "direction": "low"}
        ]
    },
    "lithium-level": {
        "clinical_significance_en": "Lithium has a narrow therapeutic index, and levels must be interpreted alongside clinical response and side effects rather than as an isolated target -- a level within range does not exclude toxicity in a vulnerable patient, and a level slightly above range may be tolerated in some. Toxicity risk rises substantially above the therapeutic range and presents with a spectrum from mild tremor and GI upset to confusion, ataxia, and, at severe levels, seizures, arrhythmias, and coma; renal impairment, dehydration, and drug interactions (notably NSAIDs, ACE inhibitors/ARBs, and thiazide diuretics, all of which reduce lithium clearance) can precipitate toxicity even without a dose change. Because lithium excretion tracks closely with sodium and water balance, any condition causing volume depletion (vomiting, diarrhea, reduced intake, hot weather) can unexpectedly raise levels and requires closer monitoring or temporary dose adjustment.",
        "associated_conditions": [
            {"condition": "Lithium toxicity (tremor, GI upset progressing to confusion, ataxia, seizures)", "direction": "high, or unexpectedly high with dehydration/renal impairment/interacting drugs"},
            {"condition": "Subtherapeutic lithium (inadequate mood stabilization)", "direction": "low"}
        ]
    },
    "adamts13-activity": {
        "clinical_significance_en": "Severely reduced ADAMTS13 activity (typically <10 IU/dL) in a patient with microangiopathic hemolytic anemia and thrombocytopenia is considered diagnostic of thrombotic thrombocytopenic purpura (TTP) in the appropriate clinical context, distinguishing it from other thrombotic microangiopathies such as hemolytic uremic syndrome, which have a normal or only mildly reduced ADAMTS13 and require different treatment. Acquired TTP (the more common form) results from an autoantibody inhibiting ADAMTS13, identified by adding an inhibitor/antibody assay when activity is low; congenital TTP (Upshaw-Schulman syndrome) instead reflects an inherited enzyme deficiency present from birth without an inhibitory antibody. Because untreated TTP can be rapidly fatal, plasma exchange therapy is often started empirically based on strong clinical suspicion (using a validated clinical prediction score) before the ADAMTS13 result is even back, with the result confirming the diagnosis and guiding continued management."
    },
    "vitamin-k": {
        "questions_to_ask_en": "Could a medication I'm taking (like long-term antibiotics) or a digestive condition be causing this deficiency? Do I need vitamin K supplementation, and how quickly will my clotting times normalize?",
        "next_steps": "Confirmed deficiency is treated with vitamin K supplementation (oral or, if malabsorption is significant or urgent correction of bleeding risk is needed, parenteral), with a repeat PT/INR after treatment to confirm correction and investigation of the underlying cause (malabsorption, antibiotic use, dietary intake) addressed where possible."
    }
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated = 0
    for slug, fields in FIXES.items():
        existing = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (slug,)).fetchone()
        if not existing:
            print(f"SKIP (not found): {slug}")
            continue
        set_clauses = []
        params = []
        if "clinical_significance_en" in fields:
            set_clauses.append("clinical_significance_en = ?")
            params.append(fields["clinical_significance_en"])
        if "associated_conditions" in fields:
            set_clauses.append("associated_conditions_json = ?")
            params.append(json.dumps(fields["associated_conditions"]))
        if "questions_to_ask_en" in fields:
            set_clauses.append("questions_to_ask_en = ?")
            params.append(fields["questions_to_ask_en"])
        if "next_steps" in fields:
            set_clauses.append("next_steps_en = ?")
            params.append(fields["next_steps"])
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        params.append(slug)
        conn.execute(f"UPDATE lab_tests SET {', '.join(set_clauses)} WHERE slug = ?", params)
        print(f"UPDATED: {slug}")
        updated += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Updated: {updated}")

if __name__ == "__main__":
    main()
