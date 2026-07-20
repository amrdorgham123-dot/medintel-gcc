"""
Seed script (batch 33) for MedForsa GCC's Lab Info reference library.
Adds core Therapeutic Drug Monitoring (TDM) tests: Vancomycin, Phenytoin,
Valproic Acid, Carbamazepine, Tacrolimus, Cyclosporine, Gentamicin,
Theophylline, and Methotrexate levels.

Run once: python3 seed_lab_tests_batch33.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "vancomycin-level", "name_en": "Vancomycin, Serum/Plasma (Therapeutic Drug Monitoring)",
        "aliases": "Vancomycin Trough, Vancomycin Level, TDM Vancomycin",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of IV vancomycin in patients being treated for serious gram-positive infections (including MRSA), balancing adequate antibacterial exposure against the risk of nephrotoxicity.",
        "specimen_type": "Venous serum or plasma (trough, drawn 0-1 hour before the next dose at steady state, usually before the 4th dose)",
        "collection_notes_en": "Trough sampling timing relative to the dose is critical to interpretation; many centers are shifting to AUC-guided dosing (24-hour area under the curve divided by minimum inhibitory concentration, target AUC/MIC 400-600) rather than trough alone, per 2020 consensus guidelines, which requires two timed levels rather than a single trough.",
        "methodology_en": "Immunoassay (e.g., particle-enhanced turbidimetric inhibition immunoassay or chemiluminescent microparticle immunoassay) on automated chemistry/immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Trough (standard target, most infections)", "population": "Adult", "range": "10-15 mcg/mL"},
            {"parameter": "Trough (target for MIC \u22651, complicated infections e.g. endocarditis, osteomyelitis, meningitis)", "population": "Adult", "range": "15-20 mcg/mL"},
            {"parameter": "Peak (rarely used for dosing decisions)", "population": "Adult", "range": "20-40 mcg/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Troughs below about 10 mcg/mL are associated with inadequate therapy and a higher risk of selecting for resistant organisms, while troughs at or above roughly 15-20 mcg/mL (or an AUC/MIC below the 400-600 target) are associated with a materially higher risk of vancomycin-induced nephrotoxicity, especially with concurrent nephrotoxins such as aminoglycosides or prolonged courses. Because trough concentration correlates imperfectly with total drug exposure (AUC), many hospital pharmacies now use AUC-guided (Bayesian) dosing software with two timed levels per course, reserving trough-only monitoring for simpler regimens or where AUC software is unavailable.",
        "associated_conditions": [
            {"condition": "Subtherapeutic exposure / risk of treatment failure or resistance", "direction": "trough or AUC below target"},
            {"condition": "Vancomycin-induced nephrotoxicity risk", "direction": "trough >15-20 mcg/mL or AUC/MIC persistently >600, especially with other nephrotoxins"}
        ],
        "questions_to_ask_en": "Is my current dose achieving the AUC/MIC target, or only a trough target? How is my kidney function being monitored while on this drug, and how often will levels be rechecked?",
        "next_steps": "Levels outside target prompt a dose or interval adjustment by the treating team or clinical pharmacist, with a repeat level after the new dose reaches steady state (typically after 3-5 doses, sooner in renal impairment); renal function (creatinine, BUN) is monitored in parallel throughout therapy.",
        "sources": [
            {"name": "Medscape/eMedicine - Vancomycin Level: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2090484-overview", "accessed": "2026-07-20"},
            {"name": "PMC - Evaluation of Therapeutic Vancomycin Monitoring (AUC/MIC vs trough)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "phenytoin-level", "name_en": "Phenytoin, Total and Free, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Phenytoin Level, Dilantin Level, TDM Phenytoin",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of phenytoin in patients treated for seizure disorders, confirms adherence, and investigates suspected toxicity or breakthrough seizures.",
        "specimen_type": "Venous serum or plasma (trough, just before the next dose)",
        "collection_notes_en": "Total phenytoin is affected by protein binding; free (unbound) phenytoin should be measured directly in patients with hypoalbuminemia, renal failure, pregnancy, or concurrent highly protein-bound drugs (e.g., valproic acid) since total levels can be misleading in these situations.",
        "methodology_en": "Immunoassay on automated analyzers, or HPLC for free-fraction measurement after ultrafiltration.",
        "reference_ranges": [
            {"parameter": "Total phenytoin", "population": "Adult, steady state", "range": "10-20 mcg/mL"},
            {"parameter": "Free phenytoin", "population": "Adult, steady state", "range": "1.0-2.0 mcg/mL (8-14% of total)"},
            {"parameter": "Total phenytoin, toxic", "population": "Adult", "range": ">30 mcg/mL associated with clinical toxicity"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Levels below 10 mcg/mL are frequently associated with inadequate seizure control, while levels above 20 mcg/mL (total) increasingly carry a risk of dose-related toxicity, classically nystagmus, ataxia, and sedation at higher levels, progressing to encephalopathy at very high concentrations. Because phenytoin follows non-linear (zero-order, saturable) kinetics near the therapeutic range, small dose increases can cause disproportionately large rises in serum level, which is why frequent monitoring is used during dose titration.",
        "associated_conditions": [
            {"condition": "Subtherapeutic phenytoin (breakthrough seizures, non-adherence)", "direction": "low"},
            {"condition": "Phenytoin toxicity (nystagmus, ataxia, sedation, encephalopathy at extreme levels)", "direction": "high, especially free fraction"}
        ],
        "questions_to_ask_en": "Should my free phenytoin level be checked given my albumin/kidney function, rather than relying on the total level alone? Could an interacting drug (like valproic acid) be affecting this result?",
        "next_steps": "Dose adjustments are typically small given the non-linear kinetics near the therapeutic range, with a repeat level after roughly 1-2 weeks (steady state) to confirm the new dose is appropriate; free-level testing is pursued when the clinical picture and total level disagree.",
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Phenytoin", "url": "https://www.ncbi.nlm.nih.gov/books/NBK551520/", "accessed": "2026-07-20"},
            {"name": "Mayo Clinic Laboratories Therapeutics Catalog - Phenytoin, Total and Free, Serum", "url": "https://therapeutics.testcatalog.org/show/PNTFT", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "valproic-acid-level", "name_en": "Valproic Acid, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Valproate Level, VPA Level, Depakote Level",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of valproic acid used for seizure disorders, bipolar disorder, and migraine prophylaxis, and investigates suspected toxicity, non-adherence, or breakthrough symptoms.",
        "specimen_type": "Venous serum or plasma (trough, just before the next dose)",
        "collection_notes_en": "Free (unbound) valproic acid is preferred over total level in hypoalbuminemia, renal failure, pregnancy, or with interacting highly protein-bound drugs (e.g., phenytoin, aspirin), since valproic acid is heavily protein bound (~90%) and its free fraction rises disproportionately as albumin falls.",
        "methodology_en": "Immunoassay on automated analyzers.",
        "reference_ranges": [
            {"parameter": "Total valproic acid", "population": "Adult, steady state", "range": "50-100 mcg/mL"},
            {"parameter": "Free valproic acid", "population": "Adult, steady state", "range": "2.5-20 mcg/mL (unbound fraction rises with hypoalbuminemia)"},
            {"parameter": "Total valproic acid, toxic", "population": "Adult", "range": ">100-150 mcg/mL associated with toxicity"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Subtherapeutic levels are associated with inadequate seizure or mood control, while levels above roughly 100-150 mcg/mL are increasingly associated with sedation, tremor, thrombocytopenia, hyperammonemic encephalopathy, and (rarely) fatal hepatotoxicity or pancreatitis; the drug also carries significant teratogenic risk, so it is generally avoided in women of childbearing potential when alternatives exist. Because total level can be misleading when albumin is low, the free fraction is the more reliable indicator of drug exposure in critically ill, elderly, pregnant, or hypoalbuminemic patients.",
        "associated_conditions": [
            {"condition": "Subtherapeutic valproic acid (breakthrough seizures/mood symptoms, non-adherence)", "direction": "low"},
            {"condition": "Valproic acid toxicity (sedation, tremor, thrombocytopenia, hyperammonemia, hepatotoxicity)", "direction": "high, especially free fraction"}
        ],
        "questions_to_ask_en": "Given my albumin level, should the free valproic acid level be checked instead of relying on total? Should my liver enzymes, platelet count, and ammonia be monitored alongside this?",
        "next_steps": "Confirmed subtherapeutic or toxic levels lead to dose adjustment with a repeat level once steady state is reached (about 3-4 days); periodic liver function tests, platelet counts, and ammonia are typically monitored alongside long-term therapy.",
        "sources": [
            {"name": "PMC - TDM of Phenytoin and Valproic Acid in Critically Ill Patients", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9350491/", "accessed": "2026-07-20"},
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "carbamazepine-level", "name_en": "Carbamazepine, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Carbamazepine Level, Tegretol Level, TDM Carbamazepine",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of carbamazepine used for seizure disorders, trigeminal neuralgia, and bipolar disorder, confirms adherence, and investigates suspected toxicity.",
        "specimen_type": "Venous serum or plasma (trough, just before the next dose)",
        "collection_notes_en": "Carbamazepine induces its own hepatic metabolism (autoinduction) over the first several weeks of therapy, so levels typically fall after initial dosing and require re-checking once autoinduction is complete (usually 2-4 weeks).",
        "methodology_en": "Immunoassay on automated analyzers.",
        "reference_ranges": [
            {"parameter": "Carbamazepine, trough", "population": "Adult, steady state", "range": "4-12 mcg/mL"},
            {"parameter": "Carbamazepine, toxic", "population": "Adult", "range": ">15 mcg/mL associated with toxicity in most patients"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Levels below 4 mcg/mL are often associated with inadequate seizure control, while levels above roughly 12-15 mcg/mL are increasingly associated with dose-related toxicity: diplopia, ataxia, dizziness, and sedation, progressing to more severe neurotoxicity at higher levels. Carbamazepine also carries idiosyncratic risks unrelated to serum level, including hyponatremia (SIADH-like effect), agranulocytosis/aplastic anemia, and severe cutaneous reactions (Stevens-Johnson syndrome/toxic epidermal necrolysis), the last of which is strongly linked to the HLA-B*15:02 allele in patients of Southeast and East Asian ancestry, for whom genetic screening is recommended before starting the drug.",
        "associated_conditions": [
            {"condition": "Subtherapeutic carbamazepine (breakthrough seizures, autoinduction-related fall in level)", "direction": "low"},
            {"condition": "Carbamazepine toxicity (diplopia, ataxia, sedation)", "direction": "high"},
            {"condition": "Idiosyncratic reactions (hyponatremia, blood dyscrasias, severe skin reactions)", "direction": "not level-dependent; monitored separately"}
        ],
        "questions_to_ask_en": "Since this drug can lower its own level over time through autoinduction, when should this be rechecked after starting or changing my dose? Do I need HLA-B*15:02 screening or monitoring of my sodium and blood counts?",
        "next_steps": "A subtherapeutic level in the first weeks of treatment is often expected due to autoinduction and re-checked after 2-4 weeks; sodium, complete blood count, and liver enzymes are typically monitored periodically during long-term therapy independent of the drug level itself.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"},
            {"name": "GGC Medicines - Therapeutic Drug Monitoring Target Concentration Ranges", "url": "https://handbook.ggcmedicines.org.uk/guidelines/appendices/appendix-3-therapeutic-drug-monitoring-target-concentration-ranges/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "tacrolimus-level", "name_en": "Tacrolimus, Whole Blood (Therapeutic Drug Monitoring)",
        "aliases": "Tacrolimus Trough, FK506 Level, TDM Tacrolimus",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of tacrolimus, a calcineurin-inhibitor immunosuppressant used after solid organ transplantation, balancing prevention of graft rejection against nephrotoxicity and infection risk.",
        "specimen_type": "Whole blood (EDTA), trough, drawn immediately before the next dose",
        "collection_notes_en": "Target trough ranges differ substantially by transplanted organ, time since transplant, and concurrent immunosuppressants, so results must be interpreted against the specific center's protocol rather than a single universal range; generic-to-brand or between-generic switches can also meaningfully change levels.",
        "methodology_en": "Chemiluminescent microparticle immunoassay (CMIA) or liquid chromatography-tandem mass spectrometry (LC-MS/MS, the more specific reference method).",
        "reference_ranges": [
            {"parameter": "Trough, early post-transplant (first 1-3 months, varies by organ/protocol)", "population": "Adult", "range": "commonly 8-15 ng/mL"},
            {"parameter": "Trough, maintenance phase (varies by organ/protocol)", "population": "Adult", "range": "commonly 5-10 ng/mL, sometimes lower with combination therapy"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Subtherapeutic tacrolimus increases the risk of acute or chronic graft rejection, while excessive levels increase the risk of nephrotoxicity, neurotoxicity (tremor, headache, posterior reversible encephalopathy syndrome in severe cases), new-onset diabetes after transplant, and opportunistic infection from over-immunosuppression. Because the therapeutic window is narrow and levels are affected by numerous drug interactions (notably CYP3A4 inhibitors like azole antifungals and inducers like rifampin) and by food (grapefruit), close, protocol-driven trough monitoring is standard throughout the life of the transplant.",
        "associated_conditions": [
            {"condition": "Acute or chronic graft rejection risk", "direction": "trough below target range"},
            {"condition": "Tacrolimus toxicity (nephrotoxicity, tremor, new-onset diabetes, opportunistic infection)", "direction": "trough above target range"}
        ],
        "questions_to_ask_en": "What is my specific target trough range at this point post-transplant? Could a medication I recently started or stopped be interacting with this drug and affecting my level?",
        "next_steps": "Levels outside the center's target range prompt a dose adjustment by the transplant team, with a repeat trough after steady state (roughly 2-3 days given the drug's half-life), alongside monitoring of kidney function, glucose, and, when relevant, a biopsy if rejection is suspected despite adequate levels.",
        "sources": [
            {"name": "PMC - Identification of Critical Values in Therapeutic Drug Monitoring (tacrolimus trough context)", "url": "https://www.nature.com/articles/s41598-024-62402-7", "accessed": "2026-07-20"},
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "cyclosporine-level", "name_en": "Cyclosporine, Whole Blood (Therapeutic Drug Monitoring)",
        "aliases": "Cyclosporine Trough, Ciclosporin Level, TDM Cyclosporine",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of cyclosporine, a calcineurin-inhibitor immunosuppressant used after solid organ or bone marrow transplantation and in some autoimmune conditions, balancing efficacy against nephrotoxicity.",
        "specimen_type": "Whole blood (EDTA), trough (C0) or 2-hour post-dose (C2) depending on protocol",
        "collection_notes_en": "Some transplant centers use C2 (2-hour post-dose) monitoring rather than trough, since it correlates better with total drug exposure (AUC) for cyclosporine specifically; sample timing must match the protocol being used for the result to be interpretable.",
        "methodology_en": "Chemiluminescent microparticle immunoassay (CMIA) or LC-MS/MS (reference method).",
        "reference_ranges": [
            {"parameter": "Trough (C0), varies by organ/protocol and time post-transplant", "population": "Adult", "range": "commonly 100-400 ng/mL depending on phase of treatment"},
            {"parameter": "2-hour post-dose (C2), where used", "population": "Adult", "range": "protocol-specific, generally higher than trough targets"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "As with tacrolimus, subtherapeutic cyclosporine raises rejection risk while excessive levels raise the risk of nephrotoxicity, hypertension, hirsutism, gingival hyperplasia, and neurotoxicity; the therapeutic window is narrow and levels are sensitive to the same major drug and food interactions (CYP3A4 inhibitors/inducers, grapefruit) as tacrolimus. Target ranges are set by the transplant center's protocol and vary by organ transplanted, time since transplant, and whether the center uses trough or C2 monitoring, so results should be interpreted against that specific protocol.",
        "associated_conditions": [
            {"condition": "Acute or chronic graft rejection risk", "direction": "level below target range"},
            {"condition": "Cyclosporine toxicity (nephrotoxicity, hypertension, hirsutism, gingival hyperplasia)", "direction": "level above target range"}
        ],
        "questions_to_ask_en": "Is my center using trough or 2-hour post-dose monitoring, and what is my current target range? Could a new medication be interacting with my cyclosporine dose?",
        "next_steps": "Levels outside target prompt dose adjustment with a repeat level at steady state, alongside monitoring of kidney function, blood pressure, and lipid profile as part of routine post-transplant follow-up.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "gentamicin-level", "name_en": "Gentamicin, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Gentamicin Peak and Trough, TDM Gentamicin",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of the aminoglycoside antibiotic gentamicin, balancing adequate antibacterial exposure (peak-dependent killing) against dose-related nephrotoxicity and ototoxicity (trough-dependent accumulation).",
        "specimen_type": "Venous serum, both peak (30-60 minutes after infusion ends) and trough (just before the next dose) depending on dosing strategy used",
        "collection_notes_en": "With extended-interval (once-daily) dosing, which is now standard for most indications, a single random level plotted on a nomogram (e.g., Hartford nomogram) is often used instead of separate peak/trough sampling; traditional multiple-daily dosing still uses paired peak and trough levels.",
        "methodology_en": "Immunoassay on automated analyzers.",
        "reference_ranges": [
            {"parameter": "Peak, traditional multiple-daily dosing", "population": "Adult", "range": "5-10 mcg/mL (higher, e.g. 8-10, for serious infections)"},
            {"parameter": "Trough, traditional multiple-daily dosing", "population": "Adult", "range": "<2 mcg/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Inadequate peak concentrations risk undertreatment, since aminoglycosides exhibit concentration-dependent bacterial killing, while elevated troughs (drug accumulation between doses) are the main driver of nephrotoxicity and irreversible ototoxicity/vestibulotoxicity. Extended-interval (once-daily) dosing was developed specifically to maximize the peak-dependent killing effect while allowing a longer drug-free interval that reduces accumulation-related toxicity compared with older multiple-daily-dose regimens.",
        "associated_conditions": [
            {"condition": "Subtherapeutic peak (risk of inadequate antibacterial effect)", "direction": "low peak"},
            {"condition": "Aminoglycoside nephrotoxicity / ototoxicity risk", "direction": "elevated trough or cumulative exposure, especially with prolonged courses or other nephrotoxins"}
        ],
        "questions_to_ask_en": "Am I on extended-interval or traditional dosing, and how does that affect when my levels are drawn? How is my kidney function and hearing being monitored during this course?",
        "next_steps": "Levels outside target prompt dose or interval adjustment, with renal function monitored throughout the course; therapy exceeding about 5-7 days generally warrants closer monitoring given cumulative toxicity risk.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "theophylline-level", "name_en": "Theophylline, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Theophylline Level, TDM Theophylline",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Guides dosing of theophylline, occasionally used for chronic obstructive pulmonary disease or asthma when other therapies are insufficient, given its narrow therapeutic index.",
        "specimen_type": "Venous serum or plasma, timing depends on formulation (trough for sustained-release oral dosing, timed level for IV infusion)",
        "collection_notes_en": "Theophylline clearance is affected by numerous factors including smoking (increases clearance), liver disease and heart failure (decrease clearance), and many drug interactions (e.g., certain macrolides and fluoroquinolones raise levels), all of which affect how a given dose translates to serum concentration.",
        "methodology_en": "Immunoassay on automated analyzers.",
        "reference_ranges": [
            {"parameter": "Theophylline, therapeutic", "population": "Adult", "range": "8-20 mcg/mL (narrower target of 10-15 often used to reduce toxicity risk)"},
            {"parameter": "Theophylline, toxic", "population": "Adult", "range": ">20 mcg/mL associated with increasing risk of toxicity"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Levels below the therapeutic range are associated with inadequate bronchodilator effect, while levels above roughly 20 mcg/mL are associated with a graded risk of toxicity: nausea, tremor, and tachycardia at moderately elevated levels, progressing to arrhythmias and seizures at higher levels, which can occur even without milder warning symptoms first. Given the narrow therapeutic index and the many factors that alter its clearance, theophylline has been largely superseded by other bronchodilators and inhaled corticosteroids in most patients, and is now reserved for select cases where monitoring is feasible.",
        "associated_conditions": [
            {"condition": "Subtherapeutic theophylline (inadequate bronchodilation)", "direction": "low"},
            {"condition": "Theophylline toxicity (nausea, tremor, tachyarrhythmia, seizures at high levels)", "direction": "high, particularly >20 mcg/mL"}
        ],
        "questions_to_ask_en": "Could smoking status, my other medications, or my liver/heart function be changing how my body clears this drug? What symptoms of toxicity should prompt me to seek care before my next scheduled level?",
        "next_steps": "Levels outside target prompt a dose adjustment and repeat level at steady state; new symptoms suggestive of toxicity (persistent vomiting, palpitations, tremor) warrant urgent evaluation rather than waiting for a scheduled level.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "methotrexate-level", "name_en": "Methotrexate, Serum (Therapeutic Drug Monitoring, High-Dose)",
        "aliases": "Methotrexate Level, MTX Level, TDM Methotrexate",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Monitors clearance of high-dose intravenous methotrexate given for certain cancers (e.g., osteosarcoma, some leukemias/lymphomas), timing and dosing of the rescue agent leucovorin (folinic acid), and identifying patients at risk for delayed methotrexate elimination and toxicity.",
        "specimen_type": "Venous serum or plasma, drawn at specified timepoints after the infusion (e.g., 24, 48, and 72 hours post-dose per institutional protocol)",
        "collection_notes_en": "This test is specific to high-dose methotrexate protocols with leucovorin rescue; it is not used to monitor the much lower weekly doses used for rheumatoid arthritis or psoriasis, where clinical response and standard toxicity labs (CBC, liver enzymes, renal function) are used instead.",
        "methodology_en": "Immunoassay (e.g., fluorescence polarization immunoassay or enzyme immunoassay) on automated analyzers; some centers use HPLC for greater specificity, particularly to avoid cross-reactivity with the DAMPA metabolite formed during glucarpidase rescue therapy.",
        "reference_ranges": [
            {"parameter": "24 hours post-infusion, expected clearance", "population": "Per institutional protocol", "range": "typically <10 micromol/L"},
            {"parameter": "48 hours post-infusion, expected clearance", "population": "Per institutional protocol", "range": "typically <1 micromol/L"},
            {"parameter": "72 hours post-infusion, expected clearance", "population": "Per institutional protocol", "range": "typically <0.1 micromol/L"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Methotrexate levels above the expected clearance curve at any monitoring timepoint indicate delayed elimination, which sharply increases the risk of severe, potentially fatal toxicity: myelosuppression, mucositis, hepatotoxicity, and nephrotoxicity from precipitation of methotrexate and its metabolites in the renal tubules. Delayed clearance most often reflects renal impairment (methotrexate is cleared primarily by the kidneys), third-spacing of fluid (ascites, pleural effusion), or drug interactions, and prompts intensified leucovorin rescue, aggressive hydration and urinary alkalinization, and in severe cases the enzyme glucarpidase to rapidly inactivate circulating methotrexate.",
        "associated_conditions": [
            {"condition": "Delayed methotrexate elimination (renal impairment, third-spacing, drug interaction)", "direction": "level above expected clearance curve"},
            {"condition": "High-dose methotrexate toxicity (myelosuppression, mucositis, hepatotoxicity, nephrotoxicity)", "direction": "correlates with degree and duration of delayed clearance"}
        ],
        "questions_to_ask_en": "Is my level following the expected clearance curve for this protocol? Do I need adjusted leucovorin dosing, extra IV fluids, or urine alkalinization based on this result?",
        "next_steps": "A level above the expected curve at any checkpoint leads to intensified leucovorin rescue and continued frequent monitoring until the level clears to a safe threshold, with aggressive hydration/alkalinization and, in severe delayed-clearance cases, glucarpidase administration.",
        "sources": [
            {"name": "MedlinePlus Medical Encyclopedia - Therapeutic Drug Levels", "url": "https://medlineplus.gov/ency/article/003430.htm", "accessed": "2026-07-20"}
        ]
    }
]

RELATED = {
    "vancomycin-level": ["serum-creatinine", "blood-urea-nitrogen", "complete-blood-count"],
    "phenytoin-level": ["albumin-serum", "valproic-acid-level"],
    "valproic-acid-level": ["albumin-serum", "phenytoin-level", "ammonia-blood"],
    "carbamazepine-level": ["sodium-na", "complete-blood-count", "alt-ast"],
    "tacrolimus-level": ["serum-creatinine", "fasting-plasma-glucose"],
    "cyclosporine-level": ["serum-creatinine", "lipid-panel"],
    "gentamicin-level": ["serum-creatinine", "blood-urea-nitrogen"],
    "theophylline-level": ["complete-blood-count"],
    "methotrexate-level": ["serum-creatinine", "alt-ast", "complete-blood-count"],
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
