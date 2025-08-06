import google.generativeai as genai

# Replace 'your-gemini-api-key' with your actual valid API key
genai.configure(api_key='your-valid-gemini-api-key')
model = genai.GenerativeModel('gemini-pro')

def generate_response(prompt):
    response = model.generate_content(
        ["You will generate answers within 75 tokens. Write in a continuous flow, avoiding bulleted lists." + prompt]
    )
    return response.text
