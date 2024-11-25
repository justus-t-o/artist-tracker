# Flask Spotify Auth App

A Flask application that uses Spotify API for authentication and functionality. This guide explains how to set up and run the application.

---

## Prerequisites

Before running the application, ensure you have the following installed on your system:
- Python 3.7+
- pip (Python package installer)
- Virtual environment tool (e.g., `venv` or `virtualenv`)

---

## Setup Instructions


### 1. Create a Virtual Environment
Set up a Python virtual environment to isolate dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

### 2. Install Dependencies
Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
The application requires Spotify API credentials. Set the following environment variables in your system:

- **CLIENT_ID**: Your Spotify application's Client ID.
- **CLIENT_SECRET**: Your Spotify application's Client Secret.

#### On Unix/Mac:
```bash
export CLIENT_ID="your_client_id"
export CLIENT_SECRET="your_client_secret"
```

#### On Windows (Command Prompt):
```cmd
set CLIENT_ID=your_client_id
set CLIENT_SECRET=your_client_secret
```

Alternatively, you can create a `.env` file in the root directory and add the variables there:
```plaintext
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```
Make sure to install `python-dotenv` if you choose this method:
```bash
pip install python-dotenv
```

### 4. Run the Application
Start the Flask development server:

```bash
python app.py
```

The app will be available at `http://127.0.0.1:8000`.

---
