from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import time
import logging

# MongoDB configuration
MONGO_URI = "YOUR_DB_URL"
MONGO_DB = "YOUR_DB_NAME"

# Initialize Flask app
app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Record start time for uptime calculation
start_time = time.time()

# Initialize MongoDB client
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB]
    user_history = db["user_history"]
except Exception as e:
    logger.error(f"Failed to initialize MongoDB client: {e}")
    raise

@app.route('/', methods=['GET'])
def health_check():
    try:
        # Calculate uptime
        uptime_seconds = int(time.time() - start_time)
        uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"

        # Check MongoDB connectivity
        mongo_client.admin.command('ping')
        health_status = "healthy"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_status = "unhealthy"

    response = {
        "status": health_status,
        "uptime": uptime_str,
        "developers": ["@ISmartDevs", "@TheSmartDev"],
        "message": "API is running. Use /stats?user=<user_id_or_username> to fetch user stats."
    }
    return jsonify(response), 200 if health_status == "healthy" else 503

@app.route('/stats', methods=['GET'])
def get_user_stats():
    try:
        # Get user parameter from query string
        user = request.args.get('user')
        if not user:
            return jsonify({"error": "User parameter is required"}), 400

        user_id = None
        username = None
        # Determine if user input is a username or user ID
        if user.startswith('@'):
            username = user
        elif user.isdigit():
            user_id = int(user)
        else:
            return jsonify({"error": "Invalid user parameter. Use user ID or username starting with '@'"}), 400

        # Query by username if provided
        if username:
            user_doc = user_history.find_one({"usernames.username": username})
            if not user_doc:
                return jsonify({"error": f"No history found for username {username}"}), 404
            user_id = user_doc["user_id"]
        else:
            # Query by user ID
            user_doc = user_history.find_one({"user_id": user_id})
            if not user_doc:
                return jsonify({"error": f"No history found for user ID {user_id}"}), 404

        # Format the response
        names = [
            {"name": entry["name"], "timestamp": entry["timestamp"].strftime("%d/%m/%y %H:%M:%S")}
            for entry in user_doc.get("names", [])
        ]
        usernames = [
            {"username": entry["username"], "timestamp": entry["timestamp"].strftime("%d/%m/%y %H:%M:%S")}
            for entry in user_doc.get("usernames", [])
        ]

        response = {
            "user_id": user_doc["user_id"],
            "names": names,
            "usernames": usernames
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error retrieving stats for user {user}: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)