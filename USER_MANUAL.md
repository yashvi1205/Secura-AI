# Secura AI - User Manual

Welcome to **Secura AI**! This manual will guide you through running the application, accessing the features, and managing the built-in Console dashboard.

## 1. Hosting and Starting the Software
The software is designed to run locally on your machine. To launch the server, use the following commands in your PowerShell terminal:

```powershell
cd c:\Users\winuser\Desktop\secura-ai
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --reload
```

*Note: The server will host live on `http://127.0.0.1:8000/`.*

## 2. Navigating the UI
Once the server is running, open your web browser and go to:
**[http://127.0.0.1:8000/ui/](http://127.0.0.1:8000/ui/)**

### Core Pages (No Setup Required)
- **Home**: An overview of the Secura AI features.
- **Downloads**: View available platform integrations.
- **Legacy Analyzer**: A tool to analyze prompt safety. Enter any prompt (e.g., "How to hack a system") and click "Analyze & Log" to see the risk level and safety score.

## 3. Setting Up the Console Database
To use the advanced dashboard features (Overview, Live Events, Detections, Incidents), you need to initialize the database and obtain an API key. I have already created the required `.env` file for you, which contains:
```env
BOOTSTRAP_TOKEN=test-token-123
AUTO_CREATE_SCHEMA=true
```

### Steps to Bootstrap:
1. Make sure your server is running. (If you just started it, verify it read the `.env` file by stopping it with `Ctrl+C` and running it again).
2. Open a **new** PowerShell window and activate the virtual environment:
   ```powershell
   cd c:\Users\winuser\Desktop\secura-ai
   .\venv\Scripts\Activate.ps1
   ```
3. Run this command to generate your API key:
   ```powershell
   $headers = @{ "X-Bootstrap-Token"="test-token-123"; "Content-Type"="application/json" }
   $body = '{"org_name": "Test"}'
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/admin/bootstrap" -Method POST -Headers $headers -Body $body
   ```
4. Find the `api_key` in the output and copy it. This is your master access key!

## 4. Configuring the Dashboard
1. Go back to your browser: [http://127.0.0.1:8000/ui/](http://127.0.0.1:8000/ui/)
2. Click on **Settings**.
3. Paste the API key into the **X-Secura-Key** input field.
4. Click **Save settings**.

Now you can click on **Overview**, **Live Events**, **Detections**, and **Incidents** on the left menu, and the data will successfully load!

## 5. Live Hosting 
If you wish to make the local software accessible over the public internet (host it live globally), you can use a tunneling tool like [`ngrok`](https://ngrok.com/):
```powershell
ngrok http 8000
```
This will give you a public `https://...` address that securely forwards to your local server. Make sure to share that URL carefully, as your dashboard is protected by the API key configured in Step 4.

Enjoy using Secura AI!
