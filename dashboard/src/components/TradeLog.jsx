import { useState } from 'react'

function TradeLog({ trades }) {
    const [filter, setFilter] = useState('all') // all, wins, losses

    const filteredTrades = trades.filter(trade => {
        if (filter === 'wins') return trade.profit_pct > 0
        if (filter === 'losses') return trade.profit_pct < 0
        return true
    })

    const formatDate = (timestamp) => {
        if (!timestamp) return 'N/A'
        const date = new Date(timestamp)
        return date.toLocaleString()
    }

    return (
        <div className="card">
            <div className="card-header">
                <div className="flex-between">
                    <h2>Trade Log</h2>
                    <div className="flex gap-1">
                        <button
                            className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                            style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
                            onClick={() => setFilter('all')}
                        >
                            All
                        </button>
                        <button
                            className={`btn ${filter === 'wins' ? 'btn-success' : 'btn-secondary'}`}
                            style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
                            onClick={() => setFilter('wins')}
                        >
                            Wins
                        </button>
                        <button
                            className={`btn ${filter === 'losses' ? 'btn-danger' : 'btn-secondary'}`}
                            style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
                            onClick={() => setFilter('losses')}
                        >
                            Losses
                        </button>
                    </div>
                </div>
            </div>

            {filteredTrades.length > 0 ? (
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Pair</th>
                            <th>Side</th>
                            <th>Entry</th>
                            <th>Exit</th>
                            <th>P/L %</th>
                            <th>P/L $</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredTrades.map((trade, index) => {
                            const isPositive = trade.profit_pct > 0
                            return (
                                <tr key={index} className={isPositive ? 'positive' : 'negative'}>
                                    <td>{formatDate(trade.close_timestamp || trade.open_timestamp)}</td>
                                    <td><strong>{trade.pair}</strong></td>
                                    <td>{trade.is_short ? 'SHORT' : 'LONG'}</td>
                                    <td>${trade.open_rate?.toFixed(4) || 'N/A'}</td>
                                    <td>${trade.close_rate?.toFixed(4) || 'N/A'}</td>
                                    <td className={isPositive ? 'stat-value positive' : 'stat-value negative'}>
                                        {isPositive ? '+' : ''}{trade.profit_pct?.toFixed(2) || 0}%
                                    </td>
                                    <td className={isPositive ? 'stat-value positive' : 'stat-value negative'}>
                                        {isPositive ? '+' : ''}${trade.profit_abs?.toFixed(2) || 0}
                                    </td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            ) : (
                <div className="text-center mt-2" style={{ color: 'var(--text-secondary)' }}>
                    {filter === 'all' ? 'No trades yet' : `No ${filter} found`}
                </div>
            )}
        </div>
    )
}

export default TradeLog
