from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'secret123'

MAX_ATTEMPTS = 5
difficulty_levels = {
    "easy": (1, 10),
    "medium": (1, 50),
    "hard": (1, 100),
}

theme_colors = {
    "easy": "theme-easy",
    "medium": "theme-medium",
    "hard": "theme-hard"
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        level = request.form.get("difficulty")
        if level in difficulty_levels:
            session["level"] = level
            session["range"] = difficulty_levels[level]
            session["number_to_guess"] = random.randint(*difficulty_levels[level])
            session["attempts"] = 0
            session["guess_history"] = []
            session["last_hint"] = ""
            return redirect(url_for("game"))
    return render_template("home.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    number_to_guess = session.get("number_to_guess")
    num_range = session.get("range", (1, 10))
    attempts = session.get("attempts", 0)
    history = session.get("guess_history", [])
    last_hint = session.get("last_hint", "")
    level = session.get("level", "easy")
    theme = theme_colors.get(level, "theme-easy")

    if request.method == "POST":
        try:
            guess = int(request.form.get("guess"))
            session["attempts"] += 1
            session["guess_history"].append(guess)

            if guess == number_to_guess:
                return redirect(url_for("result", outcome="win"))
            elif session["attempts"] >= MAX_ATTEMPTS:
                return redirect(url_for("result", outcome="lose"))
            else:
                session["last_hint"] = "Try a higher number!" if guess < number_to_guess else "Try a lower number!"
                return redirect(url_for("game"))
        except:
            session["last_hint"] = "Invalid input. Please enter a number."

    return render_template("game.html", range=num_range, attempts=attempts,
                           max_attempts=MAX_ATTEMPTS, guess_history=history,
                           hint=last_hint, theme=theme)

@app.route("/result")
def result():
    outcome = request.args.get("outcome")
    attempts = session.get("attempts", 0)
    correct_number = session.get("number_to_guess", '?')
    history = session.get("guess_history", [])
    level = session.get("level", "easy")
    theme = theme_colors.get(level, "theme-easy")
    return render_template("result.html", outcome=outcome,
                           attempts=attempts, correct_number=correct_number,
                           guess_history=history, theme=theme)

if __name__ == "__main__":
    app.run(debug=True)
