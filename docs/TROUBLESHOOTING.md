# Troubleshooting Guide

Common issues and their solutions.

## Bot Won't Start

### Error: "Python not found"
**Solution:**
1. Install Python 3.10 from python.org
2. Make sure "Add to PATH" was checked during installation
3. Restart Command Prompt
4. Verify: `python --version`

### Error: "Freqtrade not found"
**Solution:**
1. Activate virtual environment: `venv\Scripts\activate`
2. Reinstall: `pip install -r freqtrade_setup\requirements.txt`
3. Verify: `freqtrade --version`

### Error: "Invalid API keys"
**Solution:**
1. Regenerate keys at testnet.binance.vision
2. Update `.env` file with new keys
3. Ensure no extra spaces in `.env`
4. Restart bot

---

## No Trades Happening

### Bot running but zero trades

**This is often normal! Reasons:**
- ML confidence < 65% (no good opportunities)
- All pairs fail safety filters
- Low market volatility
- Bot just started (needs time to analyze)

**Check:**
1. Look at Live Log Feed - should show "Analyzing pairs..."
2. Check `user_data/logs/freqtrade.log` for ML predictions
3. Bot often waits 10-30 minutes for first trade

**If still no trades after 2 hours:**
- Check ML model is loaded (see logs)
- Verify pairs are being analyzed (logs show pair names)
- Retrain model: `python scripts/train_model.py`

---

## Dashboard Issues

### Dashboard won't load

**Check:**
1. Is Freqtrade running? (`freqtrade trade --config config.json`)
2. Is dashboard dev server running? (`npm run dev` in dashboard folder)
3. Correct URL? Should be `http://localhost:5173`

**Error: "Cannot connect to bot"**
- Freqtrade API must be running
- Check `config.json` has `"api_server": {"enabled": true}`
- Restart Freqtrade

### Dashboard shows wrong data

**Solution:**
- Hard refresh: Ctrl+F5
- Check browser console (F12) for errors
- Verify Freqtrade API endpoint: `http://localhost:8080/api/v1/status`

---

## Trading Errors

### Trades not executing

**Check logs for:**
- "Insufficient balance" → Need more USDT in account
- "Min notional" error → Pair requires minimum order size
- API rate limits → Bot is being throttled

**Solution:**
- Ensure test account has enough balance (testnet gives free funds)
- Reduce `max_open_trades` to lower API calls
- Check Binance status page

### Stop-loss not working

**Verify in config.json:**
```json
"stoploss": -0.05,  // Must be negative (5% loss)
"trailing_stop": true
```

**Check logs** for "Stop loss triggered" messages.

---

## ML Model Issues

### "Model not found" error

**Solution:**
```bash
python scripts/train_model.py
```

Wait for training to complete (30-60 min).

### Poor ML performance

**Win rate < 50%, frequent losses:**

1. **Retrain model** (markets changed)
2. **Check backtest results** - is strategy profitable historically?
3. **Lower confidence threshold** - might be too conservative
4. **Increase training data** - download more history

**Overfitting (backtest great, live terrible):**
- Retrain with more diverse data
- Increase trade count in backtest
- Test on different market periods

---

## Data Download Problems

### Download fails partway

**Common causes:**
- Internet connection dropped
- Binance rate limiting

**Solution:**
- Run `python scripts/download_data.py` again
- It will skip already downloaded pairs
- Or download specific pairs manually:
  ```bash
  freqtrade download-data --pairs BTC/USDT --timeframe 5m --days 365
  ```

### "No data available"

**Check:**
- Data is in `freqtrade_setup/user_data/data/binance/`
- JSON files exist (e.g., `BTC_USDT-5m.json`)
- Files are not empty (should be 1+ MB each)

---

## Telegram Notification Issues

### Not receiving notifications

**Check:**
1. Bot token correct in `.env`?
2. Chat ID correct in `.env`?
3. Did you send `/start` to your bot on Telegram?
4. Restart Freqtrade after updating `.env`

**Test:**
Send this to your bot on Telegram (should echo back):
```
/status
```

---

## Performance Issues

### Bot using too much CPU

**Normal during:**
- Model training (30-60 min)
- Initial data download
- First few minutes of startup

**If constantly high:**
- Lower `"process_throttle_secs"` in config.json
- Reduce number of pairs being monitored
- Close other programs

### Bot using too much RAM

**Reduce memory:**
- Lower `number_assets` in VolumePairList (trade fewer pairs)
- Increase `"refresh_period"` (update less frequently)
- Don't run other heavy programs simultaneously

---

## Cloud Deployment Issues

### Railway/Render app keeps sleeping

**Free tiers have limitations:**
- Railway: 500 hours/month
- Render: Sleeps after 15 min inactivity

**Solutions:**
- Upgrade to paid tier ($5-10/month)
- Use "keep-alive" ping service
- Accept downtime and restart manually

### Environment variables not working

**Check:**
- Variables are set in Railway/Render dashboard
- Variable names match exactly (case-sensitive)
- No quotes around values (set as: `abc123` not `"abc123"`)
- Restart service after changing variables

---

## Common Error Messages

### "ccxt.base.errors.InsufficientFunds"
**Meaning:** Not enough USDT to open trade  
**Fix:** Get more testnet USDT or lower position size

### "NoTradingPairAvailable no pair in whitelist"
**Meaning:** VolumePairList returned no pairs  
**Fix:** Check internet connection, verify Binance API is accessible

### "Strategy caused an error: module 'talib' has no attribute..."
**Meaning:** TA-Lib not installed properly  
**Fix:** Reinstall: `pip install ta-lib==0.4.32`

### "FreqAI not found"
**Meaning:** FreqAI dependencies missing  
**Fix:** `pip install -r freqtrade_setup/requirements.txt`

---

## Where to Find Logs

### Freqtrade Logs:
```
freqtrade_setup/user_data/logs/freqtrade.log
```

**What to look for:**
- Errors (search for "ERROR")
- Trade entries (search for "Bought")
- Trade exits (search for "Sold")
- ML predictions (search for "FreqAI")

### Dashboard Logs:
**Browser console:**
1. Open dashboard
2. Press F12
3. Click "Console" tab
4. Look for red error messages

---

## Getting More Help

1. **Check Documentation:**
   - SETUP_GUIDE.md
   - STRATEGY_EXPLAINED.md
   - BACKTEST_GUIDE.md

2. **Search Freqtrade Docs:**
   - [freqtrade.io/en/stable](https://freqtrade.io/en/stable/)

3. **GitHub Issues:**
   - Check existing issues
   - Open new issue with logs and error details

4. **Freqtrade Discord:**
   - Join: [Freqtrade Discord](https://discord.gg/p7nuUNVfP7)
   - Ask in #help channel

---

## Before Asking for Help

Include this information:

1. **What you're trying to do**
2. **What happened instead**
3. **Error message** (exact text)
4. **Relevant logs** (last 20-50 lines)
5. **Your setup:**
   - Windows version
   - Python version
   - Freqtrade version
6. **Steps to reproduce**

**Good question:**
> "I'm trying to start the bot but get 'Invalid API keys'. I've checked my .env file and keys are correct. Here's the error from logs: [paste]. How do I fix this?"

**Bad question:**
> "Bot doesn't work help"

---

## Quick Fixes Checklist

When something goes wrong, try these first:

- [ ] Restart bot
- [ ] Restart dashboard
- [ ] Check .env file for typos
- [ ] Activate virtual environment
- [ ] Check internet connection
- [ ] Update dependencies: `pip install -r requirements.txt`
- [ ] Check Binance status: status.binance.com
- [ ] Look at logs
- [ ] Google the exact error message

**90% of issues are solved by one of these.**
