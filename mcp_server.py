# -*- coding: utf-8 -*-
"""
GenPark Amazon Author Ranker FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkAmazonAuthorRanker

mcp = FastMCP("genpark-amazon-author-ranker")
ranker = GenParkAmazonAuthorRanker()

@mcp.tool()
def estimate_daily_sales_velocity_from_bsr(
    bsr: int,
    category: str = "books",
    unit_price_usd: float = 14.99
) -> str:
    """
    Estimates daily unit sales velocity and revenue from Amazon Best Sellers Rank (BSR).
    """
    res = ranker.estimate_daily_sales_velocity_from_bsr(bsr, category, unit_price_usd)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_title_keyword_search_relevance(
    title: str,
    subtitle: str,
    keywords_json: str
) -> str:
    """
    Calculates title keyword SEO relevance score with front-loaded weighting.
    """
    kws = json.loads(keywords_json)
    res = ranker.calculate_title_keyword_search_relevance(title, subtitle, kws)
    return json.dumps(res, indent=2)

@mcp.tool()
def model_bsr_ranking_decay_half_life(
    current_bsr: int,
    daily_organic_sales: float,
    target_bsr: int = 1000,
    half_life_days: float = 7.0
) -> str:
    """
    Models Amazon ranking decay inertia over 14 days and promotional units needed.
    """
    res = ranker.model_bsr_ranking_decay_half_life(current_bsr, daily_organic_sales, target_bsr, half_life_days)
    return json.dumps(res, indent=2)

def main():
    print("Testing Amazon Author Ranker:")
    print(estimate_daily_sales_velocity_from_bsr(1250, "books"))

if __name__ == "__main__":
    main()
