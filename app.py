from flask import Flask, request, redirect, render_template, url_for, session
import pymysql
import string, random
import time


app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Needed for session

# Database connection



# Database connection with retry logic
while True:
    try:
        db = pymysql.connect(
            host="mysql",
            user="root", # for only testing purpose hardcode credentials! 
            password="root123",
            database="url_shortener"
        )
        cursor = db.cursor()
        print("✅ Successfully connected to the database!")
        break
    except pymysql.err.OperationalError:
        print("⏳ Database not ready, retrying in 2 seconds...")
        time.sleep(2)

# Helper function

def generate_short_code(length=6):
    """Generate a random alphanumeric short code."""
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # Ensure code is unique
        cursor.execute("SELECT 1 FROM urls WHERE short_code=%s", (code,))
        if not cursor.fetchone():
            return code


# Home page: submit URL

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form.get("long_url")
        if not original_url:
            return render_template("index.html", error="URL is required")

        short_code = generate_short_code()
        cursor.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)",
            (original_url, short_code)
        )
        db.commit()

        # Store short URL in session to show once
        session["short_url"] = request.host_url + short_code
        return redirect(url_for("index"))

    # GET request
    short_url = session.pop("short_url", None)  # disappears after refresh
    return render_template("index.html", short_url=short_url)


# Redirect short URL

@app.route("/<short_code>")
def redirect_url(short_code):
    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code=%s",
        (short_code,)
    )
    result = cursor.fetchone()
    if result:
        return redirect(result[0])
    return "URL not found", 404


# Run the app
if __name__ == "__main__":
    # Ensure host is set to "0.0.0.0"
    app.run(host="0.0.0.0", port=5000, debug=True)
