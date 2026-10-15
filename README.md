# Financial Market Intelligence Bot

A graduation-project research prototype that combines financial-news collection, abstractive summarization, sentiment classification, a Telegram interface, and experimental stock-price forecasting. The original work dates from around 2022.

> **Status: legacy research prototype — not production-ready.** The code has been curated for portfolio presentation and credentials were removed from the published copy. The bot and forecasting experiments have not been fully runtime-tested in a clean environment.

## Project overview

- **News collection:** searches for Yahoo Finance news links and extracts article text with `requests` and Beautiful Soup.
- **Summarization:** uses the Hugging Face `human-centered-summarization/financial-summarization-pegasus` model.
- **Financial sentiment:** uses `ahmedrachid/FinancialBERT-Sentiment-Analysis` to classify text as positive, neutral, or negative.
- **Telegram interface:** lets users select a ticker/crypto symbol and request news analysis. The bot also contains an experimental price-forecasting path.
- **Forecasting experiments:** separate Streamlit/Prophet and PyTorch LSTM scripts are preserved under `experiments/` for review.

## Technology stack

Python · Hugging Face Transformers · PyTorch · FinancialBERT · PEGASUS · python-telegram-bot · Beautiful Soup · Requests · yfinance · Prophet · Streamlit · pandas

## Repository structure

```text
financial-market-intelligence/
├── src/telegram_bot.py
├── experiments/
│   ├── prophet_stock_forecast_app.py
│   └── lstm_forecasting_experiment.py
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Security before running

The source archive contained Telegram bot tokens embedded directly in several files. Those values have been removed from this curated repository. **Treat the old tokens as compromised and revoke/regenerate each one in Telegram's `@BotFather` before using a bot again.** I cannot revoke credentials on your behalf because that requires access to your Telegram account. Do not commit a real `.env` file or token.

1. Create a new token through `@BotFather` for the bot you intend to use.
2. Create a local `.env` file from `.env.example` and insert the new token. `.env` is ignored by Git.
3. In your terminal, activate a virtual environment and install the requirements.
4. Set `TELEGRAM_BOT_TOKEN` in the environment before starting `src/telegram_bot.py`. The example code expects this environment variable; it does not automatically load `.env`. On Windows PowerShell, use `$env:TELEGRAM_BOT_TOKEN="your-new-token"` for the current terminal session.

## Setup (Windows PowerShell)

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:TELEGRAM_BOT_TOKEN="your-new-token"
python .\src\telegram_bot.py
```

The Transformers models download on first use and may require substantial memory and disk space. Dependency compatibility may need adjustments, especially because the original Telegram integration uses the older `python-telegram-bot` v13 API. A successful package installation alone does not guarantee that the entire application works.

## Known limitations and next improvements

- The news collector relies on scraping search-engine and publisher HTML, which can change or block automated requests.
- The bot loads large NLP models at startup, increasing startup time and memory usage.
- Error handling, request timeouts, retries, logging, and automated tests need improvement.
- The forecasting scripts are experimental and have not been validated against robust baselines or leakage-safe evaluation. Their output must not be interpreted as financial advice.
- A production-quality revision should separate scraping, NLP inference, bot handlers, and forecasting into tested modules; use maintained APIs; add tests and CI; and document model/data licenses.

## Academic / financial disclaimer

This project was developed as an academic prototype. Sentiment labels and model-generated forecasts can be wrong, and historical performance does not guarantee future results. Nothing in this repository is financial advice or a recommendation to buy or sell an asset.

## Attribution

The original graduation-project bot text identifies Abdelrhman Nyazi and Saif Abdulwahab as student developers and Dr. Firas Al-Zein as supervisor. Confirm that you are comfortable publishing these names before making the repository public.
