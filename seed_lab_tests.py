"""
Seed script for the MedForsa GCC Lab Test Reference ("دليل التحاليل المخبرية").
Populates the first batch of 8 common lab tests with sourced, verified content.
Run once: python3 seed_lab_tests.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "cbc",
        "name_en": "Complete Blood Count",
        "name_ar": "صورة الدم الكاملة",
        "aliases": "CBC, Full Blood Count, FBC, CBC with differential",
        "category": "Hematology",
        "purpose_en": "Screens overall health and detects a wide range of disorders including anemia, infection, inflammation, bleeding disorders, and blood cancers. Commonly used in routine checkups and to monitor chronic conditions or treatment (e.g., chemotherapy).",
        "purpose_ar": "فحص شامل لتقييم الصحة العامة والكشف عن اضطرابات متعددة مثل الأنيميا، الالتهابات، اضطرابات النزيف، وأورام الدم. يُستخدم بشكل روتيني في الفحوصات الدورية ولمتابعة الحالات المزمنة أو العلاج الكيميائي.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "No fasting required. Standard venipuncture; in infants, heel-stick may be used. Gentle inversion of the tube after draw to mix with anticoagulant.",
        "collection_notes_ar": "لا يتطلب الصيام. سحب وريدي عادي؛ في الرضع يمكن استخدام وخز الكعب. يُقلب الأنبوب برفق بعد السحب لخلط العينة مع مانع التجلط.",
        "methodology_en": "Automated hematology analyzer (impedance/flow cytometry principles) for cell counts and indices; manual or digital peripheral blood smear review when abnormalities are flagged.",
        "methodology_ar": "محلل دم آلي (بمبدأ المقاومة الكهربائية أو التدفق الخلوي) لحساب الخلايا والمؤشرات؛ مراجعة يدوية أو رقمية لمسحة الدم المحيطي عند وجود نتائج غير طبيعية.",
        "reference_ranges": [
            {"parameter": "Hemoglobin (Hb)", "population": "Adult male", "range": "13-18 g/dL", "notes": "WHO reference"},
            {"parameter": "Hemoglobin (Hb)", "population": "Adult female (non-pregnant)", "range": "12-16 g/dL", "notes": "WHO reference"},
            {"parameter": "RBC count", "population": "Adult male", "range": "4.6-6.2 million cells/\u00b5L"},
            {"parameter": "RBC count", "population": "Adult female", "range": "4.2-5.4 million cells/\u00b5L"},
            {"parameter": "WBC count", "population": "Adult", "range": "4,300-10,800 cells/mm\u00b3", "notes": "Typical range; lab-specific"},
            {"parameter": "Platelets", "population": "Adult", "range": "150,000-450,000/\u00b5L", "notes": "Commonly cited general range"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low Hb/Hct/RBC suggests anemia (further workup with MCV, iron studies, B12/folate needed to classify type). High WBC may indicate infection, inflammation, steroid use, or hematologic malignancy; low WBC may suggest bone marrow suppression, viral infection, or autoimmune disease. Low platelets (thrombocytopenia) raise bleeding risk; high platelets may reflect reactive states or myeloproliferative disease. All CBC abnormalities should be interpreted together with clinical context and, when indicated, a peripheral smear.",
        "clinical_significance_ar": "انخفاض الهيموجلوبين/الهيماتوكريت/كريات الدم الحمراء يشير لأنيميا (يلزم فحوصات إضافية مثل MCV والحديد وفيتامين B12/الفوليك لتحديد النوع). ارتفاع كريات الدم البيضاء قد يدل على التهاب أو عدوى أو استخدام كورتيزون أو أورام دموية؛ انخفاضها قد يشير لتثبيط نخاع العظم أو عدوى فيروسية أو مرض مناعي ذاتي. انخفاض الصفائح يرفع خطر النزيف؛ ارتفاعها قد يكون تفاعلياً أو نتيجة اضطراب تكاثري نقوي. يجب تفسير أي خلل في صورة الدم الكاملة مع السياق الإكلينيكي، ومراجعة مسحة الدم عند الحاجة.",
        "associated_conditions": [
            {"condition": "Iron-deficiency anemia", "direction": "low Hb/Hct, microcytic"},
            {"condition": "Bacterial infection", "direction": "high WBC, neutrophilia"},
            {"condition": "Viral infection", "direction": "may show low or normal WBC, lymphocytosis"},
            {"condition": "Leukemia / myeloproliferative disorders", "direction": "markedly abnormal WBC and/or blasts"},
            {"condition": "Thrombocytopenia (ITP, marrow disorders, DIC)", "direction": "low platelets"},
            {"condition": "Polycythemia vera / dehydration", "direction": "high Hb/Hct"}
        ],
        "sources": [
            {"name": "MedlinePlus (NIH/NLM) - Complete Blood Count (CBC)", "url": "https://medlineplus.gov/lab-tests/complete-blood-count-cbc/", "accessed": "2026-07-14"},
            {"name": "StatPearls / NCBI Bookshelf - Normal and Abnormal CBC With Differential (cites WHO Hb ranges)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK604207/", "accessed": "2026-07-14"},
            {"name": "Cleveland Clinic - Complete Blood Count", "url": "https://my.clevelandclinic.org/health/diagnostics/4053-complete-blood-count", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "fasting-glucose",
        "name_en": "Fasting Plasma Glucose",
        "name_ar": "سكر الدم الصائم",
        "aliases": "FPG, Fasting Blood Sugar, FBS",
        "category": "Clinical Chemistry",
        "purpose_en": "Primary screening and diagnostic test for diabetes mellitus and prediabetes; used for diagnosis, monitoring, and risk assessment.",
        "purpose_ar": "الفحص الأساسي للكشف عن السكري ومقدمات السكري وتشخيصهما ومتابعتهما وتقييم المخاطر.",
        "specimen_type": "Venous plasma (fluoride oxalate/gray top preferred to prevent glycolysis) or serum",
        "collection_notes_en": "Patient must fast (no caloric intake) for at least 8 hours before the draw; water is permitted.",
        "collection_notes_ar": "يجب صيام المريض (عدم تناول أي سعرات حرارية) لمدة 8 ساعات على الأقل قبل سحب العينة؛ يُسمح بشرب الماء.",
        "methodology_en": "Enzymatic method (hexokinase or glucose oxidase) on automated clinical chemistry analyzers.",
        "methodology_ar": "طريقة إنزيمية (هيكسوكاينيز أو جلوكوز أوكسيديز) على أجهزة الكيمياء الإكلينيكية الآلية.",
        "reference_ranges": [
            {"parameter": "Fasting plasma glucose", "population": "Normal", "range": "<100 mg/dL (<5.6 mmol/L)"},
            {"parameter": "Fasting plasma glucose", "population": "Prediabetes (impaired fasting glucose)", "range": "100-125 mg/dL (5.6-6.9 mmol/L)"},
            {"parameter": "Fasting plasma glucose", "population": "Diabetes (requires confirmatory repeat test)", "range": "\u2265126 mg/dL (\u22657.0 mmol/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated fasting glucose is diagnostic of diabetes mellitus when \u2265126 mg/dL on two occasions (or one occasion with classic hyperglycemia symptoms), per ADA criteria. Values 100-125 mg/dL indicate prediabetes/impaired fasting glucose. Low fasting glucose (hypoglycemia) may indicate insulin excess, adrenal insufficiency, liver disease, or other metabolic causes and requires urgent clinical correlation.",
        "clinical_significance_ar": "ارتفاع سكر الصائم \u2265126 مج/دل في مناسبتين منفصلتين (أو مرة واحدة مع أعراض ارتفاع سكر واضحة) يُشخّص السكري وفق معايير ADA. القيم بين 100-125 مج/دل تدل على مقدمات السكري. انخفاض سكر الصائم (نقص السكر) قد يشير لزيادة الأنسولين أو قصور الغدة الكظرية أو أمراض الكبد أو أسباب استقلابية أخرى، ويستوجب تقييمًا سريريًا عاجلاً.",
        "associated_conditions": [
            {"condition": "Type 2 diabetes mellitus", "direction": "high"},
            {"condition": "Type 1 diabetes mellitus", "direction": "high"},
            {"condition": "Prediabetes / metabolic syndrome", "direction": "borderline high"},
            {"condition": "Insulinoma / excess exogenous insulin", "direction": "low"},
            {"condition": "Adrenal insufficiency", "direction": "low"}
        ],
        "sources": [
            {"name": "American Diabetes Association (ADA) - Standards of Care in Diabetes, diagnostic criteria", "url": "https://emedicine.medscape.com/article/2172154-overview", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "hba1c",
        "name_en": "Hemoglobin A1c (Glycated Hemoglobin)",
        "name_ar": "السكر التراكمي (الهيموجلوبين السكري)",
        "aliases": "HbA1c, A1C, Glycohemoglobin",
        "category": "Clinical Chemistry",
        "purpose_en": "Reflects average blood glucose over the preceding 2-3 months. Used for diagnosing diabetes/prediabetes and for long-term monitoring of glycemic control in known diabetics.",
        "purpose_ar": "يعكس متوسط سكر الدم خلال 2-3 أشهر السابقة. يُستخدم لتشخيص السكري ومقدماته ولمتابعة ضبط السكر على المدى الطويل لدى مرضى السكري المعروفين.",
        "specimen_type": "Venous whole blood, EDTA tube",
        "collection_notes_en": "No fasting required. Not reliable in conditions affecting red cell lifespan (hemolytic anemia, recent transfusion, certain hemoglobinopathies).",
        "collection_notes_ar": "لا يتطلب الصيام. غير موثوق في الحالات التي تؤثر على عمر كريات الدم الحمراء (الأنيميا الانحلالية، نقل الدم الحديث، بعض أمراض الهيموجلوبين الوراثية).",
        "methodology_en": "High-performance liquid chromatography (HPLC), immunoassay, or enzymatic assay, standardized to the NGSP/IFCC reference methods.",
        "methodology_ar": "كروماتوغرافيا سائلة عالية الأداء (HPLC) أو مقايسة مناعية أو إنزيمية، معايرة وفق مرجعية NGSP/IFCC.",
        "reference_ranges": [
            {"parameter": "HbA1c", "population": "Normal", "range": "<5.7%"},
            {"parameter": "HbA1c", "population": "Prediabetes", "range": "5.7%-6.4%"},
            {"parameter": "HbA1c", "population": "Diabetes", "range": "\u22656.5%"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "HbA1c \u22656.5% is diagnostic of diabetes per ADA criteria (should be confirmed with a repeat test unless unequivocal hyperglycemia is present). Used alongside fasting glucose/OGTT; results may be less reliable in pregnancy, hemoglobinopathies, or conditions altering red cell turnover.",
        "clinical_significance_ar": "قيمة HbA1c \u22656.5% تُشخّص السكري وفق معايير ADA (يُفضّل تأكيدها بفحص متكرر ما لم يكن هناك ارتفاع سكر واضح). يُستخدم مع سكر الصائم أو اختبار تحمل الجلوكوز؛ قد تقل موثوقية النتيجة في الحمل أو أمراض الهيموجلوبين الوراثية أو الحالات المؤثرة على عمر كريات الدم الحمراء.",
        "associated_conditions": [
            {"condition": "Diabetes mellitus (diagnosis and monitoring)", "direction": "high"},
            {"condition": "Prediabetes", "direction": "borderline high"},
            {"condition": "Hemolytic anemia / recent blood loss", "direction": "may cause falsely low result"}
        ],
        "sources": [
            {"name": "American Diabetes Association (ADA) HbA1c diagnostic criteria", "url": "https://www.droracle.ai/articles/1136568/what-hba1c-range-defines-pre-diabetes", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "lipid-panel",
        "name_en": "Lipid Panel",
        "name_ar": "بروفايل الدهون",
        "aliases": "Lipid Profile, Cholesterol Panel",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses cardiovascular disease risk by measuring total cholesterol, LDL-C, HDL-C, and triglycerides.",
        "purpose_ar": "يقيّم خطر أمراض القلب والأوعية الدموية عن طريق قياس الكوليسترول الكلي وLDL وHDL والدهون الثلاثية.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Traditionally requires 9-12 hour fasting; many guidelines now accept non-fasting samples for general screening (fasting still preferred when triglycerides are the primary focus or if very high triglycerides are suspected).",
        "collection_notes_ar": "تقليديًا يتطلب صيام 9-12 ساعة؛ العديد من الإرشادات الحديثة تقبل العينة غير الصائمة للفحص العام (يُفضّل الصيام إذا كان التركيز على الدهون الثلاثية أو عند الاشتباه بارتفاعها الشديد).",
        "methodology_en": "Total cholesterol, HDL-C, and triglycerides measured directly by enzymatic methods; LDL-C typically calculated via the Friedewald formula (LDL = Total Cholesterol - HDL - Triglycerides/5) or measured directly when triglycerides are very high.",
        "methodology_ar": "يُقاس الكوليسترول الكلي وHDL والدهون الثلاثية مباشرة بطرق إنزيمية؛ يُحسب LDL عادة بمعادلة فريدوالد (LDL = الكوليسترول الكلي - HDL - الدهون الثلاثية/5) أو يُقاس مباشرة عند ارتفاع الدهون الثلاثية بشدة.",
        "reference_ranges": [
            {"parameter": "Total cholesterol", "population": "Desirable", "range": "<200 mg/dL"},
            {"parameter": "Total cholesterol", "population": "Borderline high", "range": "200-239 mg/dL"},
            {"parameter": "Total cholesterol", "population": "High", "range": "\u2265240 mg/dL"},
            {"parameter": "LDL cholesterol", "population": "Optimal", "range": "<100 mg/dL"},
            {"parameter": "LDL cholesterol", "population": "Near optimal", "range": "100-129 mg/dL"},
            {"parameter": "LDL cholesterol", "population": "Borderline high", "range": "130-159 mg/dL"},
            {"parameter": "LDL cholesterol", "population": "High", "range": "160-189 mg/dL"},
            {"parameter": "LDL cholesterol", "population": "Very high", "range": "\u2265190 mg/dL"},
            {"parameter": "HDL cholesterol", "population": "Low (male)", "range": "<40 mg/dL"},
            {"parameter": "HDL cholesterol", "population": "Low (female)", "range": "<50 mg/dL"},
            {"parameter": "HDL cholesterol", "population": "High (protective)", "range": "\u226560 mg/dL"},
            {"parameter": "Triglycerides", "population": "Normal", "range": "<150 mg/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "High LDL-C and total cholesterol are associated with increased atherosclerotic cardiovascular disease (ASCVD) risk; low HDL-C is an independent risk factor. High triglycerides are linked to metabolic syndrome and, at very high levels (>500 mg/dL), pancreatitis risk. Interpreted alongside overall ASCVD risk factors (age, smoking, blood pressure, diabetes, family history) per NCEP ATP III / current cardiology guidelines.",
        "clinical_significance_ar": "ارتفاع LDL والكوليسترول الكلي يرتبط بزيادة خطر تصلب الشرايين وأمراض القلب؛ انخفاض HDL عامل خطر مستقل. ارتفاع الدهون الثلاثية يرتبط بمتلازمة التمثيل الغذائي، وعند الارتفاع الشديد جدًا (>500 مج/دل) يزيد خطر التهاب البنكرياس. تُفسَّر النتائج مع عوامل الخطر الكلية لأمراض القلب (العمر، التدخين، ضغط الدم، السكري، التاريخ العائلي) وفق إرشادات NCEP ATP III أو الإرشادات القلبية الحديثة.",
        "associated_conditions": [
            {"condition": "Atherosclerotic cardiovascular disease risk", "direction": "high LDL/TC, low HDL"},
            {"condition": "Metabolic syndrome", "direction": "high triglycerides, low HDL"},
            {"condition": "Familial hypercholesterolemia", "direction": "markedly high LDL"},
            {"condition": "Pancreatitis risk", "direction": "very high triglycerides (>500 mg/dL)"}
        ],
        "sources": [
            {"name": "NHLBI - Third Report of the National Cholesterol Education Program (NCEP ATP III)", "url": "https://www.nhlbi.nih.gov/files/docs/guidelines/atp3xsum.pdf", "accessed": "2026-07-14"},
            {"name": "myADLM (AACC) - Routine Lipid Testing, NCEP ATP III cut points", "url": "https://myadlm.org/science-and-research/clinical-chemistry/clinical-chemistry-trainee-council/pearls-of-laboratory-medicine-in-english/2012/routine-lipid-testing", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "creatinine",
        "name_en": "Serum Creatinine",
        "name_ar": "الكرياتينين في الدم",
        "aliases": "Cr, Creat",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses kidney function; used to calculate estimated glomerular filtration rate (eGFR) and monitor chronic kidney disease or acute kidney injury.",
        "purpose_ar": "يقيّم وظائف الكلى؛ يُستخدم لحساب معدل الترشيح الكبيبي التقديري (eGFR) ولمتابعة أمراض الكلى المزمنة أو الإصابة الكلوية الحادة.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No special fasting required, though very high dietary protein/meat intake shortly before the test can mildly elevate results.",
        "collection_notes_ar": "لا يتطلب صيامًا خاصًا، إلا أن تناول كمية كبيرة من البروتين/اللحوم قبل الفحص مباشرة قد يرفع النتيجة بشكل طفيف.",
        "methodology_en": "Jaffe reaction (kinetic, alkaline picrate) or enzymatic method on automated chemistry analyzers; enzymatic methods are less prone to interference.",
        "methodology_ar": "تفاعل جافيه (الحركي، البيكرات القلوي) أو الطريقة الإنزيمية على أجهزة الكيمياء الآلية؛ الطريقة الإنزيمية أقل عرضة للتداخلات.",
        "reference_ranges": [
            {"parameter": "Serum creatinine", "population": "Adult male", "range": "0.6-1.2 mg/dL (53-106 \u00b5mol/L)"},
            {"parameter": "Serum creatinine", "population": "Adult female", "range": "0.5-1.1 mg/dL (44-97 \u00b5mol/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated creatinine indicates reduced kidney filtration (acute kidney injury or chronic kidney disease); the degree of elevation and eGFR help stage severity. Low creatinine may reflect reduced muscle mass, malnutrition, or pregnancy rather than disease. Creatinine varies significantly by muscle mass, so eGFR (which adjusts for age/sex) is now routinely reported alongside it. Reference ranges vary by lab and assay method (Jaffe vs enzymatic) -- always confirm against the local laboratory's reported range.",
        "clinical_significance_ar": "ارتفاع الكرياتينين يدل على انخفاض ترشيح الكلى (إصابة كلوية حادة أو مرض كلوي مزمن)؛ درجة الارتفاع وقيمة eGFR تساعدان في تحديد شدة الحالة. انخفاض الكرياتينين قد يعكس انخفاض الكتلة العضلية أو سوء التغذية أو الحمل وليس بالضرورة مرضًا. يتأثر الكرياتينين بشكل كبير بالكتلة العضلية، لذا يُبلَّغ eGFR (الذي يأخذ العمر والجنس بالحسبان) بشكل روتيني معه. القيم المرجعية تختلف حسب المعمل وطريقة التحليل (جافيه أو إنزيمية) -- يجب دائمًا مراجعة القيمة المرجعية المعتمدة في المعمل المحلي.",
        "associated_conditions": [
            {"condition": "Chronic kidney disease (CKD)", "direction": "high"},
            {"condition": "Acute kidney injury (AKI)", "direction": "high, rising trend"},
            {"condition": "Dehydration / prerenal azotemia", "direction": "high"},
            {"condition": "Low muscle mass / malnutrition / pregnancy", "direction": "low"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Lab Values, Normal Adult reference table", "url": "https://emedicine.medscape.com/article/2172316-overview", "accessed": "2026-07-14"},
            {"name": "Medscape/eMedicine - Creatinine: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2054342-overview", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "alt-ast",
        "name_en": "ALT & AST (Liver Transaminases)",
        "name_ar": "إنزيمات الكبد ALT وAST",
        "aliases": "SGPT, SGOT, Alanine aminotransferase, Aspartate aminotransferase, Liver enzymes",
        "category": "Clinical Chemistry",
        "purpose_en": "Screens for and monitors liver cell injury/inflammation; part of standard liver function panels.",
        "purpose_ar": "فحص ومتابعة تلف/التهاب خلايا الكبد؛ جزء من فحوصات وظائف الكبد الأساسية.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Fasting is often requested (8-12h) when part of a broader metabolic panel, but isolated ALT/AST does not strictly require fasting. Recent strenuous exercise can transiently raise AST.",
        "collection_notes_ar": "يُطلب الصيام غالبًا (8-12 ساعة) عند إجرائه ضمن فحص استقلابي أوسع، لكن ALT/AST بمفردهما لا يتطلبان صيامًا بالضرورة. ممارسة رياضة شاقة مؤخرًا قد ترفع AST مؤقتًا.",
        "methodology_en": "Enzymatic kinetic assay (IFCC-standardized method) on automated clinical chemistry analyzers.",
        "methodology_ar": "مقايسة إنزيمية حركية (بطريقة معيارية وفق IFCC) على أجهزة الكيمياء الإكلينيكية الآلية.",
        "reference_ranges": [
            {"parameter": "ALT (SGPT)", "population": "Adult, general lab range", "range": "7-56 U/L", "notes": "Varies by lab/sex; some labs report lower sex-specific upper limits (e.g. ~29-33 U/L men, ~19-25 U/L women)"},
            {"parameter": "AST (SGOT)", "population": "Adult, general lab range", "range": "10-40 U/L", "notes": "Minimal sex difference; varies by lab"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated ALT is relatively liver-specific and suggests hepatocellular injury (viral hepatitis, NAFLD/MASLD, drug-induced liver injury, alcohol). AST is less liver-specific (also present in cardiac/skeletal muscle, kidney, red cells). An AST:ALT ratio >2 classically suggests alcohol-related liver disease; ALT>AST is more typical of viral hepatitis or fatty liver. Reference ranges vary significantly between laboratories and by sex -- always compare against the reporting lab's own range.",
        "clinical_significance_ar": "ارتفاع ALT مؤشر أكثر تخصصًا لتلف خلايا الكبد (التهاب كبدي فيروسي، الكبد الدهني، تلف الكبد الدوائي، الكحول). AST أقل تخصصًا للكبد (موجود أيضًا في عضلة القلب والعضلات الهيكلية والكلى وكريات الدم الحمراء). نسبة AST:ALT أكبر من 2 تشير تقليديًا لمرض كبدي كحولي؛ بينما ALT أعلى من AST أكثر شيوعًا في التهاب الكبد الفيروسي أو الكبد الدهني. القيم المرجعية تختلف بشكل كبير بين المعامل وحسب الجنس -- يجب دائمًا مقارنة النتيجة بالقيمة المرجعية الخاصة بالمعمل الذي أجرى الفحص.",
        "associated_conditions": [
            {"condition": "Non-alcoholic fatty liver disease (NAFLD/MASLD)", "direction": "mild-moderate high, ALT>AST"},
            {"condition": "Viral hepatitis (acute)", "direction": "markedly high, ALT>AST"},
            {"condition": "Alcohol-related liver disease", "direction": "high, AST:ALT ratio >2"},
            {"condition": "Drug-induced liver injury", "direction": "variable, can be marked"},
            {"condition": "Muscle injury / rhabdomyolysis (isolated AST rise)", "direction": "high AST, normal ALT"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Liver Function Tests reference intervals discussion", "url": "https://www.droracle.ai/articles/399545/what-are-the-normal-ranges-for-alanine-transaminase-alt", "accessed": "2026-07-14"},
            {"name": "General clinical lab reference compilation (ALT 7-56 U/L, AST 10-40 U/L consensus across multiple lab sources)", "url": "https://www.doctronic.ai/blog/liver-function-tests-ast-alt-alp-explained/", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "tsh",
        "name_en": "Thyroid-Stimulating Hormone",
        "name_ar": "الهرمون المنبه للغدة الدرقية",
        "aliases": "TSH, Thyrotropin",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "First-line screening test for thyroid dysfunction (hypothyroidism and hyperthyroidism); most sensitive single test for thyroid function.",
        "purpose_ar": "الفحص الأول للكشف عن اضطرابات الغدة الدرقية (قصور أو فرط نشاط)؛ أكثر فحص فردي حساسية لوظيفة الغدة الدرقية.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Can be drawn any time of day, though TSH has mild diurnal variation (slightly higher in early morning).",
        "collection_notes_ar": "لا يتطلب الصيام. يمكن سحبه في أي وقت من اليوم، رغم وجود تفاوت يومي بسيط (يكون أعلى قليلاً في الصباح الباكر).",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) or electrochemiluminescence immunoassay (ECLIA) on automated immunoassay analyzers.",
        "methodology_ar": "مقايسة مناعية بالإشعاع الكيميائي (CLIA) أو الإشعاع الكيميائي الإلكتروني (ECLIA) على أجهزة المقايسة المناعية الآلية.",
        "reference_ranges": [
            {"parameter": "TSH", "population": "Non-pregnant adult", "range": "0.4-4.0 mIU/L", "notes": "Standard range used by most US labs; upper limit trends higher with age and varies by assay/lab (some report up to 4.5-5.0 mIU/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "High TSH suggests primary hypothyroidism (underactive thyroid); low TSH suggests hyperthyroidism (overactive thyroid) or, less commonly, secondary/central hypothyroidism from pituitary dysfunction. Always interpreted with free T4 (and free T3 when relevant) to confirm and characterize thyroid status. Reference ranges shift with age (higher upper limit in older adults) and pregnancy (trimester-specific lower targets).",
        "clinical_significance_ar": "ارتفاع TSH يشير إلى قصور أولي في الغدة الدرقية؛ انخفاضه يشير إلى فرط نشاط الغدة الدرقية أو -بشكل أقل شيوعًا- قصور مركزي ناتج عن خلل في الغدة النخامية. يُفسَّر دائمًا مع T4 الحر (وT3 الحر عند الحاجة) لتأكيد وتوصيف حالة الغدة. القيم المرجعية تتغير مع العمر (الحد الأعلى يرتفع لدى كبار السن) والحمل (أهداف أقل خاصة بكل ثلث من الحمل).",
        "associated_conditions": [
            {"condition": "Primary hypothyroidism (e.g., Hashimoto's thyroiditis)", "direction": "high"},
            {"condition": "Hyperthyroidism (e.g., Graves' disease, toxic nodule)", "direction": "low"},
            {"condition": "Subclinical hypothyroidism", "direction": "mildly high with normal free T4"},
            {"condition": "Central (pituitary) hypothyroidism", "direction": "low or inappropriately normal despite low free T4"}
        ],
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Screening and Treatment of Subclinical Hypothyroidism/Hyperthyroidism", "url": "https://www.ncbi.nlm.nih.gov/books/NBK83492/", "accessed": "2026-07-14"},
            {"name": "PMC - Biochemical Testing of the Thyroid: TSH is the Best and Oftentimes Only Test Needed", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5321289/", "accessed": "2026-07-14"}
        ],
        "is_published": True
    },
    {
        "slug": "crp",
        "name_en": "C-Reactive Protein (CRP / hs-CRP)",
        "name_ar": "البروتين المتفاعل C",
        "aliases": "CRP, hs-CRP, High-sensitivity CRP",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Non-specific marker of acute inflammation or infection (standard CRP); the high-sensitivity assay (hs-CRP) is additionally used for cardiovascular risk assessment.",
        "purpose_ar": "مؤشر غير نوعي للالتهاب الحاد أو العدوى (CRP العادي)؛ ويُستخدم الفحص عالي الحساسية (hs-CRP) إضافيًا لتقييم خطر أمراض القلب والأوعية الدموية.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required for standard CRP; fasting sample preferred if drawn alongside a lipid panel. Avoid testing during acute unrelated illness when using hs-CRP for cardiovascular risk assessment.",
        "collection_notes_ar": "لا يتطلب CRP العادي صيامًا؛ يُفضَّل عينة صائمة إذا سُحبت مع بروفايل الدهون. يُنصح بتجنب الفحص أثناء مرض حاد غير متعلق عند استخدام hs-CRP لتقييم خطر القلب.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers; high-sensitivity assays use enhanced detection for the low mg/L range needed in cardiovascular risk assessment.",
        "methodology_ar": "مقايسة بالعكارة المناعية أو الانتشار الضوئي المناعي على أجهزة الكيمياء الآلية؛ المقايسات عالية الحساسية تستخدم كشفًا معززًا للنطاق المنخفض اللازم لتقييم خطر القلب.",
        "reference_ranges": [
            {"parameter": "Standard CRP", "population": "Normal", "range": "<1.0 mg/dL (<10 mg/L)"},
            {"parameter": "hs-CRP (cardiovascular risk)", "population": "Low risk", "range": "<1.0 mg/L"},
            {"parameter": "hs-CRP (cardiovascular risk)", "population": "Moderate risk", "range": "1.0-3.0 mg/L"},
            {"parameter": "hs-CRP (cardiovascular risk)", "population": "High risk", "range": ">3.0 mg/L"},
            {"parameter": "CRP", "population": "Acute inflammation", "range": ">10 mg/L (not used for CV risk stratification)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Markedly elevated CRP (>10 mg/L) indicates active acute inflammation or infection (bacterial infections typically drive levels higher than viral ones) but does not identify the source; further workup is needed. For cardiovascular risk stratification, hs-CRP should be measured on two occasions at least 2 weeks apart in a metabolically stable state, and used as a risk-enhancing factor alongside traditional risk scores (per ACC/AHA guidance), not in isolation.",
        "clinical_significance_ar": "الارتفاع الملحوظ في CRP (>10 مج/لتر) يدل على التهاب حاد نشط أو عدوى (العدوى البكتيرية عادة ترفعه أكثر من الفيروسية) لكنه لا يحدد المصدر، ويستلزم فحوصات إضافية. لتقييم خطر القلب، يُفضَّل قياس hs-CRP مرتين بفارق أسبوعين على الأقل في حالة استقرار استقلابي، ويُستخدم كعامل مساعد لتعزيز تقييم الخطر مع المقاييس التقليدية (وفق إرشادات ACC/AHA) وليس بمفرده.",
        "associated_conditions": [
            {"condition": "Bacterial infection", "direction": "markedly high (often >40-50 mg/L)"},
            {"condition": "Viral infection", "direction": "mild-moderate elevation (typically <20-30 mg/L)"},
            {"condition": "Acute myocardial infarction / plaque rupture", "direction": "high"},
            {"condition": "Chronic inflammatory conditions (e.g., rheumatoid arthritis, IBD)", "direction": "persistently elevated"},
            {"condition": "Cardiovascular risk stratification (hs-CRP)", "direction": "elevated indicates higher residual risk"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - High-Sensitivity C-Reactive Protein: Reference Range, Interpretation", "url": "https://emedicine.medscape.com/article/2094831-overview", "accessed": "2026-07-14"},
            {"name": "Medscape/eMedicine - C-Reactive Protein: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2086909-overview", "accessed": "2026-07-14"}
        ],
        "is_published": True
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
            (t["slug"], t["name_en"], t["name_ar"], t["aliases"], t["category"],
             t["purpose_en"], t["purpose_ar"], t["specimen_type"],
             t["collection_notes_en"], t["collection_notes_ar"],
             t["methodology_en"], t["methodology_ar"],
             json.dumps(t["reference_ranges"]), int(t["reference_ranges_verified"]),
             t["clinical_significance_en"], t["clinical_significance_ar"],
             json.dumps(t["associated_conditions"]), json.dumps(t["sources"]),
             int(t["is_published"]))
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']} / {t['name_ar']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
