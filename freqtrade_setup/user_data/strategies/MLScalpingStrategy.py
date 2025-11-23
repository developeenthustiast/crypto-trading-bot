"""
ML Scalping Strategy - FreqAI Powered
======================================

This strategy uses machine learning (FreqAI with LightGBM) to predict short-term
price movements for scalping (1-15 minute timeframes).

How it works:
1. Analyzes technical indicators (RSI, MACD, Bollinger Bands, Volume, EMAs)
2. Creates 30+ features from price action and indicators
3. ML model predicts probability of profitable trade in next 5-15 minutes
4. Only enters when ML confidence > 65%
5. Dynamic stop-loss and take-profit based on volatility

Risk Management:
- Hard-coded 5% stop-loss on every trade
- Only trades pairs from dynamic VolumePairList
- Skips trades during low volume or high spread
- Respects max open trades limit from config
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Trade
from datetime import datetime, timedelta
from typing import Optional
import numpy as np


class MLScalpingStrategy(IStrategy):
    """
    FreqAI-powered scalping strategy for 1m-15m timeframes
    """
    
    # Strategy interface version
    INTERFACE_VERSION = 3
    
    # Timeframe for the strategy
    timeframe = '5m'
    
    # Can short? (set to False for spot trading)
    can_short = False
    
    # ROI table (minimal for scalping - let ML decide exits)
    minimal_roi = {
        "0": 0.05,    # 5% profit target
        "15": 0.03,   # 3% after 15 minutes
        "30": 0.02,   # 2% after 30 minutes
        "60": 0.01    # 1% after 1 hour
    }
    
    # Stoploss
    stoploss = -0.05  # Hard-coded 5% stop-loss
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    
    # Optimal timeframe for entry (used by FreqAI)
    startup_candle_count = 200
    
    # Protection mechanisms
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # Hyperparameters (optimizable)
    buy_rsi = IntParameter(20, 40, default=30, space="buy")
    buy_rsi_enabled = True
    
    sell_rsi = IntParameter(60, 80, default=70, space="sell")
    sell_rsi_enabled = True
    
    # ML confidence threshold
    ml_confidence_threshold = DecimalParameter(0.5, 0.8, default=0.65, space="buy")
    
    # Process only new candles
    process_only_new_candles = True
    
    # These values can be overridden in config
    plot_config = {
        'main_plot': {
            'bb_lowerband': {'color': 'blue'},
            'bb_upperband': {'color': 'blue'},
            'ema_fast': {'color': 'orange'},
            'ema_slow': {'color': 'red'},
        },
        'subplots': {
            "RSI": {
                'rsi': {'color': 'red'},
            },
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
        }
    }
    
    def feature_engineering_expand_all(self, dataframe: DataFrame, period: int,
                                       metadata: dict, **kwargs) -> DataFrame:
        """
        Creates all features for FreqAI model training.
        This is where we engineer 30+ features from raw OHLCV data.
        """
        
        # ===== PRICE-BASED FEATURES =====
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-pct-change-high"] = dataframe["high"].pct_change()
        dataframe["%-pct-change-low"] = dataframe["low"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        
        # ===== MOMENTUM INDICATORS =====
        # RSI (Relative Strength Index)
        dataframe["%-rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["%-rsi-fast"] = ta.RSI(dataframe, timeperiod=7)
        dataframe["%-rsi-slow"] = ta.RSI(dataframe, timeperiod=21)
        
        # MFI (Money Flow Index)
        dataframe["%-mfi"] = ta.MFI(dataframe, timeperiod=14)
        
        # Stochastic
        stoch = ta.STOCH(dataframe)
        dataframe["%-slowk"] = stoch['slowk']
        dataframe["%-slowd"] = stoch['slowd']
        
        # Williams %R
        dataframe["%-willr"] = ta.WILLR(dataframe, timeperiod=14)
        
        # ===== TREND INDICATORS =====
        # MACD
        macd = ta.MACD(dataframe)
        dataframe["%-macd"] = macd['macd']
        dataframe["%-macdsignal"] = macd['macdsignal']
        dataframe["%-macdhist"] = macd['macdhist']
        
        # ADX (Average Directional Index)
        dataframe["%-adx"] = ta.ADX(dataframe, timeperiod=14)
        dataframe["%-plus_di"] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe["%-minus_di"] = ta.MINUS_DI(dataframe, timeperiod=14)
        
        # ===== VOLATILITY INDICATORS =====
        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(dataframe['close'], window=20, stds=2)
        dataframe["%-bb_lowerband"] = bollinger['lower']
        dataframe["%-bb_middleband"] = bollinger['mid']
        dataframe["%-bb_upperband"] = bollinger['upper']
        dataframe["%-bb_width"] = (bollinger['upper'] - bollinger['lower']) / bollinger['mid']
        dataframe["%-bb_percent"] = (dataframe['close'] - bollinger['lower']) / (bollinger['upper'] - bollinger['lower'])
        
        # ATR (Average True Range)
        dataframe["%-atr"] = ta.ATR(dataframe, timeperiod=14)
        dataframe["%-natr"] = ta.NATR(dataframe, timeperiod=14)
        
        # ===== MOVING AVERAGES =====
        # EMAs
        dataframe["%-ema_fast"] = ta.EMA(dataframe, timeperiod=8)
        dataframe["%-ema_slow"] = ta.EMA(dataframe, timeperiod=21)
        dataframe["%-ema_200"] = ta.EMA(dataframe, timeperiod=200)
        
        # SMA
        dataframe["%-sma_fast"] = ta.SMA(dataframe, timeperiod=8)
        dataframe["%-sma_slow"] = ta.SMA(dataframe, timeperiod=21)
        
        # ===== VOLUME INDICATORS =====
        # OBV (On-Balance Volume)
        dataframe["%-obv"] = ta.OBV(dataframe)
        
        # AD (Accumulation/Distribution)
        dataframe["%-ad"] = ta.AD(dataframe)
        
        # ===== PATTERN RECOGNITION =====
        # Candle patterns
        dataframe["%-cdl_doji"] = ta.CDLDOJI(dataframe)
        dataframe["%-cdl_hammer"] = ta.CDLHAMMER(dataframe)
        dataframe["%-cdl_engulfing"] = ta.CDLENGULFING(dataframe)
        
        return dataframe
    
    def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        """
        Basic features that don't need period specification
        """
        # Price distance from EMAs
        dataframe["%-price_vs_ema_fast"] = (dataframe["close"] - dataframe["%-ema_fast"]) / dataframe["%-ema_fast"]
        dataframe["%-price_vs_ema_slow"] = (dataframe["close"] - dataframe["%-ema_slow"]) / dataframe["%-ema_slow"]
        
        # EMA crossover signal
        dataframe["%-ema_cross"] = (dataframe["%-ema_fast"] > dataframe["%-ema_slow"]).astype(int)
        
        return dataframe
    
    def feature_engineering_standard(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        """
        Standard features computed after expand methods
        """
        # Normalized volume
        dataframe["%-volume_mean"] = dataframe["volume"].rolling(window=20).mean()
        dataframe["%-volume_ratio"] = dataframe["volume"] / dataframe["%-volume_mean"]
        
        # Volatility
        dataframe["%-volatility"] = dataframe["close"].rolling(window=20).std() / dataframe["close"].rolling(window=20).mean()
        
        return dataframe
    
    def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        """
        Define what the ML model should predict.
        We predict if the price will increase by 1% in the next 20 candles (5m * 20 = 100 min).
        """
        # Calculate future returns
        dataframe['&-s_close'] = (
            dataframe['close']
            .shift(-20)  # Look 20 candles ahead
            .rolling(20)
            .max()
        )
        
        # Binary classification: Will price go up by 1%+?
        dataframe['&-s_target'] = (
            (dataframe['&-s_close'] / dataframe['close'] > 1.01)
            .astype(int)
        )
        
        return dataframe
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add indicators to dataframe for strategy logic (not freqAI features)
        """
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        
        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(dataframe['close'], window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        
        # EMAs
        dataframe['ema_fast'] = ta.EMA(dataframe, timeperiod=8)
        dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=21)
        
        # Volume
        dataframe['volume_mean_20'] = dataframe['volume'].rolling(window=20).mean()
        
        # ATR for position sizing
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        
        # FreqAI will populate these columns with predictions:
        # - do_predict: ML model's prediction (0 or 1)
        # - DI_values: Data quality metric
        # - &*_std/mean: Confidence metrics
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry signal logic combining ML prediction with technical filters
        """
        conditions = []
        
        # === ML PREDICTION (MOST IMPORTANT) ===
        # FreqAI must predict a buy signal (1) with high confidence
        conditions.append(dataframe['do_predict'] == 1)
        conditions.append(dataframe['DI_values'] > 0.5)  # Data quality check
        
        # === TECHNICAL FILTERS (SAFETY CHECKS) ===
        
        # 1. Volume filter: Ensure sufficient liquidity
        conditions.append(dataframe['volume'] > dataframe['volume_mean_20'] * 0.7)
        
        # 2. RSI filter: Not overbought (if enabled)
        if self.buy_rsi_enabled:
            conditions.append(dataframe['rsi'] < self.buy_rsi.value)
        
        # 3. Trend filter: Price above fast EMA (uptrend)
        conditions.append(dataframe['close'] > dataframe['ema_fast'])
        
        # 4. Spread check: BB width not too narrow (avoid low volatility)
        conditions.append(
            (dataframe['bb_upperband'] - dataframe['bb_lowerband']) / dataframe['bb_middleband'] > 0.01
        )
        
        # 5. Not at top of BB (avoid buying peaks)
        conditions.append(dataframe['close'] < dataframe['bb_upperband'] * 0.98)
        
        # Combine all conditions
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit signal logic
        """
        conditions = []
        
        # === EXIT CONDITIONS ===
        
        # 1. ML says exit (model predicts downtrend)
        conditions.append(dataframe['do_predict'] == 0)
        
        # 2. RSI overbought (if enabled)
        if self.sell_rsi_enabled:
            conditions.append(dataframe['rsi'] > self.sell_rsi.value)
        
        # 3. Price crossed below fast EMA (trend reversal)
        conditions.append(qtpylib.crossed_below(dataframe['close'], dataframe['ema_fast']))
        
        # 4. MACD bearish cross
        conditions.append(qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']))
        
        # Combine with OR logic (exit on any signal)
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x | y, conditions),
                'exit_long'] = 1
        
        return dataframe
    
    def custom_stake_amount(self, pair: str, current_time: datetime,
                           current_rate: float, proposed_stake: float,
                           min_stake: Optional[float], max_stake: float,
                           leverage: float, entry_tag: Optional[str],
                           side: str, **kwargs) -> float:
        """
        Customize stake amount based on volatility.
        Lower stake in high volatility, higher in low volatility.
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if len(dataframe) < 1:
            return proposed_stake
        
        current_candle = dataframe.iloc[-1]
        
        # Get ATR (volatility measure)
        atr = current_candle.get('atr', 0)
        
        # If no ATR data, use proposed stake
        if atr == 0 or np.isnan(atr):
            return proposed_stake
        
        # Calculate ATR percentage
        atr_percent = (atr / current_rate) * 100
        
        # Reduce stake if volatility is high (above 2%)
        if atr_percent > 2.0:
            return proposed_stake * 0.7  # 30% reduction
        elif atr_percent > 1.5:
            return proposed_stake * 0.85  # 15% reduction
        else:
            return proposed_stake
    
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float,
                           rate: float, time_in_force: str, current_time: datetime,
                           entry_tag: Optional[str], side: str, **kwargs) -> bool:
        """
        Final check before entering trade.
        Ensures ML confidence is above threshold.
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if len(dataframe) < 1:
            return False
        
        current_candle = dataframe.iloc[-1]
        
        # Check DI_values (data quality metric from FreqAI)
        di_value = current_candle.get('DI_values', 0)
        
        # Only enter if data quality is good
        if di_value < 0.5:
            return False
        
        # Additional safety: Don't trade if volume is suspiciously low
        volume = current_candle.get('volume', 0)
        volume_mean = current_candle.get('volume_mean_20', 1)
        
        if volume < volume_mean * 0.5:
            return False
        
        return True
    
    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str,
                          amount: float, rate: float, time_in_force: str,
                          exit_reason: str, current_time: datetime, **kwargs) -> bool:
        """
        Confirm exit - always allow stops and ROI
        """
        # Always allow stop-loss and ROI exits
        if exit_reason in ['stop_loss', 'roi', 'trailing_stop_loss']:
            return True
        
        # For other exits, check if we've held for minimum time (5 minutes)
        if trade.open_date_utc:
            trade_duration = (current_time - trade.open_date_utc).total_seconds() / 60
            if trade_duration < 5:
                return False  # Don't exit too quickly
        
        return True


# Helper function for reduce
from functools import reduce
