# Disease Information for 19-Class Merged Skin Disease Dataset
# This file contains labels, descriptions, and medical advice for all disease categories

LABELS = [
    "Acne and Rosacea",
    "Bacterial Infection",
    "Contact Dermatitis",
    "Eczema",
    "Fungal Infection",
    "Hair Loss",
    "Herpes & STDs",
    "Infestations & Bites",
    "Lupus and Connective Tissue Disease",
    "Malignant Lesions",
    "Melanoma & Nevi",
    "Nail Disease",
    "Pigmentation Disorders",
    "Psoriasis & Lichen Planus",
    "Seborrheic Keratoses and other Benign Tumors",
    "Systemic Disease",
    "Urticaria",
    "Vascular Disorders",
    "Viral Infection"
]

DESCRIPTIONS = {
    "Acne and Rosacea": "Acne is caused by blocked pores and inflammation, appearing as pimples, blackheads, and cysts. Rosacea is a chronic condition causing facial redness, visible blood vessels, and sometimes acne-like bumps.",
    
    "Bacterial Infection": "Bacterial skin infections including cellulitis (red, swollen, painful skin), impetigo (red sores with honey-colored crusts), folliculitis, and other infections caused by bacteria like staph or strep.",
    
    "Contact Dermatitis": "Allergic or irritant reactions from contact with substances like poison ivy/oak, chemicals, metals, or cosmetics. Causes itchy, red, sometimes blistering rashes at the contact site.",
    
    "Eczema": "A group of conditions causing inflamed, itchy, cracked, and rough skin. Can be triggered by allergens, irritants, stress, or genetic factors. Often chronic with flare-ups.",
    
    "Fungal Infection": "Fungal infections including ringworm (tinea), athlete's foot, jock itch, yeast infections (candidiasis), and other fungal colonization of skin, causing itchy, scaly, circular patches.",
    
    "Hair Loss": "Various conditions causing hair loss including alopecia areata (autoimmune patchy hair loss), androgenic alopecia (pattern baldness), telogen effluvium, and other hair/scalp disorders.",
    
    "Herpes & STDs": "Sexually transmitted infections affecting the skin including herpes simplex (cold sores, genital herpes), genital warts (HPV), syphilis rashes, and other STD manifestations.",
    
    "Infestations & Bites": "Skin conditions from parasites and insect bites including scabies (mites causing intense itching), Lyme disease (tick-borne with bull's-eye rash), bed bugs, lice, and other infestations.",
    
    "Lupus and Connective Tissue Disease": "Autoimmune diseases affecting skin and connective tissue. Lupus causes butterfly-shaped facial rashes, photosensitivity, and other skin changes. Includes dermatomyositis and scleroderma.",
    
    "Malignant Lesions": "Precancerous and cancerous skin lesions including actinic keratosis (rough, scaly patches from sun damage), basal cell carcinoma, squamous cell carcinoma, and other malignant growths.",
    
    "Melanoma & Nevi": "Includes melanoma (most serious skin cancer requiring urgent treatment), benign moles (nevi), and atypical moles requiring monitoring. Check using ABCDE rule (Asymmetry, Border, Color, Diameter, Evolving).",
    
    "Nail Disease": "Nail disorders including fungal infections (onychomycosis causing discoloration and thickening), psoriatic nails, ingrown nails, paronychia, and other conditions affecting nail structure and appearance.",
    
    "Pigmentation Disorders": "Conditions affecting skin color including vitiligo (loss of pigment), melasma (dark patches), hyperpigmentation, hypopigmentation, and sun-induced pigmentation changes.",
    
    "Psoriasis & Lichen Planus": "Chronic inflammatory conditions. Psoriasis causes scaly, red, silver patches often on elbows, knees, scalp. Lichen planus causes purplish, itchy, flat-topped bumps on skin or mucous membranes.",
    
    "Seborrheic Keratoses and other Benign Tumors": "Non-cancerous skin growths. Seborrheic keratoses are waxy, wart-like, stuck-on appearing growths common in older adults. Includes skin tags, dermatofibromas, and other benign tumors.",
    
    "Systemic Disease": "Skin manifestations of internal diseases including diabetes (diabetic dermopathy, acanthosis nigricans), liver disease (jaundice, spider angiomas), kidney disease, thyroid disorders, and other systemic conditions.",
    
    "Urticaria": "Hives - raised, itchy, red or skin-colored welts on the skin caused by allergic reactions, medications, foods, infections, stress, or other triggers. Can be acute or chronic.",
    
    "Vascular Disorders": "Abnormalities of blood vessels including hemangiomas, port-wine stains, spider angiomas, vasculitis (inflamed blood vessels causing purpura or ulcers), and other vascular malformations or tumors.",
    
    "Viral Infection": "Viral skin infections including common warts, plantar warts, flat warts, molluscum contagiosum (flesh-colored dome-shaped bumps), and other viral-induced skin lesions."
}

FIRST_AID = {
    "Acne and Rosacea": "Keep skin clean with gentle cleanser, use non-comedogenic products. For rosacea, avoid triggers (alcohol, spicy food, hot beverages, sun exposure). See dermatologist for persistent or severe cases for prescription treatments.",
    
    "Bacterial Infection": "URGENT: See doctor immediately, especially for cellulitis. Antibiotics required. Keep area clean, avoid touching/spreading. Cover with clean bandage. Watch for spreading redness, fever, or worsening symptoms.",
    
    "Contact Dermatitis": "Immediately wash area with soap and water to remove irritant. Apply cool compresses, calamine lotion, or hydrocortisone cream. Take antihistamines for itching. See doctor if severe, spreading, or involves face/genitals.",
    
    "Eczema": "Moisturize frequently with thick, fragrance-free creams. Use mild, unscented soaps. Avoid known triggers. Apply cool compresses for itching. Over-the-counter hydrocortisone for mild flares. See doctor if infected, severe, or not improving.",
    
    "Fungal Infection": "Keep affected area clean and dry. Apply over-the-counter antifungal creams (clotrimazole, miconazole). Change socks/underwear daily. Avoid sharing towels. See doctor if not improving in 2 weeks or spreading.",
    
    "Hair Loss": "See dermatologist for proper diagnosis and treatment. Treatment depends on cause - may include medications (minoxidil, finasteride), steroid injections, or immunotherapy. Some conditions resolve spontaneously.",
    
    "Herpes & STDs": "See doctor immediately for testing and treatment. Antiviral medications available for herpes. Practice safe sex. Inform partners. Follow prescribed treatment plan. Some STDs require antibiotics or specific therapies.",
    
    "Infestations & Bites": "URGENT for Lyme disease: See doctor immediately for antibiotics within 72 hours. For scabies: Prescription cream needed, wash all bedding/clothes in hot water. For bites: Clean area, apply ice, take antihistamines.",
    
    "Lupus and Connective Tissue Disease": "MEDICAL ATTENTION NEEDED: Requires rheumatologist care for systemic management. Avoid sun exposure, wear SPF 50+ sunscreen daily. Follow prescribed immunosuppressive or anti-inflammatory medications. Monitor for systemic symptoms.",
    
    "Malignant Lesions": "URGENT: See dermatologist immediately for biopsy and treatment. Do not delay. Wear broad-spectrum SPF 50+ sunscreen daily. Avoid sun exposure. Early treatment is highly effective. May require surgical removal, cryotherapy, or other treatments.",
    
    "Melanoma & Nevi": "URGENT if mole is changing: See dermatologist immediately for full skin exam and possible biopsy. Monitor all moles monthly using ABCDE rule. Photograph suspicious lesions. Avoid sun exposure, wear sunscreen. Early detection is critical.",
    
    "Nail Disease": "See doctor or dermatologist for accurate diagnosis. Fungal infections require oral or topical antifungal medications for several months. Keep nails clean, dry, and trimmed. Avoid nail polish during treatment.",
    
    "Pigmentation Disorders": "Protect from sun with SPF 50+ broad-spectrum sunscreen daily. For melasma, avoid hormonal triggers. See dermatologist for treatment options including topical creams (hydroquinone, tretinoin), chemical peels, or laser therapy.",
    
    "Psoriasis & Lichen Planus": "See dermatologist for treatment plan. Options include topical corticosteroids, vitamin D analogs, light therapy, or systemic medications for severe cases. Moisturize regularly. Manage stress. Avoid scratching.",
    
    "Seborrheic Keratoses and other Benign Tumors": "Generally harmless, no treatment needed unless irritated or for cosmetic reasons. Can be removed by dermatologist via cryotherapy, electrocautery, or shave excision if desired. Monitor for changes.",
    
    "Systemic Disease": "MEDICAL ATTENTION NEEDED: Skin changes may indicate serious underlying condition. See doctor for comprehensive medical evaluation including blood work and organ function tests. Treat underlying systemic disease.",
    
    "Urticaria": "Take oral antihistamines (cetirizine, loratadine) to relieve itching. Apply cool compresses. Avoid known triggers. SEEK EMERGENCY CARE if experiencing throat swelling, difficulty breathing, or severe widespread hives (possible anaphylaxis).",
    
    "Vascular Disorders": "See dermatologist or vascular specialist for evaluation. Most vascular lesions are benign. Treatment options available for cosmetic concerns (laser, sclerotherapy). For vasculitis: URGENT medical attention needed for underlying cause.",
    
    "Viral Infection": "Most viral infections resolve on their own within weeks to months. Over-the-counter wart treatments available. Avoid picking or scratching. See doctor for persistent, spreading, or painful lesions. May require cryotherapy or other removal methods."
}
