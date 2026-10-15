# Financial Market Intelligence

An AI-powered financial news analysis project developed as a graduation project. It brings together natural language processing, financial sentiment analysis, text summarization, and market-data exploration in one workflow.

## Overview

Financial news can be difficult to review at scale. This project explores how NLP models can help turn financial articles into concise summaries and structured sentiment signals.

## Key Features

- **Financial news collection** — retrieves and extracts financial-news content for a selected market symbol.
- **AI-powered summarization** — generates concise summaries of longer articles using a PEGASUS-based summarization model.
- **Financial sentiment analysis** — classifies news text into positive, neutral, or negative sentiment using a FinancialBERT model.
- **Interactive Telegram interface** — provides a chat-based way to request news analysis for selected tickers and crypto symbols.
- **Market forecasting experiments** — includes separate exploratory implementations using Prophet and LSTM.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| NLP and AI | Hugging Face Transformers, FinancialBERT, PEGASUS |
| Data processing | pandas, Requests, Beautiful Soup |
| Market data | yfinance |
| Forecasting experiments | Prophet, PyTorch, LSTM |
| Interface | python-telegram-bot, Streamlit |

## Project Structure

```text
financial-market-intelligence/
├── src/
│   └── telegram_bot.py
├── experiments/
│   ├── prophet_stock_forecast_app.py
│   └── lstm_forecasting_experiment.py
├── docs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How It Works

1. A user selects a financial ticker or cryptocurrency symbol.
2. The project collects relevant financial-news content.
3. NLP models summarize article text and estimate its sentiment.
4. Separate forecasting experiments explore time-series approaches to market data.

## Scope

This is an academic project exploring the application of NLP and machine learning to financial information. The forecasting scripts are experimental and are separate from the news-analysis workflow.

## Notes

- Pre-trained models may download when first used and can require significant memory and disk space.
- External news pages and data providers may change their formats or availability.
- Results depend on the input data and model behavior; sentiment labels and forecasts should not be treated as investment recommendations.
- Model and data usage remain subject to the respective providers' licenses and terms.

## Disclaimer

This project is for educational and research purposes only. It does not provide financial advice or recommendations to buy or sell any asset.
