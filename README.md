# GEX-Levels

# Deribit Gamma Exposure (GEX) Analysis

This Python script retrieves real-time Bitcoin (BTC) options data from the Deribit exchange and calculates **Gamma Exposure (GEX)** metrics, inspired by the [Gamma Exposure (GEX) whitepaper by SqueezeMetrics](https://squeezemetrics.com/download/white_paper.pdf).

## Overview

> “The predictive power of GEX is essentially driven by the necessity of option dealers’ (market makers’) re-hedging activities. In order to limit risk and realize profit, an option market-maker must limit their exposure to deltas.”  
> — *SqueezeMetrics, Gamma Exposure Whitepaper (2017)*

This tool performs the following:

1. Fetches live BTC options from Deribit and their greeks.
2. Calculates GEX by instrument.
3. Aggregates data by expiration.
4. Identifies strike levels with the most extreme GEX (positive/negative).
5. Outputs the result to a CSV file.

## GEX Formula

As per the whitepaper, Gamma Exposure is computed as:

- **Calls:** `GEX = Γ × OI × 1`  
- **Puts:** `GEX = Γ × OI × (-1)`

Where:
- `Γ` = option gamma
- `OI` = open interest

This simplified calculation assumes 1 contract = 1 unit exposure (Deribit doesn't use standard 100-share multipliers like SPX).

## Output Files

- `order_books.csv`: Cleaned options data including gamma, OI, strike, etc.
- `gex_results.csv`: GEX summary for each expiration, showing:
  - The call option with highest positive GEX.
  - The put option with most negative GEX.
  - Total net GEX for the expiration.

## Requirements

- Python 3
- `pandas`
- `requests`
