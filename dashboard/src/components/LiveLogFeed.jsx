import { useEffect, useRef } from 'react'

function LiveLogFeed({ logs }) {
    const logFeedRef = useRef(null)

    // Auto-scroll to bottom when new logs arrive
    useEffect(() => {
        if (logFeedRef.current) {
            logFeedRef.current.scrollTop = logFeedRef.current.scrollHeight
        }
    }, [logs])

    const formatTimestamp = (timestamp) => {
        if (!timestamp) return new Date().toLocaleTimeString()
        return new Date(timestamp).toLocaleTimeString()
    }

    const getLogClass = (message) => {
        const msg = message.toLowerCase()
        if (msg.includes('error') || msg.includes('failed')) return 'error'
        if (msg.includes('success') || msg.includes('bought') || msg.includes('sold')) return 'success'
        return 'info'
    }

    return (
        <div className="card">
            <div className="card-header">
                <h2>Live Log Feed</h2>
            </div>

            <div className="log-feed" ref={logFeedRef}>
                {logs.length > 0 ? (
                    logs.slice(-100).reverse().map((log, index) => (
                        <div key={index} className={`log-entry ${getLogClass(log)}`}>
                            <span className="log-timestamp">[{formatTimestamp()}]</span>
                            <span>{log}</span>
                        </div>
                    ))
                ) : (
                    <div className="text-center" style={{ color: 'var(--text-secondary)' }}>
                        No logs available
                    </div>
                )}
            </div>

            <div className="mt-1" style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                ✓ Auto-refreshes every 10 seconds
            </div>
        </div>
    )
}

export default LiveLogFeed
