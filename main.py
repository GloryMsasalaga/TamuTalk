""" from flask import Flask, session, redirect, url_for, render_template, request, jsonify
import re
import os
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from googletrans import Translator

app = Flask(__name__)

#set a secret key for session management
app.secret_key = os.urandom(24)

try:
    raise Exception("Dataset is not available")
except Exception as e:
    print("Could not load dataset from the specified path.")
    texts = [
        "Habari! nina shilingi 500 na nataka kununua chakula, nipe pendekezo la chakula",
        "Nina shilingi 1000 na nataka kununua vinywaji, nipe pendekezo la vinywaji",
        "Nina shilingi 600 na nataka kununua chakula, nipo nafwatilia diet yangu, nipe pendekezo la chakula",
        "Nina shilingi 800 na nataka kununua chakula bora",
        "Nina shilingi 1000 nitapenda chakula kitamu leo",
        "Nina shilingi 500 na nataka kununua vinywaji, nipe pendekezo la vinywaji",
        "nina ugonjwa wa kisukari, nipe chakula cha afya",
        "nina ugonjwa wa moyo, nipe chakula cha afya",
        "habari za asubuhi!",
        "habari za mchana!",
        "habari za usiku!",
        "habari! nataka kujua kuhusu mazoezi",
        "naweza kupata taarifa zaidi kuhusu mazoezi?",
        "I have 1000 shillings and I want to buy drinks, please suggest a drink",
        "I  have 800 shillings and I want to buy good food, I am following my diet, please suggest a meal",
        "I have 1500 shillings and I want to buy delicious food today",
    ]
    labels = [
        "food_suggestion_diet", "food", "food_suggestion_diet", "drink", "food",
        "food_suggestion", "drink_suggestion", "food_suggestion", "drink_suggestion",
        "disease_related", "disease_related", "greeting", "exercise", "unknown", "unknown", "greetings"
    ]
    
#create a scikit-learn pipeline
    model = make_pipeline(CountVectorizer(), LogisticRegression(max_iter=200))
    model.fit(texts, labels)   
    
#define helper functions for intents and budget extraction
def extract_budget(text):
    match = re.search(r'(\d+)', text)
    if match:
        return int(match.group(1))
    return None

def predict_intent(text):
    if text:
        prediction = model.predict([text])[0]
        budget = extract_budget(text)
        if budget is not None and budget <500:
            return "unknown"
        return prediction
    return "unknown"

#define chatbot-related helper functions
BUDGET_SUGGESTIONS = {
    "low": {
        #"food": ["mishikaki", "samosa", "ndizi", "chapati", "matunda", "maandazi", ""]
        "English": ["Based on your budget, you might consider a small snack or a drink. Here are some suggestions: samosa, maandazi, matunda, chapati, cassava, or beef skeweres."],
        "Swahili": ["Kulingana na bajeti yako, unaweza kufikiria kitafunwa kidogo au kinywaji. Hapa kuna mapendekezo: sambusa, maandazi, matunda, chapati, mihogo au mishikaki ya ngo'mbe."]
    },
    "medium": {
        "English": ["With a medium budget, you can enjoy a decent meal. Here are some suggestions: pilau, rice with meat soup, ugali with firigisi, rice with okra soup, or grilled chicken."],
        "Swahili": ["Kwa bajeti ya kati, unaweza kufurahia chakula kizuri. Hapa kuna mapendekezo: pilau, wali na supu ya nyama, ugali na firigisi, wali na supu ya bamia, au kuku wa kuchoma."]
    },
    "high": {
        "English": ["With a high budget, you can enjoy a variety of delicious meals. Here are some suggestions: biryani, grilled fish, or a full-course meal."],
        "Swahili": ["Kwa bajeti ya juu, unaweza kufurahia aina mbalimbali za vyakula vya kupendeza. Hapa kuna mapendekezo: biryani, samaki wa kuchoma, au chakula kamili."]
    }
}

SPECIALIST = {
    "diet": {
        "English": ["For diet-related questions, you can consult a nutritionist or a dietitian."],
        "Swahili": ["Kwa maswali yanayohusiana na lishe, unaweza kushauriana na mtaalamu wa lishe au daktari wa lishe."]
    },
    "exercise": {
        "English": ["For exercise-related questions, you can consult a fitness trainer or a physiotherapist."],
        "Swahili": ["Kwa maswali yanayohusiana na mazoezi, unaweza kushauriana na mkufunzi wa mazoezi au mtaalamu wa tiba ya mwili."]
    },
    "nutritionist": {
        "English": ["For nutrition-related questions, you can consult with Dr. Purificator at glorymsasalaga@gmail.com or call +255628225468."],
        "Swahili": ["Kwa maswali yanayohusiana na lishe, unaweza kushauriana na mtaalamu wa lishe Dr. Purificator kwa barua pepe glorymsasalaga@gmail.com au piga simu +255628225468."]
    },
    "fitness":{
        "English":["For fitness training please visit https://classpass.com/try/home-workout-videos#:~:text=ClassPass%20is%20offering%20free%20home%20workout%20videos.%20Find,for%20HIIT%2C%20strength%20training%2C%20yoga%2C%20Pilates%20and%20more."],
        "Swahili":["Kwa mazoezi ya mwili tafadhali tembelea https://classpass.com/try/home-workout-videos#:~:text=ClassPass%20is%20offering%20free%20home%20workout%20videos.%20Find,for%20HIIT%2C%20strength%20training%2C%20yoga%2C%20Pilates%20and%20more."]
    }
}

NUTRITIONAL_INFO = {
    "samosa": {
        "calories": 260-320,
        "Carbohydates": 30-40,
        "Protein": 5-8,
        "Fat": 12-15,
        "Fiber": 2-4
    },
    "maandazi": {
        "calories": 150-160,
        "Carbohydates": 28-30,
        "Protein": 4-5,
        "Fat": 1.5-2,
        "Fiber": 1-2,
        "Sodium": 200-300
    },
    "matunda": {
        "Vitamins": ["Vitamin C", "Vitamin A"],
        "Calories":46-200,
        "Carbohydrates": 10-50,
        "Protein": 1-3,
        "Fat": 0-1
    },
    "chapati": {
        "calories": 250-350,
        "Carbohydrates": 30-40,
        "Protein": 5-7,
        "Total Fat": 10-15,
        "Fiber": 2-4
    },
    "beef mishikaki": {
        "calories": 200-250,
        "Carbohydrates": 0-5,
        "Protein": 25-30,
        "Total Fat": 10-15,
        "Vitamins": ["Vitamin B12", "Vitamin B6"],
        "Minerals": ["Iron", "Zinc"]
    },
    "ugali":{
        "calories": 200-250,
        "Carbohydrates": 40-50,
        "Protein": 4-6,
        "Total Fat": 0-2,
        "Fiber": 1-3
    },
    "rice with meat soup": {
        "calories": 300-400,
        "Carbohydrates": 40-50,
        "Protein": 20-25,
        "Total Fat": 10-15,
        "Fiber": 1-3
    },
    "rice with okra soup": {
        "calories": 250-350,
        "Carbohydrates": 40-50,
        "Protein": 5-10,
        "Total Fat": 5-10,
        "Fiber": 2-4
    },
    "grilled chicken": {
        "calories": 200-300,
        "Carbohydrates": 0-5,
        "Protein": 25-30,
        "Total Fat": 10-15,
        "Vitamins": ["Vitamin B6", "Vitamin B12"],
        "Minerals": ["Iron", "Zinc"]
    },
    "biryani": {
        "calories": 400-500,
        "Carbohydrates": 60-70,
        "Protein": 20-25,
        "Total Fat": 15-20,
        "Vitamins": ["Vitamin B6", "Vitamin B12"],
        "Minerals": ["Iron", "Zinc"]
    },
    "grilled fish": {
        "calories": 250-350,
        "Carbohydrates": 0-5,
        "Protein": 20-25,
        "Total Fat": 10-15,
        "Vitamins": ["Vitamin D", "Vitamin B12"],
        "Minerals": ["Selenium", "Iodine"]
    },
    "full-course meal": {
        "calories": 500-700,
        "Carbohydrates": 60-80,
        "Protein": 30-40,
        "Total Fat": 20-30,
        "Vitamins": ["Vitamin A", "Vitamin C"],
        "Minerals": ["Iron", "Calcium"]
    }
}

#in memory storage for user's health goals(connect with the database in production)
user_health_goals = {}

def get_language():
    lang = session.get("language")
    if lang in ["English", "Swahili"]:
        return lang
    return "English"

def set_language(lang):
    if lang in ["English", "Swahili"]:
        session["language"] = lang

def greetings(lang):
    if lang == "English":
        return "Hello! How can I assist you today?"
    elif lang == "Swahili":
        return "Habari! Naweza kukusaidia vipi leo?"
    else:
        return "Hello! How can I assist you today?"

def process_budget(text, lang):
    budget = extract_budget(text)
    if budget is None:
        return {
            "English": "Sorry, I couldn't extract your budget.",
            "Swahili": "Samahani, sikuweza kupata bajeti yako."
        }[lang]
    
    #define thresholds
    if budget < 500:
        tier = "low"
    elif 500 <= budget < 1000:
        tier = "medium"
    else:
        tier = "high"
    suggestions = "".join(BUDGET_SUGGESTIONS[tier][lang])
    return suggestions

def process_health_goal(user_id, text, lang):
    if "set goal" in text.lower() or "my goal" in text.lower():
        user_health_goals[user_id] = {
            "goal": text,
            "timestamp": datetime.now()
        }
        return {
            "English": "Your health goal has been set.",
            "Swahili": "Lengo lako la afya limewekwa."
        }[lang]
    else:
        if user_id in user_health_goals:
            goal = user_health_goals[user_id]["goal"]
            return {
                "English": f"Your current health goal is: {goal}",
                "Swahili": f"Lengo lako la afya kwa sasa ni: {goal}"
            }[lang]
        else:
            return {
                "English": "You haven't set a health goal yet.",
                "Swahili": "Bado hujaweka lengo la afya."
            }[lang]

def process_dietary_restrictions(text, lang):
    restrictions = []
    keywords = ["vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free", "halal"]
    for keyword in keywords:
        if keyword in text.lower():
            restrictions.append(keyword)
    if restrictions:
        return {
            "English": f"Your dietary restrictions are: {', '.join(restrictions)}.",
            "Swahili": f"Vikwazo vyako vya lishe ni: {', '.join(restrictions)}."
        }[lang]
    else:
        return {
            "English": "No dietary restrictions found.",
            "Swahili": "Hakuna vikwazo vya lishe vilivyopatikana."
        }[lang]
    
def process_specialist(text, lang):
    if "nutritionist" in text.lower():
        return SPECIALIST["nutritionist"][lang]
    elif "fitness" in text.lower() or "exercise" in text.lower():
        return SPECIALIST["fitness"][lang]
    elif "diet" in text.lower():
        return SPECIALIST["diet"][lang]
    else:
        return {
            "English": "No specialist needed.",
            "Swahili": "Hakuna mtaalamu anayehitajika."
        }[lang]
        
def process_nutritional_info(text, lang):
    food_items = re.findall(r'\b\w+\b', text.lower())
    info = {}
    for item in food_items:
        if item in NUTRITIONAL_INFO:
            info[item] = NUTRITIONAL_INFO[item]
    if info:
        return {
            "English": f"Nutritional information: {info}",
            "Swahili": f"Taarifa za lishe: {info}"
        }[lang]
    else:
        return {
            "English": "No nutritional information found.",
            "Swahili": "Hakuna taarifa za lishe zilizopatikana."
        }[lang]
        
def process_language_change(text):
    text_low = text.lower()
    if "english" in text_low:
        set_language("English")
        return {
            "English": "Language changed to English."
        }
    if "swahili" in text_low:
        set_language("Swahili")
        return {
            "English": "Lugha imebadilsishwa kwenda Swahili."
        }
    return None

def process_message(text, user_id):
    lang_change = process_language_change(text)
    lang = get_language()
    lower = text.lower()
    
    #greetings handler - must come first
    if any(g in lower for g in ["Habari", "Habari za asubuhi!", "Habari za mchana!", "Habari za usiku!", "Hello", "Hi"]):
        return {
            "English": "Hello! How can I assist you today?",
            "Swahili": "Habari! Naweza kukusaidia vipi leo?"
        }
    
    #lang change request
    lang_change = process_language_change(text)
    if lang_change:
        return {"English": lang_change["English"], "Swahili": lang_change["Swahili"]}
    
    #intent & budget logic
    response_parts = []
    intent = predict_intent(text)
    budget = extract_budget(text)
    
    if intent in ["food_suggestion_diet",  "food", "drink", "drink_suggestion"]:
        suggestion = process_budget(text, lang)
        if intent == "food_suggestion_diet":
            suggestion += "Also, please consider your dietary restrictions."
        response_parts.append(suggestion)
    elif intent == "disease_related":
        response_parts.append({
            "English": "For health-related questions, please consult a healthcare professional.",
            "Swahili": "Kwa maswali yanayohusiana na afya, tafadhali wasiliana na mtaalamu wa afya."
        }[lang])
    else:
        if any(word in text.lower() for word in ["goal", "lengo"]):
            goal_response = process_health_goal(user_id, text, lang)
            response_parts.append(goal_response)
        if any(word in text.lower() for word in ["vegan", "vegetarian", "gluten", "halal", "intolerant"]):
            dietary_resp = process_dietary_restrictions(text, lang)
            response_parts.append(dietary_resp)
        if any(word in text.lower() for word in ["nutrition", "calories", "protein", "breakdown", "lishe", "kalori"]):
            nutritional_resp = process_nutritional_info(text, lang)
            response_parts.append(nutritional_resp)
        if any(word in text.lower() for word in ["specialist", "doctor", "expert", "mtaalamu"]):
            specialist_resp = process_specialist(text, lang)
            response_parts.append(specialist_resp)
            
    if not response_parts:
        response_parts.append({
            "English": "I am TamuTalk. I can help you with food suggestions, dietary restrictions, and health goals. How may I assist today?",
            "Swahili": "Mimi ni TamuTalk. Naweza kukusaidia na mapendekezo ya chakula, list ya vyakula vya lishe, na malengo ya afya. Naweza kusaidia vipi leo?"
        }[lang])
    return "\n".join(map(str, response_parts))

@app.route("/")
def home():
    if "language" not in session:
        set_language("English")
    return render_template("home.html")

@app.route("/chat", methods=["POST"])
def chat():
    print(request.content_type,request.data)
    data = request.json
    user_message = data.get("message", "")
    #response = {"response": f"You said: {user_message}"}
    user_id = session.get("user_id", "default_user")
    
    #process the user's message and generate a response
    chatbot_response = process_message(user_message, user_id)
    
    #return the response as JSON 
    response_text = {"response": chatbot_response}
    return jsonify({
        'response': response_text,
        'swahili': response_text.get('swahili', ''),
        })
    
@app.route("/about")
def about():
    return render_template("about.html")
 """