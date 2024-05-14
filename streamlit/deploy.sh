export GCP_PROJECT='jo-gemini-search-grounded-zotn' 
export GCP_REGION='us-central1'  
export AR_REPO='gemini-streamlit-repo'  # Change this
export SERVICE_NAME='gemini-search-grounded' # This is the name of our Application and Cloud Run service. Change it if you'd like.

gcloud config set project $GCP_PROJECT

gcloud iam service-accounts create "$SERVICE_NAME"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$SERVICE_NAME@$GCP_PROJECT.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $GCP_PROJECT \
  --member="serviceAccount:$SERVICE_NAME@$GCP_PROJECT.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"

gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$GCP_REGION \
  --platform=managed  \
  --project=$GCP_PROJECT \
  --service-account="$SERVICE_NAME" \
  --set-env-vars="GCP_PROJECT=$GCP_PROJECT, GCP_REGION=$GCP_REGION, AGENT_LOCATION=$AGENT_LOCATION, DATASTORE_ID=$DATASTORE_ID, BUCKET_NAME=$BUCKET_NAME"


