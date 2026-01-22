import streamlit as st
from detector_scam import scan_linkedin_job
import time
import re
from urllib.parse import urlparse, parse_qs

# Page configuration
st.set_page_config(
    page_title="LinkedIn Job Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================================
# URL CONVERTER FUNCTIONS
# ============================================================================

def extract_job_id(linkedin_url):
    """Extract job ID from any LinkedIn job URL format"""
    
    # Format 1: Already a direct view URL
    view_match = re.search(r'/jobs/view/(\d+)', linkedin_url)
    if view_match:
        return view_match.group(1)
    
    # Format 2: Search URL with currentJobId parameter
    parsed_url = urlparse(linkedin_url)
    query_params = parse_qs(parsed_url.query)
    
    if 'currentJobId' in query_params:
        return query_params['currentJobId'][0]
    
    # Format 3: Job ID in URL path
    path_match = re.search(r'/jobs/(\d+)', linkedin_url)
    if path_match:
        return path_match.group(1)
    
    return None

def convert_to_view_url(linkedin_url):
    """Convert any LinkedIn job URL to direct view URL"""
    
    job_id = extract_job_id(linkedin_url)
    
    if job_id:
        return f"https://www.linkedin.com/jobs/view/{job_id}/"
    
    return None

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 5px;
    }
    .risk-high {
        background-color: #fee;
        padding: 1rem;
        border-left: 4px solid #f44;
        border-radius: 5px;
    }
    .risk-medium {
        background-color: #ffeaa7;
        padding: 1rem;
        border-left: 4px solid #fdcb6e;
        border-radius: 5px;
    }
    .risk-low {
        background-color: #d4edda;
        padding: 1rem;
        border-left: 4px solid #28a745;
        border-radius: 5px;
    }
    .url-converted {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-left: 3px solid #2196f3;
        border-radius: 3px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ LinkedIn Job Scam Detector</h1>
    <p>Protect yourself from fraudulent job postings in seconds</p>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔍 Scan a LinkedIn Job")
    
    job_url = st.text_input(
        "Paste LinkedIn Job URL:",
        placeholder="https://www.linkedin.com/jobs/view/1234567890/ or https://www.linkedin.com/jobs/search/?currentJobId=...",
        help="Copy and paste any LinkedIn job URL - we'll convert it automatically"
    )
    
    scan_button = st.button("🔍 Scan for Scams", type="primary", use_container_width=True)
    
    if scan_button:
        if not job_url:
            st.error("⚠️ Please enter a LinkedIn job URL")
        elif "linkedin.com/jobs" not in job_url:
            st.error("⚠️ Please enter a valid LinkedIn job URL")
        else:
            # Auto-convert URL if needed
            job_id = extract_job_id(job_url)
            
            if not job_id:
                st.error("⚠️ Could not extract job ID from URL. Please check the URL format.")
                st.info("""
                **Supported URL formats:**
                - Direct view URL: `https://www.linkedin.com/jobs/view/1234567890/`
                - Search URL: `https://www.linkedin.com/jobs/search/?currentJobId=1234567890&...`
                - Collections URL: `https://www.linkedin.com/jobs/collections/recommended/?currentJobId=1234567890`
                """)
            else:
                # Convert to standard view URL
                standardized_url = convert_to_view_url(job_url)
                
                # Show conversion if URL was modified
                if standardized_url != job_url:
                    st.markdown(f"""
                    <div class="url-converted">
                        ✅ <strong>URL Auto-Converted:</strong><br>
                        <small>Job ID: {job_id}</small><br>
                        <small>Using: {standardized_url}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Progress indicators
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                progress_text.text("🔄 Scraping job posting...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                progress_text.text("🔍 Researching company...")
                progress_bar.progress(50)
                
                # Run the scan with standardized URL
                result = scan_linkedin_job(standardized_url, verbose=False)
                
                progress_text.text("⚙️ Analyzing red flags...")
                progress_bar.progress(75)
                time.sleep(0.5)
                
                progress_bar.progress(100)
                progress_text.empty()
                progress_bar.empty()
                
                if result:
                    analysis = result['analysis']
                    job_data = result['job_data']
                    company_research = result['company_research']
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("## 📊 Scan Results")
                    
                    # Risk verdict with color coding
                    risk_score = analysis['risk_score']
                    
                    if risk_score >= 70:
                        st.markdown(f"""
                        <div class="risk-high">
                            <h2 style="color: #d63031; margin: 0;">🔴 HIGH RISK - Likely Scam</h2>
                            <p style="margin: 0.5rem 0 0 0;"><strong>Recommendation:</strong> {analysis['recommendation']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif risk_score >= 40:
                        st.markdown(f"""
                        <div class="risk-medium">
                            <h2 style="color: #f39c12; margin: 0;">🟡 MEDIUM RISK - Proceed with Caution</h2>
                            <p style="margin: 0.5rem 0 0 0;"><strong>Recommendation:</strong> {analysis['recommendation']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="risk-low">
                            <h2 style="color: #27ae60; margin: 0;">🟢 LOW RISK - Appears Legitimate</h2>
                            <p style="margin: 0.5rem 0 0 0;"><strong>Recommendation:</strong> {analysis['recommendation']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Metrics
                    st.markdown("### 📈 Key Metrics")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    
                    with col_m1:
                        st.metric("Risk Score", f"{risk_score}/100")
                    
                    with col_m2:
                        st.metric("Red Flags", analysis['total_flags'])
                    
                    with col_m3:
                        st.metric("Company Trust Score", f"{company_research['trust_score']}/100")
                    
                    # Job details
                    st.markdown("### 💼 Job Details")
                    st.write(f"**Company:** {job_data['company']}")
                    st.write(f"**Position:** {job_data['job_title']}")
                    st.write(f"**Location:** {job_data['location']}")
                    st.write(f"**Posted:** {job_data['posted']}")
                    if job_data['applicants'] != 'N/A':
                        st.write(f"**Applicants:** {job_data['applicants']}")
                    
                    # Red flags
                    if analysis['red_flags']:
                        st.markdown("### ⚠️ Detected Red Flags")
                        for i, flag in enumerate(analysis['red_flags'], 1):
                            st.warning(f"**{i}.** {flag}")
                    else:
                        st.success("✅ No red flags detected!")
                    
                    # Review sites
                    if company_research['review_sites']:
                        st.markdown("### 📋 Review Sites to Check")
                        for site in company_research['review_sites'][:3]:
                            st.markdown(f"- [{site['title']}]({site['url']})")
                    
                    # View original posting
                    st.markdown("### 🔗 View Original Posting")
                    st.markdown(f"[Open on LinkedIn]({standardized_url})")
                    
                else:
                    st.error("❌ Failed to scan job. Please check the URL and try again.")
                    st.info("💡 **Tip:** Make sure the job posting is public and the URL is correct.")

with col2:
    st.markdown("### 📚 How It Works")
    
    with st.expander("🔍 Step 1: Scrape Job"):
        st.write("""
        We extract key information from the LinkedIn job posting including:
        - Job title
        - Company name
        - Location
        - Description
        - Posted date
        - Number of applicants
        """)
    
    with st.expander("🔎 Step 2: Research Company"):
        st.write("""
        We search the web for:
        - Scam mentions
        - Fraudulent reviews
        - Company reputation
        - Glassdoor/Trustpilot reviews
        """)
    
    with st.expander("⚠️ Step 3: Detect Red Flags"):
        st.write("""
        We analyze patterns like:
        - Suspiciously high pay for entry-level
        - Vague job descriptions
        - Too many applicants too quickly
        - Remote + Intern + High Pay pattern
        - Missing company reviews
        """)
    
    st.markdown("### 🚩 Common Scam Patterns")
    st.info("""
    **Watch out for:**
    - Entry-level/intern roles with $60-100/hr pay
    - "Easy Apply" jobs with 100+ applicants in 24 hours
    - Companies with no online presence
    - Vague job descriptions under 300 characters
    - Data collection jobs disguised as ML/AI work
    """)
    
    st.markdown("### 🔗 URL Format Support")
    st.success("""
    **We accept any LinkedIn job URL:**
    - Direct view URLs
    - Search result URLs
    - Collections URLs
    - Recommended job URLs
    
    We'll automatically convert them!
    """)
    
    st.markdown("### 📊 Statistics")
    st.metric("Jobs Scanned", "3+", help="Total scans performed")
    st.metric("Scams Detected", "1", help="High-risk jobs flagged")
    
    st.markdown("### 💡 Tips")
    st.success("""
    **Stay Safe:**
    1. Always research companies independently
    2. Never share sensitive info in applications
    3. Be skeptical of too-good-to-be-true offers
    4. Check Glassdoor reviews
    5. Trust your instincts
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Built to protect job seekers from scam postings</strong></p>
    <p style="font-size: 0.9rem;">Not affiliated with LinkedIn. Use at your own discretion.</p>
</div>
""", unsafe_allow_html=True)