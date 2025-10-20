# eCourts Cause List Scraper

A **Python + Streamlit** project to fetch cause lists from **eCourts India**.  
Users can select **State → District → Complex → Court** via dropdowns or type options manually.  
The cause list is fetched automatically, and you can download it as a PDF.

---

## 🔹 Features

- Dynamically scrape **States, Districts, Complexes, Courts** from the eCourts website.
- Automatically solve Captcha using **Tesseract OCR**.
- Streamlit UI with **dropdown + text input** for flexible selection.
- Fetch **Civil or Criminal** cause lists for a specific date.
- Export cause list as a **PDF**.

---

## 📂 Folder Structure
ecourts_scraper/
│
├── captcha_solver.py # Captcha solving logic using OpenCV + Tesseract
├── scraper.py # State/District/Complex/Court extraction + cause list fetch
├── app.py # Streamlit interface
├── requirements.txt # Python dependencies
