#!/usr/bin/env python3
"""
Historical Data Downloader for Crypto Trading Bot
==================================================

This script downloads historical price data for cryptocurrency pairs
to train the ML model and run backtests.

Downloads:
- 1 year of 1-minute, 5-minute, and 15-minute candle data
- Top 50 trading pairs by volume on Binance
- Stores data in freqtrade_setup/user_data/data/binance/

Estimated time: 15-20 minutes
"""

import subprocess
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


# Configuration
TIMEFRAMES = ['1m', '5m', '15m']
DAYS_TO_DOWNLOAD = 365  # 1 year
EXCHANGE = 'binance'

# Top 50 pairs by volume (common trading pairs)
PAIRS = [
    'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT',
    'DOGE/USDT', 'SOL/USDT', 'MATIC/USDT', 'DOT/USDT', 'LTC/USDT',
    'SHIB/USDT', 'TRX/USDT', 'AVAX/USDT', 'ATOM/USDT', 'UNI/USDT',
    'LINK/USDT', 'ETC/USDT', 'XLM/USDT', 'ALGO/USDT', 'FIL/USDT',
    'VET/USDT', 'ICP/USDT', 'NEAR/USDT', 'HBAR/USDT', 'AAVE/USDT',
    'GRT/USDT', 'FTM/USDT', 'SAND/USDT', 'MANA/USDT', 'AXS/USDT',
    'THETA/USDT', 'XTZ/USDT', 'EGLD/USDT', 'RUNE/USDT', 'GALA/USDT',
    'APE/USDT', 'CHZ/USDT', 'ZEC/USDT', 'ENJ/USDT', 'ROSE/USDT',
    'LRC/USDT', 'IMX/USDT', 'CRV/USDT', 'OP/USDT', 'ARB/USDT',
    'SUI/USDT', 'SEI/USDT', 'INJ/USDT', 'PEPE/USDT', 'WLD/USDT'
]


def print_header():
    """Print script header"""
    print("\n" + "="*60)
    print("  Historical Data Downloader")
    print("="*60)
    print(f"\nThis will download {DAYS_TO_DOWNLOAD} days of data for {len(PAIRS)} pairs")
    print(f"Timeframes: {', '.join(TIMEFRAMES)}")
    print(f"Estimated time: 15-20 minutes")
    print(f"Estimated size: ~500-800 MB")
    print("\n" + "="*60 + "\n")


def check_freqtrade():
    """Check if freqtrade is installed"""
    try:
        result = subprocess.run(
            ['freqtrade', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ Freqtrade found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ERROR: Freqtrade not found!")
        print("  Please run scripts/install_windows.bat first")
        return False


def get_freqtrade_dir():
    """Get the freqtrade setup directory"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    freqtrade_dir = project_root / 'freqtrade_setup'
    
    if not freqtrade_dir.exists():
        print(f"✗ ERROR: {freqtrade_dir} not found!")
        return None
    
    return freqtrade_dir


def download_data(freqtrade_dir, pairs, timeframes, days):
    """Download historical data using freqtrade"""
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    print(f"Downloading data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print()
    
    total_downloads = len(pairs) * len(timeframes)
    current = 0
    failed = []
    
    for timeframe in timeframes:
        print(f"\n{'='*60}")
        print(f"  Downloading {timeframe} data...")
        print(f"{'='*60}\n")
        
        for pair in pairs:
            current += 1
            progress = f"[{current}/{total_downloads}]"
            
            # Format pair for filename (replace / with _)
            pair_filename = pair.replace('/', '_')
            
            print(f"{progress} Downloading {pair} ({timeframe})...", end=' ', flush=True)
            
            try:
                # Build freqtrade command
                cmd = [
                    'freqtrade',
                    'download-data',
                    '--exchange', EXCHANGE,
                    '--pairs', pair,
                    '--timeframe', timeframe,
                    '--days', str(days),
                    '--datadir', str(freqtrade_dir / 'user_data' / 'data'),
                    '--config', str(freqtrade_dir / 'config.json')
                ]
                
                # Run command
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per pair
                )
                
                if result.returncode == 0:
                    print("✓")
                else:
                    print("✗ Failed")
                    failed.append(f"{pair} ({timeframe})")
                    if result.stderr:
                        print(f"    Error: {result.stderr.strip()[:100]}")
                
            except subprocess.TimeoutExpired:
                print("✗ Timeout")
                failed.append(f"{pair} ({timeframe}) - timeout")
            except Exception as e:
                print(f"✗ Error: {str(e)[:50]}")
                failed.append(f"{pair} ({timeframe}) - {str(e)[:30]}")
    
    return failed


def verify_data(freqtrade_dir):
    """Verify downloaded data"""
    data_dir = freqtrade_dir / 'user_data' / 'data' / EXCHANGE
    
    if not data_dir.exists():
        return 0
    
    # Count JSON files
    json_files = list(data_dir.glob('*.json'))
    return len(json_files)


def main():
    """Main entry point"""
    print_header()
    
    # Check if freqtrade is installed
    if not check_freqtrade():
        sys.exit(1)
    
    # Get freqtrade directory
    freqtrade_dir = get_freqtrade_dir()
    if not freqtrade_dir:
        sys.exit(1)
    
    print(f"✓ Freqtrade directory: {freqtrade_dir}")
    print()
    
    # Confirm with user
    response = input("Start download? This will take 15-20 minutes. (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Download cancelled.")
        sys.exit(0)
    
    print("\nStarting download...\n")
    start_time = datetime.now()
    
    # Download data
    failed = download_data(freqtrade_dir, PAIRS, TIMEFRAMES, DAYS_TO_DOWNLOAD)
    
    # Calculate duration
    duration = datetime.now() - start_time
    minutes = int(duration.total_seconds() / 60)
    seconds = int(duration.total_seconds() % 60)
    
    # Print summary
    print("\n" + "="*60)
    print("  Download Complete!")
    print("="*60)
    print(f"\nDuration: {minutes}m {seconds}s")
    
    # Verify data
    file_count = verify_data(freqtrade_dir)
    print(f"Downloaded files: {file_count}")
    
    if failed:
        print(f"\n⚠ {len(failed)} downloads failed:")
        for item in failed[:10]:  # Show first 10 failures
            print(f"  - {item}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")
    else:
        print("\n✓ All downloads successful!")
    
    print("\nNEXT STEP:")
    print("  Train the ML model with: python scripts/train_model.py")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
