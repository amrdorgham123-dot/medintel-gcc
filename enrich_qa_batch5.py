"""
Enrichment batch 5: adds questions_to_ask_en + next_steps_en to 20 more
existing Lab Info tests (microbiology, ABG/ammonia/lactate, reproductive
hormones, infectious disease serology).

Run once: python3 enrich_qa_batch5.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "blood-culture": {
        "questions": "Did the organism grow in more than one bottle, since that affects whether it's a true infection or contamination? What antibiotic is this organism sensitive to? How long will I need treatment?",
        "next_steps": "A confirmed true positive guides antibiotic selection based on susceptibility results, with treatment duration depending on the source and organism; a likely contaminant usually needs no treatment, though your clinician will weigh this against your clinical picture."
    },
    "urine-culture": {
        "questions": "Does this colony count and organism confirm a urinary tract infection, or could this be contamination/colonization? What antibiotic is this organism sensitive to? Do I need this repeated after treatment to confirm it's cleared?",
        "next_steps": "A significant single-organism growth with compatible symptoms confirms UTI and guides antibiotic selection based on susceptibility results; growth without symptoms (asymptomatic bacteriuria) generally doesn't need treatment except in specific situations like pregnancy."
    },
    "h-pylori-testing": {
        "questions": "Was I off proton pump inhibitors and antibiotics long enough before this test for an accurate result? Do I need treatment, and if so, for how long? Should I be retested after treatment to confirm it's cleared?",
        "next_steps": "A positive result generally leads to a course of combination antibiotic therapy, and confirmation of eradication (via a repeat stool antigen or breath test, not serology) is recommended afterward, especially if you had an ulcer or ongoing symptoms."
    },
    "gram-stain": {
        "questions": "What does this preliminary result suggest, and how is it guiding my antibiotic treatment while we wait for the full culture? Will the antibiotics be adjusted once the final culture and sensitivity results come back?",
        "next_steps": "This result guides an initial (empiric) antibiotic choice while the full culture and susceptibility testing are still pending (typically 24-72 hours); treatment is often adjusted once those more definitive results are available."
    },
    "abg": {
        "questions": "What is the underlying cause of this acid-base pattern, and how urgently does it need to be addressed? Do I need this repeated to track whether treatment is working? Is my oxygen level adequate?",
        "next_steps": "Results guide immediate management of the underlying respiratory or metabolic problem, and repeat testing is common to track response to treatment, especially in a hospital or emergency setting."
    },
    "ammonia": {
        "questions": "Was this sample collected and handled correctly, since that affects accuracy? Does this explain any confusion or altered mental status I've had? What's being done to lower this level?",
        "next_steps": "An elevated result in someone with liver disease and altered mental status typically prompts treatment aimed at lowering ammonia (such as lactulose) and investigation for triggers of hepatic encephalopathy; in infants/children, urgent metabolic workup may be needed."
    },
    "lactate": {
        "questions": "Does this level indicate how sick I am right now? Is this trending down with treatment, which would be a good sign? What's causing this elevation?",
        "next_steps": "An elevated level, especially in the context of suspected sepsis or shock, prompts aggressive treatment and fluid resuscitation, with serial measurements used to track whether treatment is working (a falling lactate is a reassuring sign)."
    },
    "microalbumin": {
        "questions": "Does this mean my diabetes or blood pressure is affecting my kidneys? Do I need my medications adjusted (like starting an ACE inhibitor or ARB)? How often should this be rechecked?",
        "next_steps": "A confirmed elevated result (on repeat testing) typically prompts starting or intensifying blood pressure medications that also protect the kidneys (ACE inhibitors or ARBs), along with tighter blood sugar control if you have diabetes, and regular monitoring going forward."
    },
    "lh": {
        "questions": "Does this fit with where I am in my cycle, or does it suggest an issue with ovulation or menopause? Should this be checked alongside FSH and estradiol for a clearer picture? What does this mean for my fertility?",
        "next_steps": "Results are interpreted together with FSH, estradiol, and your cycle timing to assess ovarian function; unexpected results may prompt additional hormone testing or a fertility specialist referral depending on your goals and symptoms."
    },
    "fsh": {
        "questions": "Does this suggest reduced ovarian reserve, or is this within a normal range for my age? Should this affect my fertility treatment timeline? Do I need this combined with an antral follicle count for a fuller picture?",
        "next_steps": "An elevated result, especially with fertility concerns, often leads to further ovarian reserve testing (AMH, antral follicle count) and a conversation with a fertility specialist about your options and timeline."
    },
    "estradiol": {
        "questions": "Does this fit with my cycle day or menopausal status? If I'm undergoing fertility treatment, is my ovarian response on track? Could this be pointing to another cause I should be worried about?",
        "next_steps": "In fertility treatment, results guide adjustments to your stimulation medication dosing. Outside of that context, an unexpected result prompts correlation with LH/FSH and, if persistently abnormal without a clear reason, further evaluation for a hormone-producing source."
    },
    "progesterone": {
        "questions": "Does this confirm that I ovulated this cycle? If I'm pregnant, does this level raise any concern about the pregnancy's viability? Do I need this repeated or combined with other tests (like hCG)?",
        "next_steps": "A result consistent with ovulation is reassuring; a low result at the expected time may prompt further fertility evaluation. In early pregnancy, a low level is usually interpreted alongside serial hCG and ultrasound rather than acted on alone."
    },
    "anti-hcv": {
        "questions": "Does this mean I currently have hepatitis C, or could this be a past resolved infection? Do I need an HCV RNA test to clarify? If I have active infection, what treatment options are available?",
        "next_steps": "A reactive antibody result is followed by HCV RNA testing to determine whether the infection is currently active; if active, you'll be referred for antiviral treatment, which is highly effective at curing hepatitis C in most cases."
    },
    "syphilis-screening": {
        "questions": "Do both parts of this test agree, or is there a discordant result that needs explaining? Does this represent an active infection needing treatment, or a past treated infection? Do my partners need to be tested?",
        "next_steps": "A confirmed positive result leads to staging (determining how long the infection has likely been present) and antibiotic treatment, with partner notification and testing recommended; declining RPR titers after treatment confirm response."
    },
    "rubella-igg": {
        "questions": "Am I immune, or do I need vaccination? If I'm currently pregnant and not immune, what precautions should I take, and when can I get vaccinated? Do I need this rechecked before a future pregnancy?",
        "next_steps": "A non-immune result outside of pregnancy leads to vaccination; during pregnancy, vaccination is deferred until after delivery since it's a live vaccine, and precautions against exposure are discussed in the meantime."
    },
    "prealbumin": {
        "questions": "Does this reflect true malnutrition, or could recent illness/inflammation be lowering it? Is my nutritional support plan working, based on the trend? Should this be rechecked soon to track progress?",
        "next_steps": "A low result often prompts nutritional assessment and support planning, with serial testing used to track response over days to weeks given how quickly this marker changes compared to albumin."
    },
    "transferrin": {
        "questions": "Does this fit with iron deficiency, or could this reflect a nutritional or liver issue instead? Should this be interpreted alongside my ferritin and iron results? Do I need further testing to clarify the cause?",
        "next_steps": "Results are interpreted together with ferritin, serum iron, and clinical context to distinguish iron deficiency from other causes (malnutrition, liver disease, chronic inflammation) before deciding on treatment."
    },
    "dhea-s": {
        "questions": "Does this point to an adrenal or ovarian source for my symptoms (like excess hair growth)? Given how elevated this is, do I need imaging to rule out a tumor? Do I need additional hormone testing?",
        "next_steps": "Mild elevation is often managed as part of a broader hyperandrogenism workup (often PCOS-related). Markedly elevated results prompt adrenal imaging to rule out a tumor, given the strong association between very high levels and adrenal masses."
    },
    "ceruloplasmin": {
        "questions": "Does this support or rule out Wilson disease as the cause of my symptoms? Do I need additional testing (like a slit-lamp eye exam or urine copper) to confirm? Could something else explain a low result?",
        "next_steps": "A low result in someone with unexplained liver or neurological symptoms typically leads to further Wilson disease workup (slit-lamp exam for Kayser-Fleischer rings, 24-hour urine copper, possibly genetic testing) before treatment decisions are made."
    },
    "17-ohp": {
        "questions": "Does this confirm congenital adrenal hyperplasia, or do I need a stimulation test to be sure? Does this affect my fertility or menstrual symptoms? Do family members need screening?",
        "next_steps": "A markedly elevated result supports the diagnosis, while a borderline result often leads to an ACTH stimulation test for confirmation, followed by endocrinology referral to discuss management, especially for non-classic forms presenting in adulthood."
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
