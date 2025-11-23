function ControlPanel({ status, onStart, onStop, onEmergencyStop }) {
    const getStatusBadge = () => {
        if (status === 'running') {
            return <span className="status-badge running">● Running</span>
        } else if (status === 'stopped') {
            return <span className="status-badge stopped">● Stopped</span>
        } else {
            return <span className="status-badge loading">● Loading...</span>
        }
    }

    return (
        <div className="card">
            <div className="card-header">
                <div className="flex-between">
                    <h2>Control Panel</h2>
                    {getStatusBadge()}
                </div>
            </div>

            <div className="flex gap-2" style={{ flexWrap: 'wrap' }}>
                <button
                    className="btn btn-success"
                    onClick={onStart}
                    disabled={status === 'running'}
                >
                    ▶ Start Bot
                </button>

                <button
                    className="btn btn-secondary"
                    onClick={onStop}
                    disabled={status === 'stopped'}
                >
                    ⏸ Stop Bot
                </button>

                <button
                    className="btn btn-danger"
                    onClick={onEmergencyStop}
                    disabled={status === 'stopped'}
                >
                    🚨 Emergency Stop
                </button>
            </div>

            <div className="mt-2" style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                <p>💡 <strong>Start Bot:</strong> Begin trading with ML strategy</p>
                <p>💡 <strong>Stop Bot:</strong> Stop taking new trades (keeps open positions)</p>
                <p>💡 <strong>Emergency Stop:</strong> Close ALL positions and stop bot</p>
            </div>
        </div>
    )
}

export default ControlPanel
