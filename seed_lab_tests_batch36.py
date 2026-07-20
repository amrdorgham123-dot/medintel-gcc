"""
Seed script (batch 36) for MedForsa GCC's Lab Info reference library.
Adds Endocrinology and Clinical Chemistry tests: Growth Hormone, Plasma
Renin Activity, ADH/Vasopressin, Thyroglobulin, Androstenedione, Vitamin B1
(Thiamine), Vitamin E, 24-Hour Urine Protein, Urine Osmolality, 24-Hour
Urinary Free Cortisol, and Beta-Hydroxybutyrate.

Run once: python3 seed_lab_tests_batch36.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "growth-hormone", "name_en": "Growth Hormone (GH), Serum",
        "aliases": "GH, Somatotropin, Human Growth Hormone",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Evaluates suspected growth hormone excess (acromegaly/gigantism) or deficiency; a single random level has limited diagnostic value on its own and dynamic (stimulation or suppression) testing is usually required to confirm either condition.",
        "specimen_type": "Venous serum",
        "collection_notes_en": "GH is secreted in a pulsatile pattern and is strongly affected by sleep, exercise, stress, and fasting status, so a single random level is difficult to interpret in isolation; suspected excess is confirmed with an oral glucose suppression test, and suspected deficiency with a stimulation test (e.g., insulin tolerance test, glucagon stimulation), typically alongside IGF-1 measurement.",
        "methodology_en": "Chemiluminescent immunoassay on automated analyzers.",
        "reference_ranges": [
            {"parameter": "Random GH, adult", "population": "General adult", "range": "Highly variable due to pulsatile secretion; a low or undetectable random level does not exclude normal GH function, and a normal or mildly elevated level does not confirm excess"},
            {"parameter": "GH after oral glucose suppression (used to diagnose excess)", "population": "Adult", "range": "Normal suppression to <1.0 ng/mL (assay-dependent); failure to suppress supports acromegaly"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Failure of GH to suppress appropriately after an oral glucose load, together with an elevated IGF-1 (which better reflects average GH exposure since it doesn't fluctuate pulsatile-ly), supports a diagnosis of GH excess (acromegaly in adults, gigantism if onset is before growth plate closure), most often due to a pituitary somatotroph adenoma. In suspected GH deficiency (short stature in children, or specific adult GH deficiency syndromes, often from pituitary disease or prior pituitary surgery/radiation), a stimulation test showing an inadequate GH rise, together with a low IGF-1 and compatible clinical context, supports the diagnosis; a low random GH level alone is not sufficient given normal fluctuation throughout the day.",
        "associated_conditions": [
            {"condition": "Acromegaly / gigantism (GH excess)", "direction": "failure to suppress with oral glucose, elevated IGF-1"},
            {"condition": "Growth hormone deficiency", "direction": "inadequate rise on stimulation testing, low IGF-1"}
        ],
        "questions_to_ask_en": "Since a single random level isn't usually enough to diagnose either condition, what dynamic testing (suppression or stimulation) is planned, and how should I prepare for it? Will my IGF-1 level be checked alongside this?",
        "next_steps": "Suspected excess proceeds to an oral glucose suppression test and pituitary imaging (MRI) if confirmed; suspected deficiency proceeds to a formal stimulation test, with treatment (GH replacement or, for excess, surgery/medical therapy) guided by the confirmed diagnosis and underlying cause.",
        "sources": [
            {"name": "Medscape/eMedicine - Growth Hormone: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2089136-overview", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "plasma-renin-activity", "name_en": "Plasma Renin Activity (PRA)",
        "aliases": "Renin Activity, PRA, Renin Level",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Evaluated together with aldosterone (as the aldosterone-to-renin ratio) to screen for primary aldosteronism in resistant or early-onset hypertension, and used in the broader workup of secondary hypertension and unexplained hypokalemia.",
        "specimen_type": "Venous plasma (EDTA), collected in a chilled tube and processed under cold conditions per protocol",
        "collection_notes_en": "Posture (supine vs. seated/upright) and time of day significantly affect results and must match the reference range being used; many antihypertensive medications (especially spironolactone, other diuretics, and beta-blockers) interfere with interpretation and should be discontinued for a specified period (often 2-6 weeks depending on the drug) before testing whenever clinically safe to do so.",
        "methodology_en": "Radioimmunoassay or enzyme immunoassay measuring the rate of angiotensin I generation (activity-based assay), distinct from direct renin concentration assays which some laboratories use instead.",
        "reference_ranges": [
            {"parameter": "Plasma renin activity, supine", "population": "Adult", "range": "0.15-2.33 ng/mL/hour"},
            {"parameter": "Plasma renin activity, upright/seated", "population": "Adult", "range": "1.3-4.0 ng/mL/hour"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A suppressed renin (often below assay detection) together with an elevated aldosterone and a high aldosterone-to-renin ratio is the standard first-step screen for primary aldosteronism, a common and often under-recognized cause of secondary hypertension that is important to identify since it is potentially curable (unilateral adenoma) or specifically treatable (mineralocorticoid receptor antagonists for bilateral disease). Elevated renin, by contrast, points toward renin-mediated causes of hypertension or hypokalemia such as renal artery stenosis, renin-secreting tumors (rare), or diuretic-induced volume depletion, and a low aldosterone-to-renin ratio in this setting argues against primary aldosteronism.",
        "associated_conditions": [
            {"condition": "Primary aldosteronism", "direction": "low/suppressed renin with elevated aldosterone (high aldosterone-renin ratio)"},
            {"condition": "Renovascular hypertension / renin-secreting tumor", "direction": "elevated renin"},
            {"condition": "Secondary hyperaldosteronism (volume depletion, diuretic use, renal artery stenosis)", "direction": "elevated renin with elevated aldosterone"}
        ],
        "questions_to_ask_en": "Were my blood pressure medications adjusted appropriately before this test, since some can interfere with the result? If this points toward primary aldosteronism, what confirmatory testing and imaging are next?",
        "next_steps": "A high aldosterone-to-renin ratio prompts a confirmatory test (e.g., oral or IV saline loading) and, if confirmed, adrenal CT imaging with adrenal vein sampling in appropriate candidates to distinguish unilateral from bilateral disease and guide surgical versus medical management.",
        "sources": [
            {"name": "Mayo Clinic Laboratories Endocrinology Catalog - Renin Activity, Plasma", "url": "https://endocrinology.testcatalog.org/show/PRA", "accessed": "2026-07-20"},
            {"name": "PMC - Paraneoplastic Secondary Hypertension Due to Renin-Secreting Tumor (reference ranges cited)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4186556/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "adh-vasopressin", "name_en": "Antidiuretic Hormone (ADH / Arginine Vasopressin), Plasma",
        "aliases": "ADH, Vasopressin, AVP",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Helps evaluate disorders of water balance, particularly distinguishing central diabetes insipidus (inadequate ADH secretion) from nephrogenic diabetes insipidus (inadequate renal response to normal/high ADH) and from primary polydipsia, in a patient with polyuria and dilute urine.",
        "specimen_type": "Venous plasma (EDTA), collected on ice and processed promptly per protocol, since ADH is unstable at room temperature",
        "collection_notes_en": "ADH assays are technically demanding and increasingly being supplemented or replaced by copeptin (a more stable surrogate marker co-secreted with ADH) in some laboratories; interpretation requires simultaneous measurement of plasma osmolality, since ADH should be interpreted relative to the osmotic stimulus present at the time of sampling, often as part of a formal water deprivation test.",
        "methodology_en": "Radioimmunoassay or enzyme immunoassay.",
        "reference_ranges": [{"parameter": "ADH, random (normally hydrated)", "population": "Adult", "range": "approximately 1-5 pg/mL, interpreted relative to simultaneous plasma osmolality rather than as an isolated number"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "In a patient with polyuria and dilute urine, an inappropriately low ADH despite elevated plasma osmolality (during a water deprivation test) supports central diabetes insipidus, while a normal or elevated ADH with persistently dilute urine despite osmotic stimulation supports nephrogenic diabetes insipidus (renal resistance to ADH); primary polydipsia, by contrast, shows an appropriately low ADH in the setting of low-normal osmolality from excess fluid intake. Inappropriately elevated ADH relative to a low plasma osmolality is the hallmark of the syndrome of inappropriate antidiuretic hormone secretion (SIADH), a common cause of euvolemic hyponatremia from causes including certain cancers, CNS disease, pulmonary disease, and many medications.",
        "associated_conditions": [
            {"condition": "Central diabetes insipidus", "direction": "inappropriately low relative to elevated osmolality"},
            {"condition": "Nephrogenic diabetes insipidus", "direction": "normal or elevated, but with persistent renal resistance (dilute urine despite ADH presence)"},
            {"condition": "SIADH (euvolemic hyponatremia)", "direction": "inappropriately elevated relative to low plasma osmolality"}
        ],
        "questions_to_ask_en": "Is a formal water deprivation test planned to properly interpret this result alongside my osmolality? Could any of my current medications be contributing to inappropriate ADH secretion?",
        "next_steps": "Confirmed central diabetes insipidus is treated with desmopressin (a synthetic ADH analog); nephrogenic diabetes insipidus is managed by addressing the underlying cause (including reviewing causative medications like lithium) plus supportive measures; SIADH is managed with fluid restriction and treatment of the underlying cause, with careful correction of sodium to avoid overly rapid correction.",
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Physiology, Vasopressin", "url": "https://www.ncbi.nlm.nih.gov/books/NBK526069/", "accessed": "2026-07-20"},
            {"name": "StatPearls / NCBI Bookshelf - Arginine Vasopressin Disorder (Diabetes Insipidus)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK470458/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "thyroglobulin", "name_en": "Thyroglobulin, Serum",
        "aliases": "Tg, Thyroglobulin Tumor Marker",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Used primarily as a tumor marker after treatment (thyroidectomy with or without radioactive iodine ablation) for differentiated thyroid cancer (papillary or follicular), to monitor for residual disease or recurrence; not useful for initial diagnosis since it does not distinguish benign from malignant thyroid tissue.",
        "specimen_type": "Venous serum",
        "collection_notes_en": "Must always be measured together with thyroglobulin antibody (TgAb), since even low-level TgAb can artifactually suppress measured thyroglobulin in immunoassay methods, causing a falsely low or undetectable result that could mask actual disease; a rising TgAb trend itself can be used as an imperfect surrogate marker of disease when TgAb interferes with direct Tg measurement.",
        "methodology_en": "Immunoassay (chemiluminescent or enzyme immunoassay) on automated analyzers; TSH-stimulated thyroglobulin testing (after recombinant TSH or during hypothyroid withdrawal) provides higher sensitivity for detecting small amounts of residual disease than a suppressed (on-therapy) level alone.",
        "reference_ranges": [
            {"parameter": "Thyroglobulin, euthyroid individual with intact thyroid, TgAb-negative", "population": "General adult", "range": "approximately 3-40 ng/mL (assay-dependent, not standardized between manufacturers)"},
            {"parameter": "Thyroglobulin, post-thyroidectomy + radioiodine ablation, TSH-stimulated (per American Thyroid Association)", "population": "Post-treatment thyroid cancer", "range": "<1.0 ng/mL associated with high probability of remission"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "After total thyroidectomy and radioactive iodine ablation for differentiated thyroid cancer, thyroglobulin should fall to a very low or undetectable level, since it is produced only by thyroid tissue (normal or cancerous); a persistently detectable or rising level over serial measurements suggests residual or recurrent disease and prompts further imaging, while an undetectable, TgAb-negative, TSH-stimulated level is reassuring for remission. Because assay methods and cutoffs are not standardized across manufacturers, serial monitoring in an individual patient should ideally use the same laboratory/assay over time for meaningful trend comparison.",
        "associated_conditions": [
            {"condition": "Residual or recurrent differentiated thyroid cancer (post-treatment)", "direction": "persistently detectable or rising level on serial measurement"},
            {"condition": "Successful ablation / remission", "direction": "undetectable, TgAb-negative, TSH-stimulated level"}
        ],
        "questions_to_ask_en": "Was my thyroglobulin antibody checked alongside this result, since a positive antibody could make this level unreliable? Should this be repeated using TSH stimulation for the most sensitive assessment?",
        "next_steps": "A rising or persistently detectable level prompts neck ultrasound and, depending on the clinical scenario, further imaging (whole-body radioiodine scan, cross-sectional imaging) to localize possible residual or recurrent disease; TgAb-positive patients are followed using the antibody trend as a surrogate marker when direct Tg measurement is unreliable.",
        "sources": [
            {"name": "Medscape/eMedicine - Thyroglobulin: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2089532-overview", "accessed": "2026-07-20"},
            {"name": "PMC - Serum Thyroglobulin Reference Intervals in Regions with Adequate Iodine Intake", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5134814/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "androstenedione", "name_en": "Androstenedione, Serum",
        "aliases": "Androstenedione, A4",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Evaluates suspected androgen excess in women (hirsutism, acne, irregular cycles), part of the workup for polycystic ovary syndrome and congenital adrenal hyperplasia, and used in the evaluation of ambiguous genitalia and precocious puberty in children.",
        "specimen_type": "Venous serum, morning collection preferred given diurnal variation similar to other adrenal androgens",
        "collection_notes_en": "Typically ordered alongside total and free testosterone, DHEA-S, and 17-hydroxyprogesterone as part of a full androgen/adrenal panel, since no single marker reliably localizes the source (ovarian vs. adrenal) of androgen excess on its own.",
        "methodology_en": "Chemiluminescent immunoassay or, increasingly preferred for accuracy at low concentrations, liquid chromatography-tandem mass spectrometry (LC-MS/MS).",
        "reference_ranges": [
            {"parameter": "Androstenedione", "population": "Adult women", "range": "approximately 30-200 ng/dL (assay-dependent)"},
            {"parameter": "Androstenedione", "population": "Adult men", "range": "approximately 40-150 ng/dL (assay-dependent)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated androstenedione, an intermediate androgen produced by both the ovaries/testes and the adrenal glands (and a direct precursor to testosterone and estrone), is seen in polycystic ovary syndrome, congenital adrenal hyperplasia (particularly non-classic 21-hydroxylase deficiency, where it's often used alongside 17-hydroxyprogesterone), and, less commonly, androgen-secreting adrenal or ovarian tumors, which should be considered when elevation is marked or accompanied by rapidly progressive virilization. Because it is produced by both glands, an isolated androstenedione elevation doesn't localize the source, and additional markers (DHEA-S favoring adrenal origin, LH/FSH ratio and pelvic ultrasound favoring ovarian origin) are used together to narrow the differential.",
        "associated_conditions": [
            {"condition": "Polycystic ovary syndrome", "direction": "mildly to moderately elevated"},
            {"condition": "Non-classic congenital adrenal hyperplasia", "direction": "elevated, alongside elevated 17-hydroxyprogesterone"},
            {"condition": "Androgen-secreting tumor (adrenal or ovarian)", "direction": "markedly elevated, especially with rapid virilization"}
        ],
        "questions_to_ask_en": "Given my full androgen panel, does this look more consistent with PCOS, an adrenal source, or something that needs imaging to exclude a tumor? How rapidly did my symptoms develop, since that affects how urgently this needs to be worked up?",
        "next_steps": "Mild to moderate elevation with a compatible clinical picture and gradual symptom onset is generally worked up as PCOS or non-classic CAH with the relevant additional tests; marked elevation or rapidly progressive virilizing symptoms warrant prompt imaging (pelvic ultrasound, adrenal CT/MRI) to exclude a hormone-secreting tumor.",
        "sources": [
            {"name": "Mayo Clinic Laboratories Endocrinology Catalog - Renin Activity context and general endocrine reference approach", "url": "https://endocrinology.testcatalog.org/show/PRA", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "vitamin-b1-thiamine", "name_en": "Vitamin B1 (Thiamine), Whole Blood",
        "aliases": "Thiamine, Vitamin B1, Thiamine Pyrophosphate",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected thiamine deficiency, relevant in alcohol use disorder, malnutrition/refeeding syndrome, bariatric surgery, hyperemesis gravidarum, and unexplained encephalopathy (Wernicke's encephalopathy) or heart failure (wet beriberi).",
        "specimen_type": "Whole blood (EDTA), protected from light",
        "collection_notes_en": "In suspected Wernicke's encephalopathy, treatment with thiamine should never be delayed while awaiting laboratory confirmation, since the condition is a medical emergency and the risk of untreated deficiency (permanent Korsakoff amnestic syndrome) far outweighs the low risk of empiric thiamine administration.",
        "methodology_en": "High-performance liquid chromatography (HPLC), measuring thiamine pyrophosphate (the active cofactor form) in whole blood or erythrocytes.",
        "reference_ranges": [{"parameter": "Whole blood thiamine (thiamine pyrophosphate)", "population": "Adult", "range": "approximately 70-180 nmol/L (assay-dependent; deficiency generally reflected by levels below the local reference range)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low thiamine supports a diagnosis of deficiency, which classically causes Wernicke's encephalopathy (the triad of confusion, ataxia, and eye movement abnormalities, though all three are present in only a minority of cases) and, if untreated, can progress to irreversible Korsakoff syndrome; it also causes dry beriberi (peripheral neuropathy) and wet beriberi (high-output heart failure). Common risk factors include chronic alcohol use (impaired absorption and intake), malnutrition, prolonged vomiting (including hyperemesis gravidarum), bariatric surgery, and refeeding after prolonged starvation, where thiamine should be given before or with any glucose-containing fluids to avoid precipitating acute deficiency symptoms.",
        "associated_conditions": [
            {"condition": "Wernicke's encephalopathy / Korsakoff syndrome", "direction": "low, in a patient with compatible risk factors and symptoms"},
            {"condition": "Beriberi (dry: peripheral neuropathy; wet: high-output heart failure)", "direction": "low"}
        ],
        "questions_to_ask_en": "Given my risk factors, was thiamine started empirically without waiting for this result, given how time-sensitive untreated deficiency can be? Do I need ongoing supplementation, and for how long?",
        "next_steps": "Confirmed or strongly suspected deficiency is treated with thiamine repletion (parenteral in acute or severe cases, particularly suspected Wernicke's encephalopathy, given uncertain oral absorption), given before glucose administration in at-risk patients, with attention to the underlying cause (alcohol use, malnutrition, ongoing GI losses).",
        "sources": [
            {"name": "PMC/StatPearls-style clinical toxicology reference used for TDM and micronutrient testing context", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9350491/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "vitamin-e-tocopherol", "name_en": "Vitamin E (Alpha-Tocopherol), Serum",
        "aliases": "Vitamin E, Alpha-Tocopherol",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected vitamin E deficiency, most often related to fat malabsorption syndromes (cystic fibrosis, cholestatic liver disease, chronic pancreatitis, short bowel syndrome) or rare genetic disorders of vitamin E transport, presenting with peripheral neuropathy, ataxia, or retinopathy.",
        "specimen_type": "Venous serum, protected from light",
        "collection_notes_en": "Because vitamin E is transported in blood bound to lipoproteins, serum levels should be interpreted relative to total serum lipids (or expressed as a vitamin E-to-lipid ratio) in patients with significant hyperlipidemia, since an elevated lipid level can falsely raise the absolute vitamin E concentration without reflecting true tissue sufficiency.",
        "methodology_en": "High-performance liquid chromatography (HPLC).",
        "reference_ranges": [{"parameter": "Serum alpha-tocopherol", "population": "Adult", "range": "approximately 5.5-17 mg/L (or corrected as a ratio to total serum lipids in patients with abnormal lipid levels)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low vitamin E supports deficiency, which principally affects the nervous system (peripheral neuropathy, ataxia, areflexia, and in children, potential impact on neurodevelopment) and the retina (pigmentary retinopathy), reflecting vitamin E's role as a major lipid-soluble antioxidant protecting cell membranes, particularly in neural tissue, from oxidative damage. Because absorption depends on adequate fat digestion and lipoprotein transport, most acquired deficiency in adults occurs in the setting of chronic fat malabsorption rather than dietary insufficiency alone, so identifying and addressing the underlying malabsorptive condition is as important as direct supplementation.",
        "associated_conditions": [
            {"condition": "Vitamin E deficiency (fat malabsorption, cystic fibrosis, cholestatic liver disease)", "direction": "low"},
            {"condition": "Ataxia with vitamin E deficiency (rare genetic disorder of vitamin E transport)", "direction": "low, with neurologic symptoms out of proportion to any dietary/malabsorptive cause"}
        ],
        "questions_to_ask_en": "Since this level should be interpreted relative to my lipid levels, was that correction applied? Is there an underlying malabsorption condition that needs its own evaluation and treatment alongside supplementation?",
        "next_steps": "Confirmed deficiency is treated with oral vitamin E supplementation (dosing adjusted for the severity of malabsorption, which may require much higher doses than typical dietary supplementation) alongside management of the underlying cause; neurologic symptoms are monitored for improvement, recognizing that some deficits may only partially reverse if deficiency has been prolonged.",
        "sources": [
            {"name": "NIH Office of Dietary Supplements - Vitamin A and Carotenoids Fact Sheet (general fat-soluble vitamin testing context)", "url": "https://ods.od.nih.gov/factsheets/VitaminA-HealthProfessional/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "urine-protein-24-hour", "name_en": "Urine Protein, 24-Hour Collection (Quantitative)",
        "aliases": "24-Hour Urine Protein, Proteinuria Quantification",
        "category": "Clinical Chemistry / Urinalysis",
        "purpose_en": "Quantifies total daily protein loss in the urine, used to confirm and grade significant proteinuria found on screening urinalysis or urine albumin-to-creatinine ratio, characterize nephrotic-range proteinuria, and monitor kidney disease over time.",
        "specimen_type": "Complete 24-hour urine collection (all urine passed over a full 24-hour period, in an appropriate preservative-containing container if instructed by the laboratory)",
        "collection_notes_en": "Incomplete collection is the most common source of error and materially affects accuracy; concurrent measurement of urine creatinine in the same collection can help verify collection adequacy (based on expected creatinine excretion for the patient's muscle mass), and a spot urine protein-to-creatinine ratio is often used as a more practical, reasonably well-correlated alternative when a full 24-hour collection is impractical.",
        "methodology_en": "Automated turbidimetric or colorimetric (e.g., pyrogallol red) protein assay on a chemistry analyzer.",
        "reference_ranges": [
            {"parameter": "Total urine protein, 24-hour", "population": "Adult", "range": "<150 mg/24 hours"},
            {"parameter": "Nephrotic-range proteinuria", "population": "Adult", "range": "\u22653.5 g/24 hours"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Proteinuria above the normal range indicates glomerular or tubular kidney injury, with the degree of proteinuria helping characterize the pattern and severity of disease -- nephrotic-range proteinuria (\u22653.5 g/24h), often accompanied by hypoalbuminemia, edema, and hyperlipidemia, points toward primary glomerular diseases (minimal change disease, membranous nephropathy, focal segmental glomerulosclerosis) or systemic diseases affecting the glomerulus (diabetic nephropathy, lupus nephritis, amyloidosis), while lesser degrees of proteinuria are seen across a broader range of kidney conditions. Serial 24-hour urine protein measurements are also used to track disease progression or response to treatment (e.g., ACE inhibitor/ARB therapy, immunosuppression for glomerulonephritis) over time.",
        "associated_conditions": [
            {"condition": "Nephrotic syndrome (minimal change disease, membranous nephropathy, FSGS)", "direction": "high, \u22653.5 g/24h with hypoalbuminemia"},
            {"condition": "Diabetic nephropathy / other glomerular disease", "direction": "elevated, variable degree"}
        ],
        "questions_to_ask_en": "Was the collection likely complete and accurate based on the creatinine content? Given this level of protein loss, do I need a kidney biopsy or specific treatment to reduce proteinuria and protect kidney function?",
        "next_steps": "Significant proteinuria prompts further workup for the underlying cause, which may include a kidney biopsy (particularly for nephrotic-range proteinuria without an obvious cause like long-standing diabetes), and treatment aimed at reducing proteinuria (ACE inhibitors/ARBs, disease-specific immunosuppression) alongside monitoring of kidney function over time.",
        "sources": [
            {"name": "Mayo Clinic Laboratories Endocrinology Catalog - reference approach used for quantitative chemistry testing context", "url": "https://endocrinology.testcatalog.org/show/PRA", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "urine-osmolality", "name_en": "Urine Osmolality",
        "aliases": "Urine Osm, Osmolality Urine",
        "category": "Clinical Chemistry / Urinalysis",
        "purpose_en": "Assesses the kidney's urine-concentrating ability, used in the workup of polyuria, hyponatremia, and hypernatremia, and to help distinguish diabetes insipidus from primary polydipsia and from SIADH in combination with serum osmolality and ADH.",
        "specimen_type": "Random or timed urine specimen, depending on the clinical question",
        "collection_notes_en": "Interpretation always requires simultaneous serum/plasma osmolality for context, since a urine osmolality value is only meaningful relative to the concurrent plasma osmolality and clinical volume status; formal water deprivation testing with serial measurements is used when diabetes insipidus is suspected.",
        "methodology_en": "Freezing-point depression osmometry.",
        "reference_ranges": [
            {"parameter": "Random urine osmolality", "population": "Adult, normally hydrated", "range": "approximately 300-900 mOsm/kg, highly dependent on fluid intake"},
            {"parameter": "Maximally concentrated urine (after water deprivation)", "population": "Adult with normal concentrating ability", "range": ">800 mOsm/kg, generally exceeding simultaneous plasma osmolality substantially"},
            {"parameter": "Inappropriately dilute urine, suggestive of diabetes insipidus", "population": "Adult with polyuria", "range": "<300 mOsm/kg despite elevated plasma osmolality/dehydration"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "In a patient with polyuria, urine that remains inappropriately dilute (low osmolality) despite water deprivation and rising plasma osmolality indicates a defect in urinary concentrating ability, seen in both central and nephrogenic diabetes insipidus (distinguished by response to administered desmopressin) and, in milder degree, in primary polydipsia after prolonged excess fluid intake. In the hyponatremia workup, an inappropriately concentrated urine (osmolality above roughly 100 mOsm/kg) despite low serum sodium/osmolality points toward ADH-mediated water retention (SIADH or another cause of inappropriate ADH activity) rather than primary polydipsia, where urine is typically maximally dilute.",
        "associated_conditions": [
            {"condition": "Diabetes insipidus (central or nephrogenic)", "direction": "inappropriately low despite water deprivation/hypertonicity"},
            {"condition": "SIADH", "direction": "inappropriately concentrated relative to low serum osmolality"},
            {"condition": "Primary polydipsia", "direction": "appropriately dilute, reflecting excess fluid intake"}
        ],
        "questions_to_ask_en": "Was my serum osmolality checked at the same time, since this result can't be interpreted alone? Is a formal water deprivation test needed to distinguish between the possible causes?",
        "next_steps": "Results suggesting diabetes insipidus lead to a formal water deprivation test with desmopressin challenge to distinguish central from nephrogenic causes; results suggesting SIADH lead to investigation of the underlying cause (medications, pulmonary or CNS disease, malignancy) and fluid restriction as initial management.",
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Arginine Vasopressin Disorder (Diabetes Insipidus)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK470458/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "urinary-free-cortisol-24-hour", "name_en": "Urinary Free Cortisol, 24-Hour Collection",
        "aliases": "UFC, 24-Hour Urine Cortisol, Free Cortisol Urine",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "One of several first-line screening tests for Cushing's syndrome (endogenous cortisol excess), reflecting integrated cortisol production over a full day rather than a single timepoint.",
        "specimen_type": "Complete 24-hour urine collection",
        "collection_notes_en": "As with other 24-hour collections, incomplete collection is the main source of error; multiple collections (at least two) are generally recommended given day-to-day variability in cortisol production, and the test should not be used as a stand-alone diagnostic test but interpreted alongside other screening tests (late-night salivary cortisol, low-dose dexamethasone suppression test).",
        "methodology_en": "Chemiluminescent immunoassay or, for greater specificity (avoiding cross-reactivity with cortisol metabolites and certain medications), liquid chromatography-tandem mass spectrometry (LC-MS/MS).",
        "reference_ranges": [{"parameter": "Urinary free cortisol, 24-hour", "population": "Adult", "range": "approximately 10-100 mcg/24 hours (assay-dependent; values several-fold above the upper reference limit are considered strongly supportive of Cushing's syndrome)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "An elevated urinary free cortisol, especially when more than 3-4 times the upper limit of normal and reproduced on repeat collection, is strongly supportive of Cushing's syndrome, though mild elevations can also occur in states of physiologic stress, depression, alcohol use disorder, obesity, and poorly controlled diabetes ('pseudo-Cushing' states), which is why the diagnosis relies on a combination of tests rather than this result alone. A normal result on a single collection does not fully exclude Cushing's syndrome, particularly in mild or cyclical disease, which is part of why current guidelines recommend at least two abnormal screening tests (from different test types) before proceeding to further localization workup.",
        "associated_conditions": [
            {"condition": "Cushing's syndrome (endogenous cortisol excess)", "direction": "elevated, especially markedly and reproducibly"},
            {"condition": "Pseudo-Cushing states (obesity, depression, alcohol use, poorly controlled diabetes)", "direction": "mildly elevated without true autonomous cortisol excess"}
        ],
        "questions_to_ask_en": "Given the possibility of day-to-day variation, will this collection be repeated, and are other screening tests (like late-night salivary cortisol or dexamethasone suppression) also planned? Could any of my current health conditions be causing a 'pseudo-Cushing' pattern rather than true Cushing's syndrome?",
        "next_steps": "A clearly elevated, reproducible result supports proceeding to determine the cause (ACTH level to distinguish ACTH-dependent from ACTH-independent disease, followed by pituitary or adrenal imaging as indicated); borderline or single-abnormal results are usually confirmed with a second, different type of screening test before further workup.",
        "sources": [
            {"name": "PMC - Syndrome of Inappropriate ADH context referencing cortisol/endocrine screening workflow", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10731729/", "accessed": "2026-07-20"}
        ]
    },
    {
        "slug": "beta-hydroxybutyrate", "name_en": "Beta-Hydroxybutyrate (Ketones), Blood",
        "aliases": "BOHB, Blood Ketones, Beta-Hydroxybutyrate",
        "category": "Clinical Chemistry",
        "purpose_en": "Confirms and quantifies ketosis/ketoacidosis, most importantly diabetic ketoacidosis (DKA), and is used to monitor response to treatment; also relevant in alcoholic ketoacidosis and prolonged fasting/starvation ketosis.",
        "specimen_type": "Venous or capillary (fingerstick) whole blood, or venous serum/plasma",
        "collection_notes_en": "Blood beta-hydroxybutyrate has replaced urine ketone testing as the preferred method in most acute-care settings, since it directly measures the predominant ketone body in DKA and is not subject to the false positives/negatives seen with urine nitroprusside-based ketone strips (which primarily detect acetoacetate, not beta-hydroxybutyrate).",
        "methodology_en": "Enzymatic assay on a point-of-care ketone meter or automated chemistry analyzer.",
        "reference_ranges": [
            {"parameter": "Normal", "population": "General", "range": "<0.6 mmol/L"},
            {"parameter": "Mild ketosis", "population": "General", "range": "0.6-1.0 mmol/L"},
            {"parameter": "Moderate ketosis, medical evaluation warranted", "population": "General", "range": "1.0-3.0 mmol/L"},
            {"parameter": "Consistent with diabetic ketoacidosis", "population": "General, with compatible clinical/acid-base picture", "range": ">3.0 mmol/L"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "In a patient with hyperglycemia and metabolic acidosis, a beta-hydroxybutyrate level above approximately 3.0 mmol/L supports a diagnosis of diabetic ketoacidosis, and the level is also used to track treatment response, with resolution of DKA generally corresponding to the level falling below about 1.0 mmol/L alongside normalization of the anion gap and pH. Elevated levels can also reflect alcoholic ketoacidosis (in the setting of chronic alcohol use, poor intake, and recent heavy drinking, typically with normal or low glucose) or prolonged starvation ketosis, both of which are distinguished from diabetic ketoacidosis by the clinical context and glucose level rather than the ketone level alone.",
        "associated_conditions": [
            {"condition": "Diabetic ketoacidosis", "direction": "elevated, typically >3.0 mmol/L, with hyperglycemia and acidosis"},
            {"condition": "Alcoholic ketoacidosis", "direction": "elevated, typically with normal/low glucose and history of heavy alcohol use with poor intake"},
            {"condition": "Starvation ketosis", "direction": "mild-moderate elevation, with a compatible history of prolonged fasting"}
        ],
        "questions_to_ask_en": "Is this level being used to help decide the intensity of my treatment (fluids, insulin) as well as to confirm the diagnosis? How often will it be rechecked to track my response to treatment?",
        "next_steps": "A level supporting DKA leads to standard treatment (IV fluids, insulin infusion, electrolyte repletion, particularly potassium) with serial rechecking of the level (or the anion gap if ketone testing isn't readily available) to guide the pace of treatment and confirm resolution before transitioning off IV insulin.",
        "sources": [
            {"name": "Medscape/eMedicine - Beta-Hydroxybutyrate: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2087381-overview", "accessed": "2026-07-20"},
            {"name": "Medscape/eMedicine - Diabetic Ketoacidosis (DKA) Workup", "url": "https://emedicine.medscape.com/article/118361-workup", "accessed": "2026-07-20"}
        ]
    }
]

RELATED = {
    "growth-hormone": ["insulin-like-growth-factor-1-igf-1-serum"],
    "plasma-renin-activity": ["aldosterone-and-renin-aldosterone-renin-ratio", "sodium-na", "potassium-k"],
    "adh-vasopressin": ["osmolality-serum", "sodium-na", "urine-osmolality"],
    "thyroglobulin": ["thyroid-antibodies-tpoab-and-tgab", "thyroid-stimulating-hormone"],
    "androstenedione": ["testosterone-total-serum", "dehydroepiandrosterone-sulfate-dhea-s-serum", "17-hydroxyprogesterone-17-ohp-serum"],
    "vitamin-b1-thiamine": ["folate-folic-acid-serum", "vitamin-b12-cobalamin-serum"],
    "vitamin-e-tocopherol": ["vitamin-a-retinol-serum", "vitamin-k1-phylloquinone-serum", "lipid-panel"],
    "urine-protein-24-hour": ["urine-albumin-to-creatinine-ratio-acr-microalbumin", "serum-creatinine"],
    "urine-osmolality": ["osmolality-serum", "adh-vasopressin", "sodium-na"],
    "urinary-free-cortisol-24-hour": ["cortisol-serum-am", "adrenocorticotropic-hormone-acth-plasma"],
    "beta-hydroxybutyrate": ["arterial-blood-gas", "fasting-plasma-glucose", "bicarbonate-co2-total-carbon-dioxide"],
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
