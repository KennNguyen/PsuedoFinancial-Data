import numpy as np
from typing import Tuple

def simulate_heston_paths(
    initial_prices: np.ndarray,
    initial_variances: np.ndarray,
    kappa: float,
    theta: float,
    sigma_v: float,
    rho_sv: float,
    dt: float,
    factor_increments: np.ndarray,
    factor_loadings: np.ndarray,
    idio_vol: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate the Heston process for multiple stocks, incorporating
    factor-based and idiosyncratic returns as the "drift" term.

    Parameters
    ----------
    initial_prices : np.ndarray
        Shape (n_stocks,). The initial price for each stock.
    initial_variances : np.ndarray
        Shape (n_stocks,). The initial variance for each stock.
    kappa : float
        Mean reversion speed for variance.
    theta : float
        Long-run variance level.
    sigma_v : float
        Volatility of volatility.
    rho_sv : float
        Correlation between price returns and variance Brownian increments.
    dt : float
        Time step size in seconds (e.g. 1.0 for second-by-second).
    factor_increments : np.ndarray
        Shape (total_seconds, n_factors). Factor increments at each second.
    factor_loadings : np.ndarray
        Shape (n_stocks, n_factors). Loadings for each stock on each factor.
    idio_vol : float
        Idiosyncratic volatility (per sqrt(sec)) for each stock's noise.

    Returns
    -------
    prices : np.ndarray
        Shape (total_seconds + 1, n_stocks). Simulated prices over time (including t=0).
    variances : np.ndarray
        Shape (total_seconds + 1, n_stocks). Simulated variances over time (including t=0).
    """
    n_stocks = len(initial_prices)
    total_seconds = factor_increments.shape[0]

    # Initialize output arrays
    prices = np.zeros((total_seconds + 1, n_stocks))
    variances = np.zeros((total_seconds + 1, n_stocks))

    # Set initial conditions
    prices[0, :] = initial_prices
    variances[0, :] = initial_variances

    sqrt_dt = np.sqrt(dt)

    # Pre-generate random draws for each step x stock
    price_rands = np.random.randn(total_seconds, n_stocks)
    vol_rands   = np.random.randn(total_seconds, n_stocks)

    for t in range(total_seconds):
        # Factor-based increment at time t
        factor_inc_t = factor_increments[t]
        # Drift from factor loadings for each stock: factor_part[i] = beta[i,:].dot(factor_inc_t)
        factor_part = factor_loadings @ factor_inc_t

        # Idiosyncratic shock
        idio_shock = idio_vol * np.random.randn(n_stocks) * sqrt_dt

        for i in range(n_stocks):
            v_t = variances[t, i]
            s_t = prices[t, i]

            # Generate correlated Brownian increments for price & vol
            dW_v = vol_rands[t, i] * sqrt_dt
            dW_s_uncorr = price_rands[t, i] * sqrt_dt
            dW_s = rho_sv * dW_v + np.sqrt(1 - rho_sv**2) * dW_s_uncorr

            # Heston variance update
            v_next = v_t + kappa * (theta - v_t) * dt + sigma_v * np.sqrt(max(v_t, 0.0)) * dW_v
            v_next = max(v_next, 1e-12)  # guard against negative variance

            # Combine factor_part + idio_shock as a drift-like term in returns space
            drift_term = factor_part[i] + idio_shock[i]

            # Price update (Euler)
            s_next = s_t + s_t * (drift_term + np.sqrt(max(v_t, 0.0)) * dW_s)
            s_next = max(s_next, 1e-8)  # guard against negative price

            prices[t + 1, i] = s_next
            variances[t + 1, i] = v_next

    return prices, variances
