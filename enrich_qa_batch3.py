"""
Enrichment batch 3: adds questions_to_ask_en + next_steps_en to 10 more
existing Lab Info tests (tumor markers, pancreatic enzymes, blood donor
screening, pregnancy, urinalysis).

Run once: python3 enrich_qa_batch3.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

ENRICHMENT = {
    "afp": {
        "questions": "If I have known liver disease, is this rise expected or a warning sign of cancer? Do I need imaging to look for a liver tumor? If this was done during pregnancy, does it need to be repeated or combined with other screening tests?",
        "next_steps": "In liver disease patients, a rising AFP typically prompts liver imaging to look for hepatocellular carcinoma. In pregnancy, an abnormal result is usually interpreted alongside other screening markers and ultrasound findings, with dating accuracy checked first since that significantly affects interpretation."
    },
    "cea": {
        "questions": "Was my baseline level known before treatment, so this can be compared properly? Does a rising trend mean my cancer has come back or progressed? Could smoking or another benign condition explain this result?",
        "next_steps": "CEA is most useful when tracked over time against your own baseline -- a rising trend after treatment for colorectal cancer typically prompts imaging to look for recurrence, while a single elevated value without a prior baseline is interpreted more cautiously given its many non-cancer causes."
    },
    "ca-125": {
        "questions": "Given my age and menopausal status, does this result need pelvic imaging or further workup? Could a benign condition (like endometriosis or fibroids) explain this? If I have known ovarian cancer, does this reflect treatment response?",
        "next_steps": "An elevated result in a postmenopausal woman, or with a pelvic mass on exam, typically prompts pelvic ultrasound and possibly gynecologic oncology referral. In someone already diagnosed with ovarian cancer, serial CA-125 is used to help track treatment response and watch for recurrence."
    },
    "ca19-9": {
        "questions": "Do I need imaging (like a CT scan) to look for a pancreatic or biliary problem? Could bile duct blockage from a non-cancer cause explain this? If I have known pancreatic cancer, does this reflect how treatment is working?",
        "next_steps": "An elevated result often prompts abdominal imaging to look for a pancreatic or biliary mass, especially with compatible symptoms (weight loss, jaundice, abdominal pain). In diagnosed pancreatic cancer, serial levels help track treatment response and watch for recurrence."
    },
    "ca15-3": {
        "questions": "If I have a history of breast cancer, does this suggest recurrence, or could it be a false alarm? Do I need imaging to confirm? How does this compare to my previous levels?",
        "next_steps": "In someone with a breast cancer history, a rising CA 15-3 typically prompts imaging to look for recurrence or metastasis; it's not used as a general screening test for breast cancer in people without a prior diagnosis, since it lacks the sensitivity and specificity needed for that purpose."
    },
    "blood-donor-tti-screening": {
        "questions": "If any test came back reactive, what confirmatory testing is being done next? Does a reactive result definitely mean I have an infection, or could it be a false positive? Will I be notified and counseled regardless of the result?",
        "next_steps": "Any reactive screening result triggers confirmatory testing before a diagnosis is communicated, and donors with confirmed reactive results are notified, counseled, and typically deferred from future donation per blood bank protocol, with referral for appropriate follow-up care."
    },
    "amylase": {
        "questions": "Does this level, together with my symptoms, support a diagnosis of pancreatitis? Do I need a lipase test too, since it's often more specific? Could a non-pancreatic cause (like salivary gland issues) explain this?",
        "next_steps": "In suspected acute pancreatitis, amylase is typically interpreted alongside lipase (which is more specific and stays elevated longer) and imaging; a markedly elevated result with compatible abdominal pain supports the diagnosis, while a mildly elevated result without typical symptoms may not need urgent action."
    },
    "lipase": {
        "questions": "Does this confirm pancreatitis, and how severe does it look based on this level plus my symptoms? Do I need imaging (like a CT or ultrasound) to look for a cause (gallstones, etc.)? How will this be monitored going forward?",
        "next_steps": "A markedly elevated lipase with compatible symptoms generally confirms acute pancreatitis and prompts imaging to identify the cause (commonly gallstones or alcohol) and assess severity, guiding hospital management and monitoring."
    },
    "beta-hcg": {
        "questions": "Is this level appropriate for how many weeks pregnant I am thought to be? Do I need a repeat test in 48 hours to check the trend? If this isn't a pregnancy-related test, what does an elevated result mean for me?",
        "next_steps": "In early pregnancy, results are often followed with a repeat test 48 hours later to check that the level is rising appropriately, which helps distinguish a normal early pregnancy from a possible miscarriage or ectopic pregnancy -- ultrasound is added once levels reach the range where a pregnancy should be visible."
    },
    "urinalysis": {
        "questions": "Does this suggest a urinary tract infection, kidney issue, or something else? Do I need a urine culture to confirm and guide antibiotic choice if infection is suspected? Should this be repeated after treatment to confirm resolution?",
        "next_steps": "Findings suggestive of infection (positive leukocyte esterase/nitrite, elevated white cells) typically lead to a urine culture to confirm and guide antibiotic selection. Findings suggestive of kidney involvement (protein, blood, abnormal casts) typically prompt further kidney function testing and possible referral."
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
