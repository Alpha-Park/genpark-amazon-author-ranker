# -*- coding: utf-8 -*-
import json
from client import GenParkAmazonAuthorRanker

ranker = GenParkAmazonAuthorRanker()

# 1. BSR to Daily Sales & Revenue Estimation
sales = ranker.estimate_daily_sales_velocity_from_bsr(bsr=1250, category="books", unit_price_usd=16.99)
print(f"Amazon BSR 1250: DailyUnits={sales['estimated_daily_sales_units']} | MonthlyUnits={sales['estimated_monthly_sales_units']} | MonthlyRev=${sales['estimated_monthly_revenue_usd']} ({sales['bsr_tier']})")

# 2. Title & Subtitle Keyword SEO Relevance
keywords = ["artificial intelligence", "autonomous agents", "python", "machine learning"]
seo = ranker.calculate_title_keyword_search_relevance(
    title="Autonomous Agents with Python",
    subtitle="A Comprehensive Guide to Artificial Intelligence and LLM Orchestration",
    keywords=keywords
)
print()
print(f"Keyword Relevance: Score={seo['relevance_score']}/100 ({seo['seo_rating']})")
for m in seo["keyword_matches"]:
    print(f"  '{m['keyword']}': TitleFront={m['in_title_front']} | Subtitle={m['in_subtitle']} -> Weight: {m['score_weight']}")

# 3. Ranking Decay & Target BSR Gap Analysis
decay = ranker.model_bsr_ranking_decay_half_life(current_bsr=8500, daily_organic_sales=6.0, target_bsr=1000)
print()
print(f"BSR Gap Analysis: Current BSR {decay['current_bsr']} -> Target BSR {decay['target_bsr']}")
print(f"  Daily Sales Gap: {decay['daily_sales_gap_to_target']} units/day | 7-Day Promo Needed: {decay['7_day_promotional_burst_units']} units")
