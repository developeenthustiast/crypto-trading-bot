# 🤖 Crypto Trading Bot - Autonomous ML-Powered System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Freqtrade](https://img.shields.io/badge/Freqtrade-2024.11-green.svg)](https://www.freqtrade.io/)

**A complete, production-ready crypto trading bot with machine learning, web dashboard, and free cloud deployment.**

> ⚠️ **IMPORTANT DISCLAIMER**: This software is for **educational and testing purposes only**. Cryptocurrency trading carries significant risk of loss. Never invest money you cannot afford to lose. Past performance does not guarantee future results. This is not financial advice.

---

## ✨ Features

- 🧠 **Machine Learning Strategy**: FreqAI-powered scalping with LightGBM
- 📊 **Dynamic Pair Selection**: Automatically trades top 20 pairs by volume
- 🎯 **Risk Management**: 5% stop-loss, 10% daily loss limit, position sizing
- 🌐 **Modern Web Dashboard**: React-based UI for monitoring trades
- 📱 **Mobile-Friendly**: Access dashboard from any device
- 📲 **Telegram Notifications**: Real-time alerts for every trade
- ☁️ **Free Cloud Deployment**: Run 24/7 on Railway or Render
- 🧪 **Binance Testnet**: Safe paper trading with realistic conditions
- 📈 **Backtesting**: Test strategies on historical data
- 📚 **Complete Documentation**: Step-by-step guides for non-technical users

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** (required)
- **Git** for cloning the repository
- **Binance Testnet API keys** (free, get from [testnet.binance.vision](https://testnet.binance.vision))
- **Node.js 18+** (for web dashboard)

### Installation (Windows)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/crypto-trading-bot.git
cd crypto-trading-bot

# 2. Run the automated setup script
scripts\install_windows.bat

# 3. Configure your API keys
# Edit freqtrade_setup\.env with your Binance Testnet keys

# 4. Download historical data (takes 15-20 minutes)
python scripts\download_data.py

# 5. Train the ML model (takes 30-60 minutes)
python scripts\train_model.py

# 6. Run a backtest to verify everything works
python scripts\backtest.py --period 3m

# 7. Start the bot in dry-run mode
cd freqtrade_setup
freqtrade trade --config config.json

# 8. Open dashboard (in another terminal)
cd dashboard
npm install
npm run dev
# Open http://localhost:5173 in your browser
```

---

## 📁 Project Structure

```
crypto-trading-bot/
├── freqtrade_setup/          # Bot configuration
│   ├── config.json           # Main config (Testnet, risk management)
│   ├── .env.template         # API keys template
│   ├── requirements.txt      # Python dependencies
│   └── user_data/
│       └── strategies/
│           └── MLScalpingStrategy.py  # FreqAI ML strategy
│
├── dashboard/                # Web UI
│   ├── src/                  # React components
│   └── package.json
│
├── scripts/                  # Automation scripts
│   ├── install_windows.bat   # One-click setup
│   ├── download_data.py      # Historical data downloader
│   ├── train_model.py        # ML model training
│   ├── backtest.py           # Backtesting wrapper
│   └── deploy_*.sh           # Cloud deployment scripts
│
└── docs/                     # User documentation
    ├── SETUP_GUIDE.md        # Complete setup walkthrough
    ├── STRATEGY_EXPLAINED.md # ML model explanation
    ├── BACKTEST_GUIDE.md     # Interpreting results
    ├── TROUBLESHOOTING.md    # Common issues & solutions
    └── SAFETY_CHECKLIST.md   # Before going live
```

---

## 📖 Documentation

Comprehensive guides for every step:

- **[Setup Guide](docs/SETUP_GUIDE.md)**: Step-by-step installation for Windows
- **[Strategy Explained](docs/STRATEGY_EXPLAINED.md)**: How the ML model works (plain English)
- **[Backtest Guide](docs/BACKTEST_GUIDE.md)**: Interpreting backtest results
- **[Troubleshooting](docs/TROUBLESHOOTING.md)**: Common issues and fixes
- **[Safety Checklist](docs/SAFETY_CHECKLIST.md)**: Before considering real money

---

## 🎯 How It Works

### Machine Learning Strategy

The bot uses **FreqAI** (Freqtrade's ML framework) with a **LightGBM classifier** to predict profitable trades:

1. **Data Collection**: Analyzes technical indicators (RSI, MACD, Bollinger Bands, Volume)
2. **Feature Engineering**: Creates 30+ derived features (momentum, volatility patterns)
3. **ML Prediction**: Predicts buy signal probability for next 5-15 minutes
4. **Dynamic Pairs**: Scans top 20 pairs by volume, trades only high-confidence opportunities
5. **Risk Management**: Hard-coded 5% stop-loss, dynamic take-profit, daily loss limits

### Web Dashboard

Monitor your bot in real-time:

- **Control Panel**: Start/Stop bot, emergency close all positions
- **Trading Overview**: Current balance, open positions, P/L
- **Performance Metrics**: Win rate, profit/loss, equity curve
- **Trade Log**: Last 50 trades with color-coding
- **Live Logs**: Real-time bot actions and errors

---

## ☁️ Cloud Deployment

Run your bot 24/7 for free:

**Option 1: Railway (Recommended)**
```bash
# Follow instructions in scripts/deploy_railway.sh
```

**Option 2: Render**
```bash
# Follow instructions in scripts/deploy_render.sh
```

Both platforms offer free tiers (~450-750 hours/month). See [Setup Guide](docs/SETUP_GUIDE.md) for detailed deployment instructions.

---

## 🛡️ Risk Management

**Hard-Coded Protections:**
- ✅ Maximum 5% of balance per trade
- ✅ 5% stop-loss on every trade
- ✅ 10% maximum daily loss (bot stops automatically)
- ✅ Only trade when ML confidence > 65%
- ✅ Dynamic pair selection (avoid illiquid pairs)

**Safety Features:**
- ✅ Testnet mode by default (impossible to lose real money)
- ✅ Manual config change required to enable live trading
- ✅ Emergency "panic sell" button in dashboard
- ✅ Telegram alerts for every trade and error

---

## 📊 Backtesting

Test the strategy before running:

```bash
# Backtest last 3 months
python scripts/backtest.py --period 3m

# Backtest last 6 months
python scripts/backtest.py --period 6m

# Backtest last 1 year
python scripts/backtest.py --period 1y
```

Results include:
- Total return %
- Win rate
- Maximum drawdown
- Sharpe ratio
- Trade frequency
- HTML report with charts

**See [Backtest Guide](docs/BACKTEST_GUIDE.md) to understand what "good" performance looks like.**

---

## 🔔 Telegram Notifications

Get notified on your phone for every trade:

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Search for `@userinfobot` and send `/start` to get your chat ID
4. Add credentials to `freqtrade_setup/.env`

You'll receive:
- ✅ Every winning trade (pair, profit %)
- ✅ Every losing trade (pair, loss %)
- ✅ Daily summary (total trades, win rate, P/L)
- ✅ Critical alerts (bot stopped, API errors, daily loss limit hit)

---

## ⚠️ WARNINGS & DISCLAIMERS

**READ BEFORE USING:**

- ⚠️ **Cryptocurrency trading carries significant risk of loss**
- ⚠️ **Past performance does not guarantee future results**
- ⚠️ **ML models can fail, especially in unexpected market conditions**
- ⚠️ **Scalping strategies must overcome ~0.2% trading fees per round trip**
- ⚠️ **Test thoroughly on Testnet for 2-4 weeks minimum**
- ⚠️ **Never invest money you cannot afford to lose**
- ⚠️ **This is educational software, not financial advice**
- ⚠️ **Check your local laws regarding crypto trading and automated trading**
- ⚠️ **Free cloud hosting has limitations (not true 24/7)**

**This project is for LEARNING PURPOSES. Do not use real money without extensive testing and understanding the risks.**

---

## 🔧 Troubleshooting

**Common issues:**

| Issue | Solution |
|-------|----------|
| Bot not starting | Check `user_data/logs/` for errors, verify API keys in `.env` |
| No trades happening | Check ML confidence scores, verify pair list is populated |
| API errors | Regenerate Binance Testnet keys, check [status.binance.com](https://status.binance.com) |
| Dashboard not loading | Ensure Freqtrade is running with API enabled |

**See [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for complete solutions.**

---

## 🤝 Contributing

This is an educational project. Contributions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Freqtrade](https://www.freqtrade.io/)**: The amazing open-source trading bot framework
- **FreqAI**: Built-in ML capabilities
- **Binance Testnet**: Free testing environment
- **The crypto community**: For sharing knowledge and strategies

---

## 📞 Support

- **Documentation**: Check the [docs/](docs/) folder first
- **Issues**: Open a GitHub issue with detailed information
- **Questions**: See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🎓 Learning Resources

New to crypto trading or ML? Start here:

- [Freqtrade Documentation](https://www.freqtrade.io/en/stable/)
- [FreqAI Tutorial](https://www.freqtrade.io/en/stable/freqai/)
- [Strategy Explained](docs/STRATEGY_EXPLAINED.md) (plain English)
- [Technical Analysis Basics](https://www.investopedia.com/terms/t/technicalanalysis.asp)

---

**Remember: This is a learning tool. Trade responsibly. Never invest more than you can afford to lose.**

⭐ If you find this project helpful, please star the repository!
