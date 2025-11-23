function TradingOverview({ balance, openTrades, onForceExit }) {
    const totalBalance = balance?.total || 0
    const freeBalance = balance?.free || 0
    const usedBalance = balance?.used || 0

    return (
        <div className="card">
            <div className="card-header">
                <h2>Trading Overview</h2>
            </div>

            {/* Balance Stats */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-label">Total Balance</div>
                    <div className="stat-value">${totalBalance.toFixed(2)}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Available</div>
                    <div className="stat-value">${freeBalance.toFixed(2)}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">In Trades</div>
                    <div className="stat-value">${usedBalance.toFixed(2)}</div>
                </div>
                <div className="stat-card">
                    <div className="stat-label">Open Trades</div>
                    <div className="stat-value">{openTrades.length}</div>
                </div>
            </div>

            {/* Open Trades Table */}
            {openTrades.length > 0 ? (
                <>
                    <h3 className="mt-3 mb-1">Open Positions</h3>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Pair</th>
                                <th>Entry Price</th>
                                <th>Current Price</th>
                                <th>P/L %</th>
                                <th>P/L $</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {openTrades.map((trade, index) => {
                                const profitPercent = trade.profit_pct || 0
                                const profitAbs = trade.profit_abs || 0
                                const isPositive = profitPercent > 0

                                return (
                                    <tr key={index} className={isPositive ? 'positive' : 'negative'}>
                                        <td><strong>{trade.pair}</strong></td>
                                        <td>${trade.open_rate?.toFixed(4) || 'N/A'}</td>
                                        <td>${trade.current_rate?.toFixed(4) || 'N/A'}</td>
                                        <td className={isPositive ? 'stat-value positive' : 'stat-value negative'}>
                                            {isPositive ? '+' : ''}{profitPercent.toFixed(2)}%
                                        </td>
                                        <td className={isPositive ? 'stat-value positive' : 'stat-value negative'}>
                                            {isPositive ? '+' : ''}${profitAbs.toFixed(2)}
                                        </td>
                                        <td>
                                            <button
                                                className="btn btn-danger"
                                                style={{ padding: '0.25rem 0.75rem', fontSize: '0.875rem' }}
                                                onClick={() => onForceExit(trade.trade_id)}
                                            >
                                                Exit
                                            </button>
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </>
            ) : (
                <div className="text-center mt-3" style={{ color: 'var(--text-secondary)' }}>
                    No open trades
                </div>
            )}
        </div>
    )
}

export default TradingOverview
