# PsuedoFinancial-Data-Feed

## Overview: 

This project aims to design and implement a comprehensive real-time platform for generating, processing, and analyzing financial data. The platform supports various financial applications, including algorithmic trading research, market analysis, and data-driven strategy development by leveraging advanced simulation techniques, robust data streaming tools, and performance-optimized storage solutions.

### Stage One: Baseline Factor and Stock Price Simulation: (Complete)

In the initial stage, the system employs untrained stochastic and financial models to simulate synthetic stock price movements and factor returns. This stage aims to establish a foundational dataset for exploring financial phenomena, relying solely on basic statistical and financial assumptions without domain-specific optimization.

- Factor Return Simulation (factor_model.py):
This code simulates correlated factor returns using a random-walk approach. It takes inputs like factor volatilities, correlation, and a random seed to ensure reproducibility. The factors represent underlying economic drivers, and their increments and cumulative levels are calculated using a Cholesky decomposition for correlated random draws.

- Heston Model for Stock Prices (heston_model.py):
A Heston process simulates stock prices and variances, incorporating mean-reverting variance dynamics and correlations between price and volatility increments. Factor-based and idiosyncratic shocks are included in the price updates, with Euler discretization applied to ensure stepwise simulation accuracy.

### Stage Two: Data Distribution and Real-Time Processing (Ongoing)

In this stage, Kafka and Redis are employed to generate, distribute, and process synthetic financial data. The aim is to enable real-time analytics and efficient data flow across various system components. 

- Kafka will serve as the primary message broker for streaming financial data in real-time, as it is well-suited for distributing large volumes of sequential data across multiple consumers, ensuring fault tolerance and scalability in managing the data pipeline.

- Redis will act as a high-speed, in-memory database for caching and storing frequently accessed data. It compliments Kafka by providing low-latency access to recent or commonly queried data. 

### Stage Three: PostgreSQL Database: (On-Going)

In this stage, a PostgreSQL database, enhanced with TimescaleDB, is employed for persistent storage and efficient querying of the financial data. The focus is creating a scalable and performance-optimized database schema that supports historical analysis and real-time data ingestion.

- PostgreSQL serves as the core relational database, while TimescaleDB provides time-series data management capabilities, improved query performance, and support for more efficient data retention policies. 

### Objective: 

This project aims to develop a robust and scalable real-time platform for simulating, processing, and analyzing financial data. It seeks to generate realistic synthetic market data using advanced stochastic models, stream and cache it efficiently using tools like Kafka and Redis for real-time applications, and provide a performance-optimized storage solution with PostgreSQL and TimescaleDB for historical analysis. By integrating these components, the platform seeks to support various financial use cases, including algorithmic trading research, market behavior analysis, and strategy development, ensuring high performance, scalability, and low latency.

### Methodology:

- Data Simulation:

    Employ stochastic models, including random walks and the Heston process, to generate synthetic financial data.
    Simulate correlated factor returns and stock price dynamics, incorporating variance modeling and factor-based shocks.
    Validate the generated data against expected financial behaviors to establish a reliable baseline.

- Real-Time Streaming and Caching:

    Integrate Kafka as the primary message broker for streaming synthetic data, ensuring scalability and fault tolerance.
    Use Redis as an in-memory database to cache the most recent financial data for ultra-low-latency access.
    Design a robust data flow pipeline, with Kafka producing streams of tick data and Redis serving as a fast-access layer for downstream applications.

- Database Design and Optimization:

    Develop a relational database schema using PostgreSQL optimized for storing time-series financial data.
    Enhance performance by integrating TimescaleDB for time-based partitioning and efficient historical queries.
    Implement indexing and hyper tables to scale storage and querying capabilities as the data grows.

- Integration and Testing:

    Connect the simulation engine, Kafka, Redis, and the database into a unified pipeline.
    Test the system under various workloads to evaluate performance, scalability, and latency.
    Validate the correctness of data at each stage, ensuring accuracy and consistency from simulation to storage.

- Performance Evaluation:

    Benchmark the platform's ability to handle large-scale data generation, real-time processing, and historical analysis.
    Based on testing results, optimize each component (e.g., Kafka throughput, Redis latency, TimescaleDB query performance).

### Expected Outcomes: 

The expected outcome of this project is a fully operational platform capable of generating, processing, and storing large volumes of realistic financial data in real-time. The platform will simulate market behaviors using stochastic models, efficiently distribute the data through Kafka for real-time applications, and provide ultra-low-latency access to live data via Redis. Additionally, it will include a scalable PostgreSQL database, enhanced with TimescaleDB, to store historical data for long-term analysis and research. This integrated system will support various financial applications, such as algorithmic trading strategy development, market behavior analysis, and data-driven decision-making, ensuring high performance, reliability, and scalability for real-time and historical use cases.

## Built With:

- Python:
        Primary language for simulation and data processing.
        Libraries such as NumPy, pandas, and SciPy will be used for mathematical modeling and data manipulation.
- C++:
        Used for Kafka and Redis integration, leveraging its high-performance libraries for stream processing.
- SQL:
        For database schema design and querying within PostgreSQL and TimescaleDB.

- Simulation and Modeling:
        Custom Python Models: Implementation of stochastic models, including random walks and the Heston process, for synthetic data generation.
        Scientific Libraries: NumPy, pandas, and SciPy for numerical computations and data handling.

- Data Streaming:
        Apache Kafka:
            Manages the real-time streaming of simulated financial data.
            Ensures scalability and fault-tolerant distribution across consumers.

- Caching:
        Redis:
            Provides in-memory caching for ultra-low-latency access to the latest data.

- Database Management:
       PostgreSQL:
            Relational database for persistent storage of financial data.
       TimescaleDB:
            Extension of PostgreSQL optimized for time-series data, enabling efficient querying and storage partitioning.

- Performance and Integration:
        Kafka Streams:
            Processes data streams for ingestion into Redis and PostgreSQL.
        TimescaleDB Hypertables:
            Automatically partitions time-series data for improved performance.

- Data Storage:
        CSV Files:
            For initial output and debugging during the simulation stage.
        PostgreSQL Database:
            Long-term storage for structured financial data.

## Resources: 

- [FiQA and Financial Phrasebank Dataset](https://huggingface.co/datasets/KennNguyenDev/FiQA_Financial_Phrasebank_Combined)

- [General Financial News Dataset](https://huggingface.co/datasets/KennNguyenDev/General_Financial_News_Altared)
