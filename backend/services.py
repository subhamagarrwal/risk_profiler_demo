import sys
import os

# Add parent directory to path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import requests
from jsonschema import validate, ValidationError
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any

from get_json import (
    SCHEMA, call_ollama, composite, choose_weights, 
    align_weights, explain_mix, compare_sentence, drawdown,
    enum_map_loss, map_liq, map_income, map_knowledge, map_horizon
)
from backtest import download_sleeves, cagr, max_drawdown, time_to_recover
from models import *

class RiskProfilerService:
    def __init__(self):
        self.tickers = {
            "equity": "NIFTYBEES.NS",
            "bonds": "NETFLTGILT.NS", 
            "cash": "LIQUIDBEES.NS"
        }
        self._cached_data = None
    
    def create_prompt(self, answers: UserAnswers) -> str:
        """Create LLM prompt from user answers"""
        return f"""
Return ONLY valid JSON. JSON Schema:
{json.dumps(SCHEMA)}

Conversation:
- If your portfolio dropped 20% in a year, what would you do?
  -> {answers.answer1}
- What excites you more: steady growth or high gains with volatility?
  -> {answers.answer2}
- Any large cash needs next 2–3 years?
  -> {answers.answer3}

Now produce the JSON object (no prose, no extra keys).
"""

    def generate_profile(self, answers: UserAnswers) -> ProfileResponse:
        """Generate risk profile from user answers"""
        prompt = self.create_prompt(answers)
        
        try:
            # Call LLM using the same function from get_json.py
            raw = call_ollama(prompt)
            obj = json.loads(raw)
            validate(instance=obj, schema=SCHEMA)
        except (json.JSONDecodeError, ValidationError) as e:
            # Retry once if validation fails (same logic as get_json.py)
            retry_prompt = prompt + f"\nPrevious output failed schema validation: {e}. Return ONLY corrected JSON."
            raw = call_ollama(retry_prompt)
            obj = json.loads(raw)
            validate(instance=obj, schema=SCHEMA)
        except Exception as e:
            # If Ollama fails, provide a more helpful error
            raise Exception(f"Failed to connect to Ollama service: {str(e)}. Make sure Ollama is running on localhost:11434 with the 'risk-profiler' model.")
        
        # Create profile object
        profile = RiskProfile(**obj)
        
        # Calculate axes using the exact same functions as get_json.py
        axes = {
            "time_horizon": map_horizon(profile.timeline_years),
            "loss_aversion": enum_map_loss(profile.loss_aversion.value),
            "liquidity": map_liq(profile.liquidity_need.value),
            "income_stability": map_income(profile.income_stability.value),
            "knowledge_caution": map_knowledge(profile.knowledge_level.value),
        }
        
        # Calculate score and label using the exact same function as get_json.py
        score, label = composite(obj)
        
        return ProfileResponse(
            profile=profile,
            axes=axes,
            score=score,
            label=label
        )
    
    def calculate_weights(self, request: WeightsRequest) -> WeightsResponse:
        """Calculate investment weights with guardrails"""
        weights = choose_weights(request.label, request.variant.value, request.axes)
        
        # Generate explanations for guardrails
        explanations = []
        
        if request.axes.get("liquidity", 0) >= 0.75:
            explanations.append("Increased cash allocation to 10% minimum due to high liquidity needs")
        
        if request.axes.get("loss_aversion", 0) >= 0.75:
            explanations.append("Capped equity at 50% maximum due to high loss aversion")
        
        if request.variant == Variant.defensive:
            explanations.append("Applied defensive variant with reduced equity allocation")
        elif request.variant == Variant.aggressive:
            explanations.append("Applied aggressive variant with increased equity allocation")
        
        if not explanations:
            explanations.append("Using baseline allocation with no significant adjustments needed")
        
        return WeightsResponse(
            weights=weights,
            explanations=explanations
        )
    
    def _get_market_data(self) -> pd.DataFrame:
        """Get or cache market data"""
        if self._cached_data is None:
            prices = download_sleeves(self.tickers, start="2014-01-01")
            mclose = prices.resample("ME").last()
            self._cached_data = mclose.pct_change().dropna()
        
        return self._cached_data
    
    def run_analytics(self, request: AnalyticsRequest) -> AnalyticsResponse:
        """Run backtesting analytics"""
        rets = self._get_market_data()
        
        if rets.empty:
            raise ValueError("Empty returns data - check ticker dates")
        
        # Define comparison portfolios
        compare_portfolios = {
            "Your Mix": request.user_weights,
            "Defensive": choose_weights(request.label, "defensive", request.axes),
            "Aggressive": choose_weights(request.label, "aggressive", request.axes),
            "60/40": {"equity": 0.60, "bonds": 0.40, "cash": 0.0},
            "All Equity": {"equity": 1.0, "bonds": 0.0, "cash": 0.0}
        }
        
        # Run backtests
        portfolios = []
        curves = {}
        growth_chart_data = {}
        drawdown_chart_data = {}
        
        for name, weights in compare_portfolios.items():
            # Align weights and calculate returns
            wts_aligned = align_weights(weights, rets.columns)
            port_rets = rets.dot(wts_aligned)
            curve = (1 + port_rets).cumprod()
            curves[name] = curve
            
            # Calculate metrics
            metrics = PerformanceMetrics(
                CAGR_pct=round(cagr(curve) * 100, 2),
                Vol_ann_pct=round(port_rets.std() * np.sqrt(12) * 100, 2),
                MaxDD_pct=round(max_drawdown(curve) * 100, 2),
                Worst_12m_pct=round(port_rets.rolling(12).apply(lambda x: np.prod(1+x)-1).min() * 100, 2),
                Recovery_m=time_to_recover(curve)
            )
            
            # Generate explanation
            explanation = explain_mix(name, {
                "CAGR_%": metrics.CAGR_pct,
                "Vol_ann_%": metrics.Vol_ann_pct,
                "MaxDD_%": metrics.MaxDD_pct,
                "Worst_12m_%": metrics.Worst_12m_pct,
                "Recovery_m": metrics.Recovery_m
            })
            
            portfolios.append(PortfolioAnalysis(
                name=name,
                weights=weights,
                metrics=metrics,
                explanation=explanation
            ))
            
            # Prepare chart data
            dates = [d.strftime("%Y-%m") for d in curve.index]
            growth_chart_data[name] = ChartData(dates=dates, values=curve.tolist())
            
            # Drawdown data
            dd = drawdown(curve) * 100  # Convert to percentage
            drawdown_chart_data[name] = ChartData(dates=dates, values=dd.tolist())
        
        # Generate comparisons
        comparisons = []
        user_metrics = next(p.metrics for p in portfolios if p.name == "Your Mix")
        for portfolio in portfolios:
            if portfolio.name != "Your Mix":
                comparison = compare_sentence(
                    "Your Mix", 
                    {
                        "CAGR_%": user_metrics.CAGR_pct,
                        "Vol_ann_%": user_metrics.Vol_ann_pct,
                        "MaxDD_%": user_metrics.MaxDD_pct
                    },
                    portfolio.name,
                    {
                        "CAGR_%": portfolio.metrics.CAGR_pct,
                        "Vol_ann_%": portfolio.metrics.Vol_ann_pct,
                        "MaxDD_%": portfolio.metrics.MaxDD_pct
                    }
                )
                comparisons.append(comparison)
        
        return AnalyticsResponse(
            portfolios=portfolios,
            growth_chart=growth_chart_data,
            drawdown_chart=drawdown_chart_data,
            comparisons=comparisons
        )