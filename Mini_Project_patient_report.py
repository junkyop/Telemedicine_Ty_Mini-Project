from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas
from datetime import datetime

# --- Helper Functions ---
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
    return round(bmi, 2), category

def validate_input(age, temperature, heart_rate):
    if age <= 0 or age > 120:
        raise ValueError("Invalid age entered.")
    if temperature < 30 or temperature > 45:
        raise ValueError("Temperature out of expected range.")
    if heart_rate < 30 or heart_rate > 180:
        raise ValueError("Heart rate seems abnormal.")

def classify_condition(symptoms, existing_conditions):
    symptoms = symptoms.lower()
    existing = existing_conditions.lower()
    if any(k in symptoms for k in ['cancer', 'kidney failure', 'unconscious', 'bleeding']):
        return "Critical"
    if any(k in existing for k in ['diabetes', 'hypertension', 'asthma', 'cancer', 'arthritis', 'kidney']):
        return "Chronic"
    if any(k in symptoms for k in ['fever', 'cough', 'cold', 'pain', 'vomiting', 'headache', 'diarrhea']):
        return "Acute"
    return "Unknown"

def predict_possible_disease(symptoms, existing_conditions):
    symptoms = symptoms.lower()
    existing = existing_conditions.lower()
    if 'unconscious' in symptoms:
        return "Critical - Immediate Medical Attention"
    if 'bleeding' in symptoms:
        return "Critical - Severe Bleeding"
    if 'cancer' in symptoms or 'cancer' in existing:
        return "Cancer - Oncology Consultation Needed"
    if 'kidney failure' in symptoms or 'kidney' in existing:
        return "Kidney Disease - Nephrology Consultation Needed"
    if 'diabetes' in existing:
        if 'cough' in symptoms or 'fever' in symptoms:
            return "Diabetes with Possible Infection"
        return "Diabetes Management Needed"
    patterns = {'cough fever': 'Respiratory Infection', 'cough headache': 'COVID-19',
                'vomiting diarrhea': 'Gastroenteritis', 'headache nausea': 'Migraine'}
    for pattern, disease in patterns.items():
        if all(p in symptoms for p in pattern.split()):
            return disease
    return "Medical Evaluation Needed"

def risk_score(temp, heart_rate, sys, dia, severity, existing):
    score = 0
    existing = existing.lower()
    if temp > 38: score += 1
    if heart_rate > 100: score += 1
    if sys > 140 or dia > 90: score += 1
    if severity >= 7: score += 2
    if 'cancer' in existing: score += 3
    if 'kidney' in existing: score += 3
    if 'diabetes' in existing: score += 2
    if 'heart' in existing: score += 2
    return min(score, 10)

def emergency_alert(score, disease, txt):
    return txt['emergency'] if score >= 6 or "Critical" in disease else ""

def health_tips(bmi, age, disease, existing):
    tips = ""
    existing = existing.lower()
    if bmi >= 25:
        tips += "- Exercise regularly\n- Portion control\n- Avoid junk food\n\n"
    elif bmi < 18.5:
        tips += "- Nutrient-dense foods\n- Strength training\n- Frequent meals\n\n"
    if age > 60:
        tips += "- Regular checkups\n- Balance exercises\n- Medication review\n\n"
    if "cancer" in disease.lower():
        tips += "- Nutrition support\n- Manage side effects\n- Emotional care\n\n"
    if "kidney" in disease.lower():
        tips += "- Low potassium diet\n- Monitor fluid\n- Checkups\n\n"
    if "diabetes" in existing:
        tips += "- Blood sugar monitoring\n- Foot care\n- Balanced diet\n"
    return tips.strip()

def enhanced_prescription(disease, condition, age, weight, existing):
    existing = existing.lower()
    if "Cancer" in disease:
        return {"Medicines": [{"Medicine": "Oncology Referral", "Dosage": "Urgent", "Timing": "Immediately", "Notes": "No self-medication"}],
                "Advice": {"Home Remedy": "Nutrition, pain relief, support", "Follow-up": "48 hrs", "Warning": "Report new symptoms"}}
    if "Kidney" in disease:
        return {"Medicines": [{"Medicine": "Nephrology Referral", "Dosage": "Urgent", "Timing": "Immediately", "Notes": "Avoid nephrotoxic drugs"}],
                "Advice": {"Home Remedy": "Low protein, fluid management", "Follow-up": "24 hrs", "Warning": "Monitor swelling"}}
    if "Diabetes" in disease:
        meds = [{"Medicine": "Metformin", "Dosage": "500mg" if weight < 70 else "850mg", "Timing": "Twice daily"}]
        if "infection" in disease.lower():
            meds.append({"Medicine": "Antibiotic", "Dosage": "As prescribed", "Timing": "Full course", "Notes": "Monitor sugar"})
        return {"Medicines": meds, "Advice": {"Home Remedy": "Glucose checks, foot care", "Follow-up": "3 days", "Warning": "Watch for ketoacidosis"}}
    return {"Medicines": [{"Medicine": "Paracetamol", "Dosage": "500mg", "Timing": "Every 6 hrs", "Max": "4 doses/day"}],
            "Advice": {"Home Remedy": "Rest, hydration", "Follow-up": "3 days", "Warning": "See doctor if worse"}}

def generate_pdf_report(name, gender, age, bmi, bmi_category, condition, disease, score, emergency, prescription, tips, txt):
    filename = f"{name.replace(' ', '_')}_health_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    line = height - 50
    now = datetime.now()
    date_time = now.strftime("%B %d, %Y at %I:%M %p")

    def draw_line(text, offset=15, bold=False):
        nonlocal line
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 12 if bold else 11)
        c.drawString(50, line, text)
        line -= offset

    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 40, date_time)
    draw_line(txt['report'], bold=True)
    draw_line(f"{txt['name']}: {name}")
    draw_line(f"{txt['gender']}: {gender}")
    draw_line(f"{txt['age']}: {age}")
    draw_line(f"{txt['bmi']}: {bmi} ({bmi_category})")
    draw_line(f"{txt['condition']}: {condition}")
    draw_line(f"{txt['disease']}: {disease}")
    draw_line(f"{txt['risk']}: {score}/10")
    if emergency:
        draw_line(emergency, bold=True)
    draw_line(f"\n{txt['prescription']}:", bold=True)
    for med in prescription["Medicines"]:
        draw_line(f"- {txt['medicine']}: {med['Medicine']}")
        draw_line(f"  {txt['dosage']}: {med['Dosage']}")
        draw_line(f"  {txt['timing']}: {med['Timing']}")
        if 'Notes' in med:
            draw_line(f"  {txt['notes']}: {med['Notes']}")
        if 'Max' in med:
            draw_line(f"  {txt['max']}: {med['Max']}")
    draw_line(f"\n{txt['remedy']}:", bold=True)
    for tip in prescription['Advice']['Home Remedy'].split('\n'):
        draw_line(tip)
    draw_line(f"\n{txt['followup']}: {prescription['Advice']['Follow-up']}")
    draw_line(f"⚠️ {txt['warning']}: {prescription['Advice']['Warning']}")
    draw_line(f"\n{txt['tips']}:", bold=True)
    for tip in tips.split('\n'):
        draw_line(tip)
    draw_line(f"\n{txt['visit']}: {txt['yes'] if score >= 4 else txt['no']}")
    draw_line(f"{txt['hosp']}: {txt['yes'] if score >= 6 else txt['no']}")
    c.save()
    print(f"\n✅ PDF Report generated: {filename}")

# --- Main CLI Function ---
def main():
    # Language Dictionaries
    lang_dict = {
        "English": {
            "welcome": "📋 Welcome to the Enhanced Telemedicine Assistant",
            "name": "Patient name",
            "gender": "Gender",
            "age": "Age",
            "height": "Height (cm)",
            "weight": "Weight (kg)",
            "temp": "Temperature (°C)",
            "heart": "Heart rate (bpm)",
            "bp_sys": "Blood pressure (systolic)",
            "bp_dia": "Blood pressure (diastolic)",
            "symptoms": "Enter symptoms separated by commas",
            "existing": "Any existing medical conditions",
            "severity": "Rate your symptom severity (1-10)",
            "report": "🩺 --- Diagnosis Report ---",
            "bmi": "BMI",
            "condition": "Condition Type",
            "disease": "Likely Disease",
            "risk": "Risk Score",
            "emergency": "🚨 Emergency Alert: Immediate medical attention required!",
            "prescription": "💊 Prescription",
            "medicine": "Medicine",
            "dosage": "Dosage",
            "timing": "Timing",
            "remedy": "Home Remedy",
            "followup": "Follow-up",
            "tips": "Health Tips",
            "visit": "Doctor Visit Needed",
            "hosp": "Hospitalization Recommended",
            "yes": "Yes",
            "no": "No",
            "warning": "Important Warning",
            "notes": "Notes",
            "max": "Maximum"
        },
        "Hindi": {
            "welcome": "📋 उन्नत टेलीमेडिसिन सहायक में आपका स्वागत है",
            "name": "मरीज का नाम",
            "gender": "लिंग",
            "age": "उम्र",
            "height": "ऊंचाई (सेमी)",
            "weight": "वज़न (किग्रा)",
            "temp": "तापमान (°C)",
            "heart": "दिल की धड़कन (बीपीएम)",
            "bp_sys": "ब्लड प्रेशर (सिस्टोलिक)",
            "bp_dia": "ब्लड प्रेशर (डायस्टोलिक)",
            "symptoms": "लक्षण दर्ज करें (कॉमा से अलग करें)",
            "existing": "कोई मौजूदा चिकित्सा स्थिति",
            "severity": "लक्षणों की गंभीरता (1-10)",
            "report": "🩺 --- निदान रिपोर्ट ---",
            "bmi": "बीएमआई",
            "condition": "स्थिति प्रकार",
            "disease": "संभावित बीमारी",
            "risk": "जोखिम स्कोर",
            "emergency": "🚨 आपातकालीन चेतावनी: तुरंत चिकित्सा सहायता की आवश्यकता!",
            "prescription": "💊 दवा का निर्देश",
            "medicine": "दवा",
            "dosage": "खुराक",
            "timing": "समय",
            "remedy": "घरेलू उपाय",
            "followup": "फॉलो-अप",
            "tips": "स्वास्थ्य सुझाव",
            "visit": "डॉक्टर से मिलना आवश्यक है",
            "hosp": "अस्पताल में भर्ती की सिफारिश",
            "yes": "हाँ",
            "no": "नहीं",
            "warning": "महत्वपूर्ण चेतावनी",
            "notes": "टिप्पणियाँ",
            "max": "अधिकतम"
        },
        "Marathi": {
            "welcome": "📋 उन्नत टेलीमेडिसिन सहाय्यास स्वागत आहे",
            "name": "रुग्णाचे नाव",
            "gender": "लिंग",
            "age": "वय",
            "height": "उंची (से.मी.)",
            "weight": "वजन (कि. ग्रा.)",
            "temp": "तापमान (°C)",
            "heart": "हृदयगती (bpm)",
            "bp_sys": "रक्तदाब (सिस्टोलिक)",
            "bp_dia": "रक्तदाब (डायस्टोलिक)",
            "symptoms": "लक्षणे कॉमा ने विभक्त करा",
            "existing": "कोणतीही विद्यमान आजाराची स्थिती",
            "severity": "लक्षणांची तीव्रता (1-10)",
            "report": "🩺 --- निदान अहवाल ---",
            "bmi": "बीएमआय",
            "condition": "स्थिती प्रकार",
            "disease": "संभाव्य आजार",
            "risk": "जोखीम गुण",
            "emergency": "🚨 आपत्कालीन सूचना: तातडीने वैद्यकीय मदतीची गरज!",
            "prescription": "💊 औषध सूचना",
            "medicine": "औषध",
            "dosage": "मात्रा",
            "timing": "वेळ",
            "remedy": "घरी उपाय",
            "followup": "पुनरावलोकन",
            "tips": "आरोग्य सूचना",
            "visit": "डॉक्टर भेट आवश्यक",
            "hosp": "रुग्णालयात भरती शिफारसीय",
            "yes": "होय",
            "no": "नाही",
            "warning": "महत्त्वाची सूचना",
            "notes": "नोंदी",
            "max": "कमाल"
        }
    }

    print("Select language / भाषा निवडा / भाषा चुनें:")
    print("1: English")
    print("2: Hindi (हिंदी)")
    print("3: Marathi (मराठी)")
    lang_choice = input("Enter option (1/2/3): ")
    lang_map = {"1": "English", "2": "Hindi", "3": "Marathi"}
    lang_key = lang_map.get(lang_choice, "English")
    txt = lang_dict[lang_key]

    print(f"\n{txt['welcome']}")
    name = input(f"{txt['name']}: ")
    gender = input(f"{txt['gender']}: ")
    age = int(input(f"{txt['age']}: "))
    height = float(input(f"{txt['height']}: "))
    weight = float(input(f"{txt['weight']}: "))
    temperature = float(input(f"{txt['temp']}: "))
    heart_rate = int(input(f"{txt['heart']}: "))
    bp_systolic = int(input(f"{txt['bp_sys']}: "))
    bp_diastolic = int(input(f"{txt['bp_dia']}: "))
    symptoms = input(f"{txt['symptoms']}: ")
    existing_conditions = input(f"{txt['existing']}: ")
    severity = int(input(f"{txt['severity']}: "))

    try:
        validate_input(age, temperature, heart_rate)
    except ValueError as e:
        print(f"⚠️ Error: {e}")
        return

    bmi, bmi_category = calculate_bmi(weight, height)
    condition = classify_condition(symptoms, existing_conditions)
    disease = predict_possible_disease(symptoms, existing_conditions)
    score = risk_score(temperature, heart_rate, bp_systolic, bp_diastolic, severity, existing_conditions)
    emergency = emergency_alert(score, disease, txt)
    tips = health_tips(bmi, age, disease, existing_conditions)
    prescription = enhanced_prescription(disease, condition, age, weight, existing_conditions)

    print(f"\n{txt['report']}")
    print(f"{txt['name']}: {name}")
    print(f"{txt['bmi']}: {bmi} ({bmi_category})")
    print(f"{txt['condition']}: {condition}")
    print(f"{txt['disease']}: {disease}")
    print(f"{txt['risk']}: {score}/10")
    if emergency:
        print(f"\n{emergency}")

    print(f"\n{txt['prescription']}:")
    for med in prescription["Medicines"]:
        print(f"\n- {txt['medicine']}: {med['Medicine']}")
        print(f"  {txt['dosage']}: {med['Dosage']}")
        print(f"  {txt['timing']}: {med['Timing']}")
        if 'Notes' in med:
            print(f"  {txt['notes']}: {med['Notes']}")
        if 'Max' in med:
            print(f"  {txt['max']}: {med['Max']}")

    print(f"\n{txt['remedy']}:")
    print(prescription['Advice']['Home Remedy'])
    print(f"\n{txt['followup']}: {prescription['Advice']['Follow-up']}")
    if prescription['Advice']['Warning']:
        print(f"\n⚠️ {txt['warning']}: {prescription['Advice']['Warning']}")

    print(f"\n{txt['tips']}:")
    print(tips)
    print(f"\n{txt['visit']}: {txt['yes'] if score >= 4 else txt['no']}")
    print(f"{txt['hosp']}: {txt['yes'] if score >= 6 else txt['no']}")

    generate_pdf_report(name, gender, age, bmi, bmi_category, condition, disease, score, emergency, prescription, tips, txt)

if __name__ == "__main__":
    main()
