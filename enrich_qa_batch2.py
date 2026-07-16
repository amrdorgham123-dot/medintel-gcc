"""
Enrichment batch 2: adds questions_to_ask_en + next_steps_en to 20 more
existing Lab Info tests (liver enzymes, blood bank, thyroid, cardiac,
tumor markers).

Run once: python3 enrich_qa_batch2.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "alt-ast": {
        "questions": "Is this likely from fatty liver, alcohol, a viral infection, or a medication? Do I need further testing (viral hepatitis panel, imaging) to find the cause? How often should this be rechecked?",
        "next_steps": "Mild, isolated elevation is often rechecked in a few weeks along with a review of alcohol use and medications. Persistent or significant elevation typically leads to a broader liver workup -- viral hepatitis serology, liver imaging, and sometimes a liver biopsy -- depending on the pattern and your risk factors."
    },
    "crp": {
        "questions": "Does this level point to a specific infection or inflammatory condition, or is it too general to tell? Do I need more specific testing to find the source? If this is for cardiovascular risk, was it drawn correctly (fasting, not during acute illness)?",
        "next_steps": "A markedly elevated CRP with symptoms usually prompts a search for an infectious or inflammatory source (exam, cultures, imaging as indicated). If used for cardiovascular risk assessment, an elevated result is factored in alongside your other risk factors rather than treated as a standalone diagnosis."
    },
    "antibody-screen": {
        "questions": "If positive, do I need antibody identification to find out exactly which antibody this is? Does this affect how quickly compatible blood can be found for me if I need a transfusion? Should this be noted in my medical record for future reference?",
        "next_steps": "A positive screen leads to antibody identification testing to pinpoint the specific antibody, which then determines what antigen-negative blood units need to be selected for any future transfusion -- this information is typically recorded for your ongoing care, since these antibodies can persist or recur."
    },
    "dat-coombs": {
        "questions": "Does this explain symptoms I've been having (like fatigue or jaundice)? Do I need further blood tests to understand the pattern of anemia? Could a medication I'm taking be responsible?",
        "next_steps": "A positive result in someone with anemia typically leads to further hemolysis workup (LDH, haptoglobin, bilirubin, reticulocyte count) and a review of medications, since certain drugs can trigger this pattern -- treatment then depends on identifying the underlying cause."
    },
    "crossmatch": {
        "questions": "If incompatible, how will this affect the timing of my planned transfusion or surgery? Do I need special antigen-matched blood going forward?",
        "next_steps": "An incompatible result means the blood bank will select and test alternative units before any transfusion proceeds -- this is a routine safety step, though it may take some additional time, which your care team will factor into planning if a transfusion is time-sensitive."
    },
    "antibody-identification": {
        "questions": "What is the specific antibody, and how does it affect my future transfusion needs? If I'm pregnant, does this antibody carry a risk to the baby? Should I carry documentation of this for future medical visits?",
        "next_steps": "Once identified, the specific antibody determines which antigen-negative blood units are safe for you going forward, and this is typically documented for future reference since re-identifying it can take time in an emergency. If the antibody is one associated with pregnancy risk, you'll be referred for appropriate monitoring."
    },
    "kleihauer-betke": {
        "questions": "Based on this result, how much Rh immune globulin do I need? Is one dose enough, or will I need additional doses? Does this affect monitoring for the rest of my pregnancy?",
        "next_steps": "The result is used directly to calculate whether the standard dose of Rh immune globulin is sufficient or whether additional doses are needed, which your obstetric team will arrange promptly given the time-sensitive nature of RhIG administration after a sensitizing event."
    },
    "free-t4": {
        "questions": "How does this fit with my TSH result -- do they agree, or is there a discrepancy that needs explaining? Do I need my dose of thyroid medication adjusted? Is this a temporary or ongoing issue?",
        "next_steps": "Free T4 is interpreted together with TSH to fully characterize your thyroid status; if you're on thyroid medication, this result often guides a dose adjustment, with a repeat test typically done 6-8 weeks after any change to allow levels to stabilize."
    },
    "free-t3": {
        "questions": "Why was this ordered in addition to TSH and free T4 -- is there a specific concern (like hyperthyroidism)? Does this change my treatment plan?",
        "next_steps": "Free T3 is typically added when hyperthyroidism is suspected but free T4 is normal (since some hyperthyroid patients have isolated T3 elevation), or to assess severity in confirmed hyperthyroidism -- results are interpreted alongside TSH and free T4, not alone."
    },
    "pth": {
        "questions": "Does this explain my calcium result? Do I need vitamin D and kidney function testing to fully understand this? Do I need imaging of my parathyroid glands?",
        "next_steps": "PTH is always interpreted together with calcium -- the combination determines whether the picture fits primary hyperparathyroidism, secondary hyperparathyroidism (often from vitamin D deficiency or kidney disease), or hypoparathyroidism, which then guides whether imaging or further hormone testing is needed."
    },
    "cortisol": {
        "questions": "Was this drawn at the right time of day, since cortisol varies a lot through the day? Do I need a stimulation or suppression test to confirm a diagnosis? Could stress, illness, or a medication be affecting this result?",
        "next_steps": "An abnormal random or morning cortisol is rarely diagnostic on its own -- it typically leads to a dynamic test (like a cosyntropin stimulation test for suspected insufficiency, or a dexamethasone suppression test for suspected excess) to confirm the diagnosis before any treatment decision."
    },
    "serum-iron": {
        "questions": "Should this be interpreted alongside ferritin and TIBC for a full picture of my iron status? Could recent food or supplement intake have affected this result? Do I need this repeated fasting?",
        "next_steps": "Serum iron is rarely interpreted alone -- your clinician will look at it together with ferritin and TIBC/transferrin saturation to distinguish iron deficiency from other causes of anemia or from iron overload, and a fasting morning sample is often requested for accuracy."
    },
    "tibc-transferrin-saturation": {
        "questions": "Does this pattern point more toward iron deficiency or a chronic disease process? Do I need additional testing (ferritin, CRP) to clarify? Should my diet or supplements change based on this?",
        "next_steps": "The combination of TIBC and transferrin saturation, together with ferritin, is used to distinguish true iron deficiency from anemia of chronic disease -- if the picture is unclear, your clinician may add a CRP or repeat testing after treating any suspected underlying condition."
    },
    "esr": {
        "questions": "Does this level fit with a specific condition I'm being evaluated for, or is it a nonspecific finding? Do I need more specific testing (like CRP or targeted autoimmune panels) to narrow things down? Should this be tracked over time?",
        "next_steps": "Because ESR is very nonspecific, an abnormal result usually prompts your clinician to correlate it with your symptoms and consider more specific tests depending on what's suspected -- it's often tracked serially rather than acted on from a single value."
    },
    "rheumatoid-factor": {
        "questions": "Does a positive result confirm rheumatoid arthritis, or do I need more specific testing (like anti-CCP)? Could this be positive for another reason unrelated to RA? How does my titer level affect the interpretation?",
        "next_steps": "A positive RF is usually interpreted alongside anti-CCP antibody testing and your clinical exam/imaging findings, since RF alone isn't specific enough to diagnose RA -- a rheumatology referral is typical if RA is suspected based on the full picture."
    },
    "ana": {
        "questions": "Given this titer and pattern, do I need more specific antibody testing (like the ENA panel or anti-dsDNA) to identify a specific condition? Could this be a positive result without me having an autoimmune disease?",
        "next_steps": "A positive ANA, especially at a significant titer, typically leads to reflex testing for more specific antibodies (anti-dsDNA, ENA panel) to help identify a specific condition -- a low-titer positive without symptoms is often not further pursued, since ANA can be positive in healthy people too."
    },
    "troponin": {
        "questions": "Is this trending up, down, or staying flat on repeat testing, since the pattern matters more than one number? Does this level fit with a heart attack, or could something else (like kidney disease) explain it? What's the next step in my evaluation?",
        "next_steps": "Troponin is virtually always interpreted through serial testing (a rise and/or fall pattern) rather than a single value, alongside your symptoms and ECG -- your care team will use an established rule-in/rule-out protocol to decide on further cardiac testing or treatment."
    },
    "bnp": {
        "questions": "Does this level support heart failure as the cause of my symptoms, or point toward another explanation? What's my baseline level for future comparison? Do I need an echocardiogram to complete the picture?",
        "next_steps": "An elevated result in someone with shortness of breath or swelling supports a heart failure diagnosis and often prompts an echocardiogram to assess heart function; in known heart failure patients, serial levels can help track treatment response, though trends matter more than any single value."
    },
    "ck-mb": {
        "questions": "How does this compare with my troponin result, since troponin is generally the more specific marker? Could recent muscle injury or exercise explain an elevated result?",
        "next_steps": "CK-MB is now mainly used alongside troponin (rather than instead of it) in specific situations, such as detecting a re-infarction shortly after a first heart attack, since troponin stays elevated for days and CK-MB's faster return to normal can help identify a new event."
    },
    "psa": {
        "questions": "Given my age and risk factors, is this level concerning enough to warrant a biopsy, or is monitoring reasonable? Would checking % free PSA help clarify the picture? Was this drawn before or after a prostate exam, since that can affect the result?",
        "next_steps": "A borderline result often leads to additional risk-refining tests (like % free PSA or a repeat PSA) before deciding on biopsy, while your urologist weighs the result together with your age, family history, and exam findings to recommend the best next step."
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
