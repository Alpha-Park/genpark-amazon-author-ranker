# genpark-amazon-author-ranker

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-zero-success)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

GenPark Amazon Author Ranker is a zero-dependency Amazon KDP publishing and BSR algorithmic analytics engine implementing power-law log-log daily sales velocity conversion models, front-loaded title keyword SEO relevance scoring, and rank decay half-life projection curves.

```mermaid
flowchart TD
    A[Amazon Best Sellers Rank BSR] --> B[Power-Law Log-Log Regression Model]
    B --> C[Daily & Monthly Unit Sales and Revenue]
    D[Book Title & Subtitle Tokens] --> E[Front-Loaded Keyword Scoring]
    E --> F[Amazon Search Relevance Index]
    G[Current Rank & Target BSR] --> H[Half-Life Inertia Decay Engine]
    H --> I[Promotional Burst Units Required]
```

## Features
- **BSR Sales Velocity Model**: Maps category ranks to exact daily unit velocities and monthly revenue using empirical power-law formulas.
- **Title SEO Keyword Scoring**: Evaluates front-loaded title positioning, subtitle coverage, and search index density.
- **Ranking Decay Half-Life**: Projects natural rank slippage and quantifies the exact promotional sales volume needed to breach bestseller thresholds.

## Quickstart

```python
from client import GenParkAmazonAuthorRanker

ranker = GenParkAmazonAuthorRanker()
res = ranker.estimate_daily_sales_velocity_from_bsr(1000, "books")
print("Daily Units:", res["estimated_daily_sales_units"])
```

## License
MIT
