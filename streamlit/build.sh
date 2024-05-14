export GCP_PROJECT='jo-gemini-search-grounded-zotn' 
export GCP_REGION='us-central1'  
export AR_REPO='gemini-streamlit-repo'  # Change this
export SERVICE_NAME='gemini-search-grounded' # This is the name of our Application and Cloud Run service. Change it if you'd like.

#make sure you are in the active directory for 'gemini-streamlit-cloudrun'
gcloud config set project $GCP_PROJECT
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"
