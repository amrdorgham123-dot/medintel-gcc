"""
Seed script (batch 8) for MedForsa GCC's Lab Info reference library.
Adds core microbiology tests. English-only content per platform policy.

Run once: python3 seed_lab_tests_batch8.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "blood-culture", "name_en": "Blood Culture",
        "aliases": "BC, Blood C&S, Culture and Sensitivity (Blood)",
        "category": "Microbiology",
        "purpose_en": "Detects bacteria or fungi circulating in the bloodstream (bacteremia/fungemia); the cornerstone diagnostic test for suspected sepsis, endocarditis, and other serious bloodstream infections.",
        "specimen_type": "Venous whole blood, drawn directly into aerobic and anaerobic blood culture bottles",
        "collection_notes_en": "Strict aseptic skin preparation is essential to minimize contamination. Two or more culture sets should be drawn from separate venipuncture sites (not through an existing IV line unless specifically evaluating catheter-related infection), ideally before starting antibiotics, since prior antibiotic exposure can cause false-negative results. Adequate blood volume per bottle significantly improves sensitivity.",
        "methodology_en": "Inoculated bottles are incubated in a continuous-monitoring automated blood culture system (e.g., BACTEC, BacT/ALERT) that detects microbial growth via CO2/pressure changes; positive bottles are Gram-stained and subcultured for identification and antibiotic susceptibility testing, increasingly supplemented by rapid molecular identification panels.",
        "reference_ranges": [{"parameter": "Blood culture", "population": "Result categories", "range": "No growth (negative) after the standard incubation period (typically 5 days), or growth of a specific organism (positive) -- not a numeric value"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive blood culture requires distinguishing true bacteremia from contamination. Growth of a recognized pathogen (e.g., E. coli, S. aureus, Streptococcus pneumoniae) in one or more bottles is almost always clinically significant. Growth of common skin commensals (e.g., coagulase-negative staphylococci, Corynebacterium, Cutibacterium) in only one of multiple sets more often represents contamination, though the same organisms can cause true infection (e.g., catheter-related bloodstream infection), especially if grown from multiple separate draws. Results guide antibiotic selection via susceptibility testing and help monitor treatment response with repeat cultures in conditions like endocarditis.",
        "associated_conditions": [
            {"condition": "Sepsis / bacteremia / fungemia", "direction": "positive with a recognized pathogen"},
            {"condition": "Infective endocarditis", "direction": "persistently positive with a typical organism"},
            {"condition": "Blood culture contamination", "direction": "positive in only one of multiple sets, typical skin commensal"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Blood Culture: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2093349-overview", "accessed": "2026-07-14"},
            {"name": "PMC - A Guide to Bacterial Culture Identification And Results Interpretation", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6428495/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "urine-culture", "name_en": "Urine Culture",
        "aliases": "Urine C&S, Culture and Sensitivity (Urine)",
        "category": "Microbiology",
        "purpose_en": "Identifies and quantifies bacteria in urine to diagnose urinary tract infection (UTI) and guide antibiotic selection via susceptibility testing.",
        "specimen_type": "Clean-catch midstream urine, or catheterized/suprapubic aspirate specimen when indicated",
        "collection_notes_en": "Proper clean-catch technique (cleansing before collection, midstream collection) is essential to minimize contamination from perineal/urethral flora; the sample should reach the lab promptly or be refrigerated, since bacteria can multiply at room temperature and falsely raise the colony count.",
        "methodology_en": "Quantitative culture on selective/differential agar (e.g., blood agar, MacConkey agar) using a calibrated inoculating loop to determine colony-forming units per milliliter (CFU/mL); identification and susceptibility testing performed on significant growth.",
        "reference_ranges": [
            {"parameter": "Colony count, clean-catch midstream specimen", "population": "Traditional threshold for significant bacteriuria", "range": "\u2265100,000 CFU/mL (10^5) of a single uropathogen"},
            {"parameter": "Colony count, symptomatic patients (lower thresholds increasingly accepted)", "population": "IDSA-referenced lower thresholds", "range": "\u22651,000 CFU/mL (cystitis) or \u226510,000 CFU/mL (pyelonephritis) in symptomatic women, clean-catch"},
            {"parameter": "Colony count, catheterized specimen", "population": "Lower threshold applies", "range": "\u22651,000 CFU/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The classic 100,000 CFU/mL threshold (established in the 1950s) has high specificity but can miss up to half of symptomatic infections, so current guidance accepts lower colony counts as significant in symptomatic patients, particularly women and catheterized patients. Growth of multiple organism types (mixed flora) more often reflects contamination or, in catheterized patients, colonization rather than true infection, and is generally not worked up further. Asymptomatic bacteriuria (significant growth without symptoms) generally does not require treatment except in specific situations such as pregnancy or before urologic procedures involving mucosal trauma.",
        "associated_conditions": [
            {"condition": "Urinary tract infection (cystitis, pyelonephritis)", "direction": "positive, single uropathogen above the relevant threshold"},
            {"condition": "Asymptomatic bacteriuria", "direction": "positive, significant growth without symptoms -- treatment generally not indicated"},
            {"condition": "Sample contamination / catheter colonization", "direction": "mixed growth of multiple organisms"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Urine Culture: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2093272-overview", "accessed": "2026-07-14"},
            {"name": "ScienceDirect Topics - Urine Culture, citing 2010 IDSA consensus thresholds", "url": "https://www.sciencedirect.com/topics/medicine-and-dentistry/urine-culture", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "h-pylori-testing", "name_en": "Helicobacter pylori Testing (Stool Antigen / Urea Breath Test / Serology)",
        "aliases": "H. pylori, HP Stool Antigen, Urea Breath Test, H. pylori IgG",
        "category": "Microbiology / Immunoassay",
        "purpose_en": "Diagnoses active H. pylori infection, a major cause of peptic ulcer disease, chronic gastritis, and a risk factor for gastric cancer; also used non-invasively to confirm eradication after treatment.",
        "specimen_type": "Stool sample (stool antigen test), exhaled breath sample after ingesting labeled urea (urea breath test), or venous serum (serology)",
        "collection_notes_en": "Proton pump inhibitors, bismuth, and antibiotics can cause false-negative results on the stool antigen test and urea breath test, and are typically withheld for 1-2 weeks (PPIs) or 4 weeks (antibiotics/bismuth) before testing. Serology cannot distinguish active from past/resolved infection and is not recommended for confirming eradication.",
        "methodology_en": "Stool antigen: enzyme immunoassay (ELISA) or lateral-flow chromatographic immunoassay detecting H. pylori antigen in stool. Urea breath test: patient ingests 13C- or 14C-labeled urea; H. pylori urease splits the urea, releasing labeled CO2 that is detected in exhaled breath. Serology: enzyme immunoassay detecting IgG antibodies against H. pylori.",
        "reference_ranges": [{"parameter": "H. pylori test", "population": "Result categories", "range": "Negative or Positive -- qualitative result; serology may report a numeric index/titer but interpretation remains categorical (positive/negative/equivocal)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The urea breath test and stool antigen test are the preferred methods for both initial diagnosis and confirming eradication after treatment, because they detect active infection with good sensitivity and specificity (each generally 85-95%+ in most studies, though estimates vary by population and reference standard used). Serology is useful as an initial screening tool in populations not recently treated (high sensitivity, good negative predictive value to rule out infection), but a positive serology cannot distinguish current from past infection and should be confirmed with stool antigen or urea breath testing before treatment decisions, especially for confirming cure.",
        "associated_conditions": [
            {"condition": "Peptic ulcer disease", "direction": "positive"},
            {"condition": "Chronic gastritis", "direction": "positive"},
            {"condition": "Gastric cancer risk factor (chronic untreated infection)", "direction": "positive, long-standing"}
        ],
        "sources": [
            {"name": "ARUP Consult - Helicobacter pylori", "url": "https://arupconsult.com/content/helicobacter-pylori", "accessed": "2026-07-14"},
            {"name": "American Family Physician (AAFP) - Noninvasive Diagnostic Tests for Helicobacter pylori Infection", "url": "https://www.aafp.org/pubs/afp/issues/2019/0701/p16.html", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "gram-stain", "name_en": "Gram Stain",
        "aliases": "Gram Stain, Direct Smear",
        "category": "Microbiology",
        "purpose_en": "Rapid, same-day microscopic test that provides preliminary information about the presence, morphology, and Gram-reaction of bacteria in a clinical specimen, guiding initial (empiric) antibiotic therapy while culture results are pending.",
        "specimen_type": "Varies by clinical specimen: sputum, wound/abscess fluid, CSF, body fluid, or a positive blood culture broth, among others",
        "collection_notes_en": "Specimen quality matters significantly -- for example, a sputum sample with excessive squamous epithelial cells suggests oral contamination rather than a true lower respiratory sample and may be rejected or reported with a caveat.",
        "methodology_en": "A heat- or methanol-fixed smear is sequentially stained with crystal violet, iodine (mordant), an alcohol/acetone decolorizer, and a safranin counterstain; Gram-positive organisms retain the crystal violet-iodine complex and appear purple/blue, while Gram-negative organisms lose it during decolorization and take up the pink/red safranin counterstain. The smear is examined for organism morphology (cocci, bacilli, arrangement) and for host inflammatory cells (white blood cells).",
        "reference_ranges": [{"parameter": "Gram stain", "population": "Result categories", "range": "No organisms seen, or organisms present described by Gram reaction and morphology (e.g., 'Gram-positive cocci in clusters', 'Gram-negative bacilli') -- a descriptive, not numeric, result"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "The Gram stain gives clinicians same-day guidance on likely organism categories (e.g., Gram-positive cocci in clusters suggesting Staphylococcus, Gram-negative bacilli suggesting Enterobacteriaceae) to help select empiric antibiotics before final culture and susceptibility results (which take 24-72+ hours) are available. It also assesses specimen adequacy and the presence of inflammatory cells, which supports (or argues against) a true infectious process versus contamination/colonization. It does not identify the specific organism species or provide susceptibility data, which require culture.",
        "associated_conditions": [
            {"condition": "Guides empiric antibiotic selection pending culture", "direction": "organism morphology/Gram reaction observed"},
            {"condition": "Specimen quality/contamination assessment", "direction": "e.g., excess squamous cells in sputum suggesting oral contamination"}
        ],
        "sources": [{"name": "PMC - A Guide to Bacterial Culture Identification And Results Interpretation", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6428495/", "accessed": "2026-07-14"}]
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
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
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
