import streamlit as st
import requests
import json

API_GATEWAY_URL = "your-api-invoke-url/ResumeAnalyzerLambda"

def analyze_resume(file_key):
    """ Sends a request to API Gateway to analyze the resume. """
    response = requests.post(
        API_GATEWAY_URL,
        json={"s3_bucket": "bad-resume-bucket", "file_key": file_key}
    )

    s
    print("Response Status:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        try:
            data = response.json()
            
            if "feedback" in data:
                return data["feedback"]
            else:
                return f"Unexpected API response format: {data}"
        except json.JSONDecodeError:
            return f"Error parsing JSON: {response.text}"
    else:
        return f"Error: {response.text}"


st.title("📝 Bad Resume Analyzer")
st.write("Upload a resume and get feedback on common mistakes.")

uploaded_file = st.file_uploader("Choose a PDF resume", type=["pdf"])

if uploaded_file is not None:
    file_key = uploaded_file.name  
    st.write(f"📂 File uploaded: {file_key}")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing... 🔍"):
            feedback = analyze_resume(file_key)
            st.markdown(feedback)  
