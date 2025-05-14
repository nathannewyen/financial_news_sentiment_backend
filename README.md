# Financial News Sentiment Analysis Platform

A full-stack web application that provides real-time sentiment analysis of financial news and stock market data, helping investors make data-driven decisions.

## Features

- 📰 Real-time financial news aggregation
- 🧠 Sentiment analysis using NLP
- 📈 Stock market data integration
- 👤 User watchlist management
- 📊 Interactive data visualization
- 🔔 Custom alerts and notifications

## Tech Stack

### Backend
- FastAPI (Python)
- SQLAlchemy
- JWT Authentication
- RESTful API

### Frontend
- React
- TypeScript
- Modern CSS
- Chart.js

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- PostgreSQL

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Documentation
Once the backend server is running, visit:
```
http://localhost:8000/docs
```
for interactive API documentation.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/financial_news_sentiment](https://github.com/yourusername/financial_news_sentiment) 
