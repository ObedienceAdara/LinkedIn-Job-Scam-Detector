# 🛡️ LinkedIn Job Scam Detector

> **Protect yourself from fraudulent LinkedIn job postings in 30 seconds**

Built after nearly falling victim to a sophisticated job scam. This tool analyzes LinkedIn job postings and companies to detect red flags and scam patterns.

## 🚀 Live Demo

**[Try it now →](YOUR_STREAMLIT_URL_HERE)**

## 📊 Quick Stats

- ⚡ Scans completed in ~30 seconds
- 🎯 Tested on 2+ different job types
- 🔍 Analyzes 6+ scam indicators
- 🌐 Works with public LinkedIn job postings

## ⚠️ Problem

60% of LinkedIn job listings may be fake or misleading. Scam patterns include:
- Data harvesting disguised as recruitment
- Fake internships with unrealistic pay
- Companies with no online presence
- "Easy Apply" jobs that collect personal information

## ✅ Solution

Automated scam detection that:
1. **Scrapes** job posting details from LinkedIn
2. **Researches** company reputation across the web
3. **Analyzes** red flags and suspicious patterns
4. **Reports** risk level with actionable recommendations

## 🔥 Features

### Core Detection
- ✅ Web scraping of LinkedIn job postings
- ✅ Company reputation research via DuckDuckGo
- ✅ 6+ red flag pattern detection
- ✅ Risk scoring (0-100 scale)
- ✅ Color-coded verdicts (Safe/Caution/Avoid)

### Red Flags Detected
- 🚩 Unusually high pay for entry-level roles ($60-100/hr)
- 🚩 Vague or extremely short job descriptions
- 🚩 Too many applicants for recently posted jobs
- 🚩 Classic scam pattern: Remote + Intern + High Pay
- 🚩 Multiple scam mentions online
- 🚩 Missing Glassdoor/Trustpilot reviews

### User Interface
- 🎨 Clean, professional Streamlit web app
- 📊 Real-time progress indicators
- 📈 Metrics dashboard (Risk Score, Red Flags, Trust Score)
- 🔗 Links to company review sites
- 📱 Mobile responsive design

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Web Scraping**: Selenium + Undetected ChromeDriver
- **HTML Parsing**: BeautifulSoup4
- **Search**: DuckDuckGo HTML API
- **Deployment**: Streamlit Cloud (Linux/Chromium)
- **Cross-platform**: Auto-detects Windows/Linux/Mac

## 📦 Installation

### Prerequisites
- Python 3.8+
- Chrome or Brave browser (for local testing)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/linkedin-scam-detector.git
cd linkedin-scam-detector

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

### Test the Core Script

```bash
# Run standalone detector
python scam_detector.py
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `YOUR_USERNAME/linkedin-scam-detector`
   - Main file: `app.py`
   - Click "Deploy"

3. **Wait 3-5 minutes** for deployment to complete

Streamlit Cloud automatically installs:
- Python packages from `requirements.txt`
- System packages from `packages.txt` (Chromium browser)

### Alternative Platforms

- **Replit**: Upload files, run `streamlit run app.py`
- **Railway**: Connect GitHub repo, auto-deploy
- **Heroku**: Add `Procfile`, deploy with buildpacks

## 📖 Usage

### Web App

1. Visit the deployed URL
2. Paste a LinkedIn job URL (e.g., `https://www.linkedin.com/jobs/view/1234567890/`)
3. Click "Scan for Scams"
4. Review the risk assessment and red flags

### Python Script

```python
from scam_detector import scan_linkedin_job

# Scan a job
result = scan_linkedin_job("https://www.linkedin.com/jobs/view/1234567890/")

if result:
    print(f"Risk Score: {result['analysis']['risk_score']}/100")
    print(f"Verdict: {result['analysis']['verdict']}")
    print(f"Red Flags: {result['analysis']['red_flags']}")
```

## 🧪 Testing

Test with these example jobs:

**Known Scam (High Risk)**
```
https://www.linkedin.com/jobs/view/4360972282/
Expected: HIGH RISK (90-100/100)
```

**Legitimate Company (Low Risk)**
```
```

## 🐛 Known Issues & Limitations

### Current Limitations
- ⚠️ Only works with public LinkedIn job postings
- ⚠️ Requires full LinkedIn job URL (doesn't browse automatically)
- ⚠️ DuckDuckGo search can be rate limited at high volume
- ⚠️ Risk scores are estimates, not guarantees
- ⚠️ English-language jobs only
- ⚠️ LinkedIn HTML structure changes break scraping

### When It Might Break
- LinkedIn changes their HTML class names (weekly)
- DuckDuckGo blocks requests (at scale)
- Job posting uses non-standard format
- Company name contains special characters
- Browser automation is detected

### False Positives/Negatives
- New legitimate companies may be flagged (no reviews yet)
- Sophisticated scams with good online presence may pass
- International companies may be misclassified

**Always do additional research on companies independently.**

## 🗺️ Roadmap

### Next 7 Days
- [ ] Test on 50+ different jobs
- [ ] Collect user feedback
- [ ] Fix critical bugs
- [ ] Add error logging
- [ ] Improve accuracy

### Next 30 Days
- [ ] Build Chrome extension (auto-detect LinkedIn pages)
- [ ] Add job posting database (track repeat offenders)
- [ ] Train ML classifier (replace keyword matching)
- [ ] Support for Indeed, Glassdoor jobs
- [ ] Multi-language support

### Future (If Traction)
- [ ] API access for developers
- [ ] Bulk scanning for recruiters
- [ ] Email alerts for flagged companies
- [ ] Premium features ($9.99/month)
- [ ] Mobile app

## 🤝 Contributing

Found a bug? Have a feature request? Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Areas for Contribution
- Add more scam patterns
- Improve detection accuracy
- Support more job boards
- Better error handling
- Performance optimization
- Mobile UI improvements

## 📄 License

MIT License - feel free to use and modify

## ⚖️ Legal Disclaimer

This tool is for **educational and protective purposes only**.

- Not affiliated with LinkedIn
- Does not guarantee 100% accuracy
- Always research companies independently
- Use at your own discretion
- Respect website Terms of Service

## 🙏 Acknowledgments

- Built after almost falling victim to a job scam
- Inspired by the need to protect fellow job seekers
- Thanks to the open-source community

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/linkedin-scam-detector/issues)
- **Twitter/X**: [@your_handle]
- **Email**: your.email@example.com

---

**⭐ Star this repo if it helped you avoid a scam!**

**🚀 Built in one day. Shipped to help others.**