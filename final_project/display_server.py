# resource webpages listed below :)
# ––> https://realpython.com/flask-project/

from flask import Flask, request, jsonify
app = Flask(__name__)

# start by defining global variables used before the first update arrives
weather_data = "tbd"
latest_city = "tbd"
display_color = None

@app.route('/')
def home():
    # (a) choose background color
    if display_color == 'a':
        bg = "#FFFFE0" # light yellow
    elif display_color == 'b':
        bg = "#ADD8E6" # light blue
    else: # display_color == 'c'
        bg = "FFCCCC"  # light red
    
    # (b) display predicted temperature (AIDED BY CHATGPT)
    html = f"""
    <html>
    <head>
        <title>Weather Display</title>
    </head>
    <body style="background-color:{bg}; font-family:Arial; padding:20px;">
        <h2>Predicted temperature in {latest_city} is {weather_data}F</h2>
    </body>
    </html>
    """
    return html

@app.route('/send_data', methods=['POST'])
def receive_data():
    global weather_data
    # obtain the json corresponding to the POST request
    data = request.get_json()
    weather_data = data
    # return a response
    return "data transmitted succesfully :)", 200

if __name__ == "__main__":
    app.run(debug=True)
