import numpy as np
from typing import Tuple

def simulate_factor_returns(
    total_number_of_seconds: int,
    factor_volatilities: np.ndarray,
    factor_correlations: np.ndarray,
    random_seed: int,
) -> Tuple[np.ndarray, np.ndarray]:

    if not isinstance(total_number_of_seconds, int) or total_number_of_seconds <= 0:
        raise ValueError("total_number_of_seconds must be a positive integer.")

    if factor_volatilities.ndim != 1:
        raise ValueError("factor_volatilities must be a 1D array.")

    number_of_factors = factor_volatilities.shape[0]

    if factor_correlations.ndim != 2:
        raise ValueError("factor_correlations must be a 2D array.")
    if factor_correlations.shape[0] != factor_correlations.shape[1]:
        raise ValueError("factor_correlations must be a square matrix.")
    if factor_correlations.shape[0] != number_of_factors:
        raise ValueError(
            "factor_correlations dimensions must match the length of factor_volatilities."
        )

    # Check approximate symmetry
    if not np.allclose(factor_correlations, factor_correlations.T, atol=1e-8):
        raise ValueError("factor_correlations must be symmetric to be a valid correlation matrix.")
    # Check diagonal elements are ~1
    if not np.allclose(np.diag(factor_correlations), 1.0, atol=1e-8):
        raise ValueError("The diagonal entries of factor_correlations should be close to 1.0.")

    np.random.seed(random_seed)

    diagonal_of_volatilities = np.diag(factor_volatilities)
    factor_covariance = diagonal_of_volatilities @ factor_correlations @ diagonal_of_volatilities

    try:
        cholesky_factor = np.linalg.cholesky(factor_covariance)
    except np.linalg.LinAlgError as e:
        raise ValueError(
            "Covariance matrix is not positive-definite. "
            "Check that factor_volatilities are valid and factor_correlations is a valid correlation matrix."
        ) from e

    factor_return_increments = np.zeros((total_number_of_seconds, number_of_factors))
    factor_return_levels = np.zeros((total_number_of_seconds, number_of_factors))

    for time_index in range(total_number_of_seconds):
        random_values = np.random.randn(number_of_factors)
        factor_return_increments[time_index] = cholesky_factor @ random_values

        if time_index == 0:
            factor_return_levels[time_index] = factor_return_increments[time_index]
        else:
            factor_return_levels[time_index] = (
                factor_return_levels[time_index - 1] + factor_return_increments[time_index]
            )

    return factor_return_increments, factor_return_levels
