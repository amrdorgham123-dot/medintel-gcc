"""
Enrichment batch: adds questions_to_ask_en + next_steps_en (patient-guidance
sections) to 20 high-priority existing Lab Info tests that already have
critical_values/interfering_factors from earlier batches but are missing
these two newer sections. This is standard patient-communication guidance,
consistent with what any hospital patient-education page covers.

Run once: python3 enrich_qa_batch1.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "sodium": {
        "questions": "Is my result related to fluid intake, a medication, or an underlying medical condition? How quickly does this need to be corrected, and what's the safe pace? Do I need further testing (like urine sodium or osmolality) to find the cause?",
        "next_steps": "Mild abnormalities are often monitored with repeat testing and a review of fluid intake and medications. More significant abnormalities prompt a workup for the underlying cause and, if needed, careful correction under medical supervision -- correction that's too fast can itself cause serious complications, so this is not something to self-manage."
    },
    "potassium": {
        "questions": "Was this sample checked for hemolysis, since that's a common cause of a falsely high reading? Do I need an ECG given this result? Are any of my medications (like ACE inhibitors, ARBs, or potassium-sparing diuretics) affecting this level?",
        "next_steps": "A significantly abnormal result often prompts an ECG to check for cardiac effects, a repeat blood draw to confirm the value wasn't a lab artifact, and review of medications that affect potassium. Treatment (if needed) depends on the direction and severity, and severe cases require urgent medical care."
    },
    "chloride": {
        "questions": "How does this fit with my other electrolyte results (sodium, bicarbonate)? Is there a specific acid-base or fluid balance issue this is pointing to?",
        "next_steps": "Chloride is rarely acted on alone -- your clinician will look at it together with sodium, bicarbonate, and the anion gap to understand the full picture, and further testing depends on what that combination suggests."
    },
    "bicarbonate-co2": {
        "questions": "Does this suggest a breathing (respiratory) or metabolic issue? Do I need a blood gas test to get a clearer picture? Is this related to my kidney function or a medication I'm taking?",
        "next_steps": "An abnormal result usually prompts review of the full electrolyte panel and clinical context; if the cause isn't clear from that, an arterial blood gas may be ordered to directly assess your acid-base status."
    },
    "bun": {
        "questions": "Does this reflect a hydration issue, my diet, or an actual change in kidney function? How does this compare with my creatinine result? Do I need repeat testing to see if this is a trend?",
        "next_steps": "BUN is usually interpreted together with creatinine -- if both are elevated together, it points more toward a true kidney issue; if BUN is elevated out of proportion to creatinine, dehydration or GI bleeding are considered. Your clinician will decide on further testing based on that pattern."
    },
    "calcium": {
        "questions": "Was this corrected for my albumin level, or do I need an ionized calcium test for a clearer picture? Do I need a PTH or vitamin D test to find the cause? Are there symptoms I should watch for?",
        "next_steps": "Borderline results are often re-checked alongside albumin (or with a direct ionized calcium test). A confirmed abnormality typically leads to PTH and vitamin D testing to identify the cause, since treatment differs significantly depending on whether the source is parathyroid, kidney, bone, or nutritional."
    },
    "magnesium": {
        "questions": "Could this be related to a medication I'm taking (like a diuretic or PPI) or my diet? Does this explain any symptoms I've been having? Do I need supplementation, and for how long?",
        "next_steps": "Mild deficiency is often managed with oral supplementation and addressing the underlying cause (medication review, diet). More significant deficiency, especially with symptoms, may need IV replacement and closer monitoring, particularly if potassium or calcium are also low."
    },
    "phosphorus": {
        "questions": "Is this related to my kidney function, my diet, or a medication? Do I need this monitored regularly given my other health conditions? What symptoms should prompt me to seek care sooner?",
        "next_steps": "Management depends heavily on the cause and direction of the abnormality -- kidney disease-related elevation is managed differently than a nutritional deficiency, so your clinician will look at your overall clinical picture (especially kidney function and calcium) before deciding on treatment."
    },
    "albumin": {
        "questions": "Is this more likely related to nutrition, liver function, kidney protein loss, or inflammation? Does this affect how other test results (like calcium) should be interpreted? Do I need further liver or kidney testing?",
        "next_steps": "A low albumin prompts your clinician to consider liver disease, kidney protein loss, malnutrition, or chronic inflammation as possible causes, and further testing (liver panel, urine protein, nutritional assessment) is guided by which of these seems most likely given your history and other results."
    },
    "total-bilirubin": {
        "questions": "Is this from a liver problem, a bile duct blockage, or red blood cell breakdown? Do I need the direct/indirect breakdown to clarify the cause? Are my liver enzymes affected too?",
        "next_steps": "Your clinician will look at the direct vs. indirect fractions together with your liver enzymes (ALT, AST, ALP) to narrow down the cause, and further testing (imaging, hemolysis workup) depends on that pattern."
    },
    "alkaline-phosphatase": {
        "questions": "Does this look like it's coming from my liver or my bones? Do I need a GGT test to help clarify that? Is this related to a medication or a normal life stage (like pregnancy or growth)?",
        "next_steps": "A GGT test is typically added to determine whether an elevated ALP is coming from the liver/biliary system (GGT also elevated) or from bone (GGT normal), which then guides whether liver imaging or a bone-focused workup is the next step."
    },
    "ggt": {
        "questions": "Does this confirm a liver or biliary source for another abnormal result (like ALP)? Could alcohol use or a medication be contributing? Do I need imaging of my liver or bile ducts?",
        "next_steps": "An elevated GGT alongside other liver test abnormalities typically prompts further evaluation of the liver and biliary system, which may include imaging (ultrasound) and a review of alcohol intake and medications."
    },
    "uric-acid": {
        "questions": "Does this explain my joint symptoms, or is it an incidental finding? Do I need treatment even without symptoms? Are my kidneys at risk from this level?",
        "next_steps": "If you have gout symptoms, this result supports that diagnosis and guides urate-lowering treatment decisions. An incidental high level without symptoms is often just monitored, since not everyone with elevated uric acid develops gout."
    },
    "ferritin": {
        "questions": "Is this level reflecting true iron status, or could inflammation be affecting it? Do I need additional iron studies (serum iron, TIBC) for a clearer picture? If elevated, do I need testing for iron overload?",
        "next_steps": "A low ferritin generally confirms iron deficiency and leads to iron replacement and investigation of the cause (diet, blood loss, malabsorption). An elevated ferritin needs correlation with CRP and other iron studies to distinguish true iron overload from an inflammatory response."
    },
    "total-protein": {
        "questions": "Does this need to be broken down further with a protein electrophoresis? Could this be related to my nutrition, liver, kidneys, or immune system? Is there a follow-up test recommended?",
        "next_steps": "An unexplained abnormality, especially on the high side, often prompts serum protein electrophoresis to look at the specific protein fractions and rule out a monoclonal gammopathy, particularly if there's no obvious explanation like dehydration or known liver/kidney disease."
    },
    "vitamin-b12": {
        "questions": "Is my level definitively normal, or could I still have a functional deficiency despite a borderline-normal result? Do I need injections or is an oral supplement enough? What's causing my deficiency (diet, absorption, medication)?",
        "next_steps": "Confirmed deficiency is treated with B12 supplementation (oral or injectable, depending on severity and cause) and investigation of the underlying cause, especially ruling out pernicious anemia if malabsorption is suspected. Borderline results with strong clinical suspicion may prompt additional testing (methylmalonic acid) for confirmation."
    },
    "folate": {
        "questions": "Could my diet, alcohol use, or a medication (like methotrexate) be contributing to this result? Do I need to also check my B12, since the two deficiencies can look similar? If I'm pregnant or planning to be, does this affect my folic acid dosing?",
        "next_steps": "Confirmed deficiency is treated with folate supplementation alongside addressing the underlying cause. Since folate and B12 deficiency can cause a similar blood picture, both are usually checked together before starting treatment, particularly since folate supplementation alone can mask a B12 deficiency."
    },
    "pt-inr": {
        "questions": "If I'm on warfarin, is my INR in the target range for my specific condition? Do I need a dose adjustment? If I'm not on blood thinners, what's causing this result -- liver function, vitamin K, or something else?",
        "next_steps": "For patients on warfarin, results guide dose adjustments per your anticoagulation clinic's protocol. For patients not on blood thinners, an unexpectedly abnormal result prompts investigation of liver function and vitamin K status, and possibly further coagulation testing if a bleeding disorder is suspected."
    },
    "aptt": {
        "questions": "If I'm on heparin, is my level in the therapeutic range? If not on blood thinners, could this indicate a bleeding disorder, and do I need further coagulation testing (like factor levels or a mixing study)?",
        "next_steps": "For heparin-monitored patients, results guide dose adjustment per protocol. An unexplained prolongation in someone not on anticoagulants typically leads to further testing (mixing studies, specific factor levels) to identify the cause, especially before any planned surgery."
    },
    "d-dimer": {
        "questions": "Given my symptoms and risk factors, does this result rule out a blood clot, or do I need imaging to be sure? Could something else (recent surgery, pregnancy, infection) explain an elevated result?",
        "next_steps": "A normal result in someone with low clinical suspicion generally helps rule out a clot without further testing. An elevated result, or any result in someone with higher clinical suspicion, typically leads to imaging (like a CT scan or ultrasound) to directly look for a blood clot, since D-dimer alone can't confirm the diagnosis."
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
