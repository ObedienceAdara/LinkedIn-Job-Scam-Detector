#!/usr/bin/env python3
"""
Company Researcher - Scam Detection Engine
Combines LinkedIn job scraping + DuckDuckGo research
CLOUD-READY VERSION - Works on Streamlit Cloud, Replit, and local machines
"""

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests
import urllib.parse
import time
import random
import os
import platform

# User agents for DuckDuckGo
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# ============================================================================
# CROSS-PLATFORM BROWSER CONFIGURATION
# ============================================================================

def find_brave_executable():
    """Find Brave browser executable on Windows"""
    possible_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_browser_config():
    """
    Auto-detect browser configuration based on environment
    Works on: Windows (local), Linux (Streamlit Cloud, Replit), macOS
    """
    
    system = platform.system()
    
    # LINUX (Streamlit Cloud, Replit, Railway, DigitalOcean)
    if system == 'Linux':
        # Check for Chromium (Streamlit Cloud installs this via packages.txt)
        if os.path.exists('/usr/bin/chromium-browser'):
            browser_path = '/usr/bin/chromium-browser'
        elif os.path.exists('/usr/bin/chromium'):
            browser_path = '/usr/bin/chromium'
        elif os.path.exists('/usr/bin/google-chrome'):
            browser_path = '/usr/bin/google-chrome'
        else:
            browser_path = None  # Let undetected-chromedriver find it
        
        return {
            'path': browser_path,
            'args': [
                '--headless=new',
                '--no-sandbox',  # CRITICAL for Docker/containers
                '--disable-dev-shm-usage',  # Prevents crashes in containers
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--disable-setuid-sandbox',
                '--single-process',  # Streamlit Cloud compatibility
            ]
        }
    
    # WINDOWS (local development)
    elif system == 'Windows':
        brave_path = find_brave_executable()
        
        return {
            'path': brave_path,
            'args': [
                '--headless=new',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled',
            ]
        }
    
    # MACOS (local development)
    else:
        return {
            'path': None,  # Use default Chrome
            'args': [
                '--headless=new',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        }

# ============================================================================
# LINKEDIN JOB SCRAPER
# ============================================================================

def scrape_linkedin_job(job_url, verbose=True):
    """Scrape a single LinkedIn job posting"""
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"📋 STEP 1: SCRAPING JOB POSTING")
        print(f"{'='*70}")
        print(f"URL: {job_url}\n")
    
    # Get browser configuration for current environment
    config = get_browser_config()
    
    # Configure browser
    options = uc.ChromeOptions()
    
    if config['path']:
        options.binary_location = config['path']
        if verbose:
            print(f"[*] Using browser: {config['path']}")
    
    for arg in config['args']:
        options.add_argument(arg)
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=False)
        
        if verbose:
            print("[*] Loading job page...")
        driver.get(job_url)
        
        if verbose:
            print("[*] Waiting for content...")
        time.sleep(random.uniform(4, 6))
        
        # Parse HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract job details
        job_title = (
            soup.find('h1', class_='top-card-layout__title') or
            soup.find('h1', class_='topcard__title') or
            soup.find('h2', class_='topcard__title')
        )
        
        company = (
            soup.find('a', class_='topcard__org-name-link') or
            soup.find('span', class_='topcard__flavor') or
            soup.find('a', {'data-tracking-control-name': 'public_jobs_topcard-org-name'})
        )
        
        location = (
            soup.find('span', class_='topcard__flavor--bullet') or
            soup.find('span', class_='topcard__flavor topcard__flavor--bullet')
        )
        
        description = (
            soup.find('div', class_='show-more-less-html__markup') or
            soup.find('div', class_='description__text') or
            soup.find('section', class_='description')
        )
        
        posted = soup.find('span', class_='posted-time-ago__text')
        applicants = soup.find('span', class_='num-applicants__caption')
        
        result = {
            'job_title': job_title.text.strip() if job_title else 'N/A',
            'company': company.text.strip() if company else 'N/A',
            'location': location.text.strip() if location else 'N/A',
            'posted': posted.text.strip() if posted else 'N/A',
            'applicants': applicants.text.strip() if applicants else 'N/A',
            'description': description.text.strip() if description else 'N/A',
            'url': job_url
        }
        
        if verbose:
            print(f"✅ Extracted job data:")
            print(f"   Title: {result['job_title']}")
            print(f"   Company: {result['company']}")
            print(f"   Location: {result['location']}")
        
        driver.quit()
        return result
        
    except Exception as e:
        if verbose:
            print(f"[!] Scraping error: {e}")
        try:
            driver.quit()
        except:
            pass
        return None

# ============================================================================
# DUCKDUCKGO SEARCH ENGINE
# ============================================================================

def search_duckduckgo(query, num_results=10, verbose=True):
    """Search DuckDuckGo and return results"""
    
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://duckduckgo.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        result_divs = soup.find_all('div', class_='result')
        
        for div in result_divs[:num_results]:
            link = div.find('a', class_='result__a')
            if link:
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                # Extract actual URL from DuckDuckGo redirect
                if 'uddg=' in href:
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                    if 'uddg' in parsed:
                        href = parsed['uddg'][0]
                
                if href.startswith('http'):
                    snippet_elem = div.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append({
                        'title': title,
                        'url': href,
                        'snippet': snippet[:200] if snippet else ""
                    })
        
        return results
        
    except Exception as e:
        if verbose:
            print(f"   [!] Search error: {e}")
        return []

# ============================================================================
# COMPANY RESEARCH & SCAM DETECTION
# ============================================================================

def research_company(company_name, verbose=True):
    """
    Research a company for scam indicators
    
    Returns:
        dict with scam_mentions, red_flags, trust_score
    """
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"🔍 STEP 2: RESEARCHING COMPANY")
        print(f"{'='*70}")
        print(f"Company: {company_name}\n")
    
    red_flags = []
    scam_mentions = 0
    review_sites = []
    
    # SEARCH 1: Look for scam mentions
    if verbose:
        print("[*] Searching for scam mentions...")
    scam_results = search_duckduckgo(f'"{company_name}" scam reviews', verbose=False)
    
    scam_keywords = ['scam', 'fraud', 'fake', 'beware', 'warning', 'avoid', 'suspicious']
    
    for result in scam_results:
        title_lower = result['title'].lower()
        snippet_lower = result['snippet'].lower()
        
        for keyword in scam_keywords:
            if keyword in title_lower or keyword in snippet_lower:
                scam_mentions += 1
                red_flags.append(f"Found '{keyword}' in: {result['title'][:60]}...")
                if verbose:
                    print(f"   🚩 {result['title'][:70]}...")
                break
    
    # SEARCH 2: Find review sites
    if verbose:
        print(f"\n[*] Searching for reviews...")
    review_results = search_duckduckgo(f'"{company_name}" glassdoor trustpilot reviews', verbose=False)
    
    for result in review_results:
        if any(site in result['url'].lower() for site in ['glassdoor', 'indeed', 'trustpilot', 'reddit']):
            review_sites.append({
                'title': result['title'],
                'url': result['url']
            })
            if verbose:
                print(f"   📋 {result['title'][:60]}...")
    
    # Calculate trust score (inverted - more scam mentions = lower trust)
    trust_score = max(0, 100 - (scam_mentions * 20))
    
    if verbose:
        print(f"\n✅ Research complete:")
        print(f"   Scam mentions: {scam_mentions}")
        print(f"   Trust score: {trust_score}/100")
    
    return {
        'company': company_name,
        'scam_mentions': scam_mentions,
        'review_sites': review_sites[:5],
        'red_flags': red_flags,
        'trust_score': trust_score
    }

# ============================================================================
# SCAM DETECTOR - ANALYZE JOB + COMPANY DATA
# ============================================================================

def analyze_job(job_data, company_research, verbose=True):
    """
    Analyze job posting for scam indicators
    
    Returns:
        dict with risk_score, red_flags, verdict
    """
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"⚠️  STEP 3: SCAM ANALYSIS")
        print(f"{'='*70}\n")
    
    red_flags = []
    risk_score = 0
    
    # RED FLAG 1: Company has scam mentions
    if company_research['scam_mentions'] > 0:
        flag = f"Company has {company_research['scam_mentions']} scam-related search results"
        red_flags.append(flag)
        risk_score += company_research['scam_mentions'] * 20
        if verbose:
            print(f"🚩 {flag}")
    
    # RED FLAG 2: Suspiciously high pay for entry-level/intern
    title_lower = job_data['job_title'].lower()
    if ('intern' in title_lower or 'entry' in title_lower or 'junior' in title_lower):
        if any(pay in job_data['job_title'] for pay in ['$70', '$60', '$80', '$90', '$100']):
            flag = "Unusually high hourly rate for entry-level position"
            red_flags.append(flag)
            risk_score += 25
            if verbose:
                print(f"🚩 {flag}")
    
    # RED FLAG 3: Vague or very short job description
    desc_length = len(job_data['description'])
    if desc_length < 300:
        flag = f"Very short job description ({desc_length} characters)"
        red_flags.append(flag)
        risk_score += 15
        if verbose:
            print(f"🚩 {flag}")
    
    # RED FLAG 4: High applicants + recently posted = suspicious
    if job_data['applicants'] != 'N/A':
        applicants_text = job_data['applicants'].lower()
        posted_text = job_data['posted'].lower()
        
        if ('100' in applicants_text or 'over' in applicants_text) and \
           ('day' in posted_text or 'hour' in posted_text):
            flag = f"Too many applicants ({job_data['applicants']}) for recently posted job ({job_data['posted']})"
            red_flags.append(flag)
            risk_score += 20
            if verbose:
                print(f"🚩 {flag}")
    
    # RED FLAG 5: Remote + High pay + Intern = Classic scam pattern
    if 'remote' in title_lower and 'intern' in title_lower and '$' in job_data['job_title']:
        flag = "Classic scam pattern: Remote + Intern + High Pay in title"
        red_flags.append(flag)
        risk_score += 30
        if verbose:
            print(f"🚩 {flag}")
    
    # RED FLAG 6: Company has no review sites
    if len(company_research['review_sites']) == 0:
        flag = "No Glassdoor/Trustpilot reviews found for company"
        red_flags.append(flag)
        risk_score += 15
        if verbose:
            print(f"🚩 {flag}")
    
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    # Determine verdict
    if risk_score >= 70:
        verdict = "🔴 HIGH RISK - Likely Scam"
        recommendation = "AVOID - Multiple red flags detected"
    elif risk_score >= 40:
        verdict = "🟡 MEDIUM RISK - Proceed with Caution"
        recommendation = "RESEARCH FURTHER - Some concerning signs"
    else:
        verdict = "🟢 LOW RISK - Appears Legitimate"
        recommendation = "SAFE - No major red flags"
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"VERDICT: {verdict}")
        print(f"Risk Score: {risk_score}/100")
        print(f"{'='*70}")
    
    return {
        'risk_score': risk_score,
        'red_flags': red_flags,
        'verdict': verdict,
        'recommendation': recommendation,
        'total_flags': len(red_flags)
    }

# ============================================================================
# MAIN PIPELINE - FULL SCAM DETECTION
# ============================================================================

def scan_linkedin_job(job_url, verbose=True):
    """
    Complete scam detection pipeline:
    1. Scrape job posting
    2. Research company
    3. Analyze for scams
    4. Generate report
    """
    
    if verbose:
        print("\n" + "="*70)
        print("🛡️  LINKEDIN JOB SCAM DETECTOR")
        print("="*70)
    
    # STEP 1: Scrape the job
    job_data = scrape_linkedin_job(job_url, verbose=verbose)
    
    if not job_data or job_data['company'] == 'N/A':
        if verbose:
            print("\n❌ FAILED: Could not scrape job data")
        return None
    
    # STEP 2: Research the company
    company_research = research_company(job_data['company'], verbose=verbose)
    
    # STEP 3: Analyze for scams
    analysis = analyze_job(job_data, company_research, verbose=verbose)
    
    # STEP 4: Generate final report
    if verbose:
        print(f"\n{'='*70}")
        print("📊 FINAL REPORT")
        print(f"{'='*70}\n")
        
        print(f"🏢 Company: {job_data['company']}")
        print(f"💼 Position: {job_data['job_title']}")
        print(f"📍 Location: {job_data['location']}")
        print(f"📅 Posted: {job_data['posted']}")
        if job_data['applicants'] != 'N/A':
            print(f"👥 Applicants: {job_data['applicants']}")
        
        print(f"\n{analysis['verdict']}")
        print(f"📊 Risk Score: {analysis['risk_score']}/100")
        print(f"🚩 Red Flags: {analysis['total_flags']}")
        
        print(f"\n💡 Recommendation: {analysis['recommendation']}")
        
        if analysis['red_flags']:
            print(f"\n⚠️  DETECTED RED FLAGS:")
            for i, flag in enumerate(analysis['red_flags'], 1):
                print(f"   {i}. {flag}")
        
        if company_research['review_sites']:
            print(f"\n📋 REVIEW SITES TO CHECK:")
            for site in company_research['review_sites'][:3]:
                print(f"   • {site['title']}")
                print(f"     {site['url']}")
        
        print(f"\n{'='*70}\n")
    
    return {
        'job_data': job_data,
        'company_research': company_research,
        'analysis': analysis
    }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Test on the Crossing Hurdles job
    job_url = "https://www.linkedin.com/jobs/view/4360972282/"
    
    result = scan_linkedin_job(job_url)
    
    if result:
        print("✅ Scan complete!")
        print("\nYou can now:")
        print("1. Test on more LinkedIn job URLs")
        print("2. Package this as a web app")
        print("3. Add more scam detection patterns")
        print("4. Build Chrome extension")
    else:
        print("❌ Scan failed. Check error messages above.") 