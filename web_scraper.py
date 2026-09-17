import time
from duckduckgo_search import DDGS

def web_scrape_for_answer(query, gemini_model):
    """
    Search for an answer using DuckDuckGo.
    Priority 1: site:bmsce.ac.in
    Priority 2: site:reddit.com OR site:quora.com OR site:wikipedia.org
    Uses Gemini to synthesize the scraped snippets into a clean answer.
    """
    if not gemini_model:
        return None, None
        
    try:
        ddgs = DDGS()
        
        # Priority 1: Official site
        official_query = f"site:bmsce.ac.in {query}"
        results = list(ddgs.text(official_query, max_results=3))
        
        snippets = []
        sources = []
        
        if results:
            for r in results:
                snippets.append(r.get('body', ''))
                sources.append(r.get('href', ''))
        
        # If official site yielded nothing, search other specific sites
        if not snippets:
            alt_query = f"(site:reddit.com OR site:quora.com OR site:wikipedia.org) BMSCE {query}"
            results = list(ddgs.text(alt_query, max_results=5))
            for r in results:
                snippets.append(r.get('body', ''))
                sources.append(r.get('href', ''))
                
        # If still nothing, do a broad general search
        if not snippets:
            broad_query = f"BMSCE {query}"
            results = list(ddgs.text(broad_query, max_results=5))
            for r in results:
                snippets.append(r.get('body', ''))
                sources.append(r.get('href', ''))
                
        if not snippets:
            return None, None
            
        context = "\n".join(snippets)
        source_url = sources[0] if sources else "Web Search"
        
        # Synthesize with Gemini
        prompt = (
            "You are an AI for BMSCE. The user asked a question that was not in our database. "
            "We scraped the following snippets from the web related to their question:\n"
            f"{context}\n\n"
            "User Question: " + query + "\n\n"
            "Based ONLY on the snippets provided above, generate a concise, accurate answer (under 100 words). "
            "If the snippets don't contain the answer, say 'I could not find a reliable answer on the web.' "
            "Do not use markdown formatting like ** or ##."
        )
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            answer = response.text.strip()
            if "I could not find" in answer:
                return None, None
            return answer, source_url
            
    except Exception as e:
        print(f"[!] Web scraping error: {e}")
        
    return None, None
