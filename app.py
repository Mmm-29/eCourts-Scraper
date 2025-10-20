# app.py
import streamlit as st
import httpx
import datetime
from scraper import get_states, get_districts, get_complexes, get_courts, get_cause_list

st.title(" eCourts Cause List Scraper")

today = datetime.date.today().strftime("%d-%m-%Y")

with httpx.Client(follow_redirects=True) as session:
    states, app_token = get_states(session)
    state_choice = st.selectbox("Select State", [s["label"] for s in states])
    state_input = st.text_input("Or Type State Name", value="")

    selected_state = next((s for s in states if s["label"] == state_choice), None)

    if selected_state or state_input:
        districts, app_token = get_districts(session, selected_state["value"], app_token)
        dist_choice = st.selectbox("Select District", [d["label"] for d in districts])
        dist_input = st.text_input("Or Type District", value="")
        selected_district = next((d for d in districts if d["label"] == dist_choice), None)

        if selected_district or dist_input:
            complexes, app_token = get_complexes(session, selected_state["value"], selected_district["value"], app_token)
            complex_choice = st.selectbox("Select Complex", [c["label"] for c in complexes])
            complex_input = st.text_input("Or Type Complex", value="")
            selected_complex = next((c for c in complexes if c["label"] == complex_choice), None)

            if selected_complex or complex_input:
                courts, app_token = get_courts(session, selected_state["value"], selected_district["value"], selected_complex, app_token)
                court_choice = st.selectbox("Select Court", [c["label"] for c in courts])
                court_input = st.text_input("Or Type Court", value="")
                selected_court = next((c for c in courts if c["label"] == court_choice), None)

                cicri = st.selectbox("Case Type", ["civ", "cri"])
                date_input = st.date_input("Cause List Date", value=datetime.date.today())
                formatted_date = date_input.strftime("%d-%m-%Y")

                if st.button("Fetch Cause List"):
                    with st.spinner("Fetching data..."):
                        df = get_cause_list(
                            session=session,
                            state_code=selected_state["value"],
                            dist_code=selected_district["value"],
                            complex_info=selected_complex,
                            court_info=selected_court,
                            cicri=cicri,
                            date=formatted_date,
                            app_token=app_token,
                        )
                    if df is None or df.empty:
                        st.warning(" No cause list found.")
                    else:
                        st.success(f" Found {len(df)} entries.")
                        st.dataframe(df)

                        # PDF download
                        pdf = df.to_markdown(index=False)
                        st.download_button(
                            label=" Download as PDF",
                            data=pdf.encode("utf-8"),
                            file_name=f"cause_list_{formatted_date}.pdf",
                            mime="application/pdf"
                        )
