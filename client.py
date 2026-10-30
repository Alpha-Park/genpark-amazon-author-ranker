# -*- coding: utf-8 -*-
"""
GenPark Amazon Author Ranker Client
Zero-dependency Amazon Best Sellers Rank (BSR) daily sales velocity power-law modeler,
keyword title search relevance scorer, and ranking decay half-life forecaster.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkAmazonAuthorRanker:
    """
    Models Amazon BSR to daily sales conversions, scores title search relevance,
    and estimates rank decay half-life.
    """

    # Category calibrated log-log parameters: ln(Sales) = alpha - beta * ln(BSR)
    CATEGORY_MODELS = {
        "books": {"alpha": 10.5, "beta": 0.82},
        "kindle": {"alpha": 11.2, "beta": 0.86},
        "audiobooks": {"alpha": 9.4, "beta": 0.78}
    }

    def estimate_daily_sales_velocity_from_bsr(
        self,
        bsr: int,
        category: str = "books",
        unit_price_usd: float = 14.99
    ) -> Dict[str, Any]:
        """
        Estimates daily unit sales velocity and revenue from Amazon Best Sellers Rank (BSR) using power-law regression:
        Sales = exp(alpha) * BSR^(-beta)
        """
        if bsr <= 0:
            raise ValueError("BSR must be a strictly positive integer.")

        model = self.CATEGORY_MODELS.get(category.lower(), self.CATEGORY_MODELS["books"])
        alpha = model["alpha"]
        beta = model["beta"]

        # Power law conversion
        estimated_daily_units = math.exp(alpha) * math.pow(bsr, -beta)
        estimated_daily_units = max(0.1, round(estimated_daily_units, 1))

        estimated_monthly_units = int(round(estimated_daily_units * 30.4))
        daily_revenue = round(estimated_daily_units * unit_price_usd, 2)
        monthly_revenue = round(estimated_monthly_units * unit_price_usd, 2)

        return {
            "bsr": bsr,
            "category": category,
            "unit_price_usd": unit_price_usd,
            "estimated_daily_sales_units": estimated_daily_units,
            "estimated_monthly_sales_units": estimated_monthly_units,
            "estimated_daily_revenue_usd": daily_revenue,
            "estimated_monthly_revenue_usd": monthly_revenue,
            "bsr_tier": "TOP_BESTSELLER" if bsr <= 500 else ("HIGH_VELOCITY" if bsr <= 5000 else ("MODERATE_MOVER" if bsr <= 50000 else "LONG_TAIL"))
        }

    def calculate_title_keyword_search_relevance(
        self,
        title: str,
        subtitle: str,
        keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Calculates title keyword SEO relevance score: front-loaded title words receive 2x weight, subtitle receives 1x.
        """
        if not title:
            raise ValueError("Book title cannot be empty.")

        title_words = [w.strip(" .,!?:;()[]{}").lower() for w in title.split()]
        subtitle_words = [w.strip(" .,!?:;()[]{}").lower() for w in subtitle.split()]

        keyword_matches = []
        total_score = 0.0

        for kw in keywords:
            kw_clean = kw.strip().lower()
            kw_tokens = kw_clean.split()
            
            # Check title match
            in_title_front = any(token in title_words[:5] for token in kw_tokens)
            in_title = any(token in title_words for token in kw_tokens)
            in_subtitle = any(token in subtitle_words for token in kw_tokens)

            match_weight = 0.0
            if in_title_front:
                match_weight = 40.0
            elif in_title:
                match_weight = 25.0
            elif in_subtitle:
                match_weight = 15.0

            total_score += match_weight
            keyword_matches.append({
                "keyword": kw,
                "in_title_front": in_title_front,
                "in_title": in_title,
                "in_subtitle": in_subtitle,
                "score_weight": match_weight
            })

        max_possible = len(keywords) * 40.0 if keywords else 100.0
        normalized_score = round(min(100.0, 100.0 * total_score / max(1.0, max_possible)), 1)

        return {
            "title": title,
            "subtitle": subtitle,
            "keywords_audited": len(keywords),
            "relevance_score": normalized_score,
            "keyword_matches": keyword_matches,
            "seo_rating": "OPTIMAL_TITLE_SEO" if normalized_score >= 75.0 else ("FAIR" if normalized_score >= 50.0 else "POOR_KEYWORDS")
        }

    def model_bsr_ranking_decay_half_life(
        self,
        current_bsr: int,
        daily_organic_sales: float,
        target_bsr: int = 1000,
        half_life_days: float = 7.0
    ) -> Dict[str, Any]:
        """
        Models Amazon ranking decay inertia over 14 days and calculates promotional units needed to reach target BSR.
        """
        decay_constant = math.log(2.0) / half_life_days
        projections = []

        # Current vs target daily units needed
        curr_units = self.estimate_daily_sales_velocity_from_bsr(current_bsr)["estimated_daily_sales_units"]
        target_units = self.estimate_daily_sales_velocity_from_bsr(target_bsr)["estimated_daily_sales_units"]

        daily_gap_units = max(0.0, target_units - daily_organic_sales)

        curr_rank = float(current_bsr)
        for day in [1, 3, 7, 14]:
            # Decay drift towards baseline without promotion
            drift_factor = math.exp(decay_constant * day * 0.4)
            projected_rank = int(round(curr_rank * drift_factor))
            projections.append({
                "day": day,
                "projected_unpromoted_bsr": projected_rank
            })

        return {
            "current_bsr": current_bsr,
            "target_bsr": target_bsr,
            "target_daily_sales_units_needed": target_units,
            "current_organic_sales_units": daily_organic_sales,
            "daily_sales_gap_to_target": round(daily_gap_units, 1),
            "7_day_promotional_burst_units": round(daily_gap_units * 7.0, 0),
            "ranking_decay_half_life_days": half_life_days,
            "projections": projections
        }
