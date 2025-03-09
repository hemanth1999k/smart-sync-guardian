import streamlit as st
import time
import pandas as pd
import random
import os
from datetime import datetime
from airbyte_client import AirbyteClient
from ai_diagnosis import analyze_error
from predictive_analytics import generate_health_score
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
airbyte = AirbyteClient(use_mock=True)  # Set to False for real API

# App Config
st.set_page_config(page_title="Smart Sync Guardian", layout="wide")

def main():
    # Initialize session state
    if 'active_jobs' not in st.session_state:
        st.session_state.active_jobs = []
    
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = "Never"
    
    st.title("📊 Smart Sync Guardian")
    
    # Branding with error handling
    try:
        logo_path = os.path.join("assets", "airbyte-logo.png")
        if os.path.exists(logo_path):
            st.sidebar.image(logo_path, width=200)
        else:
            st.sidebar.warning("Logo not found at: assets/airbyte-logo.png")
    except Exception as e:
        st.sidebar.error(f"Error loading logo: {str(e)}")
    
    st.sidebar.markdown("""
    **Smart Sync Guardian**  
    *An unofficial prototype demonstrating  
    Airbyte reliability enhancements*
    """)
    
    # Real-time Monitoring
    st.header("Live Sync Dashboard")
    
    # Fetch data immediately on first load
    if not st.session_state.active_jobs:
        try:
            st.session_state.active_jobs = airbyte.get_active_syncs()
            st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
        except Exception as e:
            st.error(f"Failed to fetch sync data: {str(e)}")
    
    # Refresh control
    auto_refresh = st.checkbox("Enable Auto-Refresh (5s)", True)
    refresh_button = st.button("Refresh Now")

    # Fetch new data on manual refresh
    if refresh_button:
        try:
            st.session_state.active_jobs = airbyte.get_active_syncs()
            st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
        except Exception as e:
            st.error(f"Failed to fetch sync data: {str(e)}")
    
    # Auto-refresh logic (non-blocking)
    if auto_refresh:
        time.sleep(5)  # Wait 5 seconds
        st.experimental_rerun()  # Refresh the app
    
    # Display last refresh time
    st.caption(f"Last refreshed: {st.session_state.last_refresh}")
    
    # Use stored data
    active_jobs = st.session_state.active_jobs
    
    # Metrics
    cols = st.columns(4)
    cols[0].metric("Active Syncs", len(active_jobs))
    cols[1].metric("Success Rate", f"{random.randint(85,100)}%")
    cols[2].metric("Avg Latency", f"{random.randint(15,120)}s")
    cols[3].metric("Errors (24h)", random.randint(0,5))
    
    # Jobs Table
    st.subheader("Active Sync Jobs")
    jobs_df = pd.DataFrame([{
        "ID": job['id'],
        "Connection": job['connectionId'],
        "Status": job['status'],
        "Duration": f"{job['duration']}s",
        "Records": job['recordsSynced']
    } for job in active_jobs])
    st.dataframe(jobs_df, use_container_width=True)
    
    # AI Diagnosis
    st.header("🛠️ AI Error Diagnosis")
    if active_jobs:
        selected_job = st.selectbox("Select Job", [job['id'] for job in active_jobs])
        
        if st.button("Analyze with Gemini"):
            try:
                logs = airbyte.get_job_logs(selected_job)
                analysis = analyze_error("\n".join(logs))
                st.subheader("Diagnosis Report")
                st.markdown(f"```\n{analysis}\n```")
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    else:
        st.warning("No active jobs to analyze")
    
    # Predictive Analytics
    st.header("📈 Health Predictions")
    if active_jobs:
        try:
            health = generate_health_score(active_jobs)
            
            cols = st.columns(3)
            cols[0].metric("Health Score", f"{health['health_score']}/100")
            cols[1].metric("Risk Factors", len(health['risk_factors']))
            cols[2].metric("Recommendations", len(health['recommendations']))
            
            if health['risk_factors']:
                st.warning("⚠️ Potential Risks: " + ", ".join(health['risk_factors']))
            if health['recommendations']:
                st.info("💡 Recommendations: " + ", ".join(health['recommendations']))
        except Exception as e:
            st.error(f"Error generating health predictions: {str(e)}")
    else:
        st.warning("No active jobs to analyze")

if __name__ == "__main__":
    main()