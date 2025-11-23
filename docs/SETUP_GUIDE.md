# Crypto Trading Bot - Setup Guide

This guide will walk you through setting up the crypto trading bot on Windows, step-by-step.

## Prerequisites

Before you begin, make sure you have:

- ✅ **Windows 10 or 11**
- ✅ **Internet connection**
- ✅ **30-60 minutes** for initial setup
- ✅ **Basic command line knowledge** (we'll guide you)

---

## Part 1: Install Prerequisites (15 minutes)

### Step 1: Install Python 3.10

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.10.x** (latest 3.10 version)
3. Run the installer
4. ⚠️ **IMPORTANT**: Check ☑ "Add Python to PATH" before clicking Install
5. Click "Install Now"
6. Wait for installation to complete

**Verify installation:**
```bash
# Open Command Prompt and type:
python --version

# Should show: Python 3.10.x
```

### Step 2: Install Git for Windows

1. Visit [git-scm.com](https://git-scm.com/download/win)
2. Download the installer
3. Run installer with default settings
4. Click through the wizard (defaults are fine)

**Verify installation:**
```bash
git --version

# Should show: git version x.x.x
```

### Step 3: Install Node.js (for dashboard)

1. Visit [nodejs.org](https://nodejs.org/)
2. Download **LTS version** (18.x or higher)
3. Run installer with default settings

**Verify installation:**
```bash
node --version
npm --version
```

---

## Part 2: Get Binance Testnet API Keys (5 minutes)

The bot uses Binance **Testnet** - it's completely free and uses fake money.

### Creating Testnet API Keys:

1. **Visit**: [testnet.binance.vision](https://testnet.binance.vision/)
   
2. **Click**: "Generate HMAC_SHA256 Key"
   
3. You'll see:
   ```
   API Key: aKj3hF9dS...  (copy this)
   Secret Key: 9fH3kD8... (copy this)
   ```

4. **Save these somewhere safe** - you'll need them shortly!

⚠️ **Important**: These are TEST keys. They don't access real money.

---

## Part 3: Clone and Install Bot (15 minutes)

### Step 1: Clone the Repository

```bash
# Open Command Prompt
# Navigate to where you want the project (example: Desktop)
cd Desktop

# Clone the repository
git clone https://github.com/yourusername/crypto-trading-bot.git

# Enter the project folder
cd crypto-trading-bot
```

### Step 2: Run Automated Setup

```bash
# Run the installation script
scripts\install_windows.bat
```

This script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install all dependencies (5-10 minutes)
- ✅ Create `.env` file

**Wait for it to complete**. You'll see:
```
Installation Complete!
NEXT STEPS: ...
```

### Step 3: Configure API Keys

1. Open `freqtrade_setup\.env` in Notepad
2. Replace placeholders with your Binance Testnet keys:
   ```env
   BINANCE_API_KEY=aKj3hF9dS...  (paste your key)
   BINANCE_API_SECRET=9fH3kD8... (paste your secret)
   ```
3. Save and close

---

## Part 4: Download Data & Train Model (60-90 minutes)

### Step 1: Download Historical Data

This downloads 1 year of price data for training.

```bash
# Make sure virtual environment is active (if not: venv\Scripts\activate)
python scripts\download_data.py
```

- **Time**: 15-20 minutes
- **Size**: ~600 MB
- **What it does**: Downloads price history for 50 trading pairs

You'll see progress like:
```
[45/150] Downloading BTC/USDT (1m)... ✓
[46/150] Downloading ETH/USDT (1m)... ✓
```

### Step 2: Train ML Model

This trains the machine learning model.

```bash
python scripts\train_model.py
```

- **Time**: 30-60 minutes (grab a coffee!)
- **What it does**: Trains FreqAI model on historical data
- **CPU intensive**: Computer may slow down temporarily

You'll see:
```
Training ML Model
⏱ This may take 30-60 minutes...
☕ Good time for a coffee break!
```

---

## Part 5: Test with Backtest (5 minutes)

Before running live, test the strategy on historical data.

```bash
# Test on last 3 months
python scripts\backtest.py --period 3m
```

**What to expect:**
- Backtest runs for 2-5 minutes
- HTML report opens automatically in browser
- You see metrics: profit%, win rate, number of trades

**Understanding results**: See `docs\BACKTEST_GUIDE.md`

---

## Part 6: Run the Bot Locally (10 minutes)

### Step 1: Start Freqtrade Bot

```bash
cd freqtrade_setup
freq trade --config config.json
```

You should see:
```
INFO - Bot started
INFO - Using strategy MLScalpingStrategy
INFO - FreqAI enabled
INFO - Monitoring 20 pairs
```

**Leave this terminal open!**

### Step 2: Start Web Dashboard (new terminal)

Open **another Command Prompt** window:

```bash
cd crypto-trading-bot\dashboard
npm install
npm run dev
```

You should see:
```
VITE ready in 500ms
➜ Local: http://localhost:5173/
```

### Step 3: Open Dashboard

1. Open browser
2. Go to: `http://localhost:5173`
3. You should see the dashboard!

**What you'll see:**
- Bot status: Running
- Balance: 1000 USDT (testnet money)
- Open trades: 0 (at first)
- Trade log: Empty (at first)

---

## Part 7: Verify Everything Works (15 minutes)

### Checklist:

- [ ] Dashboard loads without errors
- [ ] Bot status shows "Running"
- [ ] Balance shows 1000 USDT
- [ ] No error messages in dashboard

### Wait for First Trade

The bot needs to find opportunities. This can take **10-30 minutes**.

**While waiting:**
1. Watch the "Live Log Feed" - you'll see the bot analyzing pairs
2. The bot is looking for ML-predicted profitable setups
3. First trade will appear in "Open Positions" when it enters

---

## Part 8: Set Up Telegram Notifications (Optional, 10 minutes)

Get notified on your phone for every trade!

### Step 1: Create Telegram Bot

1. Open Telegram app
2. Search for **@BotFather**
3. Send: `/newbot`
4. Follow instructions:
   - Choose a name (e.g., "My Trading Bot")
   - Choose username (e.g., "@mytradingbot123_bot")
5. **Save the token** you receive

### Step 2: Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Send: `/start`
3. It will reply with your **chat_id**
4. **Save this number**

### Step 3: Add to Configuration

1. Open `freqtrade_setup\.env`
2. Add:
   ```env
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF... (from BotFather)
   TELEGRAM_CHAT_ID=987654321 (from userinfobot)
   ```
3. Save file
4. Restart Freqtrade bot (Ctrl+C, then `freqtrade trade --config config.json`)

**Test it**: You should get a "Bot started" message on Telegram!

---

## Part 9: Cloud Deployment (Optional, 30 minutes)

Deploy to free cloud hosting to run 24/7.

See separate guides:
- **Railway**: `deploy_railway.sh` comments
- **Render**: `deploy_render.sh` comments

⚠️ **Note**: Free tiers have limitations (~450-750 hours/month)

---

## Troubleshooting

### Bot not starting?

**Check**:
1. Is virtual environment activated? (`venv\Scripts\activate`)
2. Are API keys in `.env` correct?
3. Check logs: `freqtrade_setup\user_data\logs\`

### No trades happening?

**This is normal if:**
- Bot just started (needs time to analyze)
- Market conditions don't meet ML criteria
- ML confidence is below threshold (65%)

**Check**:
- Live Log Feed shows "Analyzing pairs..."
- ML model is loaded (check startup logs)

### Dashboard not loading?

**Check**:
1. Is Freqtrade running? (should see API enabled in logs)
2. Is dashboard dev server running? (`npm run dev`)
3. Try: `http://localhost:5173` in browser
4. Check browser console for errors (F12)

### ML model not found?

**Fix**:
```bash
# Retrain model
python scripts\train_model.py
```

---

## Next Steps

1. ✅ **Monitor for 24-48 hours** on Testnet
2. ✅ **Review performance** in dashboard
3. ✅ **Read**: `docs\STRATEGY_EXPLAINED.md` to understand the ML model
4. ✅ **Read**: `docs\SAFETY_CHECKLIST.md` before even thinking about real money

---

## Getting Help

- **Troubleshooting**: See `docs\TROUBLESHOOTING.md`
- **Strategy questions**: See `docs\STRATEGY_EXPLAINED.md`
- **Backtest results**: See `docs\BACKTEST_GUIDE.md`
- **GitHub Issues**: Open an issue with your question

---

## Important Reminders

⚠️ **You are using TESTNET** - this is fake money for testing  
⚠️ **Do NOT use real money** without extensive testing (weeks minimum)  
⚠️ **Trading is risky** - only invest what you can afford to lose  
⚠️ **This is educational software** - not financial advice

---

**Congratulations!** Your bot is now running. Monitor it closely and learn how it works before considering anything else.
