import { Line } from 'react-chartjs-2'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
)

function PerformanceMetrics({ performance, tradeHistory }) {
    const totalProfit = performance?.profit_closed_coin || 0
    const totalProfitPercent = performance?.profit_closed_percent || 0
    const winRate = performance?.winning_trades && performance?.losing_trades
        ? (performance.winning_trades / (performance.winning_trades + performance.losing_trades) * 100)
        : 0

    const bestTrade = performance?.best_pair || 'N/A'
    const worstTrade = performance?.worst_pair || 'N/A'
    const totalTrades = performance?.trade_count || 0

    // Prepare equity curve data
    const equityCurveData = {
        labels: tradeHistory.slice(0, 50).reverse().map((trade, i) => i + 1),
        datasets: [
            {
                label: 'Cumulative Profit (%)',
                data: tradeHistory.slice(0, 50).reverse().reduce((acc, trade) => {
                    const lastValue = acc.length > 0 ? acc[acc.length - 1] : 0
                    acc.push(lastValue + (trade.profit_pct || 0))
                    return acc
                }, []),
                borderColor: 'rgb(102, 126, 234)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true,
            }
        ]
    }

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)'
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.5)'
                }
            },
            y: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)'
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.5)',
                    callback: function (value) {
                        return value + '%'
                    }
                }
            }
        }
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2>Performance Metrics</h2>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-label">Total Profit</div>
                    <div className={`stat-value ${totalProfit >= 0 ? 'positive' : 'negative'}`}>
                        {totalProfit >= 0 ? '+' : ''}${totalProfit.toFixed(2)}
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Profit %</div>
                    <div className={`stat-value ${totalProfitPercent >= 0 ? 'positive' : 'negative'}`}>
                        {totalProfitPercent >= 0 ? '+' : ''}{totalProfitPercent.toFixed(2)}%
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Win Rate</div>
                    <div className="stat-value">{winRate.toFixed(1)}%</div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Total Trades</div>
                    <div className="stat-value">{totalTrades}</div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Best Pair</div>
                    <div className="stat-value" style={{ fontSize: '1.25rem' }}>{bestTrade}</div>
                </div>

                <div className="stat-card">
                    <div className="stat-label">Worst Pair</div>
                    <div className="stat-value" style={{ fontSize: '1.25rem' }}>{worstTrade}</div>
                </div>
            </div>

            {tradeHistory.length > 0 && (
                <>
                    <h3 className="mt-3 mb-1">Equity Curve</h3>
                    <div style={{ height: '250px', marginTop: 'var(--spacing-md)' }}>
                        <Line data={equityCurveData} options={chartOptions} />
                    </div>
                </>
            )}
        </div>
    )
}

export default PerformanceMetrics
