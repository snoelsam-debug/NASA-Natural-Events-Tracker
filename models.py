import requests


class NaturalEvent:
    

    def __init__(
        self,
        eonet_id,
        title,
        category,
        status,
        latitude,
        longitude,
        event_date,
        magnitude=None,
        mag_unit=None,
        source_url=None):
    
        
        self.__eonet_id = eonet_id
        self.title = title
        self.category = category
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.event_date = event_date
        self.magnitude = magnitude
        self.mag_unit = mag_unit
        self.source_url = source_url
    @property
    def eonet_id(self):
        return self.__eonet_id

    def is_active(self):
        return self.status == "open"

    def summary(self):
        return f"{self.category}: {self.title} ({self.status})"

class WatchedEvent(NaturalEvent):

    def __init__(
        self,
        eonet_id,
        title,
        category,
        status,
        latitude,
        longitude,
        event_date,
        magnitude=None,
        mag_unit=None,
        source_url=None,
        note="",
        alert_active=False
    ):
        super().__init__(
            eonet_id=eonet_id,
            title=title,
            category=category,
            status=status,
            latitude=latitude,
            longitude=longitude,
            event_date=event_date,
            magnitude=magnitude,
            mag_unit=mag_unit,
            source_url=source_url
        )

        self.note = note
        self.alert_active = alert_active

    def toggle_alert(self):
        self.alert_active = not self.alert_active
        return self.alert_active

    def summary(self):
        text = super().summary()

        if self.note:
            text += f" | Note: {self.note}"

        text += f" | Alert: {'On' if self.alert_active else 'Off'}"

        return text

class EventFetcher:

    BASE_URL = "https://eonet.gsfc.nasa.gov/api/v3"

    def fetch_events(
        self,
        status="open",
        category=None,
        days=30,
        limit=20
    ):
        params = {
            "status": status,
            "days": days,
            "limit": limit
        }

        if category:
            params["category"] = category

        response = requests.get(
            f"{self.BASE_URL}/events",
            params=params,
            timeout=10
        )

        response.raise_for_status()

        api_data = response.json()
        events = api_data.get("events", [])

        result = []

        for event_data in events:
            event = self._create_event(event_data)
            result.append(event)

        return result

    def fetch_event(self, eonet_id):
        response = requests.get(
            f"{self.BASE_URL}/events/{eonet_id}",
            timeout=10
        )

        response.raise_for_status()

        event_data = response.json()
        if "events" in event_data:
            events = event_data["events"]

            if not events:
                raise ValueError("The requested event was not found.")

            event_data = events[0]

        return self._create_event(event_data)

    def fetch_categories(self):
        response = requests.get(
            f"{self.BASE_URL}/categories",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        return data.get("categories", [])

    def _create_event(self, event_data):

        categories = event_data.get("categories", [])

        if categories:
            category = categories[0].get("title", "Unknown")
        else:
            category = "Unknown"

        
        if event_data.get("closed") is None:
            status = "open"
        else:
            status = "closed"

        geometries = event_data.get("geometry", [])

        latitude = None
        longitude = None
        event_date = None
        magnitude = None
        mag_unit = None

        if geometries:
            first_geometry = geometries[0]

            event_date_value = first_geometry.get("date")

            if event_date_value:
                event_date = event_date_value[:10]

            coordinates = first_geometry.get("coordinates", [])

            if len(coordinates) >= 2:
                longitude = coordinates[0]
                latitude = coordinates[1]

            magnitude = first_geometry.get("magnitudeValue")
            mag_unit = first_geometry.get("magnitudeUnit")

        sources = event_data.get("sources", [])
        source_url = None

        if sources:
            source_url = sources[0].get("url")

        return NaturalEvent(
            eonet_id=event_data.get("id", ""),
            title=event_data.get("title", "Untitled event"),
            category=category,
            status=status,
            latitude=latitude,
            longitude=longitude,
            event_date=event_date,
            magnitude=magnitude,
            mag_unit=mag_unit,
            source_url=source_url
        )

if __name__ == "__main__":
    fetcher = EventFetcher()

    try:
        events = fetcher.fetch_events(
            status="open",
            days=30,
            limit=5
        )

        for event in events:
            print(event.summary())
            print(f"ID: {event.eonet_id}")
            print(f"Date: {event.event_date}")
            print(f"Coordinates: {event.latitude}, {event.longitude}")
            print("-" * 40)

    except requests.exceptions.RequestException as error:
        print(f"Could not connect to NASA EONET: {error}")