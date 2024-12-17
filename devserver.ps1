# Activate the virtual environment
. venv\Scripts\Activate.ps1

#set env variable
$env:FLASK_ENV = "development"

# Check if requirements are installed
if (Test-Path requirements.txt) {
    Write-Host "Installing dependencies from requirements.txt..."
    pip install -r functions/requirements.txt
} else {
    Write-Host "requirements.txt not found. Skipping dependency installation." -ForegroundColor Yellow
}

# Run the Flask development server
Write-Host "Starting Flask server..."
python -m flask --app main run --debug

# Run the Flask development server
python -m flask --app main run --debug
