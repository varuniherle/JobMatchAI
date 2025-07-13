# 🚀 JobMatchAI – Smart Job Matcher Using Google Gemini

**JobMatchAI** is a Python-based automation tool that scrapes job listings from [Naukri.com](https://www.naukri.com) based on your chosen filters, and then uses **Google Gemini 2.0 Flash-Lite** (via API) to intelligently score and assess how well each job matches your resume.

This project helps job seekers apply only to **high-fit roles**

---

## 🔍 Features

- Scrape job descriptions from Naukri.com
- Match each job with your resume using Gemini Flash AI
- Get a **score**, **match level**, and **explanation** for each job
- Save results in a timestamped CSV (e.g. `jobs_2025-06-30.csv`)
- Keep API keys safe with `.env` support

---

## 📦 Requirements

- Python 3.8+
- Gemini API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)

Install dependencies
- Get Gemini API Key
- Add .env File: GEMINI_API_KEY=your_api_key_here
- Open main.py, and replace the Naukri filter URL:: base_url = "https://www.naukri.com/python-developer-jobs-in-bangalore"
- Run the Script: python main.py


