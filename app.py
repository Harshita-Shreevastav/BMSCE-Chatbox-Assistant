"""
BMSCE Chatbot - Flask Backend + Frontend
BMS College of Engineering, Bangalore
AI Project - Complete Chatbot Application
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import re
import difflib
import os

# Gemini API fallback
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel("gemini-2.0-flash")
        GEMINI_AVAILABLE = True
        print("[+] Gemini API configured successfully")
    else:
        GEMINI_AVAILABLE = False
        print("[!] No Gemini API key found. Bot will use local knowledge base only.")
        print("    To enable AI fallback: add your key to .env file")
        print("    Get a free key at: https://aistudio.google.com/")
except ImportError:
    GEMINI_AVAILABLE = False
    print("[!] google-generativeai not installed. Run: pip install google-generativeai python-dotenv")

# ======================== SUPABASE SETUP ========================
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if supabase_url and supabase_key:
    SUPABASE_HEADERS = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    print("[+] Supabase configured successfully (REST API)")
else:
    SUPABASE_HEADERS = None
    print("[!] Supabase URL or Key missing from .env")

app = Flask(__name__)
CORS(app)

# ======================== STOP WORDS ========================
STOP_WORDS = {
    "is", "are", "the", "a", "an", "what", "which", "how", "do", "does",
    "can", "i", "me", "my", "in", "on", "at", "to", "for", "of", "and",
    "or", "it", "its", "this", "that", "there", "any", "about", "tell",
    "please", "give", "know", "want", "need", "have", "has", "been",
    "was", "were", "be", "will", "would", "should", "could", "may",
    "might", "shall", "than", "then", "so", "if", "but", "not", "no",
    "yes", "also", "very", "really", "just", "only", "some", "many",
    "much", "more", "most", "like", "get", "got", "with", "from", "by"
}

# ======================== INTENT DETECTION PATTERNS ========================
# Maps phrase patterns to intent names for smart matching
INTENT_PATTERNS = {
    # Clubs
    "best_club":     ["best club", "good club", "which club", "top club", "club join", "club recommendation"],
    "tech_clubs":    ["tech club", "coding club", "technical club", "programming club"],
    "clubs":         ["clubs", "societies", "organizations"],
    # Canteen
    "canteen_timings": ["canteen timing", "food timing", "mess timing", "canteen open", "food price",
                        "canteen menu", "where eat", "food available", "canteen close", "mess open",
                        "breakfast time", "lunch time", "dinner time", "snack price"],
    # Attendance
    "attendance_policy": ["attendance policy", "minimum attendance", "attendance percentage",
                          "attendance rule", "how much attendance"],
    "attendance_strictness": ["strict attendance", "teacher strict", "attendance strict",
                              "strict teacher attendance", "teachers strict", "strict about attendance"],
    "attendance_loopholes": ["bunk class", "skip class", "attendance hack", "proxy attendance",
                             "attendance loophole", "escape attendance", "manage attendance",
                             "shortage manage"],
    # Fests
    "fest_comparison": ["which fest", "utsav vs", "phase shift vs", "utsav or phase",
                        "best fest", "fest better", "fest comparison", "utsav phase shift"],
    # Sports
    "swimming_pool":   ["swimming pool", "pool open", "pool timing", "swim weekend", "pool weekend"],
    "gym_details":     ["gym timing", "gym open", "fitness center", "workout facility",
                        "gym fee", "is there gym", "is there a gym"],
    "sports_facilities": ["sports facility", "play sports", "basketball court", "cricket net",
                          "football ground", "badminton court"],
    # Hangout
    "hangout_spots":   ["hangout spot", "chill spot", "hidden place", "where sit",
                        "place relax", "secret spot", "hidden hangout", "place to sit",
                        "campus spot"],
    # Dress code
    "dress_code":      ["dress code", "wear shorts", "clothing rule", "what wear",
                        "uniform policy", "can wear", "shorts allowed", "crop top"],
    # Hostel
    "hostel_food":     ["hostel food", "mess food", "hostel quality", "best hostel food",
                        "hostel mess", "food hostel"],
    "hostel_rules":    ["hostel rule", "hostel curfew", "hostel facility", "hostel wifi",
                        "hostel detail", "hostel stay"],
    # Library
    "library_timings": ["library timing", "library close", "library open", "library hour",
                        "library exam", "study place", "library time"],
    # Teachers
    "strict_teachers": ["strict teacher", "tough teacher", "strictest department",
                        "hard teacher", "scary teacher", "difficult teacher",
                        "strictest teacher"],
    "best_teachers":   ["best teacher", "good teacher", "favorite teacher",
                        "popular teacher", "loved teacher"],
    # Branch change
    "branch_change":   ["branch change", "switch branch", "change department",
                        "transfer branch", "change branch", "switch department"],
    # Placements
    "cse_placement":   ["cse placement", "highest package", "cse salary", "top package",
                        "cse package", "aiml placement", "best package"],
    "all_placements":  ["branch placement", "placement stats", "placement comparison",
                        "all placement", "branch wise placement", "placement branch"],
    # Gender
    "gender_ratio":    ["gender ratio", "girls boys ratio", "male female ratio",
                        "girls ratio", "boys ratio", "girl boy ratio"],
    # General
    "about_bmsce":     ["about bmsce", "about bms", "college info", "tell about bmsce",
                        "what is bmsce", "bmsce details"],
    "admission_process": ["admission process", "how join", "cutoff rank", "entrance exam",
                          "admission bmsce", "kcet cutoff", "comedk cutoff", "get admission"],
    "wifi_campus":     ["wifi campus", "internet available", "wifi speed", "campus wifi",
                        "wifi college", "internet college"],
}


# ======================== SEARCH ENGINE ========================

def tokenize(text):
    """Convert text to lowercase tokens, removing punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return set(text.split())


def remove_stop_words(tokens):
    """Remove stop words from token set to extract meaningful words."""
    return tokens - STOP_WORDS


def detect_intent(query_lower):
    """
    Detect the intent from the user's query by matching against
    known phrase patterns. Returns intent name or None.
    """
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if pattern in query_lower:
                return intent
    return None


def fuzzy_correct(query_str, all_keywords, cutoff=0.75):
    """
    Use difflib to find close matches for each query word against
    all known keywords. Returns a set of corrected tokens.
    """
    corrected = set()
    for word in query_str.split():
        if len(word) < 3:
            corrected.add(word)
            continue
        matches = difflib.get_close_matches(word, all_keywords, n=1, cutoff=cutoff)
        corrected.add(matches[0] if matches else word)
    return corrected


def compute_score(query_tokens, query_str, entry, detected_intent, fuzzy_tokens):
    """
    Score an entry against the user query using 3 layers:
    1. Intent match (highest priority, +50)
    2. Keyword match (primary, +10 per keyword)
    3. Fuzzy match bonus (+20 if fuzzy-corrected tokens hit keywords)
    """
    score = 0

    # Layer 1: Intent match - if detected intent matches entry intents
    entry_intents = entry.get("intents", [])
    if detected_intent and detected_intent in entry_intents:
        score += 50

    # Layer 2: Keyword matching
    for kw in entry["keywords"]:
        kw_tokens = set(kw.lower().split())
        matched = kw_tokens & query_tokens
        if matched:
            score += len(matched) * 10

    # Question text matching
    question_tokens = tokenize(entry["question"])
    common = query_tokens & question_tokens
    score += len(common) * 5

    # Exact phrase bonus in keywords
    for kw in entry["keywords"]:
        if kw.lower() in query_str:
            score += 15

    # Layer 3: Fuzzy match bonus
    if fuzzy_tokens != query_tokens:
        for kw in entry["keywords"]:
            kw_tokens = set(kw.lower().split())
            fuzzy_matched = kw_tokens & fuzzy_tokens
            if fuzzy_matched and not (kw_tokens & query_tokens):
                score += len(fuzzy_matched) * 20

        # Fuzzy intent match on entry intents
        for intent_name in entry_intents:
            intent_words = set(intent_name.replace("_", " ").split())
            if intent_words & fuzzy_tokens:
                score += 15

    # Boost higher trust levels for tie-breaking
    score += (4 - entry["trust_level"]) * 0.5

    return score


def find_contradiction_group(entry_id):
    """Check if an entry belongs to a contradiction group."""
    if not SUPABASE_HEADERS: return None, []
    try:
        r = requests.get(f"{supabase_url}/rest/v1/contradiction_groups?select=*", headers=SUPABASE_HEADERS)
        if r.status_code == 200:
            groups = r.json()
            for group in groups:
                if entry_id in group.get("entry_ids", []):
                    return group["group_name"], group["entry_ids"]
    except Exception as e:
        app.logger.error(f"[!] Failed to fetch contradiction groups: {e}")
    return None, []


def search(query):
    """
    Main search function with smart matching.
    1. Removes stop words
    2. Detects intent from phrase patterns
    3. Applies fuzzy correction for typos
    4. Scores all entries and returns best match
    5. Shows multiple perspectives for contradictory topics
    """
    query_lower = query.lower().strip()
    query_clean = re.sub(r'[^\w\s]', ' ', query_lower)
    query_tokens = set(query_clean.split())

    if not query_tokens:
        return {
            "response": "Please ask me something about BMSCE! I can help with clubs, canteen, placements, hostels, and more.",
            "trust_level": 0,
            "source": "System",
            "category": "general"
        }

    # Step 1: Remove stop words for better signal
    meaningful_tokens = remove_stop_words(query_tokens)
    if not meaningful_tokens:
        meaningful_tokens = query_tokens  # fallback if all words are stop words

    # Step 2: Detect intent from raw query
    detected_intent = detect_intent(query_clean)

    # Fetch Knowledge Base from Supabase
    if not SUPABASE_HEADERS:
        knowledge_base = []
    else:
        try:
            r = requests.get(f"{supabase_url}/rest/v1/kb_entries?select=*", headers=SUPABASE_HEADERS)
            if r.status_code == 200:
                knowledge_base = r.json()
            else:
                knowledge_base = []
        except Exception as e:
            app.logger.error(f"[!] Failed to fetch data from Supabase: {e}")
            knowledge_base = []

    # Step 3: Build vocabulary for fuzzy matching
    all_keywords = set()
    for entry in knowledge_base:
        for kw in entry.get("keywords", []):
            all_keywords.update(kw.lower().split())
        for intent in entry.get("intents", []):
            all_keywords.update(intent.replace("_", " ").split())
    fuzzy_tokens = fuzzy_correct(query_clean, list(all_keywords))

    # Step 4: Score all entries
    scored = []
    for entry in knowledge_base:
        s = compute_score(meaningful_tokens, query_clean, entry, detected_intent, fuzzy_tokens)
        if s > 0:
            scored.append((s, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Debug: log top matches for troubleshooting
    if scored:
        top3 = scored[:3]
        print(f"[Search] Query: '{query_clean}' | Top match: '{top3[0][1]['id']}' (score={top3[0][0]})")
    else:
        print(f"[Search] Query: '{query_clean}' | No matches found")

    # MINIMUM SCORE THRESHOLD - prevents returning wrong low-confidence matches
    # Raised to 40 to ensure only strong matches return local KB answers
    # Weak matches (e.g. "HOD of AIML" matching "about_bmsce" by keyword "department")
    # should fall through to Gemini for a proper AI answer
    MINIMUM_SCORE_THRESHOLD = 40

    if not scored or scored[0][0] < MINIMUM_SCORE_THRESHOLD:
        return {
            "response": (
                "I don't have specific information about that in my local knowledge base. "
                "Let me search for an answer..."
            ),
            "trust_level": 0,
            "source": "System",
            "category": "general"
        }

    best_score, best_entry = scored[0]

    # Check for contradiction group
    group_name, group_ids = find_contradiction_group(best_entry["id"])
    if group_name:
        group_entries = [e for _, e in scored if e["id"] in group_ids]
        if len(group_entries) > 1:
            return build_contradiction_response(group_entries)

    return build_single_response(best_entry)


def build_single_response(entry):
    """Build response for a single matching entry."""
    answer = entry["answer"]

    # Trust level 3 prefix (if not already present)
    if entry["trust_level"] == 3 and "STUDENT OPINION" not in answer:
        answer = "STUDENT OPINION (Subjective - may vary):\n\n" + answer

    # Controversial disclaimer (if not already present)
    if entry["controversial"] and "Individual experiences may differ" not in answer:
        answer += "\n\nIndividual experiences may differ"

    # Trust badge
    badges = {1: "Official", 2: "Verified Reviews", 3: "Student Opinion"}
    badge = badges.get(entry["trust_level"], "")
    answer = f"[{badge}]\n\n{answer}"

    return {
        "response": answer,
        "trust_level": entry["trust_level"],
        "source": entry["source"],
        "category": entry["category"]
    }


def build_contradiction_response(entries):
    """Build response showing multiple perspectives."""
    parts = ["Multiple perspectives found:\n"]
    badges = {1: "Official", 2: "Verified Reviews", 3: "Student Opinion"}

    for entry in entries:
        badge = badges.get(entry["trust_level"], "")
        parts.append(f"--- [{badge}] (Source: {entry['source']}) ---")
        parts.append(entry["answer"])
        parts.append("")

    parts.append("Individual experiences may differ. Consider all viewpoints!")

    return {
        "response": "\n".join(parts),
        "trust_level": min(e["trust_level"] for e in entries),
        "source": ", ".join(set(e["source"] for e in entries)),
        "category": entries[0]["category"]
    }


# ======================== GEMINI AI ENGINE ========================

# Load BMSCE context from scraped website data
BMSCE_CONTEXT = ""
context_path = os.path.join(os.path.dirname(__file__), "bmsce_context.txt")
try:
    with open(context_path, "r", encoding="utf-8") as f:
        BMSCE_CONTEXT = f.read()
    print(f"[+] Loaded BMSCE context: {len(BMSCE_CONTEXT)} chars from bmsce_context.txt")
except FileNotFoundError:
    print("[!] bmsce_context.txt not found. Gemini will work without scraped context.")

GEMINI_SYSTEM_PROMPT = (
    "You are BMSCE Campus Assistant, an AI chatbot for BMS College of Engineering, Bangalore. "
    "You can answer ANY question - both BMSCE-specific and general knowledge questions.\n\n"
    "BEHAVIOR:\n"
    "1. For BMSCE-related questions (departments, HODs, faculty, fees, placements, clubs, "
    "hostel, library, sports, fests, admissions, campus life, etc.):\n"
    "   - Use the BMSCE REFERENCE DATA below as your PRIMARY source\n"
    "   - Give detailed, accurate answers with specific names, numbers, and URLs\n"
    "   - If info is not in the reference data, use your general knowledge\n"
    "   - Always mention the relevant bmsce.ac.in URL when applicable\n"
    "   - Add a note to verify with official sources for critical info\n\n"
    "2. For GENERAL questions (science, math, coding, history, etc.):\n"
    "   - Answer like a helpful AI assistant (similar to ChatGPT)\n"
    "   - Give clear, accurate, well-structured answers\n"
    "   - No need to redirect to BMSCE for general questions\n\n"
    "3. FORMAT: Keep answers concise but complete (under 300 words). "
    "Use bullet points and line breaks. Use plain text, no markdown ** or ##.\n\n"
    "BMSCE REFERENCE DATA:\n---\n"
    + BMSCE_CONTEXT +
    "\n---\n"
)

def ask_gemini(user_message):
    """Send question to Gemini API with full BMSCE context."""
    app.logger.error(f"[ask_gemini] Called with message: {user_message}")
    app.logger.error(f"[ask_gemini] GEMINI_AVAILABLE is {GEMINI_AVAILABLE}")
    if not GEMINI_AVAILABLE:
        return None
    try:
        prompt = GEMINI_SYSTEM_PROMPT + "\n\nUser question: " + user_message
        app.logger.error(f"[ask_gemini] Generating content...")
        response = gemini_model.generate_content(prompt)
        app.logger.error(f"[ask_gemini] Response received: {response}")
        if response and response.text:
            answer = response.text.strip()
            bmsce_kw = ["bmsce", "bms college", "department", "hod", "faculty",
                        "placement", "hostel", "canteen", "fest", "utsav",
                        "phase shift", "library", "admission", "kcet", "comedk",
                        "campus", "club", "principal", "dean"]
            is_bmsce = any(kw in user_message.lower() for kw in bmsce_kw)
            if is_bmsce:
                source_label = "BMSCE Official Data + AI"
                answer += "\n\n(Source: BMSCE official website + AI. Verify critical info at bmsce.ac.in)"
            else:
                source_label = "AI Assistant (Gemini)"
            return {
                "response": answer,
                "trust_level": 2 if is_bmsce else 3,
                "source": source_label,
                "category": "bmsce_ai" if is_bmsce else "general_ai"
            }
        else:
            app.logger.error(f"[ask_gemini] Response has no text. Parts: {response.parts if hasattr(response, 'parts') else 'None'}")
    except Exception as e:
        app.logger.error(f"[!] Gemini API error: {e}")
        import traceback
        app.logger.error(traceback.format_exc())
    return None


# ======================== API ROUTES ========================

@app.route("/chat", methods=["POST"])
def chat():
    """Main chat endpoint. Tries local KB first, falls back to Gemini API."""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Please send a JSON body with 'message' field"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    result = search(user_message)

    # If local search returned low-confidence match, try Gemini
    if result.get("source") == "System" and result.get("trust_level") == 0:
        # 1. Try dynamic web scraping
        try:
            from web_scraper import web_scrape_for_answer
            scraped_answer, source_url = web_scrape_for_answer(user_message, gemini_model if GEMINI_AVAILABLE else None)
            
            if scraped_answer:
                import uuid
                new_entry = {
                    "id": f"dynamic_{uuid.uuid4().hex[:8]}",
                    "question": user_message,
                    "answer": scraped_answer,
                    "source": source_url,
                    "trust_level": 3,
                    "category": "dynamic_web",
                    "keywords": [w for w in user_message.lower().split() if w not in STOP_WORDS and len(w) > 2],
                    "intents": [],
                    "controversial": False
                }
                if SUPABASE_HEADERS:
                    try:
                        r = requests.post(f"{supabase_url}/rest/v1/kb_entries", json=new_entry, headers=SUPABASE_HEADERS)
                        if r.status_code in (200, 201, 204):
                            print(f"[+] Dynamically appended new answer to Supabase: {new_entry['id']}")
                        else:
                            print(f"[!] Failed to insert dynamic entry: {r.text}")
                    except Exception as e:
                        print(f"[!] Failed to insert dynamic entry: {e}")
                
                return jsonify({
                    "response": f"[Web Search]\n\n{scraped_answer}\n\n(Source: {source_url})",
                    "trust_level": 3,
                    "source": source_url,
                    "category": "dynamic_web"
                })
        except Exception as e:
            app.logger.error(f"[!] Web scraping integration error: {e}")

        # 2. Fall back to general Gemini
        gemini_result = ask_gemini(user_message)
        if gemini_result:
            return jsonify(gemini_result)

    return jsonify(result)



@app.route("/")
def index():
    """Serve the chatbot frontend."""
    return render_template("index.html")


# ======================== RUN SERVER ========================
if __name__ == "__main__":
    print("\n[*] BMSCE Chatbot Server Starting...")
    print("[*] Open http://localhost:5000 in your browser")
    if GEMINI_AVAILABLE:
        print("[*] Gemini AI fallback: ENABLED")
    else:
        print("[*] Gemini AI fallback: DISABLED (local KB only)")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
