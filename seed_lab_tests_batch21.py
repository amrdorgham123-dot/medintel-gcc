"""
Seed script (batch 21) for MedForsa GCC's Lab Info reference library.
Adds 10 tests: Urinalysis, EBV Antibody Panel, HLA-B27, NSE, Varicella-Zoster
IgG/IgM, Ionized Calcium, Hepatitis A IgM, CH50 (Total Complement), Total IgE,
Serum Copper.

Run once: python3 seed_lab_tests_batch21.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "urinalysis", "name_en": "Urinalysis (Complete/Routine)",
        "aliases": "UA, Urine Routine, Complete Urinalysis",
        "category": "Clinical Chemistry / Urinalysis",
        "purpose_en": "Broad screening test evaluating kidney and urinary tract health, hydration, metabolic status (glucose, ketones), and liver function (bilirubin/urobilinogen); part of routine health checks, UTI workup, and monitoring of diabetes and kidney disease.",
        "specimen_type": "Random, first-morning, or clean-catch midstream urine, depending on the indication",
        "collection_notes_en": "Clean-catch midstream technique reduces contamination when infection is a concern; the sample should be analyzed within about an hour of collection or refrigerated, since standing at room temperature allows bacterial growth and cell/cast degradation that can alter results.",
        "methodology_en": "Three components: (1) physical examination (color, clarity), (2) chemical analysis via reagent dipstick (pH, specific gravity, protein, glucose, ketones, blood, bilirubin, urobilinogen, nitrite, leukocyte esterase), and (3) microscopic examination of centrifuged sediment for cells, casts, crystals, and organisms.",
        "reference_ranges": [
            {"parameter": "Color/Clarity", "population": "Normal", "range": "Pale yellow to amber, clear"},
            {"parameter": "pH", "population": "Normal", "range": "4.5-8.0"},
            {"parameter": "Specific gravity", "population": "Normal, random specimen", "range": "1.002-1.030"},
            {"parameter": "Protein, glucose, ketones, blood, bilirubin, nitrite", "population": "Normal", "range": "Negative"},
            {"parameter": "Leukocyte esterase", "population": "Normal", "range": "Negative (or <25 Leu/\u00b5L)"},
            {"parameter": "WBC (microscopic)", "population": "Normal", "range": "0-5/HPF"},
            {"parameter": "RBC (microscopic)", "population": "Normal", "range": "0-2/HPF"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Positive protein suggests glomerular or tubular kidney disease (or benign causes like fever/exercise) and prompts a urine albumin-to-creatinine ratio for quantification. Positive glucose usually reflects hyperglycemia above the renal threshold, prompting blood glucose/HbA1c testing. Positive leukocyte esterase and/or nitrite, together with elevated WBCs on microscopy, suggests urinary tract infection and prompts urine culture. Hematuria (positive blood with elevated RBCs) requires further workup depending on the pattern (glomerular vs. non-glomerular) -- isolated dipstick blood without RBCs on microscopy can reflect hemoglobinuria or myoglobinuria rather than true hematuria. Specific gravity reflects hydration/concentrating ability; abnormal casts or crystals on microscopy can point to specific kidney pathology or stone-forming tendencies.",
        "associated_conditions": [
            {"condition": "Urinary tract infection", "direction": "positive leukocyte esterase/nitrite, elevated WBCs"},
            {"condition": "Glomerular or tubular kidney disease", "direction": "positive protein, abnormal casts"},
            {"condition": "Diabetes mellitus (glycosuria)", "direction": "positive glucose"},
            {"condition": "Hematuria (glomerular or non-glomerular)", "direction": "positive blood with elevated RBCs on microscopy"},
            {"condition": "Diabetic ketoacidosis / starvation ketosis", "direction": "positive ketones"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Urinalysis: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2074001-overview", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ebv-antibody-panel", "name_en": "Epstein-Barr Virus (EBV) Antibody Panel",
        "aliases": "EBV Panel, VCA IgM, VCA IgG, EBNA, Mono Test, Infectious Mononucleosis Serology",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Diagnoses infectious mononucleosis and distinguishes acute/recent from past EBV infection, particularly when the rapid heterophile ('Monospot') test is negative -- common in young children and in roughly 10% of adults with true acute EBV infection.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. If drawn very early in illness, antibodies may not yet be detectable; a repeat sample 1-2 weeks later may be needed if clinical suspicion remains high with an initial negative/indeterminate result.",
        "methodology_en": "Enzyme immunoassay or chemiluminescent immunoassay measuring three components together: viral capsid antigen (VCA) IgM, VCA IgG, and EBV nuclear antigen (EBNA) IgG.",
        "reference_ranges": [{"parameter": "VCA IgM, VCA IgG, EBNA IgG", "population": "Result categories", "range": "Each reported as Negative or Positive (index-value based); interpretation depends on the combined pattern of all three, not any single result alone"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The presence of VCA IgM together with VCA IgG but without EBNA IgG indicates acute/recent primary EBV infection (EBNA typically takes 6-12 weeks to appear after primary infection). The presence of VCA IgG and EBNA IgG without VCA IgM indicates past infection with lifelong immunity -- since over 90% of adults have been infected with EBV at some point, this past-infection pattern is very common and not itself clinically significant. Absence of all three markers indicates no prior EBV exposure (EBV-naive). Some profiles are atypical or difficult to interpret (e.g., isolated VCA IgG, or all three markers positive simultaneously, which can reflect either recent infection with an early EBNA response or reactivation) and may require additional testing or clinical correlation.",
        "associated_conditions": [
            {"condition": "Acute/primary infectious mononucleosis", "direction": "VCA IgM positive, EBNA IgG negative"},
            {"condition": "Past EBV infection (lifelong immunity)", "direction": "VCA IgG and EBNA IgG positive, VCA IgM negative"},
            {"condition": "No prior EBV exposure", "direction": "all three markers negative"}
        ],
        "sources": [
            {"name": "CDC - Laboratory Testing for Epstein-Barr Virus (EBV)", "url": "https://www.cdc.gov/epstein-barr/php/laboratories/index.html", "accessed": "2026-07-14"},
            {"name": "Mayo Clinic Laboratories - Epstein-Barr Virus Antibody Profile, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/621373", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "hla-b27", "name_en": "HLA-B27 Testing",
        "aliases": "HLA-B27, Human Leukocyte Antigen B27",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Supports the diagnosis of ankylosing spondylitis, reactive arthritis, and related spondyloarthropathies in patients with compatible clinical/radiographic findings (inflammatory back pain, sacroiliitis, recurrent acute anterior uveitis).",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "No fasting required. Specimen should reach the testing lab within the stated stability window (commonly 96 hours) since the test requires viable cells for flow cytometry-based methods, or DNA for genotyping-based methods.",
        "methodology_en": "Flow cytometry (detecting the HLA-B27 antigen on lymphocytes) or PCR-based genotyping (detecting the HLA-B*27 allele); genotyping is generally more specific and can further subtype the allele.",
        "reference_ranges": [{"parameter": "HLA-B27", "population": "Result categories", "range": "Positive (P) or Negative (N) -- a qualitative genetic marker, not a numeric value"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "HLA-B27 is present in roughly 80-90% of patients with ankylosing spondylitis compared to only about 5-10% of the general population, making it a strong supportive marker when combined with compatible clinical and imaging findings -- but it is not diagnostic on its own, since roughly 10% of the general healthy population carries the allele without ever developing disease, and this test should not be used as a standalone screening tool. It is less strongly associated with reactive arthritis, psoriatic arthritis, and inflammatory bowel disease-associated arthritis, where a substantial proportion of affected patients test negative. A negative result does not rule out these conditions when clinical suspicion is high.",
        "associated_conditions": [
            {"condition": "Ankylosing spondylitis", "direction": "positive in ~80-90% of patients"},
            {"condition": "Reactive arthritis / acute anterior uveitis", "direction": "positive, with lower sensitivity than for AS"},
            {"condition": "Psoriatic arthritis / IBD-associated arthritis", "direction": "positive in a minority of patients"}
        ],
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - HLA-B27 Syndromes", "url": "https://www.ncbi.nlm.nih.gov/books/NBK551523/", "accessed": "2026-07-14"},
            {"name": "ARUP Consult - Ankylosing Spondylitis (HLA-B27) Genotyping", "url": "https://arupconsult.com/ati/ankylosing-spondylitis-hla-b27-genotyping", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "nse", "name_en": "Neuron-Specific Enolase (NSE), Serum",
        "aliases": "NSE",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker for neuroendocrine tumors, most notably small cell lung cancer (SCLC), used to support diagnosis, monitor treatment response, and detect relapse; also used as a prognostic marker after cardiac arrest/hypoxic brain injury and in neuroblastoma.",
        "specimen_type": "Venous serum (avoid hemolysis)",
        "collection_notes_en": "Sample must be processed to separate serum promptly and avoid hemolysis, since red blood cells and platelets contain enolase and hemolysis causes marked false elevation -- this is the single most important preanalytical consideration for this test.",
        "methodology_en": "Chemiluminescent or enzyme immunoassay on automated immunoassay analyzers; results can vary significantly between different assay platforms, so serial monitoring should use the same assay.",
        "reference_ranges": [{"parameter": "NSE", "population": "Healthy adult", "range": "Approximately <13-16 ng/mL", "notes": "Cutoffs vary meaningfully by assay/laboratory and study; always use the reporting lab's own reference range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated NSE at diagnosis is seen in up to 70% of small cell lung cancer patients, with higher levels generally correlating with more extensive disease stage and worse prognosis; serial NSE tracks treatment response and can signal relapse before it is clinically apparent. Other neuroendocrine tumors (carcinoid, neuroblastoma, pheochromocytoma, medullary thyroid carcinoma) can also elevate NSE. In post-cardiac-arrest care, markedly elevated NSE at 48-72 hours is one of several markers used (alongside clinical exam, EEG, and imaging) to help predict poor neurological outcome, though it should never be used as the sole basis for that prediction. Hemolysis, seizures, brain injury/stroke, and proton pump inhibitor use can all cause false elevation unrelated to tumor burden.",
        "critical_values_en": None,
        "interfering_factors_en": "Hemolysis is the most common and significant cause of falsely elevated results, since red cells and platelets are rich in enolase -- any hemolyzed sample should be recollected before an elevated NSE is acted upon. Proton pump inhibitor use, hemolytic anemia, liver failure, and kidney failure can also cause artifactual elevation; when used for neurological prognostication, recent seizure, brain injury, stroke, or encephalitis can independently raise NSE unrelated to tumor status.",
        "questions_to_ask_en": "Was my sample checked for hemolysis, since that's a common cause of a falsely high result? How does this level fit with my staging/imaging findings? If being followed serially, is the same laboratory/assay being used each time for a valid comparison? If used for prognosis after a brain injury, how is this being combined with other predictors rather than used alone?",
        "next_steps": "An elevated result in the context of a known or suspected neuroendocrine tumor typically prompts imaging correlation and, if not already done, tissue diagnosis; serial levels help track treatment response. In neurologic prognostication after cardiac arrest, results are interpreted together with clinical examination, EEG, and imaging findings by the treating team, following recommended timing (commonly 48-72 hours post-arrest) rather than acted on in isolation.",
        "associated_conditions": [
            {"condition": "Small cell lung cancer (diagnosis, staging, monitoring)", "direction": "high, correlates with disease extent"},
            {"condition": "Other neuroendocrine tumors (carcinoid, neuroblastoma, pheochromocytoma)", "direction": "high"},
            {"condition": "Poor neurological outcome after cardiac arrest (prognostic marker)", "direction": "markedly high at 48-72h post-arrest"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Neuron-Specific Enolase, Serum (test catalog)", "url": "https://oncology.testcatalog.org/show/NSE", "accessed": "2026-07-14"},
            {"name": "British Journal of Cancer (PMC) - Neurone specific enolase (NSE) in small cell lung cancer: a tumour marker of prognostic significance", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1971357/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "varicella-zoster-igg-igm", "name_en": "Varicella-Zoster Virus (VZV) IgG/IgM",
        "aliases": "VZV Serology, Chickenpox Immunity Test, Varicella Antibody",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Determines immune status to varicella-zoster virus (chickenpox/shingles), used for prenatal screening, pre-employment screening in healthcare workers, and to help diagnose acute VZV infection or reactivation (e.g., in suspected Ramsay Hunt syndrome or disseminated zoster).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. IgM testing should be reserved for patients with a clinically compatible presentation, since interpretation outside that context is limited. IgG may reflect blood product transfusion in the preceding months rather than true immunity/infection, which should be considered in the history.",
        "methodology_en": "Enzyme immunoassay or chemiluminescent immunoassay, reported as an index/antibody value with a categorical interpretation (negative/equivocal/positive).",
        "reference_ranges": [{"parameter": "VZV IgG and IgM", "population": "Result categories", "range": "Negative, Equivocal, or Positive -- reported via an index value against an assay-specific cutoff, not a single universal number"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive IgG with negative IgM indicates prior infection or vaccination and protective immunity against reinfection. A positive IgG together with a positive IgM suggests recent/acute infection or reactivation, though this pattern should be interpreted alongside the clinical presentation rather than in isolation. A negative IgG and IgM indicates no prior exposure and susceptibility to infection, but does not rule out very early infection before antibodies have developed -- repeat testing 2-3 weeks later is recommended if early infection is still suspected clinically.",
        "associated_conditions": [
            {"condition": "Immunity from past infection or vaccination", "direction": "positive IgG, negative IgM"},
            {"condition": "Acute varicella infection or zoster reactivation", "direction": "positive IgG and IgM (interpret with clinical context)"},
            {"condition": "Susceptibility to primary infection", "direction": "negative IgG and IgM"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - Varicella-Zoster Antibody, IgM and IgG, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/61856", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ionized-calcium", "name_en": "Ionized Calcium, Serum",
        "aliases": "iCa, Free Calcium, Ionized Calcium",
        "category": "Clinical Chemistry",
        "purpose_en": "Measures the physiologically active (unbound) fraction of calcium directly, avoiding the confounding effect of albumin that affects total calcium interpretation; used in critically ill patients, during large-volume transfusion (citrate can bind calcium), and when total calcium and albumin don't provide a clear picture.",
        "specimen_type": "Venous or arterial whole blood, collected anaerobically (without air exposure) in a heparinized syringe or tube",
        "collection_notes_en": "Must be collected and analyzed anaerobically, since exposure to air causes CO2 loss, raising pH and artifactually lowering ionized calcium -- this is the most important preanalytical factor. Results are typically corrected/reported at a standardized pH (7.40) to remove this variability. Point-of-care blood gas analyzers are commonly used given the need for rapid, careful handling.",
        "methodology_en": "Ion-selective electrode (ISE) method, typically on a point-of-care blood gas/electrolyte analyzer.",
        "reference_ranges": [{"parameter": "Ionized calcium", "population": "Adult", "range": "~4.60-5.40 mg/dL (1.15-1.35 mmol/L)", "notes": "Reference range varies modestly by lab/analyzer"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Ionized calcium is considered the more physiologically accurate measure of calcium status compared to total calcium, since it directly reflects the biologically active fraction without needing correction for albumin. Low ionized calcium (true hypocalcemia) can cause neuromuscular irritability, tetany, and cardiac arrhythmias, and is common in critically ill patients (sepsis, pancreatitis, massive transfusion with citrate-containing blood products, and after parathyroid/thyroid surgery). High ionized calcium (true hypercalcemia) reflects the same underlying causes as elevated total calcium (hyperparathyroidism, malignancy) but confirms that the elevation is truly in the active fraction rather than an artifact of high albumin/protein binding. In-hospital ionized calcium derangements (both high and low) have been associated with increased mortality risk in observational studies.",
        "associated_conditions": [
            {"condition": "Critical illness-associated hypocalcemia (sepsis, pancreatitis, massive transfusion)", "direction": "low"},
            {"condition": "Primary hyperparathyroidism / malignancy-associated hypercalcemia", "direction": "high"},
            {"condition": "Post-thyroidectomy/parathyroidectomy hypocalcemia", "direction": "low"}
        ],
        "critical_values_en": "In-hospital ionized calcium levels outside the 4.60-5.40 mg/dL range are associated with increased mortality risk in critically ill patients per observational data; markedly abnormal values in a critically ill patient warrant urgent clinical correlation and, for severe hypocalcemia, prompt correction.",
        "interfering_factors_en": "Exposure of the sample to air causes CO2 loss and a rise in pH, which artifactually lowers the measured ionized calcium -- anaerobic collection and prompt analysis are essential. Prolonged tourniquet time can also affect results by causing local pH shifts.",
        "sources": [{"name": "PMC - Hospital-Acquired Serum Ionized Calcium Derangements and Their Associations with In-Hospital Mortality", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7699179/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "hepatitis-a-igm", "name_en": "Hepatitis A Virus IgM Antibody",
        "aliases": "Anti-HAV IgM, HAV IgM, Hepatitis A Acute Antibody",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Diagnoses acute or recent hepatitis A virus (HAV) infection in a symptomatic patient; the standard test for confirming acute hepatitis A, as distinct from total anti-HAV (IgG+IgM), which only indicates immunity and cannot confirm active infection.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Should only be ordered in patients with a clinically compatible presentation (jaundice, elevated liver enzymes, GI symptoms with recent relevant exposure), since testing asymptomatic/low-risk individuals increases the chance of a false-positive result relative to true disease prevalence.",
        "methodology_en": "Chemiluminescent immunoassay (CIA) or enzyme immunoassay (EIA) detecting HAV-specific IgM antibody.",
        "reference_ranges": [{"parameter": "Anti-HAV IgM", "population": "Result categories", "range": "Negative or Positive (reactive) -- reported by signal-to-cutoff ratio, not a numeric concentration; equivocal results may occur early in acute infection"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive (reactive) result indicates acute or recent (generally within the past 6 months) hepatitis A infection -- IgM becomes detectable about 4 weeks after infection, persists at elevated levels for roughly 2 months, then declines to undetectable by about 6 months (rarely persisting beyond 12 months). A negative result in a patient tested very early in illness may reflect an inadequate or delayed IgM response rather than true absence of infection, and retesting in 2-4 weeks (alongside total anti-HAV) is recommended if suspicion remains. Positive results are reportable to public health authorities in most jurisdictions given the outbreak potential of hepatitis A.",
        "associated_conditions": [
            {"condition": "Acute hepatitis A infection", "direction": "positive/reactive"},
            {"condition": "Recent infection (within past several months, waning)", "direction": "positive but declining, may need serial testing"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Hepatitis A Virus IgM Antibody, Serum (test catalog)", "url": "https://microbiology.testcatalog.org/show/HAIGM", "accessed": "2026-07-14"},
            {"name": "CDC - Clinical Screening and Diagnosis for Hepatitis A", "url": "https://www.cdc.gov/hepatitis-a/hcp/diagnosis-testing/index.html", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "ch50", "name_en": "Total Complement Activity (CH50)",
        "aliases": "CH50, Complement Total, Total Hemolytic Complement",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Functional screening test for the overall integrity of the classical complement pathway (C1 through C9); used to investigate suspected complement deficiency (recurrent infections, especially with encapsulated bacteria or Neisseria species) and to help monitor autoimmune conditions like SLE.",
        "specimen_type": "Venous serum, requiring careful handling",
        "collection_notes_en": "Complement activity is very labile -- the specimen must clot properly, be separated promptly, and be frozen for transport, since delayed processing, prolonged storage at room temperature, or use of plasma instead of serum can all falsely lower results.",
        "methodology_en": "Functional hemolytic assay measuring the dilution of serum required to lyse 50% of antibody-coated sheep red blood cells; assesses the combined function of the classical complement pathway components (C1-C9) rather than measuring any individual protein level.",
        "reference_ranges": [{"parameter": "CH50", "population": "Adult", "range": "Approximately 30-75 U/mL (assay-dependent; some labs report 31-60 U/mL with an upper reporting limit of '>60')", "notes": "Reference range and units vary considerably by laboratory/method -- always use the reporting lab's own range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A markedly low or absent CH50 suggests a deficiency in one or more of the classical pathway components (C1-C9) and warrants measurement of individual complement components (C3, C4, and others) to localize the defect -- hereditary complement deficiencies increase susceptibility to recurrent bacterial infections, particularly Neisseria (meningococcal/gonococcal), and are also associated with autoimmune disease (notably lupus-like syndromes with deficiencies of early classical pathway components). Low CH50 can also reflect acquired complement consumption from active autoimmune disease (e.g., active SLE) or severe infection/sepsis, where it has been associated with worse outcomes in some studies. A normal CH50 confirms the presence of all pathway components but does not exclude a partial reduction in an individual component (e.g., C3 or C4 reduced by 50-80%), since normal serum contains these in excess of what's needed for a normal CH50 result -- individual complement levels are needed if a partial deficiency is specifically suspected.",
        "critical_values_en": None,
        "interfering_factors_en": "Improper sample handling -- delayed serum separation, insufficient clotting time, prolonged room-temperature storage, or use of plasma instead of serum -- can all cause falsely low results due to in-vitro complement degradation, independent of the patient's true in-vivo complement status.",
        "questions_to_ask_en": "If my CH50 is low, do I need testing of individual complement components (C3, C4) to identify which part of the pathway is affected? Could my recurrent infections be explained by a complement deficiency, and if so, are there vaccinations or precautions I should take? If I have an autoimmune condition, is my complement level being used to track disease activity?",
        "next_steps": "A low CH50 typically leads to measurement of individual complement components (C3, C4, and sometimes others) to localize the deficiency, and may prompt referral to immunology, particularly if recurrent bacterial infections (especially Neisseria species) are part of the clinical picture -- vaccination against encapsulated organisms is often recommended in confirmed complement deficiency.",
        "associated_conditions": [
            {"condition": "Hereditary complement deficiency (recurrent Neisseria infections)", "direction": "very low/absent"},
            {"condition": "Active systemic lupus erythematosus (complement consumption)", "direction": "low, alongside low C3/C4"},
            {"condition": "Severe sepsis/DIC (complement consumption)", "direction": "low, associated with worse prognosis in some studies"}
        ],
        "sources": [
            {"name": "Labcorp - Complement, Total (CH50) test description", "url": "https://www.labcorp.com/tests/001941/complement-total-ch50", "accessed": "2026-07-14"},
            {"name": "PMC - Reduced hemolytic complement activity in the classical pathway (CH50) is a risk factor for poor clinical outcomes of patients with infections", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12176544/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "total-ige", "name_en": "Total IgE, Serum",
        "aliases": "Total IgE, Immunoglobulin E",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Screens for atopic (allergic) disease and helps evaluate suspected allergic bronchopulmonary aspergillosis and hyper-IgE syndrome; a modestly useful adjunct in allergy/asthma workup, though allergen-specific IgE testing is more directly informative for identifying specific triggers.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Fluoroenzyme immunoassay or chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Total IgE", "population": "Adult", "range": "Approximately <100-120 kU/L (upper limit of normal)", "notes": "Reference ranges vary by lab/population and rise somewhat with age in childhood before stabilizing in adulthood; geometric mean in non-atopic adults is roughly 13-14 kU/L"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated total IgE supports (but does not confirm) atopic disease such as allergic rhinitis, asthma, and atopic dermatitis, and is also elevated in parasitic infections, allergic bronchopulmonary aspergillosis (often markedly elevated), and rare primary immunodeficiencies like hyper-IgE (Job) syndrome. The test has only moderate sensitivity and high specificity for atopy at commonly used cutoffs (roughly 100 kU/L), meaning a normal total IgE does not exclude allergic disease, and many non-allergic people can also have mildly elevated levels -- allergen-specific IgE testing or skin prick testing is generally more useful for identifying specific triggers once atopic disease is suspected.",
        "associated_conditions": [
            {"condition": "Atopic disease (allergic rhinitis, asthma, atopic dermatitis)", "direction": "high (moderate sensitivity, high specificity)"},
            {"condition": "Allergic bronchopulmonary aspergillosis", "direction": "markedly high"},
            {"condition": "Parasitic infection", "direction": "high"},
            {"condition": "Hyper-IgE (Job) syndrome (rare primary immunodeficiency)", "direction": "very high"}
        ],
        "sources": [{"name": "PMC - Reference values of serum total IgE in Uppsala \u2013 comparison over four decades", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10710850/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "copper", "name_en": "Copper, Serum",
        "aliases": "Serum Copper, Cu",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected copper deficiency or excess; used alongside ceruloplasmin in the workup of Wilson disease (where free/non-ceruloplasmin-bound copper is elevated despite low total copper) and to investigate unexplained cytopenias, neuropathy, or malabsorption where copper deficiency is suspected.",
        "specimen_type": "Venous serum, collected in a trace-element (copper-free) tube",
        "collection_notes_en": "Requires specialized trace-element collection tubes to avoid contamination, similar to zinc testing.",
        "methodology_en": "Inductively coupled plasma mass spectrometry (ICP-MS) or atomic absorption spectrophotometry.",
        "reference_ranges": [{"parameter": "Serum copper", "population": "Adult (\u226518 years)", "range": "77-206 mcg/dL", "notes": "Reference ranges vary meaningfully by lab/method (some cite 70-140 or 80-155 mcg/dL) -- always confirm against the reporting lab's range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low serum copper (with low ceruloplasmin, since most serum copper is ceruloplasmin-bound) suggests copper deficiency, which can cause anemia, neutropenia, and peripheral neuropathy -- causes include malabsorption (e.g., after bariatric surgery, celiac disease), excess zinc intake/supplementation (which blocks copper absorption), or rarely Menkes disease (a genetic copper transport disorder in infants). In Wilson disease, total serum copper is typically low (because ceruloplasmin, the major copper carrier, is reduced) despite copper accumulation in tissues -- the free/non-ceruloplasmin-bound copper fraction is actually elevated, which is why total copper alone can be misleading and is always interpreted alongside ceruloplasmin. High serum copper is seen in cholestatic liver disease (primary biliary cholangitis, primary sclerosing cholangitis), pregnancy, estrogen therapy, and as a nonspecific acute-phase reactant response.",
        "associated_conditions": [
            {"condition": "Copper deficiency (malabsorption, excess zinc, Menkes disease)", "direction": "low, with low ceruloplasmin"},
            {"condition": "Wilson disease", "direction": "low total copper despite tissue accumulation -- interpret with ceruloplasmin and free copper"},
            {"condition": "Cholestatic liver disease (primary biliary cholangitis, PSC)", "direction": "high"},
            {"condition": "Pregnancy / estrogen therapy (physiologic)", "direction": "high"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - Copper, Serum (test catalog, via Billings Clinic)", "url": "https://billingscliniclaboratory.testcatalog.org/show/Billings-Clinic-8890-Mayo-CUS1", "accessed": "2026-07-14"}]
    }
]

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
             critical_values_en, interfering_factors_en, questions_to_ask_en, next_steps_en,
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("critical_values_en"), t.get("interfering_factors_en"),
             t.get("questions_to_ask_en"), t.get("next_steps"),
             json.dumps(t.get("associated_conditions", [])), json.dumps(t["sources"]),
             1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
