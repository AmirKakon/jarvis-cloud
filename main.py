import os
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from services.github.github_routes import github_routes
import config

# Load environment variables
load_dotenv()

# Get the logger for the application
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(config.Config)

app.register_blueprint(github_routes, url_prefix="/api/github")

@app.route("/")
def show_endpoints():
    # Group routes by their URL prefix
    routes_by_group = {}

    for rule in app.url_map.iter_rules():
        # Skip static files and internal Flask routes
        if rule.endpoint != 'static' and not rule.endpoint.startswith('flask') and rule.rule != '/':
            # Get the prefix (e.g., api/github, api/test)
            parts = rule.rule.split("/")
            prefix = parts[2]

            # Group the route by prefix
            if prefix not in routes_by_group:
                routes_by_group[prefix] = []

            # Add the route to the appropriate group
            routes_by_group[prefix].append(str(rule))

    # Return HTML with grouped routes
    return render_template('endpoints.html', routes_by_group=routes_by_group)

@app.route("/api/config")
def dev():
    env = os.getenv("FLASK_ENV")
    logger.debug(f"Dev endpoint called, You are in env: {env}")
    return jsonify({"ENV": env, "PORT": app.config.get('PORT')})

if __name__ == "__main__":
    # Get port from config and start the app
    port = app.config.get('PORT', 3000)
    app.run(debug=app.config.get('DEBUG', True), host="0.0.0.0", port=port)
