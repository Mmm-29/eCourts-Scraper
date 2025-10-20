# eCourts Cause List Scraper

A **Python + Streamlit** project to fetch cause lists from **eCourts India**.  
Users can select **State → District → Complex → Court** via dropdowns or type options manually.  
The cause list is fetched automatically, and you can download it as a PDF.

---

## Features

- Dynamically scrape **States, Districts, Complexes, Courts** from the eCourts website.
- Automatically solve Captcha using **Tesseract OCR**.
- Streamlit UI with **dropdown + text input** for flexible selection.
- Fetch **Civil or Criminal** cause lists for a specific date.
- Export cause list as a **PDF**.

---

##  Folder Structure
```bash
ecourts_scraper/
│
├── captcha_solver.py      # Captcha solving logic using OpenCV + Tesseract
├── scraper.py             # State/District/Complex/Court extraction + cause list fetch
├── app.py                 # Streamlit interface
├── requirements.txt       # Python dependencies

```
##  Requirements
1. **Python Packages**  
- Add the following dependencies in requirements.txt:
```bash
streamlit
httpx
beautifulsoup4
opencv-python-headless
pillow
numpy
pandas
lxml
requests
reportlab
```
## Install dependencies:
```bash
pip install -r requirements.txt
```
 2. T**esseract OCR (System dependency)**
    Tesseract is required for Captcha solving.

    **Windows:**  
   - Download the installer from [UB Mannheim Tesseract Build](https://github.com/UB-Mannheim/tesseract/wiki)  
   - During installation, check **“Add Tesseract to system PATH”**  
   - Default installation folder:
     `C:\Program Files\Tesseract-OCR`
   - Verify installation:
     `tesseract --version`

     


