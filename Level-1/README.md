# Smart ID Card System - Level 1 (Clean Monolith)

This is a clean, fully functional, synchronous monolithic application.
It acts as the baseline for the Level 1 hackathon challenge before bugs are injected.

## Project Structure
* `backend/`: Flask application with SQLite database.
* `frontend/`: React single-page application.

## Prerequisites
* Node.js (v18+)
* Python (3.9+)

## Setup Instructions

### 1. Run the Backend
Open a terminal and navigate to the `backend/` directory:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The backend will run on `http://localhost:5000`.

### 2. Run the Frontend
Open a new terminal and navigate to the `frontend/` directory:
```bash
cd frontend
npm install
npm run dev
```
The frontend will usually be accessible at `http://localhost:5173`.

## Functional Flow
1. User submits Name, Department, and Image.
2. The record is saved in SQLite as `Pending`.
3. The system immediately updates it to `Processing`.
4. A 2-second sleep simulates the print job synchronously.
5. The record is updated to `Printed`.
6. The frontend receives a 200 OK and refreshes the queue list to show the completed card.
