"""
Final enrichment batch: adds questions_to_ask_en + next_steps_en to the last
24 existing Lab Info tests, completing full 11-section enrichment for all
148 tests currently in the library.

Run once: python3 enrich_qa_batch6.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "beta-2-microglobulin": {
        "questions": "Does this reflect my disease activity, or could reduced kidney function be raising this result instead? How does this fit into my overall staging/prognosis? Should this be tracked over time?",
        "next_steps": "Results are interpreted alongside kidney function tests to determine how much of the level reflects disease burden versus reduced clearance, and serial monitoring is often used to track disease activity or treatment response in confirmed cases."
    },
    "alpha-1-antitrypsin": {
        "questions": "Does this explain my lung or liver symptoms? Do I need phenotyping or genotyping to confirm a specific deficiency type? Should my family members be tested?",
        "next_steps": "A low result typically leads to phenotyping or genotyping to confirm the specific genetic variant, pulmonology and/or hepatology referral depending on symptoms, and consideration of family testing given the hereditary nature of this condition."
    },
    "shbg": {
        "questions": "Does this help explain my testosterone or estrogen-related symptoms? Could my weight, thyroid function, or a medication be affecting this? Should my free hormone levels be checked alongside this?",
        "next_steps": "This result is used together with total testosterone or estradiol to calculate free/bioavailable hormone levels, giving a more accurate picture than the total level alone, especially when symptoms don't match the total hormone result."
    },
    "factor-viii-activity": {
        "questions": "Does this confirm hemophilia A, or could this be related to von Willebrand disease instead? How severe is my condition based on this level? What precautions should I take for procedures or activities?",
        "next_steps": "A low result prompts von Willebrand factor testing to distinguish hemophilia A from von Willebrand disease (since the two can look similar), and the specific level obtained determines severity classification and guides precautions for surgery, dental work, and physical activity."
    },
    "ebv-antibody-panel": {
        "questions": "Does this confirm I currently have mononucleosis, or is this from a past infection? How long am I likely to be contagious or symptomatic? Do I need any activity restrictions (like avoiding contact sports)?",
        "next_steps": "A pattern consistent with acute infection is usually managed with supportive care (rest, fluids) and, if you have an enlarged spleen, temporary avoidance of contact sports or heavy lifting until it's resolved, given the small risk of splenic rupture."
    },
    "hla-b27": {
        "questions": "Given my symptoms, does this result support a specific diagnosis? Does a positive result mean I will definitely develop this condition? Do I need further imaging or rheumatology referral?",
        "next_steps": "A positive result in someone with compatible symptoms (like inflammatory back pain) supports referral to rheumatology for further evaluation, including imaging; a positive result alone in someone without symptoms is not itself actionable, since many people with this marker never develop disease."
    },
    "varicella-zoster-igg-igm": {
        "questions": "Am I immune, or susceptible to infection? If I'm pregnant and non-immune, what precautions should I take if exposed? Do I need vaccination, and when would that be safe?",
        "next_steps": "A non-immune result generally leads to vaccination recommendations (timed appropriately if you're pregnant, since it's a live vaccine); if there's been a recent exposure and you're non-immune, your clinician may discuss post-exposure options depending on your risk factors."
    },
    "ionized-calcium": {
        "questions": "Does this change how my total calcium result should be interpreted? Is this related to my critical illness or a specific medication? How urgently does this need to be corrected?",
        "next_steps": "Since this reflects the true active calcium level, results directly guide treatment decisions (calcium replacement for low levels, or investigation of the cause for high levels) more reliably than total calcium alone, especially in critically ill patients."
    },
    "hepatitis-a-igm": {
        "questions": "Does this confirm my symptoms are from hepatitis A? How long am I likely to be contagious to others? Do my close contacts need post-exposure treatment?",
        "next_steps": "A positive result confirms acute infection, and public health notification is typically required; close contacts may be offered post-exposure vaccination or immune globulin depending on timing, and you'll be advised on hygiene precautions to prevent spreading it to others."
    },
    "total-ige": {
        "questions": "Does this support an allergic condition as the cause of my symptoms? Do I need allergen-specific testing to identify triggers? Could a non-allergic cause (like a parasitic infection) explain this?",
        "next_steps": "An elevated result supportive of atopic disease often leads to allergen-specific IgE testing or skin prick testing to identify your specific triggers, since total IgE alone doesn't tell you what you're reacting to."
    },
    "copper": {
        "questions": "Does this reflect true copper deficiency or excess, or could Wilson disease or another condition better explain this? Should this be interpreted alongside ceruloplasmin? Do I need supplementation or dietary changes?",
        "next_steps": "Results are interpreted together with ceruloplasmin to distinguish true deficiency/excess from Wilson disease, and treatment (supplementation for deficiency, chelation for confirmed overload) depends on that combined picture."
    },
    "ttg-iga": {
        "questions": "Given this result and my total IgA, is celiac disease likely? Do I need a biopsy to confirm? Should I continue eating gluten until further testing is done?",
        "next_steps": "A significantly elevated result typically leads to referral for endoscopic biopsy to confirm the diagnosis before starting a gluten-free diet, since starting the diet early can make later testing less accurate -- it's important not to eliminate gluten before all testing is complete."
    },
    "myoglobin": {
        "questions": "Does this support rhabdomyolysis as the cause of my symptoms? How does this compare with my CK level? Is my kidney function being monitored given this result?",
        "next_steps": "An elevated result alongside elevated CK and compatible symptoms (muscle pain, dark urine) supports rhabdomyolysis, prompting aggressive IV hydration and monitoring of kidney function to prevent complications."
    },
    "il-6": {
        "questions": "Does this level help predict how sick I am or how I might respond to treatment? Is this being used to guide a specific medication decision? How does this compare to my other inflammatory markers?",
        "next_steps": "In critical illness, this result is used alongside clinical assessment and other markers to help gauge severity and, in specific situations (like cytokine release syndrome), may guide use of targeted anti-inflammatory therapy."
    },
    "spep": {
        "questions": "If a band was found, do I need immunofixation to identify exactly what it is? Does this explain my symptoms (like bone pain, anemia, or kidney issues)? Do I need a hematology referral?",
        "next_steps": "A detected monoclonal band leads to immunofixation electrophoresis to identify the specific protein type, along with free light chain testing and, depending on findings, hematology referral to determine whether this represents MGUS or a disease requiring treatment."
    },
    "serum-free-light-chains": {
        "questions": "Does this abnormal ratio point toward a specific plasma cell disorder? Could my kidney function be affecting this result? Do I need this combined with SPEP and imaging for a full picture?",
        "next_steps": "An abnormal ratio typically leads to further testing (SPEP, immunofixation, sometimes bone marrow biopsy and imaging) to determine the specific diagnosis and whether treatment is needed, guided by hematology."
    },
    "chromogranin-a": {
        "questions": "Could a medication I'm taking (like a PPI) be raising this result rather than a tumor? Does this need to be combined with other tests (like metanephrines) for a clearer picture? Do I need imaging?",
        "next_steps": "Given how many non-tumor causes can raise this result, your clinician will consider stopping interfering medications if possible before repeat testing, and an elevated result typically prompts imaging to look for a neuroendocrine tumor."
    },
    "gastrin": {
        "questions": "Was I properly off acid-reducing medications before this test? Does this level need a stimulation test to confirm a diagnosis? What symptoms should I watch for?",
        "next_steps": "A markedly elevated result with acid hypersecretion strongly supports Zollinger-Ellison syndrome; a more modestly elevated result often leads to a secretin stimulation test to confirm the diagnosis before treatment decisions are made."
    },
    "5-hiaa": {
        "questions": "Does this confirm carcinoid syndrome as the cause of my symptoms (like flushing or diarrhea)? Do I need imaging to locate the tumor? Will this be used to track how my treatment is working?",
        "next_steps": "An elevated result in someone with a known or suspected neuroendocrine tumor supports the diagnosis of carcinoid syndrome and is often followed serially to monitor disease activity and response to treatment (such as somatostatin analog therapy)."
    },
    "ena-panel": {
        "questions": "Which specific antibody was positive, and what condition does that point to? Does this change my diagnosis or treatment plan? If I'm pregnant, does a positive Anti-Ro/SSA affect monitoring for my baby?",
        "next_steps": "The specific antibody pattern (Ro/SSA, La/SSB, Sm, or RNP) helps confirm a specific diagnosis (Sjogren's, lupus, or mixed connective tissue disease) and guides your rheumatologist's management plan; a positive Anti-Ro/SSA in pregnancy prompts additional fetal heart monitoring."
    },
    "cold-agglutinin-titer": {
        "questions": "Does this explain my cold-related symptoms or anemia? Do I need to avoid cold exposure? If I need surgery, does this affect how it's planned?",
        "next_steps": "A significant titer prompts avoidance of cold exposure where possible and, if surgery is planned, special precautions (like keeping the operating room warm) to prevent complications from red cell agglutination during cooling."
    },
    "cryoglobulins": {
        "questions": "Does this explain my skin, joint, or kidney symptoms? Could this be related to a hepatitis C infection or another underlying condition? What further testing or treatment do I need?",
        "next_steps": "A positive result prompts investigation for the underlying cause -- most commonly hepatitis C, but also autoimmune disease or a blood cancer -- since treatment is directed at that underlying condition rather than the cryoglobulins themselves."
    },
    "rh-phenotype-extended": {
        "questions": "Does this affect what type of blood I should receive in future transfusions? If I've had a transfusion reaction before, does this help explain why? Should this be documented for my future care?",
        "next_steps": "This result is typically recorded in your record to guide antigen-matched blood selection for any future transfusions, particularly important if you're likely to need chronic transfusion support or have a history of transfusion reactions."
    },
    "weak-d-testing": {
        "questions": "Given this result, am I considered Rh-positive or Rh-negative for transfusion and pregnancy purposes? Do I need genetic testing to clarify further? Does this affect whether I need Rh immune globulin during pregnancy?",
        "next_steps": "How this result is used depends on your role -- if you're a blood donor, a weak D result is generally treated as Rh-positive; if you're a transfusion recipient or pregnant, it's typically treated as Rh-negative unless RHD genotyping specifically confirms a benign weak D type, which your care team will discuss with you."
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
