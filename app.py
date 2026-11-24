
from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory database
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Helper function to find an event using its ID
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


# GET / - Welcome message
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Event Management API"
    }), 200


# GET /events - Retrieve all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    # Validate the incoming title
    if not isinstance(data, dict):
        return jsonify({"error": "Title is required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    # Generate a unique event ID
    new_id = max((event.id for event in events), default=0) + 1

    # Create and store the event
    new_event = Event(new_id, title.strip())
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Title is required"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    event.title = title.strip()

    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
