import streamlit as st
import boto3
import requests
import json


S3_BUCKET = "your-bucket-name"
S3_REGION = "your-region"
LAMBDA_ENDPOINT = "your-lambda-api-gateway-url"


s3 = boto3.client("s3")

st.title("Bad Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    file_key = uploaded_file.name  

    
    try:
        s3.upload_fileobj(uploaded_file, S3_BUCKET, file_key)
        st.success(f"Uploaded {file_key} to S3")
    except Exception as e:
        st.error(f"Failed to upload to S3: {str(e)}")
        st.stop()

    
    payload = {"s3_bucket": S3_BUCKET, "file_key": file_key}
    response = requests.post(LAMBDA_ENDPOINT, json=payload)

    if response.status_code == 200:
        feedback = response.json().get("feedback", "No feedback received")
        st.write("### Feedback")
        st.write(feedback)
    else:
        st.error("Error from Lambda: " + response.text)
