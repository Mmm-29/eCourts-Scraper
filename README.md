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
 2. **Tesseract OCR (System dependency)**  
   Tesseract is required for Captcha solving.

      **Windows:**  
       - Download the installer from [UB Mannheim Tesseract Build](https://github.com/UB-Mannheim/tesseract/wiki)  
       - During installation, check **“Add Tesseract to system PATH”**  
       - Default installation folder:  
         `C:\Program Files\Tesseract-OCR`  
       - Verify installation:  
         ```bash
         tesseract --version
         ```  
       - If not recognized, manually add `C:\Program Files\Tesseract-OCR` to your system PATH
    
      **Linux (Ubuntu/Debian):**  
       - Install via apt:  
         ```bash
         sudo apt update
         sudo apt install tesseract-ocr
         ```  
       - Verify installation:  
         ```bash
         tesseract --version
         ```
    
      **MacOS (using Homebrew):**  
       - Install via Homebrew:  
         ```bash
         brew install tesseract
         ```  
       - Verify installation:  
         ```bash
         tesseract --version
         ```



## Setup and Run

1. **Create & Activate your virtual environment**

```bash
# Windows
python -m venv virtual_env_name
virtual_env_name\Scripts\activate
```

2.**Install dependencies**

  ```bash
    pip install -r requirements.txt
  ```
3. **Run Streamlit App**
  ```bash
  streamlit run app.py
  ```


4. **Follow the UI**
   
  - Select or type State, District, Complex, Court
   - Choose Case Type (Civil/Criminal)
   - Pick the Cause List Date (default is today)
   - Click Fetch Cause List
   - View data and download as PDF

 ## Project Flow

- States: Scraper fetches all states using get_states().
- Districts: Based on selected state, get_districts() fetches districts.
- Complexes: Based on selected district, get_complexes() fetches court complexes.
- Courts: Based on selected complex, get_courts() fetches available courts.
- Captcha: Captcha class downloads the captcha image, cleans it with OpenCV, and uses Tesseract OCR to read it.
- Cause List Fetch: get_cause_list() submits selected options and Captcha to eCourts, parses the HTML table, and returns a Pandas DataFrame.
- Streamlit: UI allows user interaction, selection of date, Civil/Criminal type, and export of cause list to PDF.



