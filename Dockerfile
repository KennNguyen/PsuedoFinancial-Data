FROM python:3.11-slim

# Install build tools and C++ compiler
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy entire app folder
COPY ./app ./app

WORKDIR /usr/src/app/app

# Compile Factor Model
RUN g++ -O3 -DSTANDALONE_BUILD models/factor_model.cpp -I ./include -o web/factor_model

# Compile Heston Model
RUN g++ -O3 -DSTANDALONE_BUILD models/heston_model.cpp -I ./include -o web/heston_model

# Install Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

WORKDIR /usr/src/app/app/web

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
