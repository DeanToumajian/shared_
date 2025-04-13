from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

user_data = {
    "dean": {"status": "Online", "messages": []},
    "jenn": {"status": "Online", "messages": []}
}

@app.route("/get/<user>")
def get_data(user):
    partner = "jenn" if user == "dean" else "dean"
    return jsonify({
        "status": user_data[partner]["status"],
        "messages": user_data[partner]["messages"]
    })

@app.route("/update/<user>", methods=["POST"])
def update(user):
    data = request.json
    user_data[user]["status"] = data["status"]
    if data["message"]:
        user_data[user]["messages"].append({
            "text": data["message"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)