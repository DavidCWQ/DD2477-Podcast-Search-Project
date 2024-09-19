# backend main.py

from backend.app import webapp


# Run the Flask application
if __name__ == '__main__':
    webapp.run(debug=True)