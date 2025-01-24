-- Equities Table
CREATE TABLE equities (
    equity_id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
);

-- Heston Parameters Table
CREATE TABLE heston_parameters (
    heston_id SERIAL PRIMARY KEY,
    equity_id INT NOT NULL REFERENCES equities(equity_id) ON DELETE CASCADE,
    kappa NUMERIC(10, 6) NOT NULL,
    theta NUMERIC(10, 6) NOT NULL,
    sigma_v NUMERIC(10, 6) NOT NULL,
    rho_sv NUMERIC(10, 6) NOT NULL,
    initial_variance NUMERIC(10, 6) NOT NULL
);

-- Factors Table
CREATE TABLE factors (
    factor_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    volatility NUMERIC(10, 6) NOT NULL
);

-- Factor Correlations Table
CREATE TABLE factor_correlations (
    correlation_id SERIAL PRIMARY KEY,
    factor_1_id INT NOT NULL REFERENCES factors(factor_id) ON DELETE CASCADE,
    factor_2_id INT NOT NULL REFERENCES factors(factor_id) ON DELETE CASCADE,
    correlation NUMERIC(10, 6) NOT NULL,
    UNIQUE(factor_1_id, factor_2_id)
);

-- Factor Time Series Table
CREATE TABLE factor_time_series (
    simulation_run_id INT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    factor_id INT NOT NULL REFERENCES factors(factor_id) ON DELETE CASCADE,
    increment NUMERIC(10, 6) NOT NULL,
    PRIMARY KEY (simulation_run_id, factor_id, timestamp)
);

-- Synthetic Prices Table
CREATE TABLE synthetic_prices (
    simulation_run_id INT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    equity_id INT NOT NULL REFERENCES equities(equity_id) ON DELETE CASCADE,
    price NUMERIC(20, 10) NOT NULL,
    variance NUMERIC(20, 10) NOT NULL,
    PRIMARY KEY (simulation_run_id, equity_id, timestamp)
);

-- Simulation Runs Table
CREATE TABLE simulation_runs (
    run_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    random_seed INT NOT NULL
);
