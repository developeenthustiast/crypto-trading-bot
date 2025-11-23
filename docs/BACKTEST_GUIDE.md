# Backtest Guide - Understanding Results

Learn how to interpret backtest results and know if your strategy is good.

## What is Backtesting?

**Backtesting** = Running your strategy on historical price data to see how it would have performed.

**Example:**
- Test strategy on Bitcoin prices from January-March 2024
- See: Would it have made money? What was win rate?

**Important:** Backtest results ≠ future performance, but they give you an idea.

---

## Running a Backtest

```bash
# Test last 3 months
python scripts/backtest.py --period 3m

# Test last 6 months
python scripts/backtest.py --period 6m

# Test last 1 year
python scripts/backtest.py --period 1y
```

Results open automatically in your browser as an HTML report.

---

## Key Metrics Explained

### 1. Total Profit / Loss

**What it is:** Total money made or lost

**Example:**
- Started with: $1,000
- Ended with: $1,150
- **Total Profit: $150** (or +15%)

**Good performance (scalping):**
- 3 months: +5% to +15%
- 6 months: +10% to +25%
- 1 year: +20% to +50%

**Red flags:**
- Negative (losing money)
- >100% in short period (likely overfitting)

### 2. Win Rate

**What it is:** Percentage of trades that were profitable

**Formula:** (Winning trades / Total trades) × 100

**Example:**
- 60 winning trades out of 100 total
- **Win rate: 60%**

**Good performance:**
- 55-65%: Excellent
- 50-55%: Good
- 45-50%: Acceptable (if average wins > average losses)
- <45%: Poor

**Note:** You can be profitable with 40% win rate if your winners are bigger than losers!

### 3. Maximum Drawdown

**What it is:** Largest peak-to-valley decline

**Example:**
- Account at $1,200 (peak)
- Drops to $1,000 (valley)
- **Max Drawdown: -16.7%**

**Good performance:**
- <10%: Excellent
- 10-20%: Good
- 20-30%: Acceptable
- >30%: High risk

**Why it matters:** Shows worst-case scenario you must stomach.

### 4. Sharpe Ratio

**What it is:** Risk-adjusted return (reward per unit of risk)

**Simple explanation:**
- High Sharpe = Good returns with low volatility
- Low Sharpe = Risky, inconsistent returns

**Good performance:**
- >2.0: Excellent
- 1.0-2.0: Good
- 0.5-1.0: Acceptable
- <0.5: Poor

**Example:**
- Strategy A: +20% profit, Sharpe 0.5 (very volatile)
- Strategy B: +15% profit, Sharpe 2.0 (smooth, consistent)
- **Strategy B is better** (less stressful)

### 5. Profit Factor

**What it is:** Gross profit divided by gross loss

**Formula:** Total $ won / Total $ lost

**Example:**
- Made $500 on winning trades
- Lost $250 on losing trades
- **Profit Factor: 2.0**

**Good performance:**
- >2.0: Excellent
- 1.5-2.0: Good
- 1.2-1.5: Acceptable
- <1.2: Poor
- <1.0: Losing money

### 6. Average Trade Profit

**What it is:** Average profit/loss per trade

**Example:**
- 100 trades total
- Net profit: $200
- **Avg trade profit: $2**

**Why it matters:**
- Must be > trading fees (usually 0.2% = $0.20 per $100 trade)
- Scalping needs many small wins

**Good performance:**
- >1% per trade: Excellent (for scalping)
- 0.5-1%: Good
- 0.2-0.5%: Acceptable
- <0.2%: May not cover fees

### 7. Trade Frequency

**What it is:** Number of trades per day/week

**Example:**
- 300 trades in 90 days
- **Trade frequency: ~3.3 trades/day**

**For scalping:**
- 2-5 trades/day: Good
- 5-10 trades/day: Active
- >10 trades/day: Very active (watch fees!)
- <1 trade/day: Not really scalping

**Red flags:**
- 0 trades: Strategy too conservative or broken
- >20 trades/day: Overtrading, high fees

---

## Reading the HTML Report

### Section 1: Summary

**Look for:**
- ✅ Total profit (positive)
- ✅ Win rate (>52%)
- ✅ Sharpe ratio (>1.0)
- ✅ Max drawdown (<20%)

### Section 2: Trade Log

Shows every individual trade:
- Entry/exit timestamps
- Pair traded
- Profit/loss
- Duration

**Check:**
- Are trades reasonable? (not random)
- Are trade durations expected? (scalping = minutes to hours)
- Are there clusters of losses? (red flag)

### Section 3: Equity Curve (Chart)

**Y-axis:** Your account balance over time  
**X-axis:** Time

**Good curve:**
- Slopes upward (making money)
- Smooth (consistent)
- Small dips (controlled losses)

**Bad curve:**
- Flat or downward (losing money)
- Huge spikes (lucky streaks = overfitting)
- Sharp drops (large drawdowns)

### Section 4: Pair Performance

Shows which pairs were most profitable:

**Example:**
- BTC/USDT: +$50 (10 trades)
- ETH/USDT: -$20 (5 trades)

**Use this to:**
- See which pairs work best
- Blacklist consistently losing pairs

---

## What's "Good" Performance for Scalping?

### Realistic Benchmarks

**3-Month Backtest:**
- Win rate: 55-62%
- Total profit: +8-15%
- Max drawdown: <12%
- Sharpe ratio: 1.2-2.5
- Trades: 150-300

**6-Month Backtest:**
- Win rate: 53-60%
- Total profit: +15-30%
- Max drawdown: <15%
- Sharpe ratio: 1.0-2.0
- Trades: 300-600

**1-Year Backtest:**
- Win rate: 52-58%
- Total profit: +25-60%
- Max drawdown: <18%
- Sharpe ratio: 0.9-1.8
- Trades: 600-1200

**Note:** Lower expectations than you might think! Consistent 2-3% monthly is excellent.

---

## Red Flags (Don't Trust These Results)

### 🚩 Too Good to Be True

- Win rate >75%
- Total profit >100% in 3 months
- Max drawdown <2%
- Every pair profitable

**Likely cause:** Overfitting (strategy memorized past data)

**What to do:**
- Test on different time periods
- Check for lookahead bias (strategy peeking at future data)
- Retrain model with more data

### 🚩 Not Enough Trades

- <50 trades in 3 months
- Long periods with no trades

**Problem:** Not enough data to judge performance (luck factor too high)

**What to do:**
- Lower ML confidence threshold
- Add more pairs to whitelist
- Check strategy logic

### 🚩 Inconsistent Across Periods

- Great in bull market, terrible in bear market
- Profitable Jan-Mar, losing Apr-Jun

**Problem:** Strategy only works in specific conditions

**What to do:**
- Train on more diverse data
- Add protections for different market conditions
- Accept: some strategies are trend-dependent

### 🚩 High Frequency with Low Profit

- 500+ trades in 3 months
- Total profit <5%

**Problem:** Trading fees are eating profits

**What to do:**
- Increase minimum profit target
- Reduce trade frequency
- Check if fees are included in backtest

---

## Comparing Strategies

### Example Comparison:

| Metric | Strategy A | Strategy B |
|--------|-----------|-----------|
| Total Profit | +25% | +18% |
| Win Rate | 48% | 60% |
| Max Drawdown | -22% | -12% |
| Sharpe Ratio | 0.8 | 1.6 |
| Trades | 450 | 280 |

**Which is better?**

**Strategy B is better because:**
- Lower drawdown (less stressful)
- Higher Sharpe (better risk-adjusted returns)
- Higher win rate (more consistent)

**Even though A has higher profit, B is more sustainable.**

---

## Backtest vs. Live Trading

### Why backtest results differ from live:

1. **Slippage:** Prices move between signal and execution
2. **Fees:** May not be perfectly simulated
3. **Market conditions:** Past ≠ future
4. **Overfitting:** Model trained on past data
5. **API delays:** Real-world latency

**Expect live performance to be 20-40% worse than backtest.**

**Example:**
- Backtest: +20% in 3 months
- Live: +12-16% (realistic)

---

## Action Plan After Backtesting

### If Results Are Good (meet benchmarks above):

1. ✅ Test on different time periods
2. ✅ Run on both bull and bear markets
3. ✅ Start on Testnet for 2-4 weeks
4. ✅ Compare Testnet results to backtest
5. ✅ Only then consider small real money

### If Results Are Poor:

1. ❌ DON'T trade with real money
2. 🔧 Retrain ML model
3. 🔧 Adjust hyperparameters
4. 🔧 Try different pairs
5. 🔧 Check for bugs in strategy
6. 📚 Study more about strategy optimization

### If Results Are Suspiciously Good:

1. ⚠️ Assume overfitting
2. 🔬 Test on completely different period
3. 🔬 Check for lookahead bias
4. 🔬 Reduce model complexity
5. 🔬 Be skeptical, proceed cautiously

---

## Summary

**Good backtest:**
- Positive profit (not too high)
- Win rate 52-65%
- Low drawdown (<20%)
- Consistent across different periods
- Trade frequency reasonable (2-5/day for scalping)

**Red flags:**
- >75% win rate or >100% profit (overfitting)
- Negative profit or <45% win rate (bad strategy)
- Huge drawdowns (>30%)
- Works in one period, fails in another

**Remember:**
- Backtest = Past performance
- Live = Future performance (will differ!)
- Use backtest to filter out bad strategies
- Don't trust backtest blindly
- Always test on Testnet before real money

---

**Next step:** If backtest looks good, run on Testnet and compare results!
