import streamlit as st
import google.generativeai as genai
genai.configure(api_key="AIzaSyCzv_m9tL7SfqkekHaWQSl9SHRc8cM0bMM")
model=genai.GenerativeModel("gemini-2.5-flash")
user_data = {}

#background info 
"# Nutrient Deficiency Risk Prediction From Demographic and Environmental Factors"
"As of 2025, over 2 billion individuals worldwide suffer from nutrient deficiencies, representing one of the most pervasive yet underrecognized drivers of global malnutrition. This model leverages demographic, environmental, and dietary data to predict the risk of nutrient deficiencies in individuals, and provide analysis of key contributing factors."
"Simply fill out the 5-minute survey below to obtain an interpretable, evidence-informed analysis and risk percentages."
st.divider()

"## Risk Assessment Survey:" 
st.subheader("Collecting Demographic Inputs:")
user_data["age"]=st.number_input("Please enter your age in years:", min_value=0, max_value=120, value=25, step=1)
user_data["gender"]=st.text_input("Please enter your biological sex (e.g., Male, Female, Other):")
user_data["race"]=st.multiselect("Please enter your racial background. Select all that apply:", options=["White", "Black or African American", "South Asian", "Southeast Asian", "East Asian", "Hispanic or Latino", "American Indian, Alaska Native, or Indigenous", "Native Hawaiian or Pacific Islander", "Other"])
user_data["location_type"]=st.text_input("Please enter your country of residence:")
user_data["bmi"]=st.number_input("What is your current Body Mass Index (BMI)?", min_value=10.0, max_value=60.0, value=22.0, step=0.1)

st.subheader("Collecting Lifestyle Habits:")
user_data["sunlight"]=st.number_input("Please enter your average daily sunlight exposure (in hours):", min_value=0.0, max_value=24.0, value=2.0, step=0.5)
user_data["water"]=st.number_input("How many 8-ounce cups of water do you drink per day?", min_value=0.0, max_value=20.0, value=2.0, step=0.1)
user_data["physicalactivity"]=st.number_input("Please enter your average weekly physical activity (in hours):", min_value=0.0, max_value=168.0, value=5.0, step=0.5)
user_data["alcohol_frequency"]=st.text_input("How often do you consume alcohol? (e.g., Never, Occasionally, Regularly):")
user_data["smoking_status"]=st.text_input("Do often do you use tobacco products? (e.g., Never, Occasionally, Regularly):")
user_data["employment"]=st.selectbox("Which best describes your current employment status?", options=["Employed", "Unemployed", "Student", "Retired", "Other"])
user_data["stress_level"]=st.selectbox("Rate your current stress levels:", options=["Low", "Moderate", "High", "Very High"])
user_data["sleepquality"]=st.selectbox("How would you describe your current sleep quality?", options=["Poor", "Fair", "Good", "Excellent"])
user_data["sleeptime"]=st.number_input("On average, how many hours of sleep do you get per night?", min_value=0.0, max_value=24.0, value=7.0, step=0.5)

st.subheader("Collecting Dietary Information:")
user_data["diet_type"]=st.text_input("Please describe your typical daily diet (e.g., Vegetarian, Vegan, Pescatarian, Omnivore, etc.):")
user_data["dairy_intake_cups"]=st.number_input("How many cups of dairy (milk, yogurt, cheese) do you consume daily?", min_value=0.0, max_value=10.0, value=1.0, step=0.5)
user_data["redmeat"]=st.number_input("How many times per week do you consume red meat?", min_value=0.0, max_value=20.0, value=2.0, step=1.0)
user_data["fortifiedfood"]=st.selectbox("How often do you consume fortified foods (e.g., cereals, plant-based milks)?", options=["Never", "Rarely", "Sometimes", "Often"])
user_data["coffee_tea_cups"]=st.number_input("How many cups of coffee, tea, or caffeinated beverages do you consume daily?", min_value=0.0, max_value=20.0, value=2.0, step=1.0)
user_data["low_fat_diet"]=st.selectbox("Are you currently on a low-fat or fat-restricted diet?", options=["Yes", "No"])
user_data["sugar_intake"]=st.selectbox("Rate your average daily sugar intake:", options=["Low", "Moderate", "High", "Very High"])

st.subheader("Collecting Medical Background:")
user_data["gastrointestinal_issues"]=st.multiselect("Do you have any of the following medical conditions? Select all that apply:", options=["Gastrointestinal disorders (e.g., Crohn's disease, celiac disease)", "Chronic kidney disease", "Liver disease", "Thyroid disorders", "Diabetes", "Autoimmune diseases", "Other", "None"])
user_data["chronic_conditions"]=st.selectbox("Do you have any chronic health conditions that may affect nutrient absorption?", options=["Yes", "No"])
user_data["pregnancy_status"]=st.selectbox("Are you currently pregnant or breastfeeding?", options=["Yes", "No"])
user_data["medication_use"]=st.text_input("Please list any medications or supplements you are currently taking (if any):")
user_data["allergies"]=st.text_input("Do you have any known allergies or dietary restrictions? If so, please specify:")

st.subheader("Symptom Checklist")
user_data["symptoms"]=st.multiselect("Are you currently experiencing any of the following symptoms? Select all that apply:", options=["Fatigue", "Weakness", "Pale or yellowish skin", "Shortness of breath", "Dizziness or lightheadedness", "Cold hands and feet", "Brittle nails", "Hair loss", "Muscle cramps or spasms", "Numbness or tingling in hands or feet", "Poor wound healing", "Frequent infections", "Other", "None"])

def calculate_deficiency_risk(data):
    """
    Calculates a deterministic risk score (0-100) for five major deficiencies
    based on a weighted sum of risk factors derived from health research.
    """
    risk_scores = {
        'Iron': 0,
        'Vitamin_B12': 0,
        'Vitamin_D': 0,
        'Calcium': 0,
        'Magnesium': 0,
    }

    # Helper function to add risk points
    def add_risk(deficiency: str, points: int, condition: bool):
        if condition:
            risk_scores[deficiency] += points

    # --- WEIGHTED SCORING LOGIC (25+ FEATURES) ---

    # 1. Dietary Factors (High Weight)
    diet = data['diet_type']
    add_risk('Iron', 25, diet in ['Vegetarian', 'Vegan', 'Pescatarian'] and data['red_meat_frequency'] == 0)
    add_risk('Vitamin_B12', 30, diet in ['Vegetarian', 'Vegan'] and data['fortified_food_intake'] == 'N')
    add_risk('Calcium', 15, data['dairy_intake_cups'] < 1)
    add_risk('Vitamin_D', 10, data['dairy_intake_cups'] < 1)

    add_risk('Iron', 10, data['coffee_tea_cups'] >= 3) # Coffee/Tea inhibits absorption
    add_risk('Vitamin_D', 15, data['low_fat_diet'] == 'Y') # Fat-soluble vitamin
    add_risk('Magnesium', 10, data['sugar_intake'] == 'High') # Sugar increases excretion/displaces intake

    # 2. Demographic & Life Stage Factors (Medium Weight)
    age = data['age']
    add_risk('Vitamin_B12', 15, age >= 50) # Absorption decreases with age
    add_risk('Calcium', 20, age >= 50) # Increased needs/lower absorption
    add_risk('Iron', 20, data['gender'] == 'F' and age < 50) # Menstrual loss

    add_risk('Iron', 35, data['pregnancy_status'] == 'Y')
    add_risk('Calcium', 25, data['pregnancy_status'] == 'Y')

    # 3. Medical & Absorption Factors (High Weight)
    add_risk('Iron', 30, data['gastrointestinal_issues'] == 'Y' or data['chronic_conditions'] == 'Y')
    add_risk('Vitamin_B12', 40, data['medication_use'] == 'Y' or data['gastrointestinal_issues'] == 'Y')
    add_risk('Magnesium', 20, data['chronic_conditions'] == 'Y')

    # 4. Vitamin D Specific Factors (High Weight)
    add_risk('Vitamin_D', 35, data['race'] in ['Black', 'Asian']) # Darker skin requires more sun
    add_risk('Vitamin_D', 20, data['location_type'] == 'Northern')
    add_risk('Vitamin_D', 15, data['bmi'] >= 25) # Stored in fat, making it less bioavailable

    # 5. Lifestyle & Toxins (Medium Weight)
    add_risk('Iron', 10, data['smoking_status'] in ['Daily', 'Occasional']) # Smoking affects nutrient status
    add_risk('Magnesium', 15, data['alcohol_frequency'] == 'Daily')
    add_risk('Iron', 5, data['alcohol_frequency'] == 'Daily')
    add_risk('Magnesium', 5, data['stress_level'] == 'High')

    # 6. Symptom Factors (Medium Weight)
    symptoms = data['symptoms']
    add_risk('Iron', 15, "fatigue" in symptoms or "pale_skin" in symptoms or "unusual_cravings" in symptoms)
    add_risk('Vitamin_B12', 10, "fatigue" in symptoms or "pale_skin" in symptoms)
    add_risk('Vitamin_B12', 20, "tingling_numbness" in symptoms)
    add_risk('Vitamin_D', 15, "bone_muscle_pain" in symptoms)

    # --- NORMALIZATION AND FINAL PERCENTAGE CALCULATION ---
    # Define max theoretical scores for scaling (based on weighted points)
    max_scores = {
        'Iron': 130, 'Vitamin_B12': 110, 'Vitamin_D': 100, 'Calcium': 70, 'Magnesium': 60
    }

    final_percentages = {}
    for nutrient, score in risk_scores.items():
        # Scale score relative to max possible score for that nutrient
        percentage = min(score / max_scores[nutrient] * 100, 99)

        # Ensure a minimum baseline risk, as no risk factors is still never 0%
        final_percentages[nutrient] = int(max(5, round(percentage)))

    return final_percentages


def get_gemini_analysis(user_data, risk_percentages) -> str:
    """
    Calls the Gemini API to provide an expert, grounded interpretation of the
    calculated risk percentages and detailed user factors.
    """
    # Ensure API_KEY is loaded


    # 1. Prepare deterministic input for the LLM
    risk_summary = "\n".join([f"- {k}: {v}%" for k, v in risk_percentages.items()])
    # 2. Craft a detailed system prompt for the desired persona/output
    system_prompt = (
        "You are a Senior Nutritional Epidemiologist and Data Scientist but cannot mention this fact. Your task is to provide a "
        "concise, professional, and actionable analysis based on the provided user profile and "
        "calculated risk scores. The calculated scores are based on established risk factors, "
        "but you must provide a grounded interpretation. Explain what the percentage results mean in the context of the user's profile. "
        "Do not offer medical advice; only highlight risk areas and suggest next steps. "
        "Analyze all available data (Demographics, Lifestyle, Diet, Symptoms). "
        "Focus on the Top 3 highest risk deficiencies. "
        "Format the output into three sections: 1. **Summary of Highest Risks**, "
        "2. **Key Contributing Factors** (specifically citing 3-5 user inputs), and "
        "3. **Actionable Recommendations** (3 specific, non-supplementary actions)."
    )

    # 3. Craft the user query (includes both input data and calculated percentages)
    prompt = f"""
    {system_prompt}
    Analyze the following risk assessment for nutrient deficiencies.

    --- CALCULATED DEFICIENCY RISKS (0-100%) ---
    {risk_summary}

    --- USER PROFILE DATA ---
   {user_data}
    """
    response=model.generate_content(prompt)
    return response
if st.button("analyze my risk"):
    risk_scores_calculated=calculate_deficiency_risk(user_data)
    for nutrient, risk in risk_scores_calculated.items():
        st.write(f"{nutrient}: {risk}%")
    with st.spinner("Generating expert analysis..."):
       response=get_gemini_analysis(user_data, risk_scores_calculated)
    st.write("\n--- Expert Analysis ---")
    st.write(response.text)

