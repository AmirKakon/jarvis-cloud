from firebase_functions import https_fn
import os
import logging
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from services.github.github_routes import github_routes
import config as config

# Load environment variables
load_dotenv()

# Get the logger for the application
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config.from_object(config.Config)

# Register the routes
app.register_blueprint(github_routes, url_prefix="/api/github")

@app.route("/")
def show_endpoints():
    # Group routes by their URL prefix
    routes_by_group = {}

    for rule in app.url_map.iter_rules():
        # Skip static files and internal Flask routes
        if rule.endpoint != 'static' and not rule.endpoint.startswith('flask') and rule.rule != '/':
            # Get the prefix (e.g., api/github, api/config)
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


# Create a function for the development environment
@https_fn.on_request(max_instances=1)
def jarvis_cloud_dev(req: https_fn.Request) -> https_fn.Response:
    env = os.getenv("FLASK_ENV")
    if env == "development":
        logger.info("Development environment detected.")
        with app.request_context(req.environ):
            return app.full_dispatch_request()
    else:
        logger.warning("Development function called in non-development environment.")
        return jsonify({"error": "Not in development environment."}), 400


# Create a function for the production environment
@https_fn.on_request(max_instances=1)
def jarvis_cloud_prod(req: https_fn.Request) -> https_fn.Response:
    env = os.getenv("FLASK_ENV")
    if env == "production":
        logger.info("Production environment detected.")
        with app.request_context(req.environ):
            return app.full_dispatch_request()
    else:
        logger.warning("Production function called in non-production environment.")
        return jsonify({"error": "Not in production environment."}), 400


if __name__ == "__main__":
    port = app.config.get('PORT', 3000)
    app.run(debug=app.config.get('DEBUG', True), host="0.0.0.0", port=port)