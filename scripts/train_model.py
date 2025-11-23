#!/usr/bin/env python3
"""
ML Model Training Script
========================

Trains the FreqAI machine learning model on historical data.

This script:
1. Updates historical data (downloads latest candles)
2. Trains the FreqAI model using MLScalpingStrategy
3. Saves the trained model
4. Displays training metrics

Estimated time: 30-60 minutes (depending on CPU)
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path


def print_header():
    """Print script header"""
    print("\n" + "="*60)
    print("  ML Model Training")
    print("="*60)
    print("\nThis will train the FreqAI model on historical data.")
    print("The model will learn to predict profitable trades.\n")
    print("⚠ This is CPU-intensive and may take 30-60 minutes!")
    print("="*60 + "\n")


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


def check_data(freqtrade_dir):
    """Check if historical data exists"""
    data_dir = freqtrade_dir / 'user_data' / 'data' / 'binance'
    
    if not data_dir.exists():
        print("✗ ERROR: No data directory found!")
        print("  Please run: python scripts/download_data.py")
        return False
    
    # Count data files
    json_files = list(data_dir.glob('*.json'))
    
    if len(json_files) < 10:
        print(f"✗ ERROR: Only {len(json_files)} data files found!")
        print("  Please run: python scripts/download_data.py")
        return False
    
    print(f"✓ Found {len(json_files)} data files")
    return True


def check_strategy(freqtrade_dir):
    """Check if strategy exists"""
    strategy_file = freqtrade_dir / 'user_data' / 'strategies' / 'MLScalpingStrategy.py'
    
    if not strategy_file.exists():
        print(f"✗ ERROR: Strategy file not found: {strategy_file}")
        return False
    
    print("✓ MLScalpingStrategy found")
    return True


def update_data(freqtrade_dir):
    """Update historical data before training"""
    print("\n" + "="*60)
    print("  Updating historical data...")
    print("="*60 + "\n")
    
    # Update last 7 days of data
    cmd = [
        'freqtrade',
        'download-data',
        '--exchange', 'binance',
        '--timeframe', '5m',
        '--days', '7',
        '--datadir', str(freqtrade_dir / 'user_data' / 'data'),
        '--config', str(freqtrade_dir / 'config.json')
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            print("✓ Data updated successfully")
            return True
        else:
            print("⚠ Data update failed, continuing with existing data")
            return True  # Continue anyway
    
    except Exception as e:
        print(f"⚠ Data update failed: {e}")
        print("  Continuing with existing data...")
        return True


def train_model(freqtrade_dir):
    """Train the FreqAI model"""
    print("\n" + "="*60)
    print("  Training ML Model")
    print("="*60)
    print("\n⏱ This may take 30-60 minutes...")
    print("☕ Good time for a coffee break!\n")
    
    # Change to freqtrade directory
    original_dir = os.getcwd()
    os.chdir(freqtrade_dir)
    
    try:
        # Build training command
        cmd = [
            'freqtrade',
            'backtesting',
            '--strategy', 'MLScalpingStrategy',
            '--config', 'config.json',
            '--timerange', '20231101-',  # Train on data from Nov 2023 onwards
            '--freqaimodel', 'LightGBMClassifier'
        ]
        
        print("Running command:")
        print(" ".join(cmd))
        print("\n" + "-"*60 + "\n")
        
        # Run training (show output in real-time)
        start_time = datetime.now()
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Print output line by line
        for line in process.stdout:
            print(line, end='', flush=True)
        
        # Wait for completion
        process.wait()
        
        # Calculate duration
        duration = datetime.now() - start_time
        minutes = int(duration.total_seconds() / 60)
        seconds = int(duration.total_seconds() % 60)
        
        if process.returncode == 0:
            print("\n" + "="*60)
            print(f"  Training Complete! ({minutes}m {seconds}s)")
            print("="*60)
            return True
        else:
            print("\n✗ Training failed!")
            return False
    
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user!")
        return False
    except Exception as e:
        print(f"\n✗ Training failed: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)


def check_model(freqtrade_dir):
    """Check if model was created"""
    models_dir = freqtrade_dir / 'user_data' / 'models'
    
    if not models_dir.exists():
        return False
    
    # Look for model files
    model_dirs = list(models_dir.glob('*'))
    
    if model_dirs:
        print(f"\n✓ Model saved to: {models_dir}")
        print(f"  Model directories: {len(model_dirs)}")
        return True
    
    return False


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
    
    # Check if data exists
    if not check_data(freqtrade_dir):
        sys.exit(1)
    
    # Check if strategy exists
    if not check_strategy(freqtrade_dir):
        sys.exit(1)
    
    print()
    
    # Confirm with user
    response = input("Start training? This will take 30-60 minutes. (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Training cancelled.")
        sys.exit(0)
    
    # Update data
    if not update_data(freqtrade_dir):
        print("\n⚠ Failed to update data. Aborting...")
        sys.exit(1)
    
    # Train model
    if not train_model(freqtrade_dir):
        print("\n⚠ Training failed!")
        print("\nTROUBLESHOOTING:")
        print("  1. Check that you have enough historical data")
        print("  2. Ensure your .env file has valid API keys")
        print("  3. Check logs in freqtrade_setup/user_data/logs/")
        sys.exit(1)
    
    # Verify model was created
    if check_model(freqtrade_dir):
        print("\n✓ Model created successfully!")
    else:
        print("\n⚠ Warning: Could not verify model files")
    
    print("\nNEXT STEPS:")
    print("  1. Run a backtest: python scripts/backtest.py --period 3m")
    print("  2. Start the bot: cd freqtrade_setup && freqtrade trade --config config.json")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
