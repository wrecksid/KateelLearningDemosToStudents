# Mesa Liquidity Data Generator

## Overview

This folder contains a synthetic financial transaction data generator intended for agent-based or simulation-style liquidity management exercises. It is a useful foundation when students want richer banking datasets with customers, accounts, balances, transactions, and liquidity-oriented attributes.

The generator is especially suitable for experimentation, simulation backlogs, and future extensions using Mesa or other agent-based modeling tools.

## Files in This Folder

- `data_generator.py` creates synthetic banking customers, accounts, and transactions for liquidity-oriented analysis

## What This Folder Is Best For

- creating richer synthetic BFSI datasets
- supporting future liquidity simulation work
- classroom experiments around customer segments, balances, channels, and transaction behavior

## How To Run

```powershell
python data_generator.py --help
```

Start with a small dataset first, then scale up after verifying the output structure.

## Suggested Uses In The Course

- payments and transaction flow simulations
- liquidity and treasury case discussions
- operational risk and monitoring exercises
- data engineering practice before modeling

## Suggested Next Improvements

- add a notebook that visualizes generated liquidity metrics
- add a sample output file and schema description
- add a Mesa simulation example that consumes this generated data
- add a README section describing the command-line options in detail
