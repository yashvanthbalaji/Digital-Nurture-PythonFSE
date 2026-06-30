from flask import Flask, jsonify
from config import Config
from courses.routes import courses_bp


# APPLICATION FACTORY PATTERN
# We put everything inside a function instead of at the top of the file.
# This avoids circular import problems and makes testing easier.

def create_app():
    # Create the Flask application
    # __name__ tells Flask where this file is located
    app = Flask(__name__)

    # Load all settings from the Config class in config.py
    app.config.from_object(Config)

    # Register the courses blueprint
    # This activates all routes defined in courses/routes.py
    app.register_blueprint(courses_bp)

    # ── ERROR HANDLERS (Task 2) ──────────────────────────────
    # By default Flask returns HTML error pages.
    # We override them to return JSON — APIs must always return JSON.

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

    return app


# Only runs when you directly execute: python app.py
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)