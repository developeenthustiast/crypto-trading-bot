#!/usr/bin/env python3
"""
Backtest Wrapper Script
=======================

Simplified interface for running backtests with the ML strategy.

Usage:
    python backtest.py --period 3m    # Last 3 months
    python backtest.py --period 6m    # Last 6 months
    python backtest.py --period 1y    # Last 1 year
"""

import subprocess
import sys
import argparse
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path


def get_freqtrade_dir():
    """Get the freqtrade setup directory"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    return project_root / 'freqtrade_setup'


def calculate_timerange(period):
    """Calculate timerange string from period"""
    end_date = datetime.now()
    
    if period == '3m':
        start_date = end_date - timedelta(days=90)
    elif period == '6m':
        start_date = end_date - timedelta(days=180)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    else:
        print(f"Unknown period: {period}")
        print("Valid periods: 3m, 6m, 1y")
        sys.exit(1)
    
    # Format: YYYYMMDD-YYYYMMDD
    return f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"


def run_backtest(freqtrade_dir, timerange):
    """Run the backtest"""
    print("\n" + "="*60)
    print("  Running Backtest")
    print("="*60)
    print(f"\nTimerange: {timerange}")
    print("Strategy: MLScalpingStrategy\n")
    
    # Build command
    cmd = [
        'freqtrade',
        'backtesting',
        '--strategy', 'MLScalpingStrategy',
        '--config', 'config.json',
        '--timerange', timerange,
        '--export', 'trades',
        '--breakdown', 'day',
    ]
    
    # Change to freqtrade directory
    import os
    original_dir = os.getcwd()
    os.chdir(freqtrade_dir)
    
    try:
        print("Running...")
        print("-"*60 + "\n")
        
        # Run backtest
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Print output
        for line in process.stdout:
            print(line, end='', flush=True)
        
        process.wait()
        
        if process.returncode == 0:
            print("\n" + "="*60)
            print("  Backtest Complete!")
            print("="*60)
            
            # Try to open HTML report
            reports_dir = freqtrade_dir / 'user_data' / 'backtest_results'
            if reports_dir.exists():
                html_files = sorted(reports_dir.glob('*.html'), key=lambda x: x.stat().st_mtime, reverse=True)
                if html_files:
                    latest_report = html_files[0]
                    print(f"\n📊 Opening backtest report: {latest_report.name}")
                    try:
                        webbrowser.open(str(latest_report))
                    except:
                        print(f"\n⚠ Could not auto-open browser. Please open manually:")
                        print(f"   {latest_report}")
            
            return True
        else:
            print("\n✗ Backtest failed!")
            return False
    
    finally:
        os.chdir(original_dir)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Run backtest on ML Scalping Strategy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backtest.py --period 3m    # Test last 3 months
  python backtest.py --period 6m    # Test last 6 months
  python backtest.py --period 1y    # Test last year
        """
    )
    parser.add_argument(
        '--period',
        choices=['3m', '6m', '1y'],
        default='3m',
        help='Period to backtest (default: 3m)'
    )
    
    args = parser.parse_args()
    
    # Get freqtrade directory
    freqtrade_dir = get_freqtrade_dir()
    if not freqtrade_dir.exists():
        print(f"✗ ERROR: {freqtrade_dir} not found!")
        sys.exit(1)
    
    # Check if strategy exists
    strategy_file = freqtrade_dir / 'user_data' / 'strategies' / 'MLScalpingStrategy.py'
    if not strategy_file.exists():
        print("✗ ERROR: MLScalpingStrategy.py not found!")
        print("  Please ensure the strategy file exists.")
        sys.exit(1)
    
    # Calculate timerange
    timerange = calculate_timerange(args.period)
    
    # Run backtest
    if not run_backtest(freqtrade_dir, timerange):
        print("\nFor help interpreting results, see: docs/BACKTEST_GUIDE.md")
        sys.exit(1)
    
    print("\nFor help interpreting results, see: docs/BACKTEST_GUIDE.md")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBacktest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
