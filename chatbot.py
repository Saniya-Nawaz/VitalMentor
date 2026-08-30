import os
import re


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KB_FOLDER = os.path.join(
    BASE_DIR,
    "knowledge_base"
)


# =========================================================
# CONVERSATION MEMORY
# =========================================================

conversation_memory = {
    "last_topic": None
}


# =========================================================
# TOPIC KEYWORDS
# =========================================================

TOPIC_KEYWORDS = {

    "fever": [
        "fever",
        "temperature",
        "high temperature",
        "pyrexia"
    ],

    "cold": [
        "cold",
        "runny nose",
        "blocked nose",
        "stuffy nose",
        "sneezing"
    ],

    "cough": [
        "cough",
        "coughing"
    ],

    "nutrition": [
        "nutrition",
        "food",
        "diet",
        "eating",
        "meal",
        "meals",
        "healthy food"
    ],

    "hydration": [
        "water",
        "hydration",
        "thirst",
        "drink",
        "drinking",
        "dehydration"
    ],

    "sleep": [
        "sleep",
        "sleeping",
        "bedtime",
        "tired",
        "rest",
        "sleep hours"
    ],

    "exercise": [
        "exercise",
        "activity",
        "physical activity",
        "walking",
        "running",
        "playing",
        "steps"
    ],

    "growth": [
        "growth",
        "height",
        "weight",
        "growing"
    ],

    "vaccines": [
        "vaccine",
        "vaccination",
        "vaccines",
        "immunization",
        "immunisation"
    ],

    "allergies": [
        "allergy",
        "allergies",
        "allergic"
    ],

    "first_aid": [
        "first aid",
        "injury",
        "wound",
        "cut",
        "burn",
        "bleeding"
    ],

    "mental_health": [
        "stress",
        "anxiety",
        "sad",
        "sadness",
        "mental health",
        "mood",
        "emotional",
        "emotion",
        "worried",
        "worry"
    ],

    "hygiene": [
        "hygiene",
        "clean",
        "cleanliness",
        "hand washing",
        "wash hands"
    ],

    "screen_time": [
        "screen",
        "screen time",
        "mobile",
        "phone",
        "tablet",
        "television",
        "tv"
    ]
}


# =========================================================
# SECTION KEYWORDS
# =========================================================

SECTION_KEYWORDS = {

    "what": "What is",
    "definition": "What is",

    "cause": "Common Causes",
    "causes": "Common Causes",
    "reason": "Common Causes",

    "symptom": "Symptoms",
    "symptoms": "Symptoms",
    "sign": "Symptoms",
    "signs": "Symptoms",

    "home": "Home Care",
    "care": "Home Care",
    "home care": "Home Care",

    "hydration": "Hydration Advice",
    "water": "Hydration Advice",
    "drink": "Hydration Advice",

    "food": "Foods to Eat",
    "foods": "Foods to Eat",
    "eat": "Foods to Eat",
    "eating": "Foods to Eat",

    "avoid": "Foods to Avoid",
    "avoid food": "Foods to Avoid",

    "doctor": "When to Consult a Doctor",
    "hospital": "When to Consult a Doctor",
    "medical help": "When to Consult a Doctor",
    "consult": "When to Consult a Doctor",

    "prevent": "Prevention",
    "prevention": "Prevention",

    "tip": "Fun Health Tip",
    "tips": "Fun Health Tip"
}


# =========================================================
# TOPIC → KNOWLEDGE BASE FILE
# =========================================================

TOPIC_FILES = {

    "fever": "fever",
    "cold": "cold",
    "cough": "cough",
    "nutrition": "nutrition",
    "hydration": "hydration",
    "sleep": "sleep",
    "exercise": "exercise",
    "growth": "growth",
    "vaccines": "vaccines",
    "allergies": "allergies",
    "first_aid": "first_aid",
    "mental_health": "mental_health",
    "hygiene": "hygiene",
    "screen_time": "screen_time"
}


# =========================================================
# READ KNOWLEDGE BASE
# =========================================================

def read_knowledge(topic):

    filename = TOPIC_FILES.get(topic)

    if filename is None:
        return None

    file_path = os.path.join(
        KB_FOLDER,
        f"{filename}.txt"
    )

    if not os.path.exists(file_path):
        return None

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception as e:

        print(
            f"Knowledge base error: {e}"
        )

        return None


# =========================================================
# FIND TOPIC
# =========================================================

def find_topic(query):

    if not query:
        return None

    query = str(query).lower().strip()

    # Check longer phrases first
    all_keywords = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            all_keywords.append(
                (keyword, topic)
            )

    all_keywords.sort(
        key=lambda x: len(x[0]),
        reverse=True
    )

    for keyword, topic in all_keywords:

        if keyword in query:
            return topic

    return None


# =========================================================
# FIND SECTION
# =========================================================

def find_section(query):

    if not query:
        return None

    query = str(query).lower().strip()

    # Longer phrases first
    section_items = sorted(
        SECTION_KEYWORDS.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    for keyword, section in section_items:

        if keyword in query:
            return section

    return None


# =========================================================
# EXTRACT SECTION FROM KNOWLEDGE BASE
# =========================================================

def get_section(content, section):

    if not content:
        return None

    # If user did not ask for a particular section,
    # return the complete knowledge base.
    if section is None:
        return content.strip()

    # Expected heading format:
    #
    # 1. What is Fever?
    # 2. Common Causes
    # 3. Symptoms
    #
    pattern = re.compile(
        r"^\s*\d+\.\s*(.+?)\s*$",
        re.MULTILINE
    )

    matches = list(
        pattern.finditer(content)
    )

    if not matches:

        return content.strip()

    target_section = section.lower().strip()

    for i, match in enumerate(matches):

        heading = match.group(1).strip()

        heading_lower = heading.lower()

        if (
            target_section in heading_lower
            or heading_lower in target_section
        ):

            start = match.end()

            if i + 1 < len(matches):

                end = matches[i + 1].start()

            else:

                end = len(content)

            result = content[
                start:end
            ].strip()

            if result:
                return result

    return (
        "Sorry, I couldn't find that specific "
        "section in my knowledge base."
    )


# =========================================================
# SAFE NUMBER CONVERSION
# =========================================================

def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        return float(value)

    except (
        ValueError,
        TypeError
    ):

        return default


# =========================================================
# PERSONALIZED HEALTH ANALYSIS
# =========================================================

def get_health_advice(data):

    advice = []

    # -----------------------------------------------------
    # WATER
    # -----------------------------------------------------

    water = safe_float(
        data.get("water_intake", 0)
    )

    if water <= 0:

        advice.append(
            "💧 Water intake data is not available yet."
        )

    elif water < 800:

        advice.append(
            f"💧 Water intake is {water:.0f} ml. "
            "This is currently on the lower side, "
            "so encourage regular water intake."
        )

    elif water < 1500:

        advice.append(
            f"💧 Water intake today is {water:.0f} ml. "
            "Keep encouraging regular hydration."
        )

    else:

        advice.append(
            f"💧 Water intake today: {water:.0f} ml. "
            "Good hydration progress! 🌊"
        )


    # -----------------------------------------------------
    # SLEEP
    # -----------------------------------------------------

    sleep = safe_float(
        data.get("sleep_hours", 0)
    )

    if sleep <= 0:

        advice.append(
            "😴 Sleep data is not available yet."
        )

    elif sleep < 6:

        advice.append(
            f"😴 Sleep was only {sleep:.1f} hours. "
            "A consistent bedtime routine may help."
        )

    elif sleep < 8:

        advice.append(
            f"😴 Sleep was {sleep:.1f} hours. "
            "Consider an earlier bedtime for better rest."
        )

    else:

        advice.append(
            f"😴 Sleep looks good at {sleep:.1f} hours. 🌙"
        )


    # -----------------------------------------------------
    # STEPS
    # -----------------------------------------------------

    steps = safe_float(
        data.get("steps", 0)
    )

    if steps < 3000:

        advice.append(
            f"👣 Activity is currently {steps:.0f} steps. "
            "Some walking, outdoor play or exercise "
            "could help increase activity."
        )

    elif steps < 7000:

        advice.append(
            f"👣 Today's activity is {steps:.0f} steps. "
            "A little more active play could be beneficial."
        )

    else:

        advice.append(
            f"👣 Great activity level today: "
            f"{steps:.0f} steps! 🎮"
        )


    # -----------------------------------------------------
    # HEART RATE
    # -----------------------------------------------------

    heart_rate = safe_float(
        data.get("heart_rate", 0)
    )

    if heart_rate > 0:

        advice.append(
            f"❤️ Latest recorded heart rate: "
            f"{heart_rate:.0f} BPM."
        )


    # -----------------------------------------------------
    # TEMPERATURE
    # -----------------------------------------------------

    temperature = safe_float(
        data.get("temperature", 0)
    )

    if temperature > 0:

        advice.append(
            f"🌡️ Latest recorded temperature: "
            f"{temperature:.1f}°C."
        )


    return advice


# =========================================================
# HEALTH STATUS SCORE
# =========================================================

def get_health_score(data):

    score = 100

    water = safe_float(
        data.get("water_intake", 0)
    )

    sleep = safe_float(
        data.get("sleep_hours", 0)
    )

    steps = safe_float(
        data.get("steps", 0)
    )

    temperature = safe_float(
        data.get("temperature", 0)
    )


    # Water
    if water < 800:
        score -= 15
    elif water < 1200:
        score -= 5


    # Sleep
    if sleep < 6:
        score -= 20
    elif sleep < 8:
        score -= 10


    # Activity
    if steps < 3000:
        score -= 15
    elif steps < 5000:
        score -= 5


    # Temperature
    if temperature >= 38:
        score -= 20


    score = max(
        0,
        min(100, score)
    )

    return score


# =========================================================
# HEALTH STATUS
# =========================================================

def get_health_status(data):

    score = get_health_score(data)

    if score >= 85:

        return (
            score,
            "🟢 Good",
            "Your child's current health indicators "
            "look generally positive."
        )

    elif score >= 65:

        return (
            score,
            "🟡 Needs Attention",
            "Some health indicators could be improved."
        )

    else:

        return (
            score,
            "🟠 Needs Monitoring",
            "Several indicators may need attention."
        )


# =========================================================
# GENERAL HEALTH QUESTION
# =========================================================

def is_health_status_question(query):

    query = str(query).lower()

    phrases = [

        "how is my child",

        "how is my child's health",

        "how is my childs health",

        "child health today",

        "my child's health today",

        "my childs health today",

        "overall health",

        "health status",

        "health today",

        "health condition",

        "is my child healthy",

        "is my child okay",

        "how healthy"

    ]

    for phrase in phrases:

        if phrase in query:
            return True

    return False


# =========================================================
# BUILD HEALTH OVERVIEW
# =========================================================

def build_health_overview(data):

    score, status, description = (
        get_health_status(data)
    )

    advice = get_health_advice(data)

    response = (
        "📊 **Your Child's Latest Health Overview**\n\n"
    )

    response += (
        f"🏅 **Health Score:** {score}/100\n"
    )

    response += (
        f"📌 **Status:** {status}\n\n"
    )

    response += (
        f"{description}\n\n"
    )

    response += (
        "### Today's Indicators\n\n"
    )

    for item in advice:

        response += (
            f"{item}\n\n"
        )

    response += (
        "💡 **Tip:** Keep monitoring these indicators "
        "regularly. A single reading should not be "
        "treated as a medical diagnosis."
    )

    return response


# =========================================================
# MEDICAL DISCLAIMER
# =========================================================

def add_medical_disclaimer(response, topic):

    medical_topics = [

        "fever",
        "cold",
        "cough",
        "first_aid",
        "allergies",
        "mental_health"
    ]

    if topic in medical_topics:

        response += (
            "\n\n---\n"
            "⚠️ **Medical Disclaimer:** "
            "This information is for educational purposes "
            "only and does not replace advice from a "
            "qualified healthcare professional."
        )

    return response


# =========================================================
# MAIN CHATBOT FUNCTION
# =========================================================

def respond(query, data):

    global conversation_memory

    if not query:

        return (
            "👋 Ask me something about your child's "
            "health, sleep, water, nutrition, activity "
            "or symptoms."
        )


    query = str(query).strip()

    query_lower = query.lower()


    # =====================================================
    # GENERAL HEALTH STATUS
    # =====================================================

    if is_health_status_question(query):

        # Remember that user asked about general health
        conversation_memory["last_topic"] = "health"

        return build_health_overview(data)


    # =====================================================
    # FIND TOPIC
    # =====================================================

    topic = find_topic(query)


    # =====================================================
    # FOLLOW-UP QUESTION
    # =====================================================

    # Example:
    #
    # User: "My child has fever"
    # Bot: fever information
    #
    # User: "What should they eat?"
    #
    # The second question doesn't contain "fever",
    # so use the previous topic.

    if topic is None:

        previous_topic = (
            conversation_memory.get(
                "last_topic"
            )
        )

        if previous_topic not in [
            None,
            "health"
        ]:

            topic = previous_topic


    # =====================================================
    # SAVE MEMORY
    # =====================================================

    if topic is not None:

        conversation_memory["last_topic"] = topic


    # =====================================================
    # DIRECT HEALTH METRIC QUESTIONS
    # =====================================================

    if "water" in query_lower:

        water = safe_float(
            data.get("water_intake", 0)
        )

        if (
            "how much" in query_lower
            or "intake" in query_lower
            or "today" in query_lower
            or "enough" in query_lower
        ):

            if water < 800:

                return (
                    f"💧 Your child's recorded water intake "
                    f"is **{water:.0f} ml** today.\n\n"
                    "This is currently on the lower side. "
                    "Encourage small amounts of water "
                    "throughout the day."
                )

            return (
                f"💧 Your child's recorded water intake "
                f"is **{water:.0f} ml** today.\n\n"
                "Keep encouraging regular hydration. 🌊"
            )


    if "sleep" in query_lower:

        sleep = safe_float(
            data.get("sleep_hours", 0)
        )

        return (
            f"😴 Your child's latest recorded sleep "
            f"duration is **{sleep:.1f} hours**.\n\n"
            + (
                "The duration is relatively low, so "
                "a consistent bedtime routine may help."
                if sleep < 6
                else
                "Keeping a regular sleep schedule is a "
                "good habit."
            )
        )


    if (
        "steps" in query_lower
        or "activity" in query_lower
    ):

        steps = safe_float(
            data.get("steps", 0)
        )

        return (
            f"👣 Your child's latest recorded activity "
            f"is **{steps:.0f} steps**.\n\n"
            + (
                "Encourage some active play or walking."
                if steps < 3000
                else
                "Nice! Keep encouraging active play. 🎮"
            )
        )


    # =====================================================
    # KNOWLEDGE BASE
    # =====================================================

    if topic:

        answer = read_knowledge(topic)

        if answer:

            section = find_section(query)

            answer = get_section(
                answer,
                section
            )


            # -------------------------------------------------
            # PERSONALIZED HEALTH DATA
            # -------------------------------------------------

            health_advice = get_health_advice(
                data
            )

            if health_advice:

                answer += (
                    "\n\n📊 **Based on the child's "
                    "latest health data:**\n\n"
                )

                for item in health_advice:

                    answer += (
                        f"{item}\n\n"
                    )


            # -------------------------------------------------
            # DISCLAIMER
            # -------------------------------------------------

            answer = add_medical_disclaimer(
                answer,
                topic
            )

            return answer


    # =====================================================
    # UNKNOWN QUESTION
    # =====================================================

    return (
        "🤔 I don't have information about that topic "
        "yet.\n\n"
        "Try asking me about:\n\n"
        "🌡️ Fever\n"
        "🤧 Cold\n"
        "😷 Cough\n"
        "💧 Hydration\n"
        "🥗 Nutrition\n"
        "😴 Sleep\n"
        "👣 Exercise\n"
        "📈 Growth\n"
        "💉 Vaccines\n"
        "🤕 First Aid\n"
        "🧠 Mental Health\n"
        "🧼 Hygiene\n"
        "📱 Screen Time\n\n"
        "You can also ask:\n"
        "👉 **How is my child's health today?**"
    )