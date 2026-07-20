"""
Seed script (batch 34) for MedForsa GCC's Lab Info reference library.
Adds core Toxicology tests: Ethanol, Acetaminophen, Salicylate,
Carboxyhemoglobin, Urine Drug Screen, and Lead (Blood).

Run once: python3 seed_lab_tests_batch34.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "ethanol-blood-alcohol", "name_en": "Ethanol, Blood (Blood Alcohol Level)",
        "aliases": "Blood Alcohol Concentration, BAC, Ethanol Level",
        "category": "Clinical Chemistry / Toxicology",
        "purpose_en": "Confirms and quantifies acute alcohol intoxication in the emergency or clinical setting, helps evaluate altered mental status, and is used for legal/forensic and workplace testing purposes.",
        "specimen_type": "Venous serum or plasma for clinical use; whole blood for forensic/legal specimens collected under chain-of-custody",
        "collection_notes_en": "The site must be cleaned with a non-alcohol-based antiseptic to avoid contaminating the sample. Serum/plasma levels run roughly 12-18% higher than whole blood levels for the same true blood alcohol concentration, which matters when comparing a clinical lab result to legal whole-blood limits.",
        "methodology_en": "Enzymatic (alcohol dehydrogenase) assay on automated chemistry analyzers, or headspace gas chromatography for forensic-grade specimens.",
        "reference_ranges": [
            {"parameter": "Ethanol", "population": "Non-drinking individual", "range": "Undetectable / <10 mg/dL"},
            {"parameter": "Ethanol", "population": "Legal driving limit (varies by jurisdiction)", "range": "commonly 50-80 mg/dL (0.05-0.08%) in many countries; Saudi Arabia prohibits alcohol consumption entirely"},
            {"parameter": "Ethanol", "population": "Significant clinical intoxication", "range": ">150-300 mg/dL, with marked impairment in most non-tolerant individuals"},
            {"parameter": "Ethanol", "population": "Potentially lethal (non-tolerant adult)", "range": ">400 mg/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The clinical effect of a given blood alcohol level varies considerably with an individual's tolerance -- a chronic heavy drinker may appear only mildly impaired at a level that would cause severe intoxication or respiratory depression in a naive drinker, so the level is interpreted alongside the clinical exam rather than in isolation. In the emergency setting, a level is often used to determine whether altered mental status is fully explained by alcohol or whether other causes (head injury, other intoxicants, metabolic derangement) need to be actively excluded, particularly if the exam doesn't improve as expected with clearance of alcohol over time.",
        "associated_conditions": [
            {"condition": "Acute alcohol intoxication", "direction": "elevated, correlating imprecisely with clinical impairment"},
            {"condition": "Altered mental status of uncertain cause", "direction": "used to determine how much of the presentation is explained by alcohol alone"}
        ],
        "questions_to_ask_en": "Does my level fully explain my symptoms, or are other causes being investigated as well? Is repeat monitoring planned to make sure my mental status is clearing as expected as the alcohol is metabolized?",
        "next_steps": "Management is primarily supportive (airway protection, monitoring, IV fluids as needed) with attention to co-ingestants and underlying causes of altered mental status; mental status that fails to improve as blood alcohol clears prompts further workup (imaging, other toxicology, metabolic panel) rather than being attributed to alcohol alone.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Alcohol Level", "url": "https://medlineplus.gov/ency/article/003611.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "acetaminophen-level", "name_en": "Acetaminophen (Paracetamol), Serum",
        "aliases": "Paracetamol Level, APAP Level, Tylenol Level",
        "category": "Clinical Chemistry / Toxicology",
        "purpose_en": "Evaluates suspected acetaminophen overdose (accidental or intentional) to predict the risk of hepatotoxicity and guide the need for N-acetylcysteine (NAC) antidote therapy, using the Rumack-Matthew nomogram.",
        "specimen_type": "Venous serum or plasma, drawn at a known, documented time after a single acute ingestion",
        "collection_notes_en": "The Rumack-Matthew nomogram is only valid starting 4 hours after a single, acute ingestion (to allow complete absorption) and does not apply to staggered/chronic supratherapeutic ingestion, which is assessed differently using total dose ingested, symptoms, and liver enzymes rather than the nomogram.",
        "methodology_en": "Enzymatic or immunoassay methods on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "Acetaminophen, therapeutic use", "population": "General", "range": "Undetectable to low single-digit mcg/mL, dose-dependent"},
            {"parameter": "Acetaminophen, possible hepatotoxicity risk (nomogram treatment line, US)", "population": "4 hours post-single acute ingestion", "range": "\u2265150 mcg/mL"},
            {"parameter": "Acetaminophen, high-risk ingestion", "population": "Above the '300-line' on the nomogram", "range": "significantly higher; may require an adjusted NAC regimen"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A level plotted on the Rumack-Matthew nomogram at or above the treatment line (150 mcg/mL at 4 hours in the commonly used US line, extrapolated forward in time) indicates a meaningful risk of hepatotoxicity and is an indication to start N-acetylcysteine, which is highly effective at preventing liver injury when started early but becomes progressively less effective the longer it is delayed after ingestion. The nomogram is not valid for chronic or staggered ingestions, ingestions of unknown timing, or extended-release formulations, all of which require a different assessment approach (empiric NAC, serial levels, and liver function monitoring) since a single timed level cannot be reliably interpreted in these scenarios.",
        "associated_conditions": [
            {"condition": "Acetaminophen-induced hepatotoxicity risk (acute overdose)", "direction": "level above the relevant nomogram treatment line"},
            {"condition": "Chronic/staggered overdose (nomogram not applicable)", "direction": "assessed by dose history, symptoms, and liver enzymes rather than a single level"}
        ],
        "questions_to_ask_en": "Is my ingestion timing well-established enough for the nomogram to apply, or will I be treated empirically instead? Will my liver function be monitored during and after treatment?",
        "next_steps": "A level above the treatment line, or any staggered/unclear-timing ingestion with a potentially toxic total dose, leads to N-acetylcysteine therapy along with monitoring of liver enzymes, INR, and renal function; a level below the treatment line at an appropriate post-ingestion time generally does not require antidote therapy.",
        "sources": [
            {"name": "Wikipedia - Rumack-Matthew Nomogram (overview and treatment lines)", "url": "https://en.wikipedia.org/wiki/Rumack%E2%80%93Matthew_nomogram", "accessed": "2026-07-20"},
            {"name": "Medscape/eMedicine - Acetaminophen Toxicity Workup", "url": "https://emedicine.medscape.com/article/820200-workup", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "salicylate-level", "name_en": "Salicylate, Serum",
        "aliases": "Aspirin Level, Salicylate Level, ASA Level",
        "category": "Clinical Chemistry / Toxicology",
        "purpose_en": "Evaluates suspected salicylate (aspirin) overdose or chronic salicylate toxicity, and monitors levels during high-dose aspirin therapy.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "A single level can underestimate severity in acute overdose because absorption can be delayed (enteric-coated tablets, bezoar formation), so serial levels every 2 hours until a clear downward trend is established are standard practice in significant ingestions, rather than relying on one result.",
        "methodology_en": "Colorimetric (Trinder) or enzymatic assay on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "Salicylate, therapeutic (anti-inflammatory dosing)", "population": "Adult", "range": "15-30 mg/dL"},
            {"parameter": "Salicylate, mild-moderate toxicity", "population": "Adult", "range": "30-50 mg/dL, with symptoms typically present"},
            {"parameter": "Salicylate, severe toxicity", "population": "Adult", "range": ">50-100 mg/dL, life-threatening"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Salicylate toxicity classically produces a mixed acid-base picture (early respiratory alkalosis from direct respiratory center stimulation, followed by an anion-gap metabolic acidosis), tinnitus, hyperthermia, and altered mental status, with severity correlating imperfectly with a single serum level -- clinical status, pH, and the trend of serial levels matter more than one absolute number, particularly in chronic toxicity where levels can be misleadingly lower than the degree of illness. Chronic salicylate toxicity (seen especially in elderly patients on long-term high-dose aspirin) is often more dangerous than it appears because of subtler presentation and can occur at lower serum levels than acute single-dose overdose.",
        "associated_conditions": [
            {"condition": "Acute salicylate overdose", "direction": "elevated, trending on serial measurement"},
            {"condition": "Chronic salicylate toxicity (often under-recognized, especially in elderly patients)", "direction": "may be only modestly elevated relative to severity of illness"}
        ],
        "questions_to_ask_en": "Since a single level can underestimate the severity of this kind of overdose, will levels be repeated to check the trend? Is urine alkalinization being considered to help my body eliminate the drug?",
        "next_steps": "Significant toxicity is managed with IV fluids, urinary alkalinization (sodium bicarbonate, which enhances renal elimination of salicylate) and, in severe cases, hemodialysis; serial levels and arterial blood gas monitoring guide the intensity and duration of treatment.",
        "sources": [
            {"name": "Medscape/eMedicine - Acetaminophen Toxicity Workup (context on co-ingestant salicylate testing)", "url": "https://emedicine.medscape.com/article/820200-workup", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "carboxyhemoglobin", "name_en": "Carboxyhemoglobin (Carbon Monoxide, Blood)",
        "aliases": "COHb, Carbon Monoxide Level, CO-Hemoglobin",
        "category": "Clinical Chemistry / Toxicology",
        "purpose_en": "Confirms and quantifies carbon monoxide poisoning in patients with suspected exposure (smoke inhalation, faulty heating/generators, industrial exposure) and guides the intensity of treatment, including the decision for hyperbaric oxygen.",
        "specimen_type": "Arterial or venous whole blood (venous is generally acceptable for this specific measurement, unlike most blood gas parameters)",
        "collection_notes_en": "Standard pulse oximetry cannot distinguish carboxyhemoglobin from oxyhemoglobin and will read falsely normal or near-normal oxygen saturation in CO poisoning; a co-oximeter (or laboratory blood gas analyzer with co-oximetry) is required to measure carboxyhemoglobin directly.",
        "methodology_en": "Co-oximetry, typically performed on the same blood gas analyzer used for arterial blood gas testing.",
        "reference_ranges": [
            {"parameter": "Carboxyhemoglobin", "population": "Non-smoker", "range": "<3%"},
            {"parameter": "Carboxyhemoglobin", "population": "Smoker", "range": "up to 10-15% depending on smoking intensity"},
            {"parameter": "Carboxyhemoglobin", "population": "Symptomatic poisoning (headache, nausea, confusion)", "range": "generally >20-25%"},
            {"parameter": "Carboxyhemoglobin", "population": "Severe/life-threatening poisoning", "range": ">40-50%, risk of coma, cardiac ischemia, death"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Carbon monoxide binds hemoglobin with roughly 200-250 times the affinity of oxygen, displacing oxygen delivery to tissues and causing symptoms that correlate imperfectly with the measured level -- a level obtained after the patient has already received supplemental oxygen (which accelerates CO elimination) may substantially underestimate the peak exposure, so the level is interpreted alongside symptoms, exposure history, and any loss of consciousness rather than in isolation. Delayed neurological sequelae (cognitive changes, parkinsonism-like symptoms) can occur days to weeks after apparent recovery from significant poisoning, which is part of why more severe exposures are treated aggressively even after the acute level has come down.",
        "associated_conditions": [
            {"condition": "Carbon monoxide poisoning (smoke inhalation, faulty heating, industrial exposure)", "direction": "elevated, though level alone doesn't fully predict severity or delayed sequelae"}
        ],
        "questions_to_ask_en": "Since this level may already be falling because of the oxygen I've been given, does it fully reflect how severe my exposure was? Am I a candidate for hyperbaric oxygen therapy, and what does that involve?",
        "next_steps": "Confirmed poisoning is treated with high-flow 100% oxygen (which accelerates CO elimination compared to room air) and, for severe exposures (very high levels, loss of consciousness, pregnancy, cardiac ischemia, or neurological symptoms), hyperbaric oxygen therapy is considered to reduce the risk of delayed neurological sequelae.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Carboxyhemoglobin", "url": "https://medlineplus.gov/ency/article/003643.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "urine-drug-screen", "name_en": "Urine Drug Screen (Multi-Panel Toxicology)",
        "aliases": "UDS, Urine Toxicology Screen, Drug of Abuse Panel",
        "category": "Clinical Chemistry / Toxicology",
        "purpose_en": "Screens for recent use of common drugs of abuse in the emergency, clinical, workplace, forensic, or substance-use-treatment setting; commonly panels include opiates, cocaine metabolite, amphetamines/methamphetamine, cannabinoids (THC), benzodiazepines, barbiturates, and PCP, with panel composition varying by protocol.",
        "specimen_type": "Random urine specimen; observed collection with chain-of-custody documentation is required for forensic/legal or employment testing",
        "collection_notes_en": "Immunoassay screens are prone to both false positives (cross-reactivity with certain prescription or over-the-counter medications, e.g. some cold medications causing false-positive amphetamine results, poppy seeds causing false-positive opiate results) and false negatives (many synthetic opioids like fentanyl and newer synthetic drugs are not detected by standard opiate immunoassays and require specific separate testing).",
        "methodology_en": "Immunoassay screening (point-of-care or laboratory-based), with presumptive positive results generally confirmed by gas chromatography-mass spectrometry (GC-MS) or liquid chromatography-tandem mass spectrometry (LC-MS/MS) when the result has clinical, legal, or employment consequences.",
        "reference_ranges": [{"parameter": "Result categories", "population": "Per substance tested", "range": "Negative or Presumptive Positive (screening); confirmatory testing required for a legally or clinically definitive positive result"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A screening immunoassay result indicates presumptive, not definitive, presence of a substance class and reflects recent use over a variable detection window (hours for some substances to weeks for chronic heavy cannabis use), not impairment at the time of testing or the exact substance/dose used -- interpretation requires knowing which specific panel was run and its known cross-reactivities. Because standard opiate immunoassays often do not detect synthetic opioids (fentanyl, and many novel psychoactive substances), a negative standard panel does not rule out these exposures in a clinical toxicology context, and specific fentanyl testing or broader confirmatory panels should be requested when suspicion is high despite a negative screen.",
        "associated_conditions": [
            {"condition": "Recent use of screened substance class (presumptive)", "direction": "positive screen, pending confirmation if clinically or legally significant"},
            {"condition": "Fentanyl/novel synthetic opioid exposure (often missed by standard opiate panels)", "direction": "requires specific testing beyond the standard panel"}
        ],
        "questions_to_ask_en": "Which specific substances were included in this panel, and were any results confirmed with a more specific method? Could a medication I'm taking explain a positive result on this screen?",
        "next_steps": "A presumptive positive result with clinical, legal, or employment implications should be sent for confirmatory testing (GC-MS or LC-MS/MS) before being acted upon as definitive; in the acute clinical setting, management is guided primarily by the patient's symptoms and vital signs rather than waiting for a screen result.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Drug Screen (Comprehensive)", "url": "https://medlineplus.gov/ency/article/003578.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "lead-blood", "name_en": "Lead, Blood",
        "aliases": "Blood Lead Level, BLL, Lead Level",
        "category": "Clinical Chemistry / Toxicology",
        "purpose_en": "Screens for and quantifies lead exposure, particularly in young children (developmental risk) and in adults with occupational or environmental exposure (battery manufacturing, smelting, some traditional cosmetics/remedies, renovation of older housing with lead paint).",
        "specimen_type": "Venous whole blood (EDTA); capillary (finger-stick) samples may be used for initial screening but a positive capillary result should be confirmed with a venous sample",
        "collection_notes_en": "Strict attention to lead-free collection technique is required, since skin contamination or inadequately cleaned equipment can falsely elevate capillary results; venous confirmation of any elevated capillary result is standard practice.",
        "methodology_en": "Graphite furnace atomic absorption spectrometry or inductively coupled plasma mass spectrometry (ICP-MS).",
        "reference_ranges": [
            {"parameter": "Blood lead reference value (CDC, children 1-5 years, 97.5th percentile)", "population": "Children", "range": "\u22653.5 \u00b5g/dL identifies levels higher than most children's"},
            {"parameter": "Occupational threshold prompting workplace investigation (OSHA, general industry)", "population": "Adult, occupational", "range": "\u226525 \u00b5g/dL considered actionable"},
            {"parameter": "Medical removal threshold (occupational, various guidelines)", "population": "Adult, occupational", "range": ">30 \u00b5g/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "There is no known safe threshold for lead exposure in children, since even low-level exposure has been associated with measurable, largely irreversible effects on cognitive development and behavior; the CDC's blood lead reference value (lowered to 3.5 \u00b5g/dL in 2021) is used to identify children in the top 2.5% of exposure for prompt investigation of the source and follow-up, not as a 'safe' cutoff. In adults, lead toxicity affects the hematologic (microcytic anemia, basophilic stippling), neurologic (peripheral neuropathy, encephalopathy at high levels), renal, and reproductive systems, with occupational exposure being the dominant cause; regulatory action levels exist to trigger workplace exposure controls and, at higher levels, medical removal from the lead-exposed task.",
        "associated_conditions": [
            {"condition": "Childhood lead exposure (developmental/cognitive risk, no safe threshold)", "direction": "any detectable elevation above reference value prompts evaluation"},
            {"condition": "Occupational or environmental lead poisoning in adults (anemia, neuropathy, encephalopathy at high levels)", "direction": "elevated, severity correlating with level and duration of exposure"}
        ],
        "questions_to_ask_en": "What is the likely source of this exposure, and how can it be reduced or eliminated? For a child, what follow-up testing and developmental monitoring is recommended at this level?",
        "next_steps": "Any confirmed elevation in a child prompts investigation of the exposure source (commonly old paint, contaminated soil, or certain imported products) and periodic repeat testing; higher levels in children or adults may warrant chelation therapy per current guidelines, always alongside source identification and removal, since chelation without addressing ongoing exposure has limited benefit.",
        "sources": [
            {"name": "CDC - Blood Lead Reference Value Update", "url": "https://www.cdc.gov/lead-prevention/php/news-features/updates-blood-lead-reference-value.html", "accessed": "2026-07-20"},
            {"name": "CDC/NIOSH - Blood Lead Level Guidance for Adults", "url": "https://www.cdc.gov/niosh/lead/bll-reference/index.html", "accessed": "2026-07-20"}
        ]
    }
]

RELATED = {
    "ethanol-blood-alcohol": ["osmolality-serum", "urine-drug-screen"],
    "acetaminophen-level": ["alt-ast", "total-bilirubin", "prothrombin-time-inr"],
    "salicylate-level": ["arterial-blood-gas", "bicarbonate-co2-total-carbon-dioxide"],
    "carboxyhemoglobin": ["arterial-blood-gas", "lactate-blood"],
    "urine-drug-screen": ["ethanol-blood-alcohol"],
    "lead-blood": ["complete-blood-count", "zinc-serum"],
}

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
             questions_to_ask_en, next_steps_en,
             associated_conditions_json, related_tests_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("questions_to_ask_en"), t.get("next_steps"),
             json.dumps(t.get("associated_conditions", [])),
             json.dumps(RELATED.get(t["slug"], [])),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
