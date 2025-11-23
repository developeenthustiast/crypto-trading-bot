# Freqtrade Bot Dashboard

A modern, responsive web dashboard for monitoring your Freqtrade trading bot.

## Features

- 📊 Real-time trading overview
- 📈 Performance metrics with equity curve  
- 🎮 Bot control (start/stop/emergency exit)
- 📜 Trade history log with filters
- 📡 Live log feed
- 📱 Mobile-responsive design
- 🌙 Dark theme

## Quick Start

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Dashboard will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Output in `dist/` folder.

## Configuration

The dashboard connects to Freqtrade REST API.

**API endpoint:** Configured in `vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8080',  // Freqtrade API
    changeOrigin: true,
  }
}
```

**For cloud deployment:** Update target to your deployed Freqtrade URL.

## Components

- **ControlPanel**: Start/stop bot, emergency stop
- **TradingOverview**: Balance and open positions
- **PerformanceMetrics**: Profit stats and equity curve
- **TradeLog**: Historical trades with filtering
- **LiveLogFeed**: Real-time bot activity logs

## Requirements

- Node.js 18+
- Freqtrade with REST API enabled

## Troubleshooting

**Dashboard won't connect:**
- Ensure Freqtrade is running with `--config config.json`
- Check API is enabled in config.json
- Verify API endpoint in vite.config.js

**Build errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## License

MIT
