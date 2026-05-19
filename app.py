from flask import Flask, render_template, request, jsonify
from chatbot.groq_ai import ask_groq

import mysql.connector
import os

app = Flask(__name__)


# MYSQL CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="nsp_chatbot"
)

cursor = db.cursor()


# HOME PAGE
@app.route("/")
def home():

    return render_template("index.html")


# CHAT ROUTE
@app.route("/chat", methods=["POST"])
def chat():

    try:

        user_message = request.form.get("message")

        if not user_message:
            user_message = ""

        # GET AI RESPONSE
        bot_response = ask_groq(user_message)

        # SAVE HISTORY
        sql = """
        INSERT INTO chats
        (user_message, bot_response)
        VALUES (%s, %s)
        """

        values = (user_message, bot_response)

        cursor.execute(sql, values)

        db.commit()

        return jsonify({
            "response": bot_response
        })

    except Exception as e:

        print("APP ERROR:", e)

        return jsonify({
            "response": "Server Error"
        })


# GET HISTORY
@app.route("/history", methods=["GET"])
def history():

    cursor.execute("""
    SELECT id, user_message, bot_response
    FROM chats
    ORDER BY id DESC
    """)

    chats = cursor.fetchall()

    history_data = []

    for chat in chats:

        history_data.append({
            "id": chat[0],
            "message": chat[1],
            "response": chat[2]
        })

    return jsonify(history_data)


# DELETE SINGLE HISTORY
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_history(id):

    cursor.execute(
        "DELETE FROM chats WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({
        "success": True
    })


# DELETE ALL HISTORY
@app.route("/delete_all", methods=["DELETE"])
def delete_all():

    cursor.execute("DELETE FROM chats")

    db.commit()

    return jsonify({
        "success": True
    })


# RUN APP
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)