# Activate the virtual environment
. .venv\Scripts\Activate.ps1

#set env variable
$env:FLASK_ENV = "development"

# Run the Flask development server
python -m flask --app main run --debug
