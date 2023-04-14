import os
import openai
from flask import Flask, request, render_template_string
app = Flask(__name__, static_folder='static', static_url_path='')


app = Flask(__name__)

openai.api_key = "your-openai-api-key"

html_template = '''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BizVisor.ai</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        .logo {
            max-width: 15%;
            max-height: 15%;
            justify-content: center;
            align-items: center;
        }
        
        body {
            font-family: Arial, sans-serif;
            background-color: #F0F0F0;
        }
        .container {
            max-width: 800px;
            margin: 0px auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            color: #333333;
        }
        .chat-box {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 5px;
            overflow-y: auto;
            height: 300px;
            margin-bottom: 20px;
            box-shadow: inset 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .chat-entry {
            margin-bottom: 15px;
        }
        .you {
            text-align: right;
        }
        .therapist {
            text-align: left;
        }
        .you p, .therapist p {
            display: inline-block;
            padding: 10px;
            border-radius: 5px;
        }
        .you p {
            background-color: #6C95CF;
            color: #ffffff;
        }
        .therapist p {
            background-color: #999999;
            color: #ffffff;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333333;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            background-color: #ffffff;
            color: #333333;
        }
        input[type="submit"] {
            background-color: #6C95CF;
            color: #ffffff;
            font-weight: bold;
            text-transform: uppercase;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #4b73b1;
        }
        
        .userPrompt { 
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: bold;
        }
        
        #foot { 
        padding: 10px auto;
        text-align: center;
        }
        
        .disclaimer {
            font-size: 0.6rem;
            color: red; 
            font-weight: bold;    
        }
    </style>
</head>
<body>
<div class="container">
<img class="logo" src="{{ url_for('static', filename='Logo.png') }}" alt="BizVisor.ai" style="display: block; margin-left: auto; margin-right: auto; width: 150px; height: auto; padding-bottom: 20px;">
    <div class="chat-box">
        {% for entry in chat_history %}
            <div class="chat-entry {{ 'you' if entry[0] == 'You' else 'BizVisor' }}">
                <p><strong>{{ entry[0] }}:</strong> {{ entry[1] }}</p>
            </div>
        {% endfor %}
    </div>
    <form method="post">
        <label for="message" class="userPrompt">Ask for business advice:</label>
        <input type="text"
        <input type="text" name="message" id="message" required>
        <input type="submit" value="Send">
    </form>
    <div id="foot">
        <br>
        <h5>BizVisor.ai is not free to host, every small contribution can make a big difference.</h5>
        <h5>Please consider donating today to support our cause and help make a positive impact in the world!</h5>
        <br>
        <a href="https://www.paypal.me/digitalmud">I want to make a difference!</a>
        <br><br>
        <p class="disclaimer">BizVisor.ai is Powered by an AI language model API and should not be taken as legitimate business or financial advice.</p>
        <p class="disclaimer">BizVisor.ai is not responsible for any losses or damages that may occur from the use of this website.</p>
    </div>
</div>
</body>
</html>
'''

chat_history = []


@app.route('/', methods=['GET', 'POST'])
def chat():
    global chat_history
    if request.method == 'POST':
        user_message = request.form['message']
        chat_history.append(("You", user_message))

        conversation_history = "".join([f"{entry[0]}: {entry[1]}\n" for entry in chat_history])

        prompt = f"{user_message}\nAI: Pretend you are a professional business development consultant, what advice do you have? \n {conversation_history}\nAI:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )
        ai_message = response.choices[0].text.strip()
        chat_history.append(("BizVisor: ", ai_message))

    return render_template_string(html_template, chat_history=chat_history)


if __name__ == '__main__':
    app.run(debug=True)
