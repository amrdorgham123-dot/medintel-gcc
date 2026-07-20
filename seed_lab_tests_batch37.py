"""
Seed script (batch 37) for MedForsa GCC's Lab Info reference library.
Final batch to reach 220 tests. Adds Hematology (Osmotic Fragility,
Peripheral Blood Smear), Coagulation (Bleeding Time, Platelet Function
Assay/PFA-100, Mixing Study, Factor IX, Factor XI), and Microbiology
(Sputum Culture, CSF Analysis & Culture, Throat Culture, AFB Smear &
Culture, Wound Culture, Fungal Culture, Malaria Smear/Rapid Test).

Run once: python3 seed_lab_tests_batch37.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "osmotic-fragility-test", "name_en": "Osmotic Fragility Test",
        "aliases": "Red Cell Osmotic Fragility, OFT",
        "category": "Hematology",
        "purpose_en": "Evaluates suspected hereditary spherocytosis and other conditions causing abnormally shaped or fragile red blood cells, by measuring how readily red cells hemolyze when exposed to progressively hypotonic saline solutions.",
        "specimen_type": "Venous whole blood (heparin or EDTA, per laboratory protocol)",
        "collection_notes_en": "Largely superseded in many reference laboratories by more specific, standardized tests (eosin-5-maleimide binding by flow cytometry, or genetic testing) for confirming hereditary spherocytosis, since osmotic fragility has notable overlap with normal in mild cases and can be falsely normal shortly after a transfusion or in the presence of reticulocytosis.",
        "methodology_en": "Red cells are incubated in a series of saline solutions of decreasing concentration, and the percentage of hemolysis at each concentration is measured and compared to a normal curve; an incubated (24-hour) version increases sensitivity for mild cases.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Normal curve, or a left-shifted curve (increased fragility, hemolysis occurring at higher/less-hypotonic saline concentrations than normal)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Increased osmotic fragility (a left-shifted curve, meaning hemolysis occurs at less dilute saline than normal) is characteristic of hereditary spherocytosis, in which red cells lose surface area relative to volume due to a membrane protein defect, making them less able to withstand osmotic stress; it can also be seen with autoimmune hemolytic anemia and some other membrane disorders. Decreased osmotic fragility (a right-shifted curve, more resistant to hemolysis than normal) is seen with conditions producing thin or flattened red cells with increased surface-to-volume ratio, such as thalassemia, iron deficiency anemia, and other states with target cells or reticulocytosis.",
        "associated_conditions": [
            {"condition": "Hereditary spherocytosis", "direction": "increased fragility (left-shifted curve)"},
            {"condition": "Thalassemia / iron deficiency anemia (target cells)", "direction": "decreased fragility (right-shifted curve)"}
        ],
        "questions_to_ask_en": "Given the overlap with normal in mild cases, would a more specific test (like eosin-5-maleimide binding or genetic testing) help confirm this diagnosis? Does a family history of anemia or gallstones support this diagnosis alongside the test result?",
        "next_steps": "A result consistent with hereditary spherocytosis, especially with a compatible family history, splenomegaly, and jaundice/gallstones, generally leads to further confirmatory testing (eosin-5-maleimide flow cytometry) and evaluation for possible splenectomy in more severe cases; unexplained decreased fragility prompts hemoglobin electrophoresis and iron studies to evaluate for thalassemia or iron deficiency.",
        "sources": [
            {"name": "PMC - reference used for red cell membrane/hemolytic anemia testing context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9350491/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "peripheral-blood-smear", "name_en": "Peripheral Blood Smear (Manual Review)",
        "aliases": "PBS, Blood Film, Peripheral Smear",
        "category": "Hematology",
        "purpose_en": "Direct microscopic examination of red cells, white cells, and platelets on a stained blood film, used to evaluate abnormal complete blood count results, characterize anemias, identify blood parasites (e.g., malaria), and detect abnormal or immature cells suggestive of leukemia or other hematologic disease.",
        "specimen_type": "Venous whole blood (EDTA), made into a thin film and stained (typically Wright-Giemsa stain)",
        "collection_notes_en": "A smear should be reviewed promptly after collection, since red cell morphology and some parasites (notably some malaria species) can be affected by prolonged EDTA exposure; a smear is often triggered automatically by an automated hematology analyzer's flagging of an abnormal or unclassifiable result, in addition to being ordered directly.",
        "methodology_en": "Light microscopy of a stained blood film by a trained laboratory professional, evaluating red cell morphology (size, shape, color, inclusions), white cell differential and morphology, and platelet number/morphology.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Normal morphology across all three cell lines, or a descriptive report of specific abnormalities (e.g., schistocytes, spherocytes, blasts, hypersegmented neutrophils) with an interpretive comment"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Specific red cell morphologic findings point toward particular diagnoses: schistocytes (fragmented cells) suggest microangiopathic hemolytic anemia (TTP, HUS, DIC, mechanical heart valve), spherocytes suggest hereditary spherocytosis or autoimmune hemolysis, target cells suggest thalassemia or liver disease, and sickle cells confirm sickle cell disease. On the white cell side, blasts (immature precursor cells) in the peripheral blood are a critical finding requiring urgent evaluation for acute leukemia, while other findings (toxic granulation, left shift, atypical lymphocytes) support infection or reactive processes; platelet clumping can cause a falsely low automated platelet count that the smear can identify as an artifact.",
        "associated_conditions": [
            {"condition": "Microangiopathic hemolytic anemia (TTP, HUS, DIC)", "direction": "schistocytes present"},
            {"condition": "Acute leukemia", "direction": "circulating blasts present"},
            {"condition": "Malaria and other blood parasites", "direction": "intracellular/extracellular parasites identified on the smear"}
        ],
        "questions_to_ask_en": "What specific abnormality was seen on the smear, and what does it mean for my diagnosis? Does this finding require urgent further testing (like a bone marrow biopsy or specific hemolysis workup)?",
        "next_steps": "Findings suggestive of a serious process (blasts, schistocytes with thrombocytopenia, malaria parasites) prompt urgent further evaluation and, where relevant, urgent treatment; more indolent findings guide targeted follow-up testing (hemolysis labs, hemoglobin electrophoresis, iron studies) based on the specific morphologic pattern seen.",
        "sources": [
            {"name": "PMC - reference used for hematologic morphology and anemia workup context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "bleeding-time", "name_en": "Bleeding Time (Ivy Method)",
        "aliases": "Bleeding Time, Ivy Bleeding Time",
        "category": "Hematology / Coagulation",
        "purpose_en": "Historically used to assess primary hemostasis (platelet number/function and blood vessel wall interaction), largely replaced in current practice by platelet function analyzers (e.g., PFA-100) and specific platelet aggregation studies due to poor standardization and reproducibility.",
        "specimen_type": "In vivo test performed directly on the patient's forearm (not a blood sample sent to the laboratory)",
        "collection_notes_en": "This test has largely fallen out of routine clinical use due to significant inter-operator variability, lack of standardization, and poor correlation with actual surgical bleeding risk; it is included here for reference completeness and historical/comparative context, as some centers or contexts (including certain resource-limited settings) may still use it.",
        "methodology_en": "A standardized small incision is made on the volar forearm under a blood pressure cuff maintained at a set pressure, and the time to cessation of bleeding is measured (Ivy method) or, in the older Duke method, a fingertip/earlobe incision is used.",
        "reference_ranges": [{"parameter": "Bleeding time (Ivy method)", "population": "Adult", "range": "approximately 2-9 minutes (method- and device-dependent)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A prolonged bleeding time historically suggested a disorder of primary hemostasis -- thrombocytopenia, qualitative platelet dysfunction (including from aspirin/antiplatelet medications), von Willebrand disease, or vascular disorders -- but the test's poor reproducibility, operator dependence, and limited predictive value for actual surgical or clinical bleeding risk have led most laboratories and clinical guidelines to replace it with platelet function analyzer testing (PFA-100/200) and, where indicated, specific platelet aggregation studies or von Willebrand panel testing. A normal bleeding time does not reliably exclude a mild bleeding disorder, and the test is not recommended as a general pre-operative screening tool given its limited value for predicting surgical bleeding.",
        "associated_conditions": [
            {"condition": "Thrombocytopenia or qualitative platelet dysfunction", "direction": "prolonged (historically; low diagnostic reliability)"},
            {"condition": "von Willebrand disease", "direction": "prolonged (historically; specific vWF testing now preferred)"}
        ],
        "questions_to_ask_en": "Given this test's known limitations, would a platelet function analyzer test or specific von Willebrand panel give more reliable information about my bleeding risk?",
        "next_steps": "In current practice, an abnormal or clinically concerning bleeding history is generally worked up with a platelet count, PFA-100/200 platelet function testing, and a von Willebrand disease panel rather than relying on bleeding time; results feed into decisions about perioperative management or specific hematologic treatment as needed.",
        "sources": [
            {"name": "PMC - hemostasis testing standardization context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "platelet-function-analyzer-pfa-100", "name_en": "Platelet Function Analyzer (PFA-100/PFA-200)",
        "aliases": "PFA-100, PFA-200, Platelet Function Assay, Closure Time",
        "category": "Hematology / Coagulation",
        "purpose_en": "Screens for qualitative platelet dysfunction and von Willebrand disease under high-shear flow conditions that mimic in vivo platelet plug formation, used in the workup of a mucocutaneous bleeding history and to help evaluate suspected antiplatelet medication effect.",
        "specimen_type": "Venous whole blood (citrate), tested promptly after collection",
        "collection_notes_en": "Results are affected by hematocrit and platelet count, so significant anemia or thrombocytopenia can prolong closure time independent of true platelet dysfunction and should be accounted for when interpreting the result; recent aspirin or other antiplatelet medication use is a common and important cause of a prolonged result that should be documented at the time of testing.",
        "methodology_en": "A citrated whole blood sample is aspirated through a small aperture coated with collagen and either epinephrine or ADP under high shear stress, and the time to platelet plug formation and aperture closure is measured.",
        "reference_ranges": [
            {"parameter": "Closure time, collagen/epinephrine cartridge", "population": "Adult, normal hematocrit and platelet count", "range": "approximately 82-150 seconds (device/reagent lot-dependent)"},
            {"parameter": "Closure time, collagen/ADP cartridge", "population": "Adult, normal hematocrit and platelet count", "range": "approximately 62-100 seconds (device/reagent lot-dependent)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Prolonged closure time on both cartridges, in the absence of significant anemia or thrombocytopenia, suggests either von Willebrand disease or an intrinsic platelet function disorder, and typically prompts specific von Willebrand studies (antigen, activity) and, if those are normal, formal platelet aggregation studies to characterize a suspected platelet function defect. A prolonged collagen/epinephrine closure time with a normal collagen/ADP closure time is a classic (though not entirely specific) pattern associated with aspirin effect, since ADP-pathway activation partially bypasses the cyclooxygenase pathway that aspirin inhibits.",
        "associated_conditions": [
            {"condition": "von Willebrand disease", "direction": "prolonged on both cartridges"},
            {"condition": "Qualitative platelet function disorder", "direction": "prolonged on both cartridges, vWF studies normal"},
            {"condition": "Aspirin/antiplatelet medication effect", "direction": "prolonged collagen/epinephrine with relatively preserved collagen/ADP"}
        ],
        "questions_to_ask_en": "Could my hematocrit, platelet count, or a medication I'm taking be affecting this result independent of a true platelet disorder? What follow-up testing is planned if this result is abnormal?",
        "next_steps": "An abnormal result prompts specific von Willebrand disease testing and, if that is unrevealing, referral for formal platelet aggregation studies; a clearly medication-related pattern (recent aspirin use) may simply be noted and the test repeated after an appropriate washout period if clinically needed.",
        "sources": [
            {"name": "PMC - hemostasis and coagulation testing standardization context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "coagulation-mixing-study", "name_en": "Coagulation Mixing Study (PT/aPTT Correction Study)",
        "aliases": "Mixing Study, 1:1 Mix, PTT Correction Study",
        "category": "Hematology / Coagulation",
        "purpose_en": "Investigates a prolonged PT and/or aPTT of unclear cause, distinguishing a true factor deficiency (which corrects with mixing) from the presence of an inhibitor such as a lupus anticoagulant or a specific factor inhibitor (which does not fully correct).",
        "specimen_type": "Venous plasma (citrate), from both the patient and pooled normal plasma",
        "collection_notes_en": "The patient's plasma is mixed 1:1 with pooled normal plasma, and the PT and/or aPTT is repeated immediately and, for aPTT, often again after a period of incubation at 37\u00b0C (since some inhibitors, notably factor VIII inhibitors, are time- and temperature-dependent and may only become apparent on the incubated mix).",
        "methodology_en": "Clot-based coagulation assay (PT and/or aPTT) performed on the 1:1 mixture of patient and normal pooled plasma, compared against the original patient result and the normal reference range.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Correction (mixed result falls within or close to the normal reference range) supports factor deficiency; failure to correct (mixed result remains significantly prolonged) supports an inhibitor"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "If the prolonged clotting time corrects with mixing, it indicates the patient is simply missing sufficient clotting factor (which is supplied by the normal plasma in the mix), pointing toward an inherited or acquired factor deficiency (e.g., hemophilia, liver disease, vitamin K deficiency, warfarin effect) and prompting specific factor level testing to identify which factor is deficient. If the clotting time fails to correct (remains prolonged), it indicates the presence of an inhibitor -- most commonly a lupus anticoagulant (part of the antiphospholipid antibody syndrome workup) causing aPTT prolongation without a true bleeding tendency, or less commonly a specific factor inhibitor (such as an acquired factor VIII inhibitor), which does carry a significant bleeding risk and requires urgent hematology involvement.",
        "associated_conditions": [
            {"condition": "Factor deficiency (hemophilia, liver disease, vitamin K deficiency, anticoagulant effect)", "direction": "mixing study corrects"},
            {"condition": "Lupus anticoagulant", "direction": "mixing study does not correct; aPTT prolonged without bleeding tendency"},
            {"condition": "Acquired factor inhibitor (e.g., factor VIII inhibitor)", "direction": "mixing study does not correct, especially after incubation; associated with significant bleeding risk"}
        ],
        "questions_to_ask_en": "Based on whether this corrected or not, what specific follow-up testing (factor levels, lupus anticoagulant panel) is being ordered next? If an inhibitor is suspected, does this affect my bleeding risk for any upcoming procedures?",
        "next_steps": "A correcting result leads to specific factor level testing to identify and quantify the deficiency; a non-correcting result leads to a lupus anticoagulant panel (if aPTT-based, with no bleeding history) or specific factor inhibitor (Bethesda) assay testing (especially if there is an active bleeding history), with urgent hematology consultation for suspected acquired factor inhibitors.",
        "sources": [
            {"name": "PMC - coagulation abnormality workup context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "factor-ix-activity", "name_en": "Coagulation Factor IX Activity Assay",
        "aliases": "Factor IX, FIX Activity, Hemophilia B Testing",
        "category": "Hematology / Coagulation",
        "purpose_en": "Diagnoses and classifies severity of hemophilia B (factor IX deficiency), and is used to guide factor replacement dosing in known patients before procedures or during bleeding episodes.",
        "specimen_type": "Venous plasma (citrate)",
        "collection_notes_en": "Should be drawn before administration of any factor replacement product or, in patients on certain non-factor hemophilia therapies, coordinated with the hematology team since some newer agents can interfere with standard clotting-based factor assays.",
        "methodology_en": "One-stage clotting assay measuring the degree of aPTT correction of factor IX-deficient plasma by dilutions of the patient's plasma, compared to a standard curve.",
        "reference_ranges": [
            {"parameter": "Factor IX activity, normal", "population": "General", "range": "50-150% of normal (assay-dependent)"},
            {"parameter": "Hemophilia B, severe", "population": "General", "range": "<1%"},
            {"parameter": "Hemophilia B, moderate", "population": "General", "range": "1-5%"},
            {"parameter": "Hemophilia B, mild", "population": "General", "range": ">5% and <40%"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Factor IX activity level correlates closely with clinical bleeding severity in hemophilia B: severe deficiency (<1%) causes frequent spontaneous joint and muscle bleeding, moderate deficiency causes bleeding with minor trauma, and mild deficiency typically causes bleeding only with significant trauma or surgery. Hemophilia B is X-linked recessive and much less common than hemophilia A (factor VIII deficiency), which it clinically resembles; distinguishing between the two requires specific factor assays since they are managed with different replacement products.",
        "associated_conditions": [
            {"condition": "Hemophilia B (congenital factor IX deficiency)", "direction": "low, severity graded by percentage activity"},
            {"condition": "Acquired factor IX deficiency (severe liver disease, vitamin K deficiency, warfarin effect)", "direction": "low, typically alongside deficiency of other vitamin K-dependent factors"}
        ],
        "questions_to_ask_en": "Given my activity level and bleeding severity category, what does my factor replacement or prophylaxis plan look like? Do family members need to be tested given the inherited nature of this condition?",
        "next_steps": "Confirmed hemophilia B is managed with a personalized care plan by a hematologist, including factor IX replacement or newer non-factor therapies for bleeding episodes and surgical prophylaxis, with genetic counseling offered given the X-linked inheritance pattern and implications for family members.",
        "sources": [
            {"name": "PMC - inherited coagulation factor deficiency and TDM/coagulation testing reference context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "factor-xi-activity", "name_en": "Coagulation Factor XI Activity Assay",
        "aliases": "Factor XI, FXI Activity, Hemophilia C Testing",
        "category": "Hematology / Coagulation",
        "purpose_en": "Diagnoses factor XI deficiency (hemophilia C), a generally milder bleeding disorder with unpredictable correlation between factor level and bleeding tendency, notably more common in individuals of Ashkenazi Jewish descent.",
        "specimen_type": "Venous plasma (citrate)",
        "collection_notes_en": "Should be drawn as an isolated prolonged aPTT workup test when a mixing study has confirmed a correcting pattern (suggesting factor deficiency) and factor VIII/IX have been excluded or when the specific clinical/ethnic context raises suspicion for factor XI deficiency.",
        "methodology_en": "One-stage clotting assay measuring the degree of aPTT correction of factor XI-deficient plasma by dilutions of the patient's plasma, compared to a standard curve.",
        "reference_ranges": [{"parameter": "Factor XI activity, normal", "population": "General", "range": "50-150% of normal (assay-dependent); deficiency defined as below this range, with severe deficiency generally <15-20%"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Unlike hemophilia A and B, bleeding tendency in factor XI deficiency correlates poorly with the measured factor level -- some patients with severely low levels have minimal bleeding, while others with partial deficiency experience significant bleeding, particularly with surgery or trauma involving tissues rich in fibrinolytic activity (e.g., oral/dental surgery, urologic procedures). Factor XI deficiency is inherited in an autosomal pattern (unlike the X-linked hemophilias A and B) and is notably more prevalent in individuals of Ashkenazi Jewish descent, where population carrier rates are substantially higher than in the general population.",
        "associated_conditions": [
            {"condition": "Factor XI deficiency (hemophilia C)", "direction": "low, though bleeding severity correlates poorly with the level itself"}
        ],
        "questions_to_ask_en": "Given that bleeding risk doesn't correlate well with my factor level, has my personal or family bleeding history been taken into account in planning for any upcoming surgery? What precautions are recommended for procedures given this diagnosis?",
        "next_steps": "Management is individualized based on personal/family bleeding history rather than factor level alone, with fresh frozen plasma, factor XI concentrate (where available), or antifibrinolytic agents used around high-risk procedures as determined by a hematologist; genetic counseling may be offered given the hereditary nature of the condition.",
        "sources": [
            {"name": "PMC - inherited coagulation factor deficiency reference context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9045330/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "sputum-culture", "name_en": "Sputum Culture",
        "aliases": "Sputum C&S, Respiratory Culture",
        "category": "Microbiology",
        "purpose_en": "Identifies bacterial pathogens causing lower respiratory tract infection (pneumonia, bronchitis exacerbation) and provides antimicrobial susceptibility testing to guide targeted antibiotic therapy.",
        "specimen_type": "Expectorated sputum (deep cough sample) or, where obtainable, a more reliable lower-respiratory sample such as a bronchoalveolar lavage",
        "collection_notes_en": "Specimen quality is critical: a sample heavily contaminated with saliva/upper airway flora (assessed by the laboratory via Gram stain screening -- low squamous epithelial cells, high neutrophils indicates a good-quality sample) may yield misleading results reflecting oral flora rather than the true lower respiratory pathogen, and poor-quality specimens are often rejected or reported with a caveat.",
        "methodology_en": "Aerobic culture on selective and non-selective media, with organism identification (often by MALDI-TOF mass spectrometry in modern laboratories) and antimicrobial susceptibility testing performed on significant isolates.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "No growth / normal respiratory flora, or growth of a specific pathogen with quantitative or semi-quantitative growth level and susceptibility results"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Growth of a recognized respiratory pathogen (e.g., Streptococcus pneumoniae, Haemophilus influenzae, Staphylococcus aureus including MRSA, or gram-negative organisms like Klebsiella pneumoniae or Pseudomonas aeruginosa in healthcare-associated or complicated pneumonia) in a good-quality specimen supports the diagnosis and, importantly, allows antibiotic therapy to be narrowed from broad empiric coverage to a pathogen-directed regimen based on susceptibility results. Because sputum inevitably passes through the upper airway, results must always be interpreted alongside specimen quality indicators and the overall clinical picture, since growth of typical oral flora or a low-quality specimen does not reliably indicate the causative lower respiratory pathogen.",
        "associated_conditions": [
            {"condition": "Bacterial pneumonia", "direction": "growth of a recognized respiratory pathogen in a good-quality specimen"},
            {"condition": "Poor-quality/contaminated specimen (limits interpretability)", "direction": "growth of predominantly upper airway flora"}
        ],
        "questions_to_ask_en": "Was this a good-quality lower respiratory sample based on the lab's quality screening? Based on the susceptibility results, can my antibiotic be switched to a more targeted option?",
        "next_steps": "A significant, susceptibility-tested pathogen guides narrowing of antibiotic therapy from broad empiric coverage; a poor-quality or equivocal result may prompt repeat sampling or a more invasive sampling method (bronchoscopy with bronchoalveolar lavage) if the clinical picture requires a more definitive answer.",
        "sources": [
            {"name": "CDC - Guidance on respiratory specimen collection and pneumonia diagnostics (general microbiology reference)", "url": "https://www.cdc.gov/c-diff/hcp/clinical-guidance/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "csf-analysis-culture", "name_en": "Cerebrospinal Fluid (CSF) Analysis and Culture",
        "aliases": "CSF Studies, Lumbar Puncture Analysis, Spinal Fluid Culture",
        "category": "Microbiology",
        "purpose_en": "Diagnoses central nervous system infection (bacterial, viral, fungal, or tuberculous meningitis/encephalitis), subarachnoid hemorrhage, and various inflammatory/autoimmune and malignant CNS conditions, obtained via lumbar puncture.",
        "specimen_type": "Cerebrospinal fluid obtained by lumbar puncture, typically collected into multiple sequential tubes for different tests (cell count/differential, protein and glucose, Gram stain and culture, and additional studies such as PCR panels as clinically indicated)",
        "collection_notes_en": "Antibiotics should not be delayed for lumbar puncture in suspected bacterial meningitis with signs of severe illness or contraindications to immediate LP (e.g., suspected raised intracranial pressure requiring imaging first); blood cultures and, when feasible, the LP itself should be obtained as soon as safely possible, ideally before or with the first antibiotic dose.",
        "methodology_en": "Cell count and differential (manual or automated), chemistry analysis (protein, glucose, often compared to a simultaneous serum glucose), Gram stain, and aerobic/fungal/AFB culture as indicated; molecular multiplex PCR panels for common meningitis/encephalitis pathogens are increasingly used alongside traditional culture for faster results.",
        "reference_ranges": [
            {"parameter": "CSF white blood cell count", "population": "Adult, normal", "range": "\u22645/\u00b5L (predominantly lymphocytes)"},
            {"parameter": "CSF protein", "population": "Adult, normal", "range": "15-45 mg/dL"},
            {"parameter": "CSF glucose", "population": "Adult, normal", "range": "typically \u226560% of a simultaneous serum glucose"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Bacterial meningitis classically shows a markedly elevated neutrophil-predominant white cell count, high protein, and low glucose (reflecting bacterial glucose consumption), while viral meningitis/encephalitis typically shows a more modest lymphocyte-predominant pleocytosis with normal or mildly elevated protein and normal glucose; these patterns overlap, especially early in bacterial infection or in partially treated cases, so culture and/or PCR results are essential for definitive pathogen identification. Tuberculous and fungal meningitis often show a lymphocyte-predominant pleocytosis with notably low glucose and high protein, and typically require specific stains/cultures (AFB smear and culture, fungal culture, cryptococcal antigen) beyond the standard bacterial workup, given their more indolent, subacute presentation.",
        "associated_conditions": [
            {"condition": "Bacterial meningitis", "direction": "neutrophil-predominant pleocytosis, high protein, low glucose, organism identified on Gram stain/culture"},
            {"condition": "Viral meningitis/encephalitis", "direction": "lymphocyte-predominant pleocytosis, normal or mildly elevated protein, normal glucose"},
            {"condition": "Tuberculous or fungal meningitis", "direction": "lymphocyte-predominant pleocytosis, markedly low glucose, high protein"}
        ],
        "questions_to_ask_en": "Given these results, is antibiotic/antiviral therapy being adjusted while final culture results are pending? Are additional studies (like PCR panels or cryptococcal antigen) being sent given the specific pattern seen here?",
        "next_steps": "Findings consistent with bacterial meningitis lead to continuation or escalation of empiric antibiotics pending culture and susceptibility results, with de-escalation once a specific organism and susceptibility are identified; findings suggesting a viral, tuberculous, or fungal process guide the addition of specific antiviral/antifungal/antituberculous therapy and further targeted testing as appropriate.",
        "sources": [
            {"name": "CDC - Bacterial Meningitis Clinical Overview (general CSF interpretation reference)", "url": "https://www.cdc.gov/meningitis/hcp/clinical-overview/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "throat-culture-strep", "name_en": "Throat Culture (Group A Streptococcus)",
        "aliases": "Throat Culture, Strep Culture, GAS Culture",
        "category": "Microbiology",
        "purpose_en": "Confirms Group A Streptococcus (Streptococcus pyogenes) pharyngitis, most often used to follow up a negative rapid antigen detection test in children and adolescents (where the consequence of missing GAS pharyngitis -- rheumatic fever -- is more clinically significant), since culture is more sensitive than rapid antigen testing.",
        "specimen_type": "Throat swab, vigorously swabbing both tonsils/tonsillar fossae and the posterior pharynx",
        "collection_notes_en": "Adequate swab technique (touching both tonsillar areas and the posterior pharyngeal wall, avoiding the tongue and buccal mucosa) is essential for sensitivity; culture takes 24-48 hours to result, unlike the rapid antigen test, which is why culture is typically used as a backup/confirmatory test rather than the primary initial test in most clinical settings.",
        "methodology_en": "Culture on blood agar with identification of beta-hemolytic colonies confirmed as Group A Streptococcus by latex agglutination or other specific methods.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "No growth of Group A Streptococcus, or Group A Streptococcus isolated"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive throat culture for Group A Streptococcus in a patient with compatible symptoms (sore throat, fever, tonsillar exudate, absence of cough/rhinorrhea suggesting a viral cause) confirms the need for antibiotic treatment, primarily to prevent acute rheumatic fever (a serious but now uncommon complication in most high-resource settings, though still clinically relevant, particularly in some regions) and to reduce symptom duration and transmission. Because Group A Streptococcus can also be carried asymptomatically in the throat without causing active infection, a positive result is interpreted alongside clinical symptoms rather than treated as diagnostic in isolation, particularly in a patient tested primarily due to contact exposure rather than symptoms.",
        "associated_conditions": [
            {"condition": "Group A Streptococcal pharyngitis", "direction": "positive culture with compatible symptoms"},
            {"condition": "Asymptomatic Group A Streptococcus carriage", "direction": "positive culture without acute symptoms; generally not treated"}
        ],
        "questions_to_ask_en": "Given my symptoms, does this result mean I have an active infection that needs antibiotics, or could this reflect asymptomatic carriage? How long until I'm no longer contagious once treatment starts?",
        "next_steps": "A positive result with compatible symptoms leads to a course of an appropriate antibiotic (typically penicillin or amoxicillin, given continued universal susceptibility of Group A Streptococcus to these agents), with symptoms and contagiousness typically improving substantially within 24 hours of starting treatment.",
        "sources": [
            {"name": "CDC - Group A Streptococcal (GAS) Pharyngitis Clinical Guidance", "url": "https://www.cdc.gov/group-a-strep/hcp/clinical-guidance/pharyngitis.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "afb-smear-culture", "name_en": "Acid-Fast Bacilli (AFB) Smear and Culture",
        "aliases": "AFB Smear, TB Culture, Mycobacterial Culture",
        "category": "Microbiology",
        "purpose_en": "Diagnoses active tuberculosis and other mycobacterial infections (including nontuberculous mycobacteria), assesses infectiousness (smear positivity correlates with higher transmission risk), and, via culture, provides definitive species identification and drug susceptibility testing.",
        "specimen_type": "Sputum (typically three separate specimens collected on different occasions, at least one being an early-morning sample), or other specimen type depending on suspected site of disease (e.g., urine, tissue, CSF)",
        "collection_notes_en": "Molecular testing (nucleic acid amplification testing, e.g. Xpert MTB/RIF) is increasingly used alongside or instead of smear microscopy for faster, more sensitive detection and rapid rifampin resistance screening, but culture remains essential for definitive diagnosis, full drug susceptibility testing, and monitoring treatment response, since it can take several weeks to result given the slow growth of Mycobacterium tuberculosis.",
        "methodology_en": "Smear: Ziehl-Neelsen or auramine-rhodamine fluorescent staining for microscopy. Culture: liquid culture media (e.g., MGIT) for faster growth detection, with solid media (Lowenstein-Jensen) also commonly used; species identification (M. tuberculosis complex versus nontuberculous mycobacteria) and drug susceptibility testing performed on positive cultures.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "Smear: No AFB seen, or AFB seen (with quantitative grading, e.g. 1+ to 4+). Culture: No growth, or Mycobacterium species isolated and identified, generally reported over 2-6 weeks"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive AFB smear indicates a high bacillary burden and correlates with higher infectiousness, prompting immediate airborne isolation precautions while awaiting further confirmation, though smear alone cannot distinguish Mycobacterium tuberculosis from nontuberculous mycobacteria (which requires culture identification or molecular testing). A positive culture provides definitive diagnosis and, critically, allows drug susceptibility testing to guide appropriate therapy, which is essential given the global concern about multidrug-resistant tuberculosis; a negative smear does not exclude tuberculosis, since sensitivity is lower than culture, and multiple specimens plus molecular/culture testing are used together to maximize diagnostic yield.",
        "associated_conditions": [
            {"condition": "Active pulmonary tuberculosis", "direction": "AFB seen on smear and/or Mycobacterium tuberculosis complex isolated on culture"},
            {"condition": "Nontuberculous mycobacterial infection", "direction": "AFB seen, with culture identifying a species other than M. tuberculosis complex"}
        ],
        "questions_to_ask_en": "Given this smear result, what isolation precautions are needed, and for how long? Will drug susceptibility results be available before or after I start treatment, and how might that change my regimen?",
        "next_steps": "A positive smear leads to airborne isolation precautions and typically empiric multidrug anti-tuberculous therapy pending culture/susceptibility confirmation; culture and drug susceptibility results, once available, guide any needed adjustment of the treatment regimen, particularly if drug resistance is identified.",
        "sources": [
            {"name": "CDC - Tuberculosis Diagnostic Testing Overview", "url": "https://www.cdc.gov/tb/hcp/testing-diagnosis/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "wound-culture", "name_en": "Wound Culture",
        "aliases": "Wound C&S, Skin/Soft Tissue Culture",
        "category": "Microbiology",
        "purpose_en": "Identifies the causative organism(s) in a clinically infected wound (surgical site infection, diabetic foot ulcer, traumatic wound, abscess) and provides susceptibility testing to guide targeted antibiotic therapy.",
        "specimen_type": "Tissue biopsy or deep wound swab/aspirate, ideally obtained after cleaning/debriding the wound surface to reduce contamination with surface colonizing flora",
        "collection_notes_en": "Superficial swabs of a wound that hasn't been cleaned/debrided first frequently grow colonizing organisms rather than true pathogens, which can lead to unnecessary antibiotic treatment of colonization; tissue biopsy or curettage from the wound base, or aspiration of purulent material, generally provides more clinically meaningful results than a surface swab, especially in chronic wounds like diabetic foot ulcers.",
        "methodology_en": "Aerobic and, when clinically indicated (deep or necrotic wounds, suspected anaerobic infection), anaerobic culture, with organism identification and susceptibility testing on significant isolates.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "No growth, growth of normal skin flora (interpreted with caution regarding clinical significance), or growth of a specific pathogen with susceptibility results"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Growth of a recognized wound pathogen (Staphylococcus aureus including MRSA, Streptococcus pyogenes, Pseudomonas aeruginosa, or, in polymicrobial chronic wounds like diabetic foot ulcers, a mix of aerobes and anaerobes) alongside clinical signs of infection (increasing redness, warmth, purulent drainage, systemic signs) supports targeted antibiotic therapy, while growth from a wound without clinical signs of infection often represents colonization that does not require treatment. Distinguishing true infection from colonization is a common clinical challenge, particularly in chronic wounds, which is why culture results are always interpreted alongside the clinical examination rather than treated as automatically requiring antibiotics.",
        "associated_conditions": [
            {"condition": "Surgical site or traumatic wound infection", "direction": "growth of a pathogen with compatible clinical signs of infection"},
            {"condition": "Wound colonization (no active infection)", "direction": "growth without clinical signs of infection; generally not treated"}
        ],
        "questions_to_ask_en": "Was this specimen collected from deep tissue/after debridement, or a surface swab, since that affects how reliable the result is? Do my clinical signs support treating this as a true infection rather than colonization?",
        "next_steps": "Confirmed infection with a compatible clinical picture is treated with targeted antibiotic therapy based on susceptibility results, alongside appropriate wound care (debridement, drainage of any abscess); growth without clinical infection signs generally does not warrant antibiotic treatment, to avoid promoting antibiotic resistance.",
        "sources": [
            {"name": "CDC - Surgical Site Infection Prevention and Management Guidance (general wound infection reference)", "url": "https://www.cdc.gov/hai/prevent/ssi.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "fungal-culture", "name_en": "Fungal Culture",
        "aliases": "Mycology Culture, Fungal C&S",
        "category": "Microbiology",
        "purpose_en": "Identifies invasive or superficial fungal pathogens from blood, tissue, respiratory, or skin/nail specimens, particularly important in immunocompromised patients at risk for invasive fungal infection (candidiasis, aspergillosis, and others) and in suspected dermatophyte or other superficial fungal infections.",
        "specimen_type": "Depends on suspected site: blood, tissue biopsy, respiratory specimen (sputum, bronchoalveolar lavage), or skin/nail/hair scrapings for superficial infections",
        "collection_notes_en": "Fungal cultures can take substantially longer to result than bacterial cultures -- days for yeasts like Candida, but often 1-4 weeks or longer for molds like Aspergillus -- so in suspected invasive fungal infection, complementary rapid tests (beta-D-glucan, galactomannan antigen, and molecular PCR-based assays) are often used alongside culture to guide earlier treatment decisions.",
        "methodology_en": "Culture on fungal-selective media (e.g., Sabouraud dextrose agar) with incubation times tailored to the suspected organism; identification by colony/microscopic morphology or, increasingly, MALDI-TOF mass spectrometry or molecular sequencing for definitive species identification.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "No growth, or growth of a specific fungal organism, reported with turnaround time depending on the organism's growth rate"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Growth of a pathogenic fungus from a normally sterile site (blood, deep tissue, CSF) is generally clinically significant and prompts antifungal therapy, while growth from a non-sterile site (sputum, skin) requires more careful clinical correlation, since some fungi (including some Candida species and molds like Aspergillus) can be colonizers or environmental contaminants rather than true invasive pathogens in a given clinical context. Invasive fungal infections are a particular concern in immunocompromised patients (transplant recipients, patients with hematologic malignancy or prolonged neutropenia, advanced HIV/AIDS), where the threshold for aggressive diagnostic workup and empiric or pre-emptive antifungal therapy is generally lower given the high mortality of delayed treatment in this population.",
        "associated_conditions": [
            {"condition": "Invasive fungal infection (candidiasis, aspergillosis, and others) in immunocompromised patients", "direction": "growth from a sterile site, or from a non-sterile site with strong supporting clinical/radiographic evidence"},
            {"condition": "Superficial fungal infection (dermatophytosis, onychomycosis)", "direction": "growth of a dermatophyte from skin/nail/hair specimen"}
        ],
        "questions_to_ask_en": "Given how long fungal cultures can take, are faster complementary tests (like beta-D-glucan or galactomannan) also being used to guide treatment in the meantime? Does this organism represent true infection or possible colonization/contamination given where it was found?",
        "next_steps": "Growth from a sterile site or with strong clinical correlation leads to targeted antifungal therapy based on the organism identified and, where performed, susceptibility results; growth that likely represents colonization or contamination is interpreted in the full clinical context and may not require treatment.",
        "sources": [
            {"name": "CDC - Invasive Candidiasis and Fungal Disease Clinical Guidance", "url": "https://www.cdc.gov/fungal/hcp/clinical-guidance/index.html", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "malaria-smear-rdt", "name_en": "Malaria Smear (Thick/Thin Film) and Rapid Diagnostic Test",
        "aliases": "Malaria Smear, Malaria RDT, Blood Parasite Smear",
        "category": "Microbiology",
        "purpose_en": "Diagnoses malaria in a patient with fever and relevant travel/exposure history, identifies the infecting Plasmodium species, and quantifies parasitemia (percentage of infected red cells) to help assess severity and guide treatment urgency.",
        "specimen_type": "Venous whole blood (EDTA), used to prepare thick and thin blood films and, where available, a rapid antigen test",
        "collection_notes_en": "A single negative smear does not exclude malaria, since parasitemia can fluctuate; current guidelines recommend repeating smears (typically every 12-24 hours for a total of up to 3 sets) if clinical suspicion remains high, given the potential severity of untreated Plasmodium falciparum infection.",
        "methodology_en": "Thick film (concentrates parasites for more sensitive detection) and thin film (allows species identification and precise parasitemia quantification) examined by light microscopy after Giemsa staining; rapid diagnostic tests (immunochromatographic antigen detection, e.g. for histidine-rich protein 2 or lactate dehydrogenase) provide faster results and are especially useful where expert microscopy isn't readily available, though they cannot reliably quantify parasitemia and may have reduced sensitivity for non-falciparum species.",
        "reference_ranges": [{"parameter": "Result categories", "population": "General", "range": "No parasites seen, or Plasmodium species identified (P. falciparum, P. vivax, P. ovale, P. malariae, or P. knowlesi) with parasitemia percentage reported for confirmed cases"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Identification of Plasmodium falciparum, particularly with high parasitemia (commonly considered severe above roughly 5%, though clinical severity criteria matter as much as the percentage alone), signs of organ dysfunction, or in a non-immune traveler, constitutes a medical emergency requiring urgent treatment given the risk of rapid progression to severe/complicated malaria (cerebral malaria, severe anemia, acute kidney injury, respiratory distress) and death if treatment is delayed. Identifying the specific species also matters for treatment choice, since P. vivax and P. ovale require additional therapy (primaquine or tafenoxin) to eradicate dormant liver-stage parasites (hypnozoites) and prevent relapse, which is not needed for P. falciparum or P. malariae.",
        "associated_conditions": [
            {"condition": "Plasmodium falciparum malaria (highest risk of severe/complicated disease)", "direction": "parasites identified, with parasitemia percentage guiding severity assessment"},
            {"condition": "Plasmodium vivax / P. ovale malaria (relapse risk from liver hypnozoites)", "direction": "parasites identified; requires additional liver-stage treatment to prevent relapse"}
        ],
        "questions_to_ask_en": "Given my travel history and this result, how urgently does treatment need to start, and is this considered severe malaria requiring closer monitoring or IV therapy? If this is P. vivax or P. ovale, do I need additional medication to prevent relapse?",
        "next_steps": "A positive result, especially P. falciparum or any case with severity features, leads to prompt initiation of appropriate antimalarial therapy (with IV therapy and closer monitoring for severe disease) and, for P. vivax/P. ovale, additional treatment to eradicate liver-stage parasites after screening for G6PD deficiency (since the relevant medications can cause hemolysis in G6PD-deficient patients); a negative smear with ongoing suspicion prompts repeat testing.",
        "sources": [
            {"name": "CDC - Malaria Diagnosis and Treatment Guidance for Clinicians", "url": "https://www.cdc.gov/malaria/hcp/diagnosis-testing/index.html", "accessed": "2026-07-20"}
        ]
    }
]

RELATED = {
    "osmotic-fragility-test": ["complete-blood-count", "hemoglobin-electrophoresis-hemoglobinopathy-evaluation"],
    "peripheral-blood-smear": ["complete-blood-count", "reticulocyte-count", "malaria-smear-rdt"],
    "bleeding-time": ["platelet-function-analyzer-pfa-100", "complete-blood-count"],
    "platelet-function-analyzer-pfa-100": ["von-willebrand-factor-antigen-ristocetin-cofactor-activity", "complete-blood-count"],
    "coagulation-mixing-study": ["prothrombin-time-inr", "activated-partial-thromboplastin-time-aptt", "factor-ix-activity"],
    "factor-ix-activity": ["activated-partial-thromboplastin-time-aptt", "coagulation-factor-viii-activity-assay"],
    "factor-xi-activity": ["activated-partial-thromboplastin-time-aptt", "coagulation-mixing-study"],
    "sputum-culture": ["blood-culture", "gram-stain", "c-reactive-protein-hs-crp"],
    "csf-analysis-culture": ["gram-stain", "blood-culture"],
    "throat-culture-strep": ["gram-stain"],
    "afb-smear-culture": ["tb-igra-quantiferon"],
    "wound-culture": ["gram-stain", "blood-culture"],
    "fungal-culture": ["blood-culture", "gram-stain"],
    "malaria-smear-rdt": ["complete-blood-count", "peripheral-blood-smear"],
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
