# ⚠️ SAFETY CHECKLIST - Before Going Live

**READ THIS ENTIRE DOCUMENT BEFORE EVEN THINKING ABOUT USING REAL MONEY**

---

## Critical Disclaimers

### Legal and Financial Warnings

⚠️ **CRYPTOCURRENCY TRADING CARRIES EXTREME RISK OF LOSS**
- You can lose 100% of your investment
- Past performance does NOT guarantee future results
- Automated trading can malfunction
- Market conditions change rapidly

⚠️ **THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY**
- Not financial advice
- Not a guaranteed profit system
- No warranty or guarantees provided
- Use at your own risk

⚠️ **LEGAL CONSIDERATIONS**
- Check your local laws regarding crypto trading
- Check laws regarding automated trading
- You are responsible for tax reporting
- Some jurisdictions prohibit or restrict crypto trading

⚠️ **BINANCE TERMS OF SERVICE**
- You must comply with Binance's terms
- Automated trading may have restrictions
- You are responsible for your account security
- Use API keys with appropriate permissions only

---

## Minimum Testing Requirements

### DO NOT use real money until you have:

#### 1. Testnet Verification (2-4 weeks minimum)

Run on Binance Testnet for **at least 2-4 weeks** and verify:

- [ ] Bot runs without crashes for 7+ consecutive days
- [ ] ML model makes logical trade entries
- [ ] Stop-losses trigger correctly
- [ ] Daily loss limit (10%) triggers correctly
- [ ] Dashboard and notifications work reliably
- [ ] You understand why each trade was made
- [ ] Win rate is above 50%
- [ ] Overall profit is positive (after fees)

#### 2. Backtest on Multiple Periods

Run backtests on different time periods:

- [ ] Last 3 months
- [ ] Last 6 months
- [ ] Last 1 year
- [ ] Bear market period (when prices dropped)
- [ ] Bull market period (when prices rose)
- [ ] Sideways market period (choppy, no clear trend)

**All periods should show:**
- Win rate > 52%
- Positive total profit
- Maximum drawdown < 20%
- No period with >50% loss

#### 3. Strategy Understanding

You MUST be able to answer these questions:

- [ ] What indicators does the ML model use?
- [ ] What is the confidence threshold and why?
- [ ] When does the stop-loss trigger?
- [ ] What is the maximum loss per trade?
- [ ] What is the maximum daily loss?
- [ ] How does dynamic pair selection work?
- [ ] When should you retrain the model?
- [ ] What is overfitting and how to detect it?

**If you can't answer these, read `STRATEGY_EXPLAINED.md` again.**

---

## Performance Benchmarks

### Before considering real money, Testnet performance should meet:

#### Minimum Requirements:
- ✅ Win rate: > 55%
- ✅ Total profit: > +5% after 2 weeks
- ✅ Maximum drawdown: < 15%
- ✅ Profit factor: > 1.2 (gross profit / gross loss)
- ✅ Average trade: > 0.5% profit
- ✅ No single day loss > 10%

#### Red Flags (DO NOT go live if you see):
- ❌ Win rate < 50%
- ❌ Negative total profit
- ❌ Any single day loss > 15%
- ❌ Frequent stop-loss triggers (>70% of trades)
- ❌ Very few trades (<10 in 2 weeks)
- ❌ Only profitable in one market condition

---

## Risk Management (If You Proceed)

### Start with Minimum Real Money

**Recommended first real-money test:**
- Start with < 1% of your total crypto portfolio
- Example: If you have $10,000 in crypto, start with $100
- Treat this as "tuition" (you might lose it)

### Position Sizing

**Default config (5% per trade) is AGGRESSIVE for real money.**

Before going live, consider changing in `config.json`:

```json
"tradable_balance_ratio": 0.02,  // 2% per trade instead of 5%
"max_open_trades": 2,  // Max 2 trades instead of 3
```

This reduces risk but also reduces potential profit.

### Daily Monitoring (First Month)

Check the dashboard **at least twice daily**:
- [ ] Morning: Check overnight performance
- [ ] Evening: Review day's trades
- [ ] Look for unusual behavior
- [ ] Verify stop-losses are working
- [ ] Check for API errors

**Set up Telegram notifications** - you'll get alerts immediately.

---

## Security Checklist

### API Key Safety

- [ ] Use API keys with **SPOT trading only** (no futures)
- [ ] Enable **IP whitelist** on Binance (lock to your IP)
- [ ] **Disable withdrawals** on API key permissions
- [ ] Store API keys in `.env` file (never commit to git)
- [ ] Never share API keys with anyone
- [ ] Regenerate keys if you suspect compromise

### Computer Security

- [ ] Use antivirus / Windows Defender
- [ ] Keep Windows updated
- [ ] Don't run bot on public / shared computers
- [ ] Use strong password for your Binance account
- [ ] Enable 2FA (two-factor authentication) on Binance
- [ ] Backup your `.env` file somewhere safe (encrypted)

---

## Switching from Testnet to Live Trading

### Configuration Changes Required

**1. Update `.env` with REAL Binance API keys:**

```env
# Replace testnet keys with REAL Binance keys
BINANCE_API_KEY=your_REAL_binance_api_key
BINANCE_API_SECRET=your_REAL_binance_secret
```

**2. Update `config.json` exchange URLs:**

Change this:
```json
"urls": {
  "api": {
    "public": "https://testnet.binance.vision/api",
    "private": "https://testnet.binance.vision/api"
  }
}
```

To this:
```json
"urls": {
  "api": {
    "public": "https://api.binance.com",
    "private": "https://api.binance.com"
  }
}
```

**3. Set dry_run to false (DANGEROUS):**

```json
"dry_run": false,  // REAL TRADES NOW
"dry_run_wallet": 1000,  // Ignored when dry_run = false
```

### Confirmation Steps

After making changes:

1. **Double-check config.json**
   - API endpoints are live Binance
   - `dry_run: false`
   
2. **Test with tiny amount first**
   - Set `"max_open_trades": 1`
   - Set `"tradable_balance_ratio": 0.01`
   - Let it make 1-2 trades
   
3. **Verify trades appear in Binance**
   - Check Binance app/website
   - Trade should show in "Spot Trading" history
   
4. **If successful, gradually increase**
   - Don't jump to full settings
   - Increase over days/weeks

---

## Red Flags to Stop Immediately

Stop the bot and investigate if:

1. **Performance Issues:**
   - Win rate drops below 40%
   - 3+ consecutive losing days
   - Daily loss exceeds 10%
   - Unusual trading frequency (100+ trades/day or 0 trades/week)

2. **Technical Issues:**
   - API errors in logs
   - Dashboard shows incorrect data
   - Trades not executing properly
   - Stop-losses not triggering

3. **Your Emotional State:**
   - You're checking dashboard every 5 minutes
   - You're losing sleep over it
   - You're afraid to stop it (fear of missing out)
   - You're ignoring warning signs

**If you're emotionally affected, it's too much money at risk.**

---

## What Can Go Wrong

### Realistic Scenarios:

1. **Market Conditions Change**
   - ML model trained on bull market, then bear market hits
   - Solution: Retrain frequently, monitor performance

2. **API Outage**
   - Binance API goes down mid-trade
   - Solution: Bot should reconnect. Check logs. Manual intervention may be needed.

3. **Flash Crash**
   - Sudden 20% drop in seconds
   - Solution: Stop-loss triggers (5%). You lose 5% on that trade.

4. **Model Overfitting**
   - Backtest shows 70% win rate, live shows 40%
   - Solution: More diverse training data, retrain, lower stakes

5. **Bug in Strategy**
   - Code has an edge case that causes bad trades
   - Solution: Test thoroughly first. Report bugs on GitHub.

---

## Psychology of Automated Trading

### Common Mistakes:

1. **Over-Optimizing**
   - Tweaking settings after every loss
   - Solution: Let it run for 2+ weeks before judging

2. **Revenge Trading**
   - Manually forcing trades after losses
   - Solution: Trust the system or stop using it

3. **Greed**
   - Increasing position size after wins
   - Solution: Stick to original plan

4. **Fear**
   - Stopping bot during drawdown (when it might recover)
   - Solution: Set rules beforehand. Stop at -X%, not emotionally.

### Healthy Mindset:

- ✅ "This is a probability game, not certainty"
- ✅ "I will have losing days/weeks"
- ✅ "I only risk what I can lose"
- ✅ "I evaluate performance over weeks, not days"

---

## Final Decision Checklist

Before enabling real trading, **check every box**:

### Testing:
- [ ] Ran on Testnet for 2-4 weeks minimum
- [ ] Backtested on 3+ different market periods
- [ ] Win rate consistently > 55%
- [ ] Overall profitable on Testnet
- [ ] Understand every component of the strategy

### Risk Management:
- [ ] Starting with < 1% of portfolio
- [ ] Position size is 2% or less per trade
- [ ] Stop-loss is 5% or less
- [ ] Daily loss limit enabled
- [ ] Comfortable losing entire test amount

### Technical:
- [ ] API keys have correct permissions (trading only, no withdrawal)
- [ ] IP whitelist enabled on Binance
- [ ] 2FA enabled on Binance account
- [ ] Telegram notifications working
- [ ] No errors in logs

### Psychological:
- [ ] Not using borrowed money
- [ ] Won't panic if I lose 10%
- [ ] Will check performance weekly, not hourly
- [ ] Have a plan to stop if X happens
- [ ] Family/commitments won't be affected by potential loss

### Legal:
- [ ] Checked local laws on crypto trading
- [ ] Understand tax implications
- [ ] Agree to take full responsibility

---

## If You Can't Check All Boxes

**STOP.** You're not ready.

Either:
- Continue testing on Testnet
- Learn more about the strategy
- Reduce risk further
- Or don't trade with real money at all

**There's no rush. Markets will still be there next month.**

---

## Resources for Responsible Trading

- [Investopedia - Crypto Trading](https://www.investopedia.com/cryptocurrency-trading-guide)
- [Binance Academy](https://academy.binance.com/)
- [Risk Management Guide](https://www.investopedia.com/articles/trading/09/risk-management.asp)

---

## Summary

**The safest path:**

1. Test on Testnet for 1+ month
2. Verify positive, consistent performance
3. Start with $50-100 real money (amount you can lose)
4. Run for 2 weeks
5. If successful, cautiously increase
6. Never risk more than you can afford to lose
7. Stop immediately if red flags appear

**Remember:**
- This is experimental software
- You are the beta tester for your own money
- No one can predict market movements
- Losses are always possible

**If in doubt, DON'T.**

---

**By proceeding to real trading, you acknowledge you've read and understood this entire document and accept all risks.**
