import streamlit as st
import requests
import base64

# OpenAI API Key
api_key = "Your_openai_api_key_here"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_base64(base64_image):
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        },
    }

# Streamlit App
st.title("GPT-4 Vision QA App")
st.write("Upload an image and ask questions about its content.")

# User input
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "gif"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    question = st.text_input("Ask a Question:")

    if st.button("Submit"):
        file_content = uploaded_file.getvalue()
        base64_image = base64.b64encode(file_content).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        process_image_base64(base64_image),
                    ],
                }
            ],
            "max_tokens": 300
        }

        # API Request
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Display result or error message
        try:
            model_response = response.json()["choices"][0]["message"]["content"]
            st.write("Model Response:")
            st.write(model_response)
        except KeyError:
            st.error("Error in processing the response. Please check your input and try again.")
            st.write("Response from API:")
            st.write(response.text)  # Display full API response for debugging
