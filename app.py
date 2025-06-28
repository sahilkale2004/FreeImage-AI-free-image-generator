from flask import Flask, render_template, request, send_file
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")  # Correct ENV variable name

app = Flask(__name__)

# ✅ Initialize GenAI client with loaded API key
client = genai.Client(api_key=api_key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        contents = request.form.get('prompt', '')
        if contents:
            response = client.models.generate_content(
                model="models/gemini-2.0-flash-exp",
                contents=contents,
                config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save("generated_image.png", "PNG")
                    return send_file("generated_image.png", mimetype='image/png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)