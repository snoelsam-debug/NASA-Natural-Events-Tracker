# NASA Natural Events Tracker

## Description

NASA Natural Events Tracker is a Flask web application that uses NASA's
EONET API to display current and past natural events such as wildfires,
storms, and volcanoes.

Users can browse natural events, filter the events by category, status,
and number of days, and view detailed information about individual events.

The application uses Python, Flask, SQLite, HTML, CSS, and the Requests
library.

## Setup

1. Clone or download the project.

2. Create a virtual environment:

   python -m venv .venv

3. Activate the virtual environment.

   Windows PowerShell:

   .\.venv\Scripts\Activate.ps1

4. Install the required packages:

   pip install -r requirements.txt

5. Start the Flask application:

   flask run

6. Open the application in your browser:

   http://127.0.0.1:5000


## OOP Design

The application uses object-oriented programming in models.py.

### NaturalEvent

NaturalEvent represents a natural event received from the NASA EONET API.

It stores information such as:
- EONET ID
- title
- category
- status
- latitude
- longitude
- date
- magnitude
- magnitude unit
- source URL

### WatchedEvent

WatchedEvent inherits from NaturalEvent.

It represents an event that has been saved to the user's watch list.
It also contains additional information such as a note and whether an
alert is active.

### EventFetcher

EventFetcher communicates with the NASA EONET API using the Requests
library.

It can:
- fetch multiple natural events
- fetch one event using its EONET ID
- fetch available event categories
- convert API data into NaturalEvent objects


## Known Limitations

- The application depends on the NASA EONET API and requires an internet
  connection.
- If the NASA API is slow or unavailable, event information may not load.
- Some NASA events do not contain magnitude information.