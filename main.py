import streamlit as st
from scam_detector import scan_linkedin_job
import time

# Page configuration
st.set_page_config(
    page_title="LinkedIn Job Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for better UI
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
        placeholder="https://www.linkedin.com/jobs/view/1234567890/",
        help="Copy and paste the full URL of any LinkedIn job posting"
    )
    
    scan_button = st.button("🔍 Scan for Scams", type="primary", use_container_width=True)
    
    if scan_button:
        if not job_url:
            st.error("⚠️ Please enter a LinkedIn job URL")
        elif "linkedin.com/jobs/view" not in job_url:
            st.error("⚠️ Please enter a valid LinkedIn job URL")
        else:
            # Progress indicators
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            progress_text.text("🔄 Scraping job posting...")
            progress_bar.progress(25)
            time.sleep(0.5)
            
            progress_text.text("🔍 Researching company...")
            progress_bar.progress(50)
            
            # Run the scan (verbose=False for cleaner Streamlit output)
            result = scan_linkedin_job(job_url, verbose=False)
            
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
                st.markdown(f"[Open on LinkedIn]({job_url})")
                
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
    
    st.markdown("### 📊 Statistics")
    st.metric("Jobs Scanned", "2", help="Total scans performed (demo)")
    st.metric("Scams Detected", "1", help="High-risk jobs flagged (demo)")
    
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