import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from factor_model import simulate_factor_returns
from heston_model import simulate_heston_paths

def generate_trading_timestamps(
    start_date: datetime,
    days: int,
    hours_per_day: float = 6.5
) -> pd.DatetimeIndex:
    """
    Generate second-by-second timestamps for a given number of trading days,
    each day from 9:30 AM to 4:00 PM, skipping non-trading hours in between.

    Parameters
    ----------
    start_date : datetime
        The date/time at which to start (assumed 9:30 AM of some day).
    days : int
        Number of trading days to simulate.
    hours_per_day : float
        Trading hours per day (default 6.5 = 9:30 - 16:00).

    Returns
    -------
    timestamps : pd.DatetimeIndex
        All timestamps (second resolution) across all days, continuous
        in business/trading hours.
    """
    seconds_per_day = int(hours_per_day * 3600)
    all_timestamps = []

    current_time = start_date
    for day_idx in range(days):
        for sec in range(seconds_per_day):
            if day_idx == 0 and sec == 0:
                all_timestamps.append(current_time)
            else:
                current_time += timedelta(seconds=1)
                all_timestamps.append(current_time)

        # Move to next day 9:30 if not the last day
        if day_idx < days - 1:
            # Jump from 16:00 to next day 9:30 (17.5 hours = 63000 seconds)
            current_time += timedelta(seconds=63000)
            # Make sure it's exactly 9:30
            current_time = current_time.replace(hour=9, minute=30, second=0)

    # Return as a Pandas DatetimeIndex
    return pd.DatetimeIndex(all_timestamps)

def main():
    TICKERS = [
        # Hot Equities
        "AAPL", "AMZN", "MSFT", "GOOGL", "META", "TSLA", "NVDA", "NFLX", "BRK.B", "JPM", "JNJ",
        "V", "PG", "DIS", "WMT", "MA", "BAC", "HD", "XOM", "KO", "NKE",
        "INTC", "IBM", "PFE", "WFC", "CVX", "ADBE", "CRM", "T", "VZ", "PEP",
        "CSCO", "BA", "ABBV", "CMCSA", "ORCL", "AVGO", "MCD",
        # Mild Equities
        "SBUX", "PYPL", "SHOP", "SQ", "F", "GM", "AXP", "UBER", "LYFT",
        "ZM", "ROKU", "SNAP", "PLTR", "DKNG", "BYND", "DPZ", "FDX", "UAA", "CRWD",
        "EA", "MTCH", "MRNA", "CAT", "DOCU", "PINS", "ABNB", "Z", "DELL", "YELP",
        "PLNT", "ZTS", "WYNN", "OXY", "TMUS", "CI", "GILD",
        # Cold Equities
        "ETSY", "OSTK", "CHWY", "BE", "RKT", "GPRO", "BARK", "SPWR", "UPST", "SDC", "PLUG",
        "SPCE", "APRN", "TLRY", "CGC", "GOEV", "FSR", "LAZR", "ARVL", "NKLA", "TTCF",
        "GRAB", "RDFN", "UPWK", "JMIA", "SNDL"
    ]

    N_STOCKS = 100
    N_FACTORS = 3
    DAYS = 5
    HOURS_PER_DAY = 6.5
    SEED = 42

    # Factor parameters
    factor_vols = np.array([0.01, 0.008, 0.006])
    factor_corr = np.array([
        [1.0,  0.3, -0.2],
        [0.3,  1.0,  0.1],
        [-0.2, 0.1,  1.0]
    ])
    # Factor loadings: shape (N_STOCKS, N_FACTORS)
    factor_loadings = 0.5 * np.random.randn(N_STOCKS, N_FACTORS)

    # Idiosyncratic volatility for each stock
    idio_vol = 0.005

    # Heston parameters
    kappa = 1.5
    theta = 0.04
    sigma_v = 0.3
    rho_sv = -0.7
    initial_variance = 0.04

    # All stocks start at price = 100
    initial_prices = np.full(N_STOCKS, 100.0)
    initial_variances = np.full(N_STOCKS, initial_variance)

    start_date = datetime(2025, 1, 6, 9, 30)  # 01/06/25 at 9:30
    timestamps = generate_trading_timestamps(start_date, DAYS, HOURS_PER_DAY)
    total_seconds = len(timestamps) - 1

    factor_increments, factor_levels = simulate_factor_returns(
        total_seconds=total_seconds,
        factor_vols=factor_vols,
        factor_corr=factor_corr,
        seed=SEED
    )

    dt = 1.0 
    prices, variances = simulate_heston_paths(
        initial_prices=initial_prices,
        initial_variances=initial_variances,
        kappa=kappa,
        theta=theta,
        sigma_v=sigma_v,
        rho_sv=rho_sv,
        dt=dt,
        factor_increments=factor_increments,
        factor_loadings=factor_loadings,
        idio_vol=idio_vol
    )

    # Case: Ticker list is bigger than N_STOCKS
    use_tickers = TICKERS[:N_STOCKS]

    df_prices = pd.DataFrame(
        data=prices,
        columns=use_tickers,
        index=timestamps
    )

    # Change output as needed
    output_folder = r"D:\FinData"
    os.makedirs(output_folder, exist_ok=True)

    for ticker in df_prices.columns:
        out_csv = os.path.join(output_folder, f"{ticker}.csv")
        df_prices[[ticker]].to_csv(out_csv, index_label="timestamp")

    print("Synthetic data generated for all tickers!")
    print(f"Individual CSVs have been written to: {output_folder}")

if __name__ == "__main__":
    main()
