# Deploying to Railway

Deploy your crypto trading bot to Railway's free tier.

## Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Bot code pushed to GitHub repository

## Step 1: Connect GitHub

1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub
3. Authorize Railway to access your repositories

## Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `crypto-trading-bot` repository
4. Railway will detect it as a Python project

## Step 3: Configure Environment Variables

In Railway dashboard, add these variables:

```
BINANCE_API_KEY=your_testnet_or_live_key
BINANCE_API_SECRET=your_secret
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
FREQTRADE_API_USERNAME=admin
FREQTRADE_API_PASSWORD=your_secure_password
```

⚠️ **For Testnet:** Use testnet keys  
⚠️ **For Live:** Use real Binance keys (BE CAREFUL)

## Step 4: Configure Start Command

Railway needs to know how to start your bot.

Create `Procfile` in project root:
```
web: cd freqtrade_setup && freqtrade trade --config config.json
```

## Step 5: Deploy

1. Railway will auto-deploy on code push
2. Monitor deployment logs
3. Once deployed, bot will start automatically

## Step 6: Access Dashboard

Railway provides a public URL. To access dashboard:

1. Deploy dashboard separately OR
2. Serve dashboard from bot (requires additional setup)

**Recommended:** Run dashboard locally, connect to Railway bot API

## Free Tier Limits

- **500 execution hours per month**
- **1 GB RAM**
- **1 GB disk storage**
- No credit card required (but recommended for more hours)

## Keeping Bot Alive

Free tier doesn't sleep (unlike Render), but you get 500 hours/month.

**Math:** 500 hours = ~20 days of 24/7 operation

**Solutions:**
- Monitor hours usage
- Pause during low-activity periods
- Upgrade to $5/month for unlimited

## Monitoring

**View logs:**
1. Go to Railway project dashboard
2. Click on deployment
3. Click "View Logs"

**Restart bot:**
- Push new commit, or
- Use Railway dashboard "Restart" button

## Updating API Keys

1. Go to Railway project → Variables
2. Update the variable
3. Restart service

## Troubleshooting

**"Application failed to respond"**
- Check logs for errors
- Verify API keys are correct
- Ensure config.json is valid

**High memory usage**
- Reduce number of monitored pairs
- Lower training frequency

**Connection timeout**
- Railway may be restarting
- Check service status

## Cost Estimation

**Free tier:**
- $0 for first 500 hours (~20 days/month)

**Paid tier ($5/month):**
- Unlimited hours
- Better performance
- Priority support

## Security

- Never commit API keys
- Use environment variables only
- Enable IP whitelist on Binance (if possible with Railway IP)

---

For more help: [Railway Documentation](https://docs.railway.app/)
