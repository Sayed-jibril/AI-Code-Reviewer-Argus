# How to Run AI Code Reviewer

This document explains how to run the AI Code Reviewer project using the required commands.

## Prerequisites

- Python 3.10+ installed
- Node.js and npm installed
- All dependencies installed (see README.md for setup instructions)

## Running the Project

### Step 1: Start the Backend Server

Open a terminal/command prompt in the project root directory and run:

```bash
uvicorn server.main:app --reload --port 8000
```

**What this command does:**
- `uvicorn` - ASGI server for running FastAPI applications
- `server.main:app` - Points to the FastAPI app instance in `server/main.py`
- `--reload` - Enables auto-reload when code changes (development mode)
- `--port 8000` - Runs the server on port 8000

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['C:\\path\\to\\Ai-Code-Reviewer']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using WatchFiles
INFO:     Started server process [xxxx]
```

**Access points:**
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Step 2: Start the Frontend Server

Open another terminal/command prompt, navigate to the web directory, and run:

```bash
cd web
npm run dev
```

**What this command does:**
- `cd web` - Changes directory to the frontend folder
- `npm run dev` - Runs the Vite development server for React

**Expected output:**
```
> dev
> vite

  VITE v5.4.19  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Note:** If port 5173 is in use, Vite will automatically try the next available port (e.g., 5174).

**Access point:**
- Frontend UI: http://localhost:5173 (or the port shown in output)

## Using the Application

1. Open your browser and go to the frontend URL (e.g., http://localhost:5173)
2. Upload Python files using the file input
3. Click "Review" to analyze your code
4. View the detected issues, metrics, and suggestions

## Stopping the Servers

- **Backend**: Press `Ctrl+C` in the terminal running uvicorn
- **Frontend**: Press `Ctrl+C` in the terminal running npm

## Troubleshooting

- If you get "port already in use" errors, either:
  - Stop the process using that port, or
  - Use a different port (e.g., `--port 8001` for backend, Vite will auto-select for frontend)
- Make sure both servers are running simultaneously for the application to work properly
- The frontend automatically proxies API calls to the backend on port 8000
