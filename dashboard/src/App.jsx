import { useState, useEffect } from 'react'
import './index.css'
import ControlPanel from './components/ControlPanel'
import TradingOverview from './components/TradingOverview'
import PerformanceMetrics from './components/PerformanceMetrics'
import TradeLog from './components/TradeLog'
import LiveLogFeed from './components/LiveLogFeed'

const API_BASE_URL = '/api/v1'
const REFRESH_INTERVAL = 10000 // 10 seconds

function App() {
    const [botStatus, setBotStatus] = useState('loading')
    const [balance, setBalance] = useState(null)
    const [openTrades, setOpenTrades] = useState([])
    const [tradeHistory, setTradeHistory] = useState([])
    const [performance, setPerformance] = useState(null)
    const [logs, setLogs] = useState([])
    const [error, setError] = useState(null)
    const [lastUpdate, setLastUpdate] = useState(null)

    // Fetch bot status
    const fetchStatus = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/status`)
            if (!response.ok) throw new Error('Failed to fetch status')
            const data = await response.json()
            setBotStatus(data.state || 'stopped')
            setError(null)
        } catch (err) {
            setError('Cannot connect to bot. Make sure Freqtrade is running.')
            setBotStatus('error')
        }
    }

    // Fetch balance
    const fetchBalance = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/balance`)
            if (!response.ok) throw new Error('Failed to fetch balance')
            const data = await response.json()
            setBalance(data)
        } catch (err) {
            console.error('Balance fetch error:', err)
        }
    }

    // Fetch open trades
    const fetchOpenTrades = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/status`)
            if (!response.ok) throw new Error('Failed to fetch trades')
            const data = await response.json()
            setOpenTrades(data.open_trades || [])
        } catch (err) {
            console.error('Open trades fetch error:', err)
        }
    }

    // Fetch trade history
    const fetchTradeHistory = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/trades?limit=50`)
            if (!response.ok) throw new Error('Failed to fetch trade history')
            const data = await response.json()
            setTradeHistory(data.trades || [])
        } catch (err) {
            console.error('Trade history fetch error:', err)
        }
    }

    // Fetch performance metrics
    const fetchPerformance = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/profit`)
            if (!response.ok) throw new Error('Failed to fetch performance')
            const data = await response.json()
            setPerformance(data)
        } catch (err) {
            console.error('Performance fetch error:', err)
        }
    }

    // Fetch logs
    const fetchLogs = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/logs?limit=50`)
            if (!response.ok) throw new Error('Failed to fetch logs')
            const data = await response.json()
            setLogs(data.log || [])
        } catch (err) {
            console.error('Logs fetch error:', err)
        }
    }

    // Fetch all data
    const fetchAllData = async () => {
        await Promise.all([
            fetchStatus(),
            fetchBalance(),
            fetchOpenTrades(),
            fetchTradeHistory(),
            fetchPerformance(),
            fetchLogs()
        ])
        setLastUpdate(new Date())
    }

    // Initial fetch
    useEffect(() => {
        fetchAllData()

        // Set up polling
        const interval = setInterval(fetchAllData, REFRESH_INTERVAL)

        return () => clearInterval(interval)
    }, [])

    // Control actions
    const handleStart = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/start`, { method: 'POST' })
            if (!response.ok) throw new Error('Failed to start bot')
            await fetchStatus()
        } catch (err) {
            alert('Failed to start bot: ' + err.message)
        }
    }

    const handleStop = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stop`, { method: 'POST' })
            if (!response.ok) throw new Error('Failed to stop bot')
            await fetchStatus()
        } catch (err) {
            alert('Failed to stop bot: ' + err.message)
        }
    }

    const handleForceExit = async (tradeId) => {
        if (!confirm('Are you sure you want to force exit this trade?')) return

        try {
            const response = await fetch(`${API_BASE_URL}/forceexit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tradeid: tradeId })
            })
            if (!response.ok) throw new Error('Failed to force exit')
            await fetchAllData()
        } catch (err) {
            alert('Failed to force exit: ' + err.message)
        }
    }

    const handleEmergencyStop = async () => {
        if (!confirm('⚠️ EMERGENCY STOP: This will close all open positions. Are you sure?')) return

        try {
            // Stop the bot first
            await handleStop()

            // Force exit all open trades
            for (const trade of openTrades) {
                await handleForceExit(trade.trade_id)
            }

            alert('Emergency stop completed. All positions closed.')
        } catch (err) {
            alert('Emergency stop failed: ' + err.message)
        }
    }

    return (
        <div className="app">
            <header className="app-header">
                <h1>🤖 Crypto Trading Bot</h1>
                <p>ML-Powered Autonomous Trading System</p>
                {lastUpdate && (
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                        Last updated: {lastUpdate.toLocaleTimeString()}
                    </p>
                )}
            </header>

            {error && (
                <div className="error-message">
                    <strong>Connection Error:</strong> {error}
                    <br />
                    <small>Make sure Freqtrade is running with: freqtrade trade --config config.json</small>
                </div>
            )}

            <div className="dashboard-grid">
                <ControlPanel
                    status={botStatus}
                    onStart={handleStart}
                    onStop={handleStop}
                    onEmergencyStop={handleEmergencyStop}
                />

                <TradingOverview
                    balance={balance}
                    openTrades={openTrades}
                    onForceExit={handleForceExit}
                />

                <PerformanceMetrics
                    performance={performance}
                    tradeHistory={tradeHistory}
                />

                <TradeLog trades={tradeHistory} />

                <LiveLogFeed logs={logs} />
            </div>
        </div>
    )
}

export default App
