"""
Enrichment batch 2: adds critical_values_en / interfering_factors_en to more
existing Lab Info tests. Sources: ARUP Laboratories Critical Values list,
Medscape/eMedicine reference articles already cited for these tests, and
standard laboratory medicine preanalytical-error literature.

Run once: python3 enrich_critical_values_batch2.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "creatinine": {
        "critical": "No single universal panic value exists for creatinine (unlike potassium or glucose), since acute versus chronic elevation matters more than an absolute cutoff -- however, a rapidly rising creatinine (e.g., doubling within 48 hours) meets criteria for acute kidney injury (KDIGO) and warrants urgent clinical correlation regardless of the absolute value.",
        "interfering": "Very high bilirubin or hemolysis can interfere with the Jaffe (alkaline picrate) method, historically the most common source of assay-specific bias; enzymatic methods are less affected. Recent very high dietary protein/meat intake or intense exercise (muscle breakdown) can transiently raise results; certain medications (e.g., trimethoprim, cimetidine) can raise creatinine by blocking tubular secretion without truly reducing GFR."
    },
    "bun": {
        "critical": "No single universal panic value; markedly elevated BUN (often with a disproportionately high BUN:creatinine ratio) in an acutely ill patient warrants urgent evaluation for GI bleeding, severe dehydration, or acute kidney injury.",
        "interfering": "High-protein diet, GI bleeding (digested blood is a protein load metabolized to urea), and corticosteroid use raise BUN independent of true kidney function. Dehydration/volume depletion raises BUN more than creatinine (elevated BUN:creatinine ratio), while liver disease and malnutrition can lower it independent of kidney function."
    },
    "chloride": {
        "critical": "Adult critical range: <81 mmol/L or >119 mmol/L (commonly cited hospital critical-value threshold; confirm against the reporting lab's own policy, as chloride appears on a minority of institutional critical-value lists).",
        "interfering": "Severe hypertriglyceridemia can cause a spurious result (pseudohypochloremia) with older methodologies, similar to the sodium electrode interference. Bromide intoxication can falsely elevate chloride results on some analyzer methods due to cross-reactivity."
    },
    "bicarbonate-co2": {
        "critical": "Adult critical range: <11 mmol/L or >39 mmol/L (commonly cited hospital critical-value threshold). Severe derangement reflects a significant underlying acid-base disorder (e.g., severe metabolic acidosis or a compensatory response to chronic respiratory disease) and should prompt correlation with an arterial blood gas.",
        "interfering": "Bicarbonate measured on a routine chemistry panel is total CO2 (bicarbonate plus a small amount of dissolved CO2), which is not identical to the calculated HCO3 on an arterial blood gas -- results can differ slightly between a venous chemistry panel and an ABG drawn at the same time. A sample left uncapped or handled improperly can lose CO2 to the air, falsely lowering the result."
    },
    "fibrinogen": {
        "critical": "Fibrinogen <100 mg/dL is generally considered a critical/actionable value indicating significant bleeding risk, and is a common trigger for fibrinogen replacement (cryoprecipitate or fibrinogen concentrate) in actively bleeding patients, particularly in DIC or massive transfusion settings.",
        "interfering": "As an acute-phase reactant, fibrinogen is nonspecifically elevated by any acute inflammation, infection, recent surgery, or pregnancy, which can mask an underlying mild congenital deficiency. Sample clotting during collection (inadequate mixing with the citrate anticoagulant) falsely lowers the measured level."
    },
    "abo-rh-typing": {
        "critical": "A discrepancy between forward and reverse ABO typing, or any ABO/Rh typing result that does not match a patient's historical blood type on record, is treated as a critical/actionable finding requiring immediate investigation before any transfusion proceeds -- this is one of the few 'critical values' in blood banking that is procedural/qualitative rather than a numeric threshold.",
        "interfering": "Recent transfusion of non-identical blood group components, bone marrow/stem cell transplant, and certain B-cell malignancies or IV immunoglobulin therapy can all cause a transient or persistent mixed-field or discrepant typing result that does not reflect the patient's native blood group -- transfusion and transplant history must always be reviewed when interpreting an unexpected typing result."
    },
    "crossmatch": {
        "critical": "An incompatible crossmatch result is itself a critical, actionable finding -- the unit must not be released for that patient, and the blood bank must immediately investigate (repeat testing, antibody workup) and select alternative compatible units, especially urgent when the patient has an active transfusion need.",
        "interfering": "Cold agglutinins, rouleaux formation (e.g., in multiple myeloma), and recent high-dose IV immunoglobulin or monoclonal antibody therapy (e.g., anti-CD38 agents like daratumumab) can cause pan-reactive or falsely incompatible crossmatch results that require specialized techniques (e.g., DTT treatment) to resolve."
    },
    "troponin": {
        "critical": "ARUP Laboratories lists a high-sensitivity troponin I critical value of \u2265200 ng/L; local critical-value thresholds vary substantially by assay generation (high-sensitivity vs. conventional) and institution -- always use the reporting lab's own critical-value policy, and interpret a single value in the context of serial trends per the local rule-in/rule-out algorithm.",
        "interfering": "Skeletal muscle injury (rhabdomyolysis, intense exercise), chronic kidney disease (reduced clearance), heart failure, and tachyarrhythmias can all cause troponin elevation without acute coronary syndrome. Heterophile antibodies or rheumatoid factor can rarely cause assay interference (false elevation) on some immunoassay platforms."
    }
}

def main():
    conn = sqlite3.connect(DB_PATH)
    updated, missing = 0, []
    for slug, data in ENRICHMENT.items():
        row = conn.execute("SELECT id, critical_values_en FROM lab_tests WHERE slug = ?", (slug,)).fetchone()
        if not row:
            missing.append(slug)
            continue
        if row[1]:  # already enriched in an earlier batch -- don't overwrite
            print(f"SKIP (already enriched): {slug}")
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
