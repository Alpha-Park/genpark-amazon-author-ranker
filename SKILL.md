---
description: Author Performance Ranker. Tracks and analyzes creator/author performance across multi-year datasets based on feedback and frequency.
license: MIT
metadata:
  last_deployed: "2026-04-25"
  version: "1.0.0"
  source: "https://github.com/anikaahluwalia/amazon-best-sellers-analysis"
---

# Amazon Author Ranker

This skill focuses on the "human element" of e-commerce data. It ranks and analyzes authors or creators based on their longitudinal performance, helping identifying consistent "hits" and rising stars.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Instructions
1. **Consistency Tracking:** Count occurrences of a specific author/creator across multi-year datasets to measure market longevity.
2. **Quality Scoring:** Weight rankings by average user ratings and total review counts to ensure quality is prioritized over volume.
3. **Sentiment Extraction:** (If text data is available) Summarize general customer sentiment toward specific authors.
4. **Output:** Generate a leaderboard of creators with detailed metrics on their average price point and rating stability.

## Examples
- "Who are the most consistent best-selling authors in the Non-Fiction category from 2010 to 2020?"
- "Rank authors in this dataset by a combination of their total number of best-sellers and their average user rating."
