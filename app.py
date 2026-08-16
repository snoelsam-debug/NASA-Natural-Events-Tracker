import sqlite3

from flask import Flask, render_template, request, flash,redirect, url_for

from models import EventFetcher


app = Flask(__name__)
app.secret_key = "nasa-tracker-secret-key"

DATABASE = "events.db"

event_fetcher = EventFetcher()


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS watched_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eonet_id TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            category TEXT,
            status TEXT,
            latitude REAL,
            longitude REAL,
            event_date TEXT,
            magnitude REAL,
            mag_unit TEXT,
            source_url TEXT,
            note TEXT DEFAULT '',
            alert_active INTEGER DEFAULT 0,
            saved_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL UNIQUE,
            label TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS search_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT,
            searched_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    connection.commit()
    connection.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/browse")
def browse():
    status = request.args.get("status", "open")
    category = request.args.get("category", "")
    days = request.args.get("days", "30")

    try:
        days_number = int(days)
    except ValueError:
        days_number = 30
        days = "30"

    try:
        events = event_fetcher.fetch_events(
            status=status,
            category=category or None,
            days=days_number,
            limit=20
        )

        categories = event_fetcher.fetch_categories()

        if not events:
            flash("No events were found for these filters.", "warning")

    except Exception:
        events = []
        categories = []

        flash(
            "NASA EONET is currently unavailable. Please try again later.",
            "error"
        )

    return render_template(
        "browse.html",
        events=events,
        categories=categories,
        selected_status=status,
        selected_category=category,
        selected_days=days
    )


@app.route("/event/<eonet_id>")
def event_detail(eonet_id):
    try:
        event = event_fetcher.fetch_event(eonet_id)

        return render_template(
            "event_detail.html",
            event=event
        )

    except Exception:
        flash(
            "NASA EONET is currently taking too long to respond. Please try again.",
            "error"
        )

        return redirect(url_for("browse"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)