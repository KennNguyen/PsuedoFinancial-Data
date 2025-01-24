import numpy as np
from typing import Tuple

def simulate_heston_paths(
    initial_prices: np.ndarray,
    initial_variances: np.ndarray,
    kappa: float,
    theta: float,
    sigma_v: float,
    rho_sv: float,
    delta_time: float,
    factor_increments: np.ndarray,
    factor_loadings: np.ndarray,
    idio_vol: float,
) -> Tuple[np.ndarray, np.ndarray]:
    
    if initial_prices.ndim != 1 or initial_variances.ndim != 1:
        raise ValueError("initial_prices and initial_variances must be 1D arrays.")
    if initial_prices.shape != initial_variances.shape:
        raise ValueError("initial_prices and initial_variances must be the same shape.")

    if factor_increments.ndim != 2:
        raise ValueError("factor_increments must be a 2D array (n_steps x n_factors).")
    if factor_loadings.ndim != 2:
        raise ValueError("factor_loadings must be a 2D array (n_stocks x n_factors).")

    if delta_time <= 0:
        raise ValueError("delta_time must be a positive number.")
    if kappa < 0:
        raise ValueError("kappa (mean reversion speed) should be non-negative.")
    if theta < 0:
        raise ValueError("theta (long-term variance) should be non-negative.")
    if sigma_v < 0:
        raise ValueError("sigma_v (vol of vol) should be non-negative.")
    if not -1 <= rho_sv <= 1:
        raise ValueError("rho_sv (correlation) must be in the range [-1, 1].")
    if idio_vol < 0:
        raise ValueError("idio_vol (idiosyncratic volatility) should be non-negative.")

    number_of_stocks = len(initial_prices)
    total_steps = factor_increments.shape[0]

    if factor_loadings.shape[0] != number_of_stocks:
        raise ValueError(
            "factor_loadings first dimension must match the number of stocks "
            f"({factor_loadings.shape[0]} != {number_of_stocks})."
        )
    if factor_increments.shape[1] != factor_loadings.shape[1]:
        raise ValueError(
            "Number of factors in factor_increments and factor_loadings must match."
        )

    # Initialize output arrays
    prices = np.zeros((total_steps + 1, number_of_stocks), dtype=float)
    variances = np.zeros((total_steps + 1, number_of_stocks), dtype=float)

    # Set initial conditions
    prices[0, :] = initial_prices
    variances[0, :] = initial_variances

    sqrt_delta_time = np.sqrt(delta_time)

    # Pre-generate random draws for each step x stock
    # Ensures the random increments are generated only once for reproducibility & performance
    price_random = np.random.randn(total_steps, number_of_stocks)
    vol_random = np.random.randn(total_steps, number_of_stocks)

    for step_index in range(total_steps):
        # Factor-based increment at time step
        factor_increment_current = factor_increments[step_index]
        
        # Contribution from factor loadings for each stock
        # factor_contribution[i] = factor_loadings[i,:] . factor_increment_current
        factor_contribution = factor_loadings @ factor_increment_current

        # Idiosyncratic shock
        idiosyncratic_shock = idio_vol * np.random.randn(number_of_stocks) * sqrt_delta_time

        for i in range(number_of_stocks):
            current_variance = variances[step_index, i]
            current_price = prices[step_index, i]

            # Generate correlated Brownian increments for price & variance
            vol_brownian_increment = vol_random[step_index, i] * sqrt_delta_time
            uncorrelated_price_brownian_increment = price_random[step_index, i] * sqrt_delta_time
            
            price_brownian_increment = (
                rho_sv * vol_brownian_increment 
                + np.sqrt(1 - rho_sv**2) * uncorrelated_price_brownian_increment
            )

            # Heston variance update
            next_variance = (
                current_variance 
                + kappa * (theta - current_variance) * delta_time
                + sigma_v * np.sqrt(max(current_variance, 0.0)) * vol_brownian_increment
            )
            next_variance = max(next_variance, 1e-12)  # guard against negative variance

            # Combine factor_contribution + idiosyncratic_shock as a drift-like term
            drift_term = factor_contribution[i] + idiosyncratic_shock[i]

            # Price update (Euler)
            next_price = current_price + current_price * (
                drift_term + np.sqrt(max(current_variance, 0.0)) * price_brownian_increment
            )
            next_price = max(next_price, 1e-8)  # guard against negative price

            # Store results
            prices[step_index + 1, i] = next_price
            variances[step_index + 1, i] = next_variance

    return prices, variances