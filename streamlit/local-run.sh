python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate

export GCP_PROJECT='jo-gemini-search-grounded-zotn' 
export GCP_REGION='us-central1'

streamlit run app.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8080