"""
Enriches the most commonly viewed Lab Info tests with two new patient-guidance
sections: questions_to_ask_en ('Questions to Ask Your Doctor') and
next_steps_en ('What Happens Next'). This is practical, standard-of-care
communication guidance (not a specific clinical claim), so it isn't tied to
an external citation the way reference ranges are -- it mirrors the kind of
guidance found on any hospital patient-education page for these tests.

Run once: python3 enrich_patient_guidance.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "cbc": {
        "questions": "Is my result normal for my age and sex? If something is abnormal, is it new or has it been trending this way over time? Do I need a peripheral blood smear or repeat testing to clarify the result? Could any of my current medications or recent illness explain an abnormal finding? Do I need iron, B12, or folate studies based on my red cell indices?",
        "next_steps": "A normal CBC usually needs no further action beyond routine follow-up. An abnormal result typically leads to one of: a repeat test to confirm it isn't a lab or collection artifact, additional targeted tests (e.g., iron studies, B12/folate, reticulocyte count, peripheral smear) to investigate the specific abnormality, or referral to hematology if the pattern suggests a more complex blood disorder. Your clinician will interpret the result alongside your symptoms and history rather than in isolation."
    },
    "fasting-glucose": {
        "questions": "Was I truly fasting for at least 8 hours, and could that affect this result? Does this result need to be confirmed with a repeat test or an HbA1c before a diagnosis is made? What lifestyle changes are recommended if my glucose is borderline? If I'm diagnosed with prediabetes or diabetes, what's the plan for monitoring and follow-up?",
        "next_steps": "A single elevated result is not usually enough to diagnose diabetes -- ADA criteria generally require either two abnormal tests or one abnormal test plus classic symptoms of high blood sugar. Depending on the result, your clinician may order a repeat fasting glucose, an HbA1c, or an oral glucose tolerance test, and may discuss diet, weight, and activity changes even for borderline (prediabetes-range) results."
    },
    "hba1c": {
        "questions": "What is my target HbA1c, and does it differ from the general population target based on my age or other health conditions? How does this result compare to my last one -- am I improving, stable, or worsening? Could an underlying condition (e.g., anemia, hemoglobin variant) be making this result inaccurate? How often should I repeat this test going forward?",
        "next_steps": "If this is a new diagnosis of prediabetes or diabetes, your clinician will typically discuss lifestyle modification and, for diabetes, may start or adjust medication, along with baseline screening for diabetes-related complications (eye exam, kidney function, foot exam). If you're already being treated for diabetes, the result guides whether your current treatment plan needs to be intensified, continued, or reduced."
    },
    "lipid-panel": {
        "questions": "What is my individual cardiovascular risk category, and how does that affect my treatment targets? Do I need additional testing (e.g., Lp(a), ApoB, coronary calcium score) to refine my risk assessment? Should I be on lipid-lowering medication, or are lifestyle changes enough at this stage? How often should this be rechecked?",
        "next_steps": "Your clinician will interpret this result alongside your overall cardiovascular risk factors (age, blood pressure, smoking status, diabetes, family history) rather than any single number in isolation. Depending on your risk category, next steps may include dietary and exercise counseling, a statin or other lipid-lowering therapy, or further risk-stratifying tests before a treatment decision is made."
    },
    "tsh": {
        "questions": "Do I need a free T4 (and possibly free T3) to fully interpret this result? Could any of my medications (e.g., biotin supplements, thyroid medication timing) be affecting the accuracy of this result? If my result is abnormal, is this likely to be a temporary or a chronic condition? How often will my thyroid function need to be monitored going forward?",
        "next_steps": "An abnormal TSH is typically followed up with a free T4 (and sometimes free T3) to determine the type and severity of thyroid dysfunction before any treatment decision. Mildly abnormal results in an otherwise well patient are often rechecked in a few weeks to months before starting treatment, since transient illness and lab variability can affect a single result."
    },
    "creatinine": {
        "questions": "What is my estimated GFR (eGFR) based on this result, and what stage of kidney function does that represent? Is this a new finding or has my kidney function been declining over time? Could any of my medications need dose adjustment based on this result? Do I need additional testing (e.g., urine albumin/creatinine ratio, renal ultrasound) to investigate further?",
        "next_steps": "An isolated mild abnormality is often rechecked to confirm it isn't due to dehydration, recent heavy exercise, or a temporary cause. A significant or persistent abnormality typically prompts calculation of eGFR, review of medications that affect or are affected by kidney function, urine testing (e.g., albumin/creatinine ratio), and possible referral to nephrology depending on severity and trend."
    },
    "abo-rh-typing": {
        "questions": "Has this result been confirmed with a second sample, as required before major transfusion in many facilities? If I'm RhD-negative, do I need Rh immune globulin (e.g., during pregnancy or after a sensitizing event)? Does my blood type have any implications for donating blood or organ/tissue matching?",
        "next_steps": "For transfusion purposes, your blood type is recorded in your record and used alongside an antibody screen and crossmatch before any blood product is issued to you. If you are RhD-negative and pregnant (or have had a potentially sensitizing event), your care team will discuss the timing of Rh immune globulin to prevent Rh alloimmunization in future pregnancies."
    },
    "vitamin-d": {
        "questions": "Given my result, do I need supplementation, and if so, what dose and for how long? Should this be rechecked after starting supplementation, and if so, when? Could my result be related to limited sun exposure, diet, malabsorption, or a medication I'm taking? Are there other tests (e.g., calcium, PTH) I should have alongside this?",
        "next_steps": "Deficient or insufficient results are commonly managed with vitamin D supplementation, with the dose and duration depending on how low the result is and your individual risk factors; a repeat level is often checked after a few months of supplementation to confirm the response. Levels within the sufficient range generally need no action beyond routine monitoring as advised by your clinician."
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
            "UPDATE lab_tests SET questions_to_ask_en = ?, next_steps_en = ? WHERE slug = ?",
            (data["questions"], data["next_steps"], slug)
        )
        updated += 1
    conn.commit()
    conn.close()
    print(f"Updated: {updated}")
    if missing:
        print(f"Not found in DB (skipped): {missing}")

if __name__ == "__main__":
    main()
