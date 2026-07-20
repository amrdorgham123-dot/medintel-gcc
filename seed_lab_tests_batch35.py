"""
Seed script (batch 35) for MedForsa GCC's Lab Info reference library.
Adds Infectious Disease molecular/antigen and serology tests: SARS-CoV-2
RT-PCR, Influenza A/B, RSV, TB IGRA (QuantiFERON-TB Gold), C. difficile
Toxin, Chlamydia/Gonorrhea NAAT, HSV 1/2 IgG, Measles IgG, and Hepatitis B
Core Antibody (Total).

Run once: python3 seed_lab_tests_batch35.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "sars-cov-2-rt-pcr", "name_en": "SARS-CoV-2 RT-PCR (COVID-19 Molecular Test)",
        "aliases": "COVID-19 PCR, SARS-CoV-2 NAAT, Coronavirus PCR",
        "category": "Molecular Diagnostics / Infectious Disease",
        "purpose_en": "Detects current SARS-CoV-2 infection with high sensitivity, used for diagnosis in symptomatic patients, pre-procedure/admission screening, and outbreak investigation.",
        "specimen_type": "Nasopharyngeal or mid-turbinate nasal swab; saliva accepted by some assay platforms",
        "collection_notes_en": "Proper swab technique and adequate sample collection depth in the nasopharynx materially affect sensitivity; timing relative to symptom onset also matters, since viral load rises and falls over the course of infection.",
        "methodology_en": "Real-time reverse transcription polymerase chain reaction (RT-PCR), targeting one or more SARS-CoV-2 gene regions (e.g., N, ORF1ab, S genes).",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Detected (Positive) or Not Detected (Negative); some platforms report a cycle threshold (Ct) value, which correlates inversely with viral load but is not standardized for cross-platform comparison"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "RT-PCR remains the reference-standard method for detecting current SARS-CoV-2 infection due to its high analytical sensitivity, and a positive result in a symptomatic patient is highly reliable, though the test can remain positive for a period after infectiousness has resolved since it detects viral RNA rather than live, transmissible virus. A negative result does not fully exclude infection, particularly very early in the course of illness before viral load rises to detectable levels or with a poorly collected specimen, so repeat testing or an alternative specimen may be considered when clinical suspicion remains high despite an initial negative result.",
        "associated_conditions": [
            {"condition": "Active SARS-CoV-2 infection", "direction": "detected/positive"},
            {"condition": "Early infection or inadequate specimen (false-negative risk)", "direction": "not detected despite ongoing clinical suspicion"}
        ],
        "questions_to_ask_en": "Given my symptoms and exposure history, does a negative result here rule out COVID-19, or should I be retested? How long should I isolate based on this result and current guidance?",
        "next_steps": "A positive result guides isolation precautions and, in higher-risk patients, consideration of antiviral therapy per current clinical guidelines; a negative result with ongoing strong clinical suspicion may prompt repeat testing 24-48 hours later or consideration of alternative diagnoses.",
        "sources": [
            {"name": "CDC - COVID-19 Testing Overview and Guidance", "url": "https://www.cdc.gov/covid/testing/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "influenza-a-b", "name_en": "Influenza A/B (Rapid Antigen and Molecular Testing)",
        "aliases": "Flu Test, Influenza PCR, Rapid Flu Antigen",
        "category": "Molecular Diagnostics / Infectious Disease",
        "purpose_en": "Diagnoses influenza A or B infection to guide antiviral treatment decisions, infection control precautions, and, in outbreak settings, epidemiologic surveillance.",
        "specimen_type": "Nasopharyngeal or nasal swab",
        "collection_notes_en": "Rapid antigen tests have notably lower sensitivity than molecular (PCR) methods, particularly in adults and later in the illness course, so a negative rapid antigen result in a symptomatic patient during flu season does not reliably exclude infection and may warrant confirmatory PCR testing.",
        "methodology_en": "Rapid immunoassay (lateral flow antigen detection) for point-of-care use, or real-time RT-PCR (often as part of a multiplex respiratory panel with RSV and SARS-CoV-2) for higher sensitivity.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Detected (Positive, with type A or B specified) or Not Detected (Negative)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive result in a patient with compatible symptoms confirms influenza and, in patients at higher risk of complications or presenting early in illness, supports starting antiviral therapy (e.g., oseltamivir), which is most effective when started within 48 hours of symptom onset. Distinguishing influenza from other respiratory viruses (including SARS-CoV-2 and RSV, which can present nearly identically) matters for both treatment (antivirals differ by pathogen) and infection control precautions, which is why multiplex PCR panels testing for several respiratory viruses simultaneously are increasingly used in hospital settings.",
        "associated_conditions": [
            {"condition": "Influenza A or B infection", "direction": "detected/positive"},
            {"condition": "Other respiratory viral infection (clinically similar presentation)", "direction": "influenza negative; consider multiplex respiratory panel if available"}
        ],
        "questions_to_ask_en": "Given my symptom duration, am I still within the window where antiviral treatment would be most effective? If this rapid test is negative but I'm still very symptomatic, should a more sensitive PCR test be done?",
        "next_steps": "A positive result in a higher-risk or early-presenting patient generally leads to antiviral therapy and appropriate isolation/infection control measures; a negative rapid antigen result with ongoing strong clinical suspicion, especially during a high-prevalence period, is often followed by PCR confirmation.",
        "sources": [
            {"name": "CDC - Information for Clinicians on Influenza Virus Testing", "url": "https://www.cdc.gov/flu/hcp/testing/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "rsv-antigen-pcr", "name_en": "Respiratory Syncytial Virus (RSV) Antigen/PCR",
        "aliases": "RSV Test, RSV Antigen, RSV PCR",
        "category": "Molecular Diagnostics / Infectious Disease",
        "purpose_en": "Diagnoses RSV infection, particularly important in infants and young children with bronchiolitis, and in older or immunocompromised adults with severe respiratory illness, to guide clinical management and infection control (RSV spreads readily in hospital and daycare settings).",
        "specimen_type": "Nasopharyngeal or nasal swab/aspirate",
        "collection_notes_en": "Rapid antigen testing performs best in young children, who tend to have higher viral loads, and less reliably in adults, where PCR is preferred given its greater sensitivity.",
        "methodology_en": "Rapid immunoassay (antigen detection) for point-of-care use in pediatric patients, or real-time RT-PCR (often as part of a multiplex respiratory panel) for higher sensitivity.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Detected (Positive) or Not Detected (Negative)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive result in an infant with bronchiolitis symptoms (wheezing, increased work of breathing, following a viral prodrome) confirms the diagnosis and supports cohorting/isolation precautions to limit nosocomial spread, since RSV is highly contagious in healthcare settings; management remains largely supportive (oxygen, hydration, suctioning) regardless of confirmation, as there is no widely used specific antiviral for most patients. In adults, particularly the elderly or those with chronic cardiopulmonary disease, RSV can cause severe lower respiratory tract disease that clinically resembles influenza or COVID-19, so confirming the specific pathogen (often via multiplex panel) helps guide isolation decisions and, where relevant, eligibility discussions for RSV-specific preventive vaccines in future seasons.",
        "associated_conditions": [
            {"condition": "RSV bronchiolitis (infants/young children)", "direction": "detected/positive"},
            {"condition": "RSV lower respiratory tract infection (older adults, immunocompromised)", "direction": "detected/positive"}
        ],
        "questions_to_ask_en": "Does this result change the treatment plan, or is supportive care the main approach either way? What precautions should be taken to avoid spreading this to other children or vulnerable family members?",
        "next_steps": "Management for most patients is supportive regardless of confirmation; hospitalized patients with a positive result are placed on appropriate contact/droplet precautions, and severe cases in high-risk patients may prompt closer monitoring for respiratory decompensation.",
        "sources": [
            {"name": "CDC - RSV Clinical Overview", "url": "https://www.cdc.gov/rsv/hcp/clinical-overview/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "tb-igra-quantiferon", "name_en": "Tuberculosis Interferon-Gamma Release Assay (IGRA, e.g. QuantiFERON-TB Gold)",
        "aliases": "IGRA, QuantiFERON-TB, TB Gold, T-SPOT.TB",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Detects immune sensitization to Mycobacterium tuberculosis antigens to diagnose latent TB infection (LTBI), and is used as an alternative to the tuberculin skin test (TST), particularly in patients previously vaccinated with BCG (which can cause false-positive TST results).",
        "specimen_type": "Venous whole blood collected into specialized antigen tubes (must be incubated per manufacturer protocol within a defined time window after draw)",
        "collection_notes_en": "Strict adherence to blood volume, incubation temperature, and incubation timing is required for a valid result; samples that sit too long before incubation or are under/over-filled can produce indeterminate results.",
        "methodology_en": "Interferon-gamma release assay: whole blood is incubated with TB-specific antigen peptides, and the interferon-gamma released by sensitized T-cells is measured, most commonly by ELISA (QuantiFERON) or ELISPOT (T-SPOT.TB).",
        "reference_ranges": [
            {"parameter": "Result categories (QuantiFERON-TB Gold, standard cutoff)", "population": "General", "range": "Negative (<0.35 IU/mL TB-antigen minus nil response, meeting negative criteria) or Positive (\u22650.35 IU/mL and \u226525% of nil)"},
            {"parameter": "Borderline/equivocal zone (used by some laboratories)", "population": "General", "range": "approximately 0.20-0.99 IU/mL; some laboratories recommend retesting results in this range"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive IGRA indicates immune sensitization consistent with TB infection (latent or active) but, like the tuberculin skin test, cannot on its own distinguish latent infection from active disease -- a positive result in a patient without symptoms and a normal chest X-ray supports latent TB infection, warranting consideration of preventive treatment, while a positive result with compatible symptoms or imaging findings prompts full evaluation for active disease (sputum studies, imaging). Unlike the tuberculin skin test, IGRA results are not affected by prior BCG vaccination, making it the preferred test in BCG-vaccinated populations, though results near the assay cutoff can show meaningful inter-run and inter-laboratory variability and are sometimes retested before being acted upon.",
        "associated_conditions": [
            {"condition": "Latent tuberculosis infection", "direction": "positive, with normal chest imaging and no symptoms"},
            {"condition": "Active tuberculosis (requires additional testing to confirm)", "direction": "positive, with compatible symptoms/imaging prompting further workup"}
        ],
        "questions_to_ask_en": "Does this result mean I have latent infection, active disease, or could it be a borderline result that should be repeated? If latent infection is confirmed, what does preventive treatment involve?",
        "next_steps": "A positive result without symptoms or radiographic abnormality typically leads to a chest X-ray to exclude active disease, followed by consideration of latent TB preventive treatment; a positive result with symptoms or imaging findings leads to sputum studies (smear, culture, and/or molecular testing) to evaluate for active tuberculosis.",
        "sources": [
            {"name": "PMC - Refining the Diagnostic Approach to Latent TB with QuantiFERON Gold Plus (cutoffs and borderline zone)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12416684/", "accessed": "2026-07-20"},
            {"name": "PMC - A Borderline Range for QuantiFERON Gold In-Tube Results", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5667766/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "c-difficile-toxin", "name_en": "Clostridioides difficile Toxin (Stool)",
        "aliases": "C. diff Toxin, CDAD Testing, C. difficile PCR/GDH/Toxin",
        "category": "Microbiology",
        "purpose_en": "Diagnoses Clostridioides difficile infection in patients with diarrhea, most often following antibiotic use, healthcare exposure, or advanced age, and distinguishes true infection from asymptomatic colonization.",
        "specimen_type": "Unformed (liquid or soft) stool specimen; formed stool should not be tested since it usually reflects colonization rather than infection",
        "collection_notes_en": "Testing should only be performed on patients with clinically significant diarrhea (typically \u22653 unformed stools in 24 hours) without another obvious cause; testing formed stool or asymptomatic patients is discouraged because C. difficile PCR can detect colonization without true infection, leading to overdiagnosis and unnecessary treatment.",
        "methodology_en": "Multi-step algorithm commonly used: glutamate dehydrogenase (GDH) antigen screen plus toxin A/B enzyme immunoassay, with nucleic acid amplification testing (NAAT/PCR) for the toxin gene used to resolve discordant results or as a standalone highly sensitive molecular test.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Negative or Positive; algorithm-dependent (GDH+/Toxin+, GDH+/Toxin-/NAAT+, etc.) interpretation may require correlation with clinical presentation"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive toxin EIA result, reflecting active toxin production, correlates best with clinically significant disease, while a positive NAAT/PCR alone (detecting the toxin gene without confirmed toxin production) can reflect either true infection or asymptomatic carriage/colonization, which is why many laboratories use a two- or three-step algorithm rather than PCR alone to reduce overdiagnosis and unnecessary antibiotic treatment in colonized but asymptomatic patients. Risk factors include recent antibiotic use (especially broad-spectrum agents), hospitalization, advanced age, and proton pump inhibitor use; recurrence after treatment is common and a topic of ongoing clinical management (repeat treatment, fecal microbiota transplantation for recurrent cases).",
        "associated_conditions": [
            {"condition": "Clostridioides difficile infection (symptomatic)", "direction": "positive toxin (with or without positive GDH/NAAT), correlating with clinical diarrhea"},
            {"condition": "Asymptomatic colonization (NAAT-positive, toxin-negative, no diarrhea)", "direction": "generally not treated as active infection"}
        ],
        "questions_to_ask_en": "Which specific test(s) in the algorithm came back positive, and does that combination indicate active infection rather than colonization? Should any antibiotics I'm currently taking be reviewed given this result?",
        "next_steps": "Confirmed infection is treated with a specific oral antibiotic regimen (commonly vancomycin or fidaxomicin) and discontinuation of the inciting antibiotic where possible; recurrent episodes may prompt extended or alternative regimens, or referral for fecal microbiota transplantation in select cases.",
        "sources": [
            {"name": "CDC - Clostridioides difficile Infection Clinical Guidance", "url": "https://www.cdc.gov/c-diff/hcp/clinical-guidance/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "chlamydia-gonorrhea-naat", "name_en": "Chlamydia trachomatis / Neisseria gonorrhoeae NAAT",
        "aliases": "CT/NG NAAT, Chlamydia and Gonorrhea PCR, STI Molecular Panel",
        "category": "Molecular Diagnostics / Infectious Disease",
        "purpose_en": "Diagnoses genital, rectal, or pharyngeal chlamydia and gonorrhea infection; used for symptomatic evaluation, routine screening in sexually active individuals per risk-based guidelines, and test-of-cure in specific situations (notably pharyngeal gonorrhea or in pregnancy).",
        "specimen_type": "Depends on exposure site and symptoms: first-catch urine, vaginal swab (self- or clinician-collected), endocervical swab, or extragenital (rectal/pharyngeal) swab",
        "collection_notes_en": "Vaginal swabs (including self-collected) generally perform as well as or better than urine for detecting infection in women and are preferred by many guidelines; extragenital site testing should be based on actual reported exposure sites, since infections at these sites are frequently asymptomatic and missed if only genital testing is performed.",
        "methodology_en": "Nucleic acid amplification testing (NAAT), the current reference-standard method given its high sensitivity and specificity compared with older culture or antigen methods.",
        "reference_ranges": [{"parameter": "Result categories", "population": "Per organism and site tested", "range": "Detected (Positive) or Not Detected (Negative)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Both infections are frequently asymptomatic, particularly in women and at extragenital sites, which is why risk-based screening (not just symptom-triggered testing) is recommended in sexually active individuals under 25 and others with risk factors, since untreated infection can lead to pelvic inflammatory disease, infertility, ectopic pregnancy, and facilitates HIV transmission. Because NAAT detects genetic material rather than viable organism, a test-of-cure (repeat testing) at an appropriate interval after treatment, rather than immediately, is recommended specifically for pharyngeal gonorrhea and in pregnancy, since a repeat test too soon after treatment can show a false positive from residual non-viable organism DNA.",
        "associated_conditions": [
            {"condition": "Chlamydia trachomatis infection", "direction": "detected/positive"},
            {"condition": "Neisseria gonorrhoeae infection", "direction": "detected/positive"},
            {"condition": "Pelvic inflammatory disease / infertility risk (untreated infection)", "direction": "associated with delayed or missed diagnosis"}
        ],
        "questions_to_ask_en": "Should my partner(s) also be tested and treated to prevent reinfection? Given the site(s) of my exposure, was testing done at all relevant sites (not just genital)?",
        "next_steps": "A positive result is treated with the current recommended antibiotic regimen, with partner notification and treatment strongly encouraged to prevent reinfection and further transmission; abstinence from sexual activity is generally advised until treatment is completed and, where recommended, until a test-of-cure at the appropriate interval.",
        "sources": [
            {"name": "CDC - STI Treatment Guidelines: Chlamydia and Gonorrhea", "url": "https://www.cdc.gov/std/treatment-guidelines/default.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "hsv-1-2-igg", "name_en": "Herpes Simplex Virus (HSV) Type-Specific IgG (HSV-1/HSV-2)",
        "aliases": "HSV IgG, Herpes Type-Specific Serology, HSV-1/2 Antibody",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Determines prior HSV-1 or HSV-2 infection status using type-specific serology, useful for confirming a clinical diagnosis of genital herpes when lesion-based testing (PCR/culture) isn't available, evaluating an asymptomatic partner of someone with known genital herpes, and in pregnancy risk assessment for neonatal herpes.",
        "specimen_type": "Venous serum",
        "collection_notes_en": "Only type-specific glycoprotein G (gG)-based assays reliably distinguish HSV-1 from HSV-2; older non-type-specific HSV antibody tests should not be used for this purpose since they cannot differentiate the two types, and antibodies may take several weeks after initial infection to become detectable (seroconversion window).",
        "methodology_en": "Type-specific enzyme immunoassay (EIA) targeting glycoprotein G1 (HSV-1) and glycoprotein G2 (HSV-2).",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Negative, Positive, or Equivocal, reported separately for HSV-1 IgG and HSV-2 IgG"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive HSV-2 IgG indicates prior genital herpes infection in most cases (HSV-2 is predominantly a genital infection), while a positive HSV-1 IgG is common in the general population and does not distinguish oral from genital infection, since HSV-1 increasingly causes genital disease as well -- this limits the usefulness of HSV-1 serology alone in confirming genital involvement without a corresponding lesion-based test. Serologic testing detects prior exposure, not necessarily active shedding or lesion status, so a positive result in an asymptomatic person indicates infection has occurred (with implications for counseling on transmission risk and, in pregnancy, monitoring), while it cannot confirm whether a current lesion is due to HSV without direct lesion testing (PCR or culture).",
        "associated_conditions": [
            {"condition": "Prior HSV-2 infection (predominantly genital)", "direction": "positive"},
            {"condition": "Prior HSV-1 infection (oral and/or genital)", "direction": "positive, site not distinguished by serology alone"}
        ],
        "questions_to_ask_en": "What does this result mean for transmission risk to a current or future partner? If I'm pregnant, does this affect the delivery plan or need for suppressive therapy near term?",
        "next_steps": "A positive result prompts counseling on transmission risk, safer-sex practices, and, for genital HSV-2, discussion of suppressive antiviral therapy options; in pregnancy, a known history (or a new diagnosis) informs monitoring and delivery planning to reduce the risk of neonatal transmission.",
        "sources": [
            {"name": "CDC - STI Treatment Guidelines: Genital HSV Infections (serologic testing section)", "url": "https://www.cdc.gov/std/treatment-guidelines/herpes.htm", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "measles-igg", "name_en": "Measles IgG (Immunity Status)",
        "aliases": "Measles Antibody, Rubeola IgG, Measles Immunity Screen",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Confirms immune status to measles (rubeola), used for healthcare worker immunity documentation, outbreak/exposure investigation, and in patients with uncertain vaccination history.",
        "specimen_type": "Venous serum",
        "collection_notes_en": "For outbreak investigation or suspected acute infection (rather than immunity screening), IgM serology and/or molecular testing (RT-PCR from a throat/nasopharyngeal swab or urine) is used instead, since IgG mainly reflects past infection or vaccination rather than acute illness.",
        "methodology_en": "Enzyme immunoassay (EIA) on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Non-immune (negative/equivocal) or Immune (positive), with some assays reporting a quantitative index value alongside the qualitative interpretation"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive (immune) result indicates protective antibody from prior infection or vaccination and generally requires no further action; a negative or equivocal result in a healthcare worker, traveler, or other individual at risk of exposure prompts a recommendation for MMR vaccination (unless contraindicated), since measles is highly contagious and can cause serious complications including pneumonia and encephalitis, with additional risk to unvaccinated infants and immunocompromised contacts. Following documented significant exposure in a non-immune individual, post-exposure prophylaxis (MMR vaccine or immune globulin, depending on timing and the individual's risk factors) may be indicated rather than relying on serology alone, given the short window in which post-exposure measures are effective.",
        "associated_conditions": [
            {"condition": "Measles immunity (from prior infection or vaccination)", "direction": "positive"},
            {"condition": "Susceptibility to measles infection", "direction": "negative or equivocal, especially relevant after a known exposure"}
        ],
        "questions_to_ask_en": "If I'm not immune, is there still time for post-exposure prophylaxis to be effective given when I was exposed? Do I need a booster MMR vaccine, or is my vaccination history sufficient going forward?",
        "next_steps": "A negative or equivocal result generally leads to a recommendation for MMR vaccination (two doses if no prior documented vaccination); a documented significant exposure in a non-immune person may warrant urgent evaluation for post-exposure prophylaxis rather than waiting on routine vaccination scheduling.",
        "sources": [
            {"name": "CDC - Measles (Rubeola) Clinical Overview and Immunity Assessment", "url": "https://www.cdc.gov/measles/hcp/clinical-overview/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "hepatitis-b-core-antibody-total", "name_en": "Hepatitis B Core Antibody, Total (Anti-HBc)",
        "aliases": "Anti-HBc Total, HBcAb, Hepatitis B Core Antibody",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Detects prior or current hepatitis B infection as part of a complete hepatitis B panel (alongside HBsAg and anti-HBs), used to distinguish natural infection (past or present) from vaccine-induced immunity, and to identify occult or resolved infection before immunosuppressive therapy.",
        "specimen_type": "Venous serum",
        "collection_notes_en": "Interpretation requires the full panel (HBsAg, anti-HBc total, anti-HBs) together, since anti-HBc alone cannot distinguish current from past infection; IgM anti-HBc specifically indicates recent/acute infection and is ordered separately when acute hepatitis B is suspected.",
        "methodology_en": "Chemiluminescent immunoassay or enzyme immunoassay on automated analyzers.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Non-reactive or Reactive; interpreted alongside HBsAg and anti-HBs (e.g., anti-HBc reactive with anti-HBs reactive and HBsAg non-reactive indicates resolved past infection with natural immunity, distinct from vaccine-induced immunity which is anti-HBc non-reactive with anti-HBs reactive)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Because anti-HBc becomes positive with any hepatitis B infection (acute, chronic, or resolved) but is not produced by vaccination alone, its pattern relative to HBsAg and anti-HBs distinguishes resolved natural infection (anti-HBc+/anti-HBs+/HBsAg-) from vaccine immunity (anti-HBc-/anti-HBs+/HBsAg-) and from chronic active infection (anti-HBc+/HBsAg+). Isolated anti-HBc positivity (with negative HBsAg and negative or low anti-HBs) can represent a window period of acute infection, a false positive, or -- importantly -- occult hepatitis B infection with the potential for reactivation if the patient later receives immunosuppressive or biologic therapy, which is why anti-HBc is included in pre-treatment screening panels for such therapies.",
        "associated_conditions": [
            {"condition": "Resolved past hepatitis B infection (natural immunity)", "direction": "anti-HBc reactive with anti-HBs reactive, HBsAg non-reactive"},
            {"condition": "Chronic hepatitis B infection", "direction": "anti-HBc reactive with HBsAg reactive"},
            {"condition": "Occult hepatitis B infection / reactivation risk before immunosuppression", "direction": "isolated anti-HBc reactivity"}
        ],
        "questions_to_ask_en": "Given my full hepatitis B panel results, do I have natural immunity, vaccine-induced immunity, or an active infection? If I'm starting immunosuppressive or biologic therapy, does this result mean I need antiviral prophylaxis to prevent reactivation?",
        "next_steps": "The pattern of results across the full panel determines next steps: reactive HBsAg leads to further evaluation for chronic hepatitis B (viral load, liver assessment); isolated anti-HBc positivity before planned immunosuppressive therapy generally prompts hepatitis B DNA testing and consideration of prophylactic antiviral therapy to prevent reactivation.",
        "sources": [
            {"name": "CDC - Hepatitis B Serology Interpretation Table", "url": "https://www.cdc.gov/hepatitis-b/hcp/diagnosis-testing/index.html", "accessed": "2026-07-20"}
        ]
    }
]

RELATED = {
    "sars-cov-2-rt-pcr": ["influenza-a-b", "rsv-antigen-pcr", "c-reactive-protein-hs-crp"],
    "influenza-a-b": ["sars-cov-2-rt-pcr", "rsv-antigen-pcr", "procalcitonin-pct-serum"],
    "rsv-antigen-pcr": ["influenza-a-b", "sars-cov-2-rt-pcr"],
    "tb-igra-quantiferon": ["complete-blood-count"],
    "c-difficile-toxin": ["stool-culture", "fecal-calprotectin"],
    "chlamydia-gonorrhea-naat": ["hiv-antigen-antibody-combination-screen", "syphilis-screening-rpr-vdrl-with-treponemal-confirmation"],
    "hsv-1-2-igg": ["varicella-zoster-virus-vzv-igg-igm"],
    "measles-igg": ["rubella-igg-immunity-status", "varicella-zoster-virus-vzv-igg-igm"],
    "hepatitis-b-core-antibody-total": ["hepatitis-b-surface-antigen-hbsag", "hepatitis-b-surface-antibody-anti-hbs"],
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
