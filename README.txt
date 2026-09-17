========================================
  BMSCE CHATBOT - DESKTOP WEBSITE
  BMS College of Engineering, Bangalore
  AI Project
========================================

FOLDER STRUCTURE
----------------
ai project/
  app.py                  -- Flask backend (search engine + API)
  knowledge_base.py       -- All BMSCE data (20+ entries with trust levels)
  requirements.txt        -- Python dependencies
  README.txt              -- This file
  templates/
    index.html            -- 3-column desktop HTML layout
  static/
    style.css             -- Premium dark theme CSS (min-width 1280px)
    script.js             -- Desktop features (tabs, shortcuts, export, etc.)


HOW TO RUN
----------
Step 1: Open terminal/command prompt in this folder

Step 2: Install dependencies
    py -m pip install -r requirements.txt

Step 3: Run the server
    py app.py

Step 4: Open in browser (desktop/laptop only)
    http://localhost:5000

The website is designed for screens 1280px+ wide.


FEATURES
--------
- 3-column desktop layout (left nav, chat, right sidebar)
- Smart question matching with intent detection + fuzzy typo correction
- 20+ knowledge base entries covering clubs, canteen, attendance, fests,
  sports, hostels, library, placements, dress code, branch change, and more
- Trust level badges: Official (green), Verified (yellow), Student Opinion (red)
- Contradiction handler: shows multiple perspectives for conflicting topics
- Multi-tab chat windows (Ctrl+N for new tab)
- Export conversation as .txt file (Ctrl+E)
- Search in chat history (Ctrl+F)
- Resizable columns (drag the borders between columns)
- Drag & drop .txt files into chat
- Desktop notifications (browser permission required)
- Particle background with parallax mouse effect
- Copy answer with source and trust level
- Message history cycling (Ctrl+Up/Down)
- Trust meter showing % of official answers in session
- Popular questions with click counters
- LocalStorage persistence for chat across page refresh


KEYBOARD SHORTCUTS
------------------
Ctrl+K       Focus input
Enter        Send message
Shift+Enter  New line
Ctrl+N       New chat tab
Ctrl+E       Export conversation
Ctrl+F       Search in chat
Ctrl+Up/Down Cycle through sent messages
Esc          Clear input / close search


TEST QUESTIONS
--------------
Try these to verify smart matching:

  "which is the best club?"         -> IEEE BMSCE answer
  "canteen timings"                 -> All 4 canteens + prices
  "are teachers strict?"            -> Department-wise breakdown
  "can i wear shorts?"              -> Dress code policy
  "best hangout spots"              -> Backyard, Mech Lawn, CSE Corridor
  "canteen timmings" (typo)         -> Still matches canteen timings
  "attandance strict" (typo)        -> Still matches attendance strictness
  "branch change after first year"  -> CGPA requirements
  "highest package cse"             -> 25-51 LPA, Microsoft/Amazon/Google
  "girls to boys ratio"             -> 1:4 overall, varies by department


TECH STACK
----------
Backend:  Python + Flask + Flask-CORS
Frontend: HTML5 + CSS3 + Vanilla JavaScript
Search:   Keyword matching + Intent detection + Fuzzy matching (difflib)
Data:     Python dict knowledge base (no database needed)
