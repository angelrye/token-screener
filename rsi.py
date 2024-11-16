import pandas as pd
import ta
import logging


def calculate_rsi(df, period=14):
    """Calculates RSI for a given DataFrame"""
    if df is None:
        logging.error("Cannot calculate RSI because the DataFrame is None")
        return None

    try:
        df['rsi'] = ta.momentum.rsi(df['close'], window=period)
        return df
    except Exception as e:
        logging.error(f"Error calculating RSI: {e}")
        return None


def check_rsi_conditions(df, recent_period=10):
    """Checks if the RSI conditions are met for a given DataFrame"""
    df = calculate_rsi(df)

    if df is None:
        return False, None

    recent_rsi_touch = (df.tail(recent_period)['rsi'] >= 70).any()
    current_rsi = df.iloc[-1]['rsi']

    if recent_rsi_touch and 40 < current_rsi < 60:
        return True, current_rsi
    return False, current_rsi
