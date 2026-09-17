# 🌊 Blue Ocean

A Streamlit application for automated data extraction and analysis.

## Step 1: Scaffolding

This repository contains the baseline scaffold for deployment to [Streamlit Community Cloud](https://share.streamlit.io/).

### Running Locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Deploying to Streamlit Community Cloud

1. Log in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account (`bryanmsh`).
2. Click **Create app** > **Deploy a public app from GitHub**.
3. Select:
   - **Repository:** `bryanmsh/blue-ocean`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy!**
