import numpy as np
from typing import Tuple

def simulate_factor_returns(
    total_seconds: int,
    factor_vols: np.ndarray,
    factor_corr: np.ndarray,
    seed: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate correlated factor returns and cumulative factor levels
    using a simple random-walk approach.

    Parameters
    ----------
    total_seconds : int
        Number of time steps (in seconds) to simulate.
    factor_vols : np.ndarray
        1D array of factor volatilities (per sqrt(sec)).
        e.g. array([0.01, 0.008, 0.006]) for 3 factors.
    factor_corr : np.ndarray
        Correlation matrix for the factors (shape NxN).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    factor_increments : np.ndarray
        Shape (total_seconds, n_factors). The increments of each factor at each second.
    factor_levels : np.ndarray
        Shape (total_seconds, n_factors). The cumulative factor levels at each second.
        factor_levels[t] = sum of factor_increments up to t.
    """
    np.random.seed(seed)

    # Derive covariance from volume & correlation
    diag_vols = np.diag(factor_vols)
    factor_cov = diag_vols @ factor_corr @ diag_vols

    # Cholesky decomp. for correlated draws
    L_factors = np.linalg.cholesky(factor_cov)

    n_factors = len(factor_vols)
    factor_increments = np.zeros((total_seconds, n_factors))
    factor_levels = np.zeros((total_seconds, n_factors))

    # Generate increments
    for t in range(total_seconds):
        z = np.random.randn(n_factors)
        factor_increments[t] = L_factors @ z

        if t == 0:
            factor_levels[t] = factor_increments[t]
        else:
            factor_levels[t] = factor_levels[t - 1] + factor_increments[t]

    return factor_increments, factor_levels
