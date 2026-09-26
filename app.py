from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

app = Flask(__name__)

# Get OpenAI API key
api_key = os.getenv("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")

if not api_key:
    print("ERROR: OPENAI_API_KEY was not found in .env")
    client = None
else:
    print("OpenAI API key loaded successfully.")
    client = OpenAI(api_key=api_key)


# Calculator page
@app.route("/")
def home():
    return render_template("index.html")


# AI explanation
@app.route("/ask-ai", methods=["POST"])
def ask_ai():

    if client is None:
        return jsonify({
            "answer": "OpenAI API key is missing. Please check your .env file."
        }), 500

    try:
        data = request.get_json()

        calculation = data.get("calculation", "").strip()

        if not calculation:
            return jsonify({
                "answer": "Please calculate something first."
            })

        prompt = f"""
You are the AI assistant inside a calculator.

The user calculated:

{calculation}

Explain the calculation in a simple and friendly way.

Give the answer and briefly explain how the calculation works.

For example:

125 × 18 = 2250

You can explain:
125 multiplied by 18 equals 2250.

Keep your answer short and easy to understand.
"""

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        answer = response.output_text

        return jsonify({
            "answer": answer
        })

    except Exception as error:

        print("================================")
        print("AI ERROR:")
        print(error)
        print("================================")

        return jsonify({
            "answer": "The AI could not respond. Please check your OpenAI API connection."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)