# resource webpages listed below :)
# -> https://realpython.com/flask-project/
# –> https://www.geeksforgeeks.org/python/flask-http-method/

from flask import Flask, request, jsonify
app = Flask(__name__)

# start by defining global variables used before the first update arrives
weather_data = "tbd"
latest_city = "tbd"
display_color = None

@app.route('/')
def home():
    # (a) choose background color
    if display_color == 'yellow':
        bg = "#FFFFE0"  # light yellow
    elif display_color == 'blue':
        bg = "#ADD8E6"  # light blue
    elif display_color == 'red':
        bg = "#FFCCCC"  # light red

    # (b) display predicted temperature with correct bg color (AIDED BY CHATGPT)
    html = f"""
    <html>
    <head>
        <title>Weather Display</title>
    </head>
    <body style="background-color:{bg}; font-family:Arial; padding:20px;">
        <h2>Predicted temperature in {latest_city} is {weather_data}F >_< </h2>
    </body>
    </html>
    """
    return html

@app.route('/send_data', methods=['POST'])
def receive_data():
    global weather_data, latest_city, display_color

    # obtain the json corresponding to the POST request
    data = request.get_json()

    if "weather_prediction" in data:
        dictionary = data["weather_prediction"]
        latest_city = dictionary["city"]
        weather_data = dictionary["predicted_temp_F"]

    display_color = data['display_color']

    # return a response
    return "data transmitted successfully :)", 200

if __name__ == "__main__":
    app.run(debug=True)
