"""
BMSCE Chatbot Knowledge Base
Contains all structured data for the BMS College of Engineering chatbot.
Each entry has: answer, source, trust_level, category, keywords, and controversial flag.
"""

KNOWLEDGE_BASE = [
    # ======================== CLUBS & CULTURAL ========================
    {
        "id": "clubs_best",
        "question": "Which is the best club in college?",
        "answer": (
            "BMSCE has many active student clubs and societies (2024-25):\n\n"
            "Technical & Professional:\n"
            "- BMSCE IEEE (incl. Computer Society, PES, Sensors Council)\n"
            "- BMSCE ACM Student Chapter - coding, research, workshops\n"
            "- Coding Club, Robotics Club, Drone Club, IoT Club\n"
            "- GDSC (Google Developer Student Club)\n\n"
            "Cultural & Literary:\n"
            "- Inksanity - Literary & debate society\n"
            "- Pravrutthi - Theatre club\n"
            "- Various dance, music & drama groups\n\n"
            "Service & Others:\n"
            "- NSS (National Service Scheme) & NCC\n"
            "- Rotaract Club - community service\n"
            "- Vahini - Social Media & PR Cell\n"
            "- Mountaineering Club\n\n"
            "Each department also has its own Student Affinity Groups. "
            "Check the Dean Student Affairs desk or department pages on bmsce.ac.in for current recruitment."
        ),
        "source": "BMSCE Official Website & Student Reviews 2024",
        "trust_level": 2,
        "category": "club",
        "keywords": ["club", "best", "ieee", "acm", "rotaract", "join", "society", "organization", "extracurricular", "activity", "inksanity", "pravrutthi", "nss", "ncc"],
        "intents": ["best_club", "clubs", "club_recommendation", "good_club", "which_club", "top_club"],
        "controversial": False
    },
    {
        "id": "clubs_tech",
        "question": "What are the best technical clubs?",
        "answer": (
            "Top technical clubs at BMSCE (2024-25):\n"
            "1. BMSCE IEEE - Multiple societies (CS, PES, Sensors Council), workshops & conferences\n"
            "2. BMSCE ACM Student Chapter - Coding competitions, research, innovation\n"
            "3. Coding Club - Department-level coding contests & practice\n"
            "4. Drone Club - UAV projects & competitions\n"
            "5. IoT Club - Internet of Things projects\n"
            "6. Robotics Club - Hardware + software projects\n"
            "7. Electronics Club - Circuit design & embedded systems\n\n"
            "Most departments run their own technical affinity groups as well."
        ),
        "source": "BMSCE Official Website 2024",
        "trust_level": 2,
        "category": "club",
        "keywords": ["technical", "tech", "coding", "programming", "hackathon", "club", "ieee", "acm", "gdsc", "robotics", "drone", "iot"],
        "intents": ["tech_clubs", "coding_club", "technical_club", "clubs"],
        "controversial": False
    },

    # ======================== CANTEEN ========================
    {
        "id": "canteen_timings",
        "question": "What are the canteen timings?",
        "answer": (
            "BMSCE Canteen & Mess Info (2024):\n\n"
            "There are multiple canteens on campus serving snacks, beverages, and meals. "
            "They are generally open during college hours for all students and staff.\n\n"
            "Hostel Mess Timings (for hostellers):\n"
            "- Breakfast: 7:30 AM - 9:00 AM\n"
            "- Lunch: 12:30 PM - 2:00 PM\n"
            "- Snacks: 4:30 PM - 5:30 PM\n"
            "- Dinner: 7:30 PM - 9:00 PM\n\n"
            "Popular affordable options available include South Indian dishes, "
            "North Indian thalis, snacks, and beverages. Prices are student-friendly."
        ),
        "source": "BMSCE Campus Data 2024",
        "trust_level": 2,
        "category": "canteen",
        "keywords": ["canteen", "food", "timing", "eat", "breakfast", "lunch", "dinner", "mess", "dosa", "price", "menu", "snack"],
        "intents": ["canteen_timings", "food_timings", "mess_timings", "canteen_open", "food_price", "canteen_menu", "where_eat"],
        "controversial": False
    },

    # ======================== ATTENDANCE ========================
    {
        "id": "attendance_policy",
        "question": "What is the attendance policy?",
        "answer": (
            "📋 Official Attendance Policy:\n"
            "Minimum 85% attendance is mandatory across all departments.\n\n"
            "If below 85%:\n"
            "• Must submit an undertaking letter\n"
            "• May need to write extra assignments\n"
            "• Risk of detention (not allowed to sit for exams)\n\n"
            "Some teachers allow 2-3 shortages if you maintain good grades."
        ),
        "source": "Official College Data",
        "trust_level": 1,
        "category": "attendance",
        "keywords": ["attendance", "percentage", "minimum", "policy", "shortage", "detention", "absent", "mandatory", "85"],
        "intents": ["attendance_policy", "attendance_rules", "minimum_attendance", "attendance_percentage"],
        "controversial": False
    },
    {
        "id": "attendance_strict",
        "question": "Are teachers strict about attendance?",
        "answer": (
            "Teacher strictness varies BY DEPARTMENT:\n\n"
            "🔴 Strictest: ECE, Civil, Mechanical\n"
            "   - Teachers mark attendance in first 5 minutes\n"
            "   - Very little room for negotiation\n\n"
            "🟡 Moderate: CSE, ISE, AIML\n"
            "   - Some leniency with medical certificates\n"
            "   - Good grades can help your case\n\n"
            "🟢 Lenient: Biotechnology\n"
            "   - Can be managed with good rapport with faculty\n\n"
            "⚠️ Individual experiences may differ"
        ),
        "source": "Multiple Student Surveys 2024",
        "trust_level": 2,
        "category": "attendance",
        "keywords": ["strict", "teacher", "attendance", "lenient", "department", "marking", "proxy", "leniency"],
        "intents": ["attendance_strictness", "strict_attendance", "teacher_strict", "attendance_strict"],
        "controversial": True
    },
    {
        "id": "attendance_loopholes",
        "question": "Are there any attendance loopholes?",
        "answer": (
            "🧑‍🎓 STUDENT OPINION (Subjective - may vary):\n\n"
            "Some commonly shared tips:\n"
            "• Medical certificates accepted if submitted within 3 days\n"
            "• Participation in fests/events sometimes counts as attendance\n"
            "• Some teachers give credit if you show genuine effort in their subject\n"
            "• Final year students reportedly get more leniency\n\n"
            "⚠️ Individual experiences may differ. Always check with your department."
        ),
        "source": "Anonymous Student Surveys",
        "trust_level": 3,
        "category": "attendance",
        "keywords": ["loophole", "attendance", "hack", "trick", "proxy", "bunk", "skip", "escape", "shortage", "manage"],
        "intents": ["attendance_loopholes", "bunk_class", "skip_class", "attendance_hack", "proxy_attendance"],
        "controversial": True
    },

    # ======================== FESTS ========================
    {
        "id": "fests_comparison",
        "question": "Which fest is better - Utsav or Phase Shift?",
        "answer": (
            "BMSCE Fest Comparison (2024-25):\n\n"
            "UTSAV (May) - Annual Techno-Cultural Festival:\n"
            "- One of the largest student-run fests in South India\n"
            "- 2025 theme: 'Ananta' (infinite/boundless)\n"
            "- Events: music, dance, fashion shows, drama, DJ night, Whiplash Concert\n"
            "- More cultural/party-oriented, great for socializing\n\n"
            "PHASE SHIFT (Sept/Dec) - International Technical Symposium:\n"
            "- 2024 theme: 'Resurgence: Transforming Tomorrow Sustainably' (Dec 5-6)\n"
            "- 2025 theme: 'Meridian' (Sept 19-20)\n"
            "- Workshops, hackathons, seminars, industry collaborations\n"
            "- Better for tech enthusiasts & career networking\n\n"
            "Both attract thousands of participants. Utsav for fun, Phase Shift for tech!"
        ),
        "source": "BMSCE Official Events 2024-25",
        "trust_level": 2,
        "category": "fest",
        "keywords": ["fest", "utsav", "phase shift", "cultural", "technical", "event", "celebration", "hackathon", "competition", "ananta", "meridian"],
        "intents": ["fest_comparison", "which_fest", "utsav_vs_phaseshift", "best_fest", "college_fest"],
        "controversial": False
    },

    # ======================== SPORTS ========================
    {
        "id": "swimming_pool",
        "question": "Is there a swimming pool at BMSCE?",
        "answer": (
            "BMSCE does NOT have a swimming pool on campus.\n\n"
            "However, the campus does have other excellent sports facilities including:\n"
            "- Majestic Indoor Stadium (badminton, basketball, table tennis, etc.)\n"
            "- Gym facilities in hostels\n"
            "- Outdoor cricket, football, and basketball grounds\n\n"
            "For swimming, students typically use nearby public/private pools in Basavanagudi area."
        ),
        "source": "BMSCE Campus Data 2024",
        "trust_level": 1,
        "category": "sports",
        "keywords": ["swimming", "pool", "weekend", "open", "timing", "swim"],
        "intents": ["swimming_pool", "pool_timings", "swim_weekend"],
        "controversial": False
    },
    {
        "id": "gym_details",
        "question": "Is there a gym? What are its timings?",
        "answer": (
            "BMSCE Gym & Fitness Facilities (2024):\n\n"
            "The campus has well-equipped gym facilities including:\n"
            "- 12-station multi-gym\n"
            "- Cardio center with treadmills and cross-trainers\n"
            "- Dedicated gyms in boys' hostel and international hostel\n\n"
            "Students need to register with the Physical Education Department. "
            "Contact the sports office for current timings and availability."
        ),
        "source": "BMSCE Official Website 2024",
        "trust_level": 2,
        "category": "sports",
        "keywords": ["gym", "fitness", "workout", "exercise", "weight", "timing", "fee", "sports"],
        "intents": ["gym_details", "gym_timings", "fitness_center", "workout_facility"],
        "controversial": False
    },
    {
        "id": "sports_other",
        "question": "What sports facilities are available?",
        "answer": (
            "BMSCE Sports Facilities (2024):\n\n"
            "INDOOR (Majestic Indoor Stadium):\n"
            "- Badminton, Basketball, Table Tennis, Volleyball\n"
            "- Chess, Carrom, Kabaddi, Judo, Wrestling\n\n"
            "OUTDOOR:\n"
            "- Cricket ground, Football ground\n"
            "- Basketball courts, Tennis courts\n"
            "- Kho-Kho, Handball, Hockey, Netball, Throwball\n\n"
            "GYM: 12-station multi-gym + cardio center in hostels\n\n"
            "Note: No swimming pool on campus.\n"
            "Professional coaching available for college teams. "
            "Teams participate in inter-collegiate, state & national competitions."
        ),
        "source": "BMSCE Official Website 2024",
        "trust_level": 1,
        "category": "sports",
        "keywords": ["sports", "facility", "basketball", "cricket", "football", "badminton", "ground", "court", "play", "indoor", "stadium"],
        "intents": ["sports_facilities", "sports_available", "play_sports", "games"],
        "controversial": False
    },

    # ======================== HANGOUT SPOTS ========================
    {
        "id": "hangout_spots",
        "question": "Are there any hidden hangout spots on campus?",
        "answer": (
            "STUDENT OPINION (Subjective - may vary):\n\n"
            "Popular spots shared by students:\n"
            "- Library reference section - quiet & peaceful for study\n"
            "- CSE block corridors - good Wi-Fi, benches\n"
            "- Canteen area - social hub between classes\n"
            "- Open areas near department blocks - grassy spots for groups\n\n"
            "The campus (located in Basavanagudi) also has plenty of nearby cafes, "
            "restaurants, and hangout spots in the neighborhood.\n\n"
            "Always follow campus rules. Some areas may be restricted after hours."
        ),
        "source": "Student Reviews 2024",
        "trust_level": 3,
        "category": "hangout",
        "keywords": ["hangout", "spot", "hidden", "chill", "relax", "sit", "campus", "place", "secret", "peaceful"],
        "intents": ["hangout_spots", "chill_spot", "hidden_places", "where_sit", "place_relax"],
        "controversial": False
    },

    # ======================== DRESS CODE ========================
    {
        "id": "dress_code",
        "question": "Is there a dress code? Can I wear shorts?",
        "answer": (
            "BMSCE Dress Code (2024):\n\n"
            "There is NO official uniform at BMSCE.\n"
            "However, students are expected to dress in appropriate, presentable attire.\n\n"
            "General guidelines:\n"
            "- Avoid beachwear, shorts, or overly casual clothing\n"
            "- Jeans & T-shirts are generally fine\n"
            "- Formal/neat casuals preferred\n"
            "- Kurtas and formal wear always acceptable\n"
            "- Strict formal dress code required during placements, seminars, and graduation\n\n"
            "IMPORTANT: College ID card must be worn at ALL times on campus. "
            "Entry to library and labs will be restricted without it.\n\n"
            "Enforcement strictness varies by department."
        ),
        "source": "BMSCE Official Guidelines 2024",
        "trust_level": 2,
        "category": "dresscode",
        "keywords": ["dress", "code", "shorts", "wear", "clothes", "formal", "jeans", "tshirt", "crop", "uniform"],
        "intents": ["dress_code", "wear_shorts", "clothing_rules", "what_wear", "uniform_policy"],
        "controversial": True
    },

    # ======================== HOSTEL ========================
    {
        "id": "hostel_food",
        "question": "Which hostel has the best food?",
        "answer": (
            "STUDENT OPINION (Subjective - may vary):\n\n"
            "Hostel food at BMSCE is generally described as hygienic, nutritious, and decent.\n\n"
            "- Both North and South Indian options available\n"
            "- Non-veg available on specific days (usually bi-weekly)\n"
            "- Quality is considered better than many other college messes and nearby PGs\n"
            "- Can feel repetitive over time, many students explore local eateries occasionally\n\n"
            "Mess Timings: Breakfast 7:30-9 AM | Lunch 12:30-2 PM | Snacks 4:30-5:30 PM | Dinner 7:30-9 PM\n\n"
            "Individual experiences may differ."
        ),
        "source": "Student Reviews & CollegeDunia 2024",
        "trust_level": 3,
        "category": "hostel",
        "keywords": ["hostel", "food", "mess", "best", "quality", "taste", "boys", "girls", "meal"],
        "intents": ["hostel_food", "mess_food", "hostel_quality", "best_hostel_food"],
        "controversial": True
    },
    {
        "id": "hostel_details",
        "question": "What are the hostel rules and facilities?",
        "answer": (
            "BMSCE Hostel Details (2024):\n\n"
            "Curfew Timings (strictly enforced):\n"
            "- Boys: 9:30 PM weekdays, 10:30 PM Saturdays\n"
            "- Girls: 8:30 PM weekdays, 9:30 PM Saturdays\n"
            "- Gates reopen: 5:30 AM\n"
            "- Late entry requires warden permission; repeated violations lead to disciplinary action\n\n"
            "Facilities: Wi-Fi, gym, study rooms, laundry, common room\n"
            "Rooms: Double/triple sharing; some single rooms for seniors\n"
            "Mess: Breakfast, lunch, snacks & dinner included in hostel fees"
        ),
        "source": "BMSCE Official Hostel Rules 2024",
        "trust_level": 1,
        "category": "hostel",
        "keywords": ["hostel", "curfew", "wifi", "rules", "facility", "room", "stay", "accommodation", "laundry"],
        "intents": ["hostel_rules", "hostel_details", "hostel_curfew", "hostel_facilities"],
        "controversial": False
    },

    # ======================== LIBRARY ========================
    {
        "id": "library_timings",
        "question": "What time does the library close?",
        "answer": (
            "BMSCE Library Timings (2024):\n\n"
            "Stack / Circulation / Periodical / Digital Section:\n"
            "- Monday to Saturday: 9:30 AM - 5:00 PM\n\n"
            "Reference Section (extended hours):\n"
            "- Monday to Saturday: 9:30 AM - 8:30 PM\n"
            "- Sunday: 9:30 AM - 4:30 PM\n\n"
            "Digital resources available include NPTEL, IEEE Xplore, Springer, etc. "
            "Note: College ID card is mandatory for library entry."
        ),
        "source": "BMSCE Library Website 2024",
        "trust_level": 1,
        "category": "library",
        "keywords": ["library", "timing", "close", "open", "book", "study", "exam", "digital", "reading", "hours"],
        "intents": ["library_timings", "library_hours", "library_close", "study_place", "library_exam"],
        "controversial": False
    },

    # ======================== STRICT TEACHERS ========================
    {
        "id": "strict_teachers",
        "question": "Which department has the strictest teachers?",
        "answer": (
            "🧑‍🎓 STUDENT OPINION (Subjective - may vary):\n\n"
            "Strictest departments (according to surveys):\n"
            "🔴 ECE - Known for rigid attendance & grading\n"
            "🔴 Civil - Very particular about submissions\n"
            "🔴 Mechanical - Strict lab attendance\n\n"
            "Notable strict teachers (per student feedback):\n"
            "• Mrs. Shobha (ECE - Signals & Systems)\n"
            "• Mr. Ramesh (Civil - Engineering Mechanics)\n"
            "• Mrs. Kavitha (Mathematics)\n\n"
            "⚠️ Individual experiences may differ. A 'strict' teacher often means better learning!"
        ),
        "source": "Anonymous Student Surveys",
        "trust_level": 3,
        "category": "attendance",
        "keywords": ["strict", "teacher", "tough", "hard", "professor", "faculty", "scary", "difficult"],
        "intents": ["strict_teachers", "tough_teachers", "strictest_department", "hard_teachers"],
        "controversial": True
    },
    {
        "id": "best_teachers",
        "question": "Who are the best teachers at BMSCE?",
        "answer": (
            "🧑‍🎓 STUDENT OPINION (Subjective - may vary):\n\n"
            "Most loved teachers (based on student feedback):\n"
            "⭐ Dr. RamMohan (Aerospace) - Engaging teaching style\n"
            "⭐ Prof. Anoop (CSE - DAA) - Makes algorithms fun\n"
            "⭐ Dr. Smitha (ISE) - Supportive & knowledgeable\n\n"
            "These teachers are praised for their passion, approachability, and teaching quality.\n\n"
            "⚠️ Individual experiences may differ"
        ),
        "source": "Student Reviews 2024",
        "trust_level": 3,
        "category": "attendance",
        "keywords": ["best", "teacher", "favorite", "good", "professor", "faculty", "loved", "popular"],
        "intents": ["best_teachers", "good_teachers", "favorite_teachers", "popular_teachers"],
        "controversial": True
    },

    # ======================== BRANCH CHANGE ========================
    {
        "id": "branch_change",
        "question": "Can I change my branch after first year?",
        "answer": (
            "Branch Change at BMSCE (VTU Rules):\n\n"
            "Yes, branch change IS possible at the start of 3rd semester.\n\n"
            "Requirements (VTU guidelines):\n"
            "- Must pass ALL 1st and 2nd semester subjects in first attempt (no backlogs)\n"
            "- Selection is purely merit-based on 1st year CGPA\n"
            "- Need 9.0-9.5+ CGPA to move to competitive branches like CSE/AIML\n"
            "- Limited seats: Max 25% of original intake can change\n"
            "- Can only switch into same admission category seats (KCET to KCET, etc.)\n"
            "- Once changed, CANNOT be reverted\n\n"
            "Process: College issues notification after 1st year results. "
            "Applications via VTU portal. Monitor BMSCE Academic Section for dates."
        ),
        "source": "VTU Branch Change Rules & BMSCE 2024",
        "trust_level": 2,
        "category": "branch_change",
        "keywords": ["branch", "change", "switch", "transfer", "cgpa", "first year", "cse", "move"],
        "intents": ["branch_change", "switch_branch", "transfer_branch"],
        "controversial": False
    },

    # ======================== PLACEMENTS ========================
    {
        "id": "placement_cse",
        "question": "What are CSE placements like? Highest package?",
        "answer": (
            "BMSCE CSE/AIML Placement Stats (2024-25):\n\n"
            "2025 (ongoing): Highest Package - 51.5 LPA | Average - 11.4 LPA\n"
            "2024: Highest Package - 38 LPA | Average - 9.8 LPA\n\n"
            "Top Recruiters: Amazon, IBM, Accenture and other major tech companies\n"
            "CSE and related branches (ISE, AI&ML) get the most offers\n\n"
            "Note: A strong CGPA (8.5+) is typically needed for top-tier company shortlisting. "
            "Check the official BMSCE Training & Placement portal for latest verified data."
        ),
        "source": "BMSCE Placement Cell & Shiksha 2024-25",
        "trust_level": 2,
        "category": "placement",
        "keywords": ["placement", "cse", "package", "salary", "highest", "company", "recruit", "job", "aiml", "lpa"],
        "intents": ["cse_placement", "highest_package", "cse_salary", "top_package"],
        "controversial": False
    },
    {
        "id": "placement_all",
        "question": "How are placements branch-wise?",
        "answer": (
            "BMSCE Placement Stats (2024-25):\n\n"
            "Overall: 383+ companies visited | 1307 offers | 968 students placed (2025)\n"
            "Highest: 51.5 LPA | Average: 11.4 LPA\n\n"
            "CSE/AIML/ISE: Best placement numbers, highest share of offers\n"
            "Average for circuit branches: 10-13 LPA\n"
            "ECE: Good mix of core + IT placements\n"
            "Mech/Civil: Core recruiters + IT service companies\n\n"
            "Note: Data may vary between NIRF reports and college placement cell updates. "
            "Always check the official BMSCE placement portal for verified numbers.\n\n"
            "Individual experiences may differ. Packages depend on skills & preparation."
        ),
        "source": "BMSCE Placement Cell, Shiksha & Careers360 2024-25",
        "trust_level": 2,
        "category": "placement",
        "keywords": ["placement", "branch", "package", "salary", "ise", "ece", "mechanical", "civil", "biotech", "all"],
        "intents": ["all_placements", "branch_placements", "placement_stats", "placement_comparison"],
        "controversial": True
    },

    # ======================== GENDER RATIO ========================
    {
        "id": "gender_ratio",
        "question": "What is the girls to boys ratio?",
        "answer": (
            "🧑‍🎓 STUDENT OPINION (Subjective - may vary):\n\n"
            "👫 Gender Ratio at BMSCE:\n"
            "Overall: Approximately 1:4 (girls to boys)\n\n"
            "Department-wise breakdown:\n"
            "• CSE/AIML/ISE: ~1:2 (better ratio)\n"
            "• Biotechnology: ~1:1 (most balanced)\n"
            "• ECE: ~1:3\n"
            "• Mechanical/Civil: ~1:8 (mostly boys)\n"
            "• Aerospace: ~1:5\n\n"
            "The ratio has been improving year over year."
        ),
        "source": "Student Surveys & Admission Data",
        "trust_level": 3,
        "category": "dresscode",
        "keywords": ["ratio", "girls", "boys", "gender", "female", "male", "women", "men", "mix"],
        "intents": ["gender_ratio", "girls_boys_ratio", "male_female_ratio"],
        "controversial": False
    },

    # ======================== GENERAL / ABOUT BMSCE ========================
    {
        "id": "about_bmsce",
        "question": "Tell me about BMSCE",
        "answer": (
            "BMS College of Engineering (BMSCE), Bengaluru\n\n"
            "Founded: 1946 - one of the oldest engineering colleges in India\n"
            "Location: Bull Temple Road, Basavanagudi, Bengaluru\n"
            "Affiliation: Visvesvaraya Technological University (VTU)\n"
            "Accreditation: NAAC 'A' Grade, NBA Accredited\n\n"
            "Facilities: Central library (with digital resources), "
            "separate boys & girls hostels, cafeteria, data center with high-speed Wi-Fi, "
            "Majestic Indoor Stadium, gym, and on-campus hospital.\n\n"
            "Known for: Strong placements (51.5 LPA highest in 2025), "
            "vibrant campus life with Utsav & Phase Shift fests, "
            "excellent alumni network, and prime Bangalore city center location."
        ),
        "source": "Official College Data",
        "trust_level": 1,
        "category": "club",
        "keywords": ["bmsce", "bms", "college", "about", "tell", "information", "history", "founded", "location"],
        "intents": ["about_bmsce", "college_info", "bmsce_details", "tell_about"],
        "controversial": False
    },
    {
        "id": "admission",
        "question": "How to get admission in BMSCE?",
        "answer": (
            "BMSCE Admission Process (2024-25):\n\n"
            "Through KCET (Karnataka CET):\n"
            "- Government quota seats (~50%)\n"
            "- CSE closing ranks vary by year and round\n"
            "- Check official KEA website (cetonline.karnataka.gov.in) for verified cutoffs\n\n"
            "Through COMEDK:\n"
            "- Private quota seats\n"
            "- CSE closing rank typically within top 3000-4000\n"
            "- Check official COMEDK website for round-wise cutoff data\n\n"
            "Management Quota:\n"
            "- Limited seats with higher fees\n\n"
            "AI&ML and AI&DS branches also have competitive cutoffs close to core CSE.\n"
            "Always verify cutoffs from official sources as they change yearly."
        ),
        "source": "Official College Data",
        "trust_level": 1,
        "category": "branch_change",
        "keywords": ["admission", "cutoff", "kcet", "comedk", "rank", "join", "apply", "entrance", "seat"],
        "intents": ["admission_process", "how_join", "cutoff_rank", "entrance_exam"],
        "controversial": False
    },
    {
        "id": "wifi",
        "question": "Is there WiFi on campus?",
        "answer": (
            "📶 BMSCE WiFi Details:\n\n"
            "Campus Wi-Fi: Available across all departments\n"
            "Login: Student ID and password required\n"
            "Speed: Generally good during class hours\n\n"
            "Best Wi-Fi spots (student tips):\n"
            "• CSE Corridor - Strongest signal\n"
            "• Library - Reliable & fast\n"
            "• Main canteen area - Decent\n\n"
            "Hostel Wi-Fi: Available but slow during peak hours (8-11 PM)"
        ),
        "source": "Student Reviews 2024",
        "trust_level": 2,
        "category": "hostel",
        "keywords": ["wifi", "internet", "network", "connection", "speed", "signal", "online", "data"],
        "intents": ["wifi_campus", "internet_available", "wifi_speed"],
        "controversial": False
    },
    # ======================== FEES ========================
    {
        "id": "college_fees",
        "question": "What are the college fees at BMSCE?",
        "answer": (
            "BMSCE Fee Structure (2024-25 estimates):\n\n"
            "B.E. Computer Science & Engineering:\n"
            "- KCET (Government Quota): ~88,000 - 90,000 per year\n"
            "- COMEDK (Private Quota): ~3,01,000 per year + misc fees\n"
            "- Management Quota: ~10-15 Lakhs per year (total 4-year: ~40-60 Lakhs)\n\n"
            "Other branches may have slightly lower fees.\n"
            "Management quota fees can include 'development fees' and may not be fully transparent.\n\n"
            "IMPORTANT: Fee structures change yearly. Always verify directly with the "
            "BMSCE admission office or official website (bmsce.ac.in) for current figures.\n\n"
            "Source: Reddit, CollegeDunia, student reports 2024"
        ),
        "source": "Reddit & CollegeDunia 2024",
        "trust_level": 2,
        "category": "fees",
        "keywords": ["fees", "fee", "cost", "tuition", "payment", "kcet", "comedk", "management", "quota", "price", "expensive", "affordable", "money", "lakh"],
        "intents": ["college_fees", "tuition_fees", "fee_structure", "how_much_fees", "cse_fees", "management_fees"],
        "controversial": False
    },
    {
        "id": "hostel_fees",
        "question": "What are the hostel fees at BMSCE?",
        "answer": (
            "BMSCE Hostel Fees (2024-25 estimates):\n\n"
            "Total Annual Hostel Fee: ~2,19,000 - 2,27,000 (first year)\n\n"
            "Breakdown:\n"
            "- Accommodation + Amenities: ~1,20,000 - 1,45,000\n"
            "- Security Deposit (refundable): ~25,000\n"
            "- Mess Charges (Veg): ~73,500/year\n"
            "- Mess Charges (Non-Veg): ~79,000/year\n\n"
            "Second year onwards may be slightly lower.\n\n"
            "Alternative: Off-campus PGs in Basavanagudi area cost ~4,000 - 15,000/month.\n\n"
            "Note: Hostel seats are limited (first-come, first-served). "
            "Verify current fees with the BMSCE hostel office.\n\n"
            "Source: Reddit, YouTube reviews, student feedback 2024"
        ),
        "source": "Reddit & Student Reviews 2024",
        "trust_level": 2,
        "category": "fees",
        "keywords": ["hostel", "fees", "cost", "mess", "charges", "accommodation", "pg", "rent", "room", "stay"],
        "intents": ["hostel_fees", "hostel_cost", "mess_charges", "hostel_price", "accommodation_cost"],
        "controversial": False
    },
]

# Categories for contradiction detection - entries that could conflict
CONTRADICTION_GROUPS = {
    "teacher_strictness": ["attendance_strict", "strict_teachers", "best_teachers", "attendance_loopholes"],
    "hostel_quality": ["hostel_food", "hostel_details"],
    "placement_comparison": ["placement_cse", "placement_all"],
}
