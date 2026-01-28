# Work-Life Balance Agent

An AI-powered application that analyzes your daily routine and provides personalized recommendations for better work-life balance using LangGraph and Groq API.

## Features

- AI-driven work-life balance analysis
- Personalized recommendations based on your routine
- Risk level assessment (Low, Medium, High)
- Saved routines tracking for trend analysis
- Deployed on Render for easy access
- Beautiful, responsive UI

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Groq API key (get it from [console.groq.com](https://console.groq.com))

## Local Setup

### Deployment Status

- **Frontend:** Can be opened locally or deployed anywhere
- **Backend (Default):** Uses deployed Render service at `https://work-life-balance-agent.onrender.com/analyze`
  - Service may take 30-60 seconds to wake up on first use
  - Once active, provides lightning-fast response times
  
**Note:** The frontend is configured to use the deployed backend by default. Follow the steps below only if you want to run the backend locally.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Code
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from: https://console.groq.com

### 5. (Optional) Run Backend Locally

To run the backend on your local machine instead of using the deployed service:

```bash
uvicorn api:app --host 127.0.0.1 --port 8001 --reload
```

The API will be available at: `http://127.0.0.1:8001`

Then update the API endpoint in `index.html` (line 408):
```javascript
// Change from:
const response = await fetch("https://work-life-balance-agent.onrender.com/analyze", {

// To:
const response = await fetch("http://127.0.0.1:8001/api/patient/work-life-balance/analyze", {
```

### 6. Open the Frontend

Open `index.html` in your browser or use a local server:

```bash
python -m http.server 5500
```

Then visit: `http://127.0.0.1:5500`

## Project Structure

```
.
├── api.py                 # FastAPI backend server
├── agent_groq.py         # LangGraph agent with Groq integration
├── index.html            # Frontend UI
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (add your GROQ_API_KEY)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `langgraph` - Graph-based agent framework
- `langchain_groq` - Groq LLM integration
- `pydantic` - Data validation
- `python-dotenv` - Environment variables
- `groq` - Groq API client
- `httpx` - HTTP client

## API Endpoints

### Health Check
```
GET /health
```

### Analyze Routine
```
POST /api/patient/work-life-balance/analyze
Content-Type: application/json

{
  "messages": [
    {
      "role": "user",
      "content": "Your daily routine description"
    }
  ]
}
```

Response:
```json
{
  "agent_name": "work-life-agent",
  "status": "success",
  "data": {
    "message": {
      "balanced": true,
      "risk_level": "low",
      "summary": "...",
      "signals": ["..."],
      "recommendations": [...]
    }
  },
  "error_message": null
}
```

## Deployed Version

The application is deployed on Render and available at:
https://work-life-balance-agent.onrender.com

**Note:** The service may take 30-60 seconds to wake up on first use, but will have lightning-fast response times after that.

## Usage

1. Describe your daily routine in the input field
2. Click "Analyze Routine" to get AI-powered insights
3. Review your work-life balance assessment and recommendations
4. Save your routine to track progress over time
5. Download your saved routines as JSON

## Troubleshooting

### "GROQ_API_KEY not found"
- Make sure `.env` file exists with `GROQ_API_KEY=your_key`
- Restart the server after adding the key

### Backend not responding
- Verify the server is running on port 8001
- Check firewall settings
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### CORS errors
- Backend is configured to accept requests from `http://127.0.0.1:5500`
- Update `allow_origins` in `api.py` if using a different frontend URL

## Development

### Running Tests
```bash
python supervisor_test.py
python test_groq.py
```

### Code Structure

- **agent_groq.py**: Defines the LangGraph agent workflow with Groq LLM
- **api.py**: FastAPI endpoints and request/response models
- **index.html**: Frontend UI built with Tailwind CSS

## License

This project is open source.

## Support

For issues or questions, please check the code comments or create an issue in the repository.
