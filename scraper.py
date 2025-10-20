# scraper.py
import httpx
from bs4 import BeautifulSoup
import re
import pandas as pd
from captcha_solver import Captcha

BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"
STATE_PAGE = "?p=casestatus/index/"
DISTRICT_ENDPOINT = "?p=casestatus/fillDistrict"
COMPLEX_ENDPOINT = "?p=casestatus/fillcomplex"
CAUSELIST_ENDPOINT = "?p=cause_list/fillCauseList"


def parse_options(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    return [
        {"value": o.get("value"), "label": o.text.strip()}
        for o in soup.select("option")
        if o.get("value") and "select" not in o.text.strip().lower()
    ]


def get_app_token(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    token_input = soup.find("input", {"name": "app_token"})
    if token_input:
        return token_input.get("value")
    for script in soup.find_all("script"):
        if script.string and "app_token" in script.string:
            match = re.search(r"app_token\s*[:=]\s*['\"]([a-f0-9]{64})['\"]", script.string)
            if match:
                return match.group(1)
    raise Exception("app_token not found in HTML!")


def parse_complex_options(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    out = []
    for o in soup.select("option"):
        v = o.get("value")
        lbl = o.text.strip()
        if not v or "select" in lbl.lower() or not v[0].isdigit():
            continue
        est_match = re.search(r'@([\d,]+)', v)
        est_code = est_match.group(1) if est_match else ""
        code_match = re.match(r"(\d+)", v)
        pure_code = code_match.group(1) if code_match else v
        out.append({
            "label": lbl,
            "court_complex_code": pure_code,
            "est_code": est_code
        })
    return out


def get_states(session):
    r = session.get(BASE_URL + STATE_PAGE)
    return parse_options(r.text), get_app_token(r.text)


def get_districts(session, state_code, app_token):
    r = session.post(BASE_URL + DISTRICT_ENDPOINT, data={
        "state_code": state_code,
        "ajax_req": "true",
        "app_token": app_token
    })
    res = r.json()
    return parse_options(res["dist_list"]), res.get("app_token", app_token)


def get_complexes(session, state_code, dist_code, app_token):
    r = session.post(BASE_URL + COMPLEX_ENDPOINT, data={
        "state_code": state_code,
        "dist_code": dist_code,
        "ajax_req": "true",
        "app_token": app_token
    })
    res = r.json()
    return parse_complex_options(res["complex_list"]), res.get("app_token", app_token)


def get_courts(session, state_code, dist_code, complex_info, app_token):
    data_cause = {
        "state_code": state_code,
        "dist_code": dist_code,
        "court_complex_code": complex_info["court_complex_code"],
        "est_code": complex_info["est_code"],
        "search_act": "undefined",
        "ajax_req": "true",
        "app_token": app_token,
    }
    r = session.post(BASE_URL + CAUSELIST_ENDPOINT, data=data_cause)
    cause_json = r.json()
    courts_html = cause_json["cause_list"]
    courts_opts_raw = parse_options(courts_html)
    return [
        {"label": c["label"], "value": c["value"]}
        for c in courts_opts_raw if re.match(r"^\d+\^\d+$", str(c["value"]))
    ], cause_json.get("app_token", app_token)


def get_cause_list(session, state_code, dist_code, complex_info, court_info, cicri, date, app_token):
    captcha_solver = Captcha(session=session)
    captcha_code = captcha_solver.solve()

    payload = {
        "CL_court_no": court_info["value"],
        "causelist_date": date,
        "cause_list_captcha_code": captcha_code,
        "court_name_txt": court_info["label"],
        "state_code": state_code,
        "dist_code": dist_code,
        "court_complex_code": complex_info["court_complex_code"],
        "est_code": "null",
        "cicri": cicri,
        "selprevdays": "0",
        "ajax_req": "true",
        "app_token": app_token,
    }

    r = session.post(BASE_URL + "cause_list/submitCauseList", data=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")

    if not table:
        return None

    headers = [th.text.strip() for th in table.find_all("th")]
    rows_data = []
    for row in table.find_all("tr")[1:]:
        cols = [td.text.strip() for td in row.find_all("td")]
        if cols:
            rows_data.append(dict(zip(headers, cols)))

    return pd.DataFrame(rows_data)
