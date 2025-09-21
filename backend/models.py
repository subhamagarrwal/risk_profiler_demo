from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from enum import Enum

class LossAversion(str, Enum):
    very_low = "very_low"
    low = "low"
    moderate = "moderate"
    high = "high"
    very_high = "very_high"

class LiquidityNeed(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"

class IncomeStability(str, Enum):
    stable = "stable"
    variable = "variable"
    unstable = "unstable"

class KnowledgeLevel(str, Enum):
    novice = "novice"
    intermediate = "intermediate"
    advanced = "advanced"

class Variant(str, Enum):
    baseline = "baseline"
    defensive = "defensive"
    aggressive = "aggressive"

class UserAnswers(BaseModel):
    answer1: str  # 20% drop question
    answer2: str  # growth vs stability question  
    answer3: str  # cash needs question

class ProfileRequest(BaseModel):
    answers: UserAnswers

class RiskProfile(BaseModel):
    goal: str
    timeline_years: float
    loss_aversion: LossAversion
    liquidity_need: LiquidityNeed
    income_stability: IncomeStability
    knowledge_level: KnowledgeLevel
    notes: str
    confidences: Optional[Dict[str, float]] = None

class ProfileResponse(BaseModel):
    profile: RiskProfile
    axes: Dict[str, float]
    score: float
    label: str

class WeightsRequest(BaseModel):
    label: str
    variant: Variant
    axes: Dict[str, float]

class WeightsResponse(BaseModel):
    weights: Dict[str, float]
    explanations: List[str]

class AnalyticsRequest(BaseModel):
    user_weights: Dict[str, float]
    label: str
    axes: Dict[str, float]

class PerformanceMetrics(BaseModel):
    CAGR_pct: float
    Vol_ann_pct: float
    MaxDD_pct: float
    Worst_12m_pct: float
    Recovery_m: Optional[int]

class PortfolioAnalysis(BaseModel):
    name: str
    weights: Dict[str, float]
    metrics: PerformanceMetrics
    explanation: str

class ChartData(BaseModel):
    dates: List[str]
    values: List[float]

class AnalyticsResponse(BaseModel):
    portfolios: List[PortfolioAnalysis]
    growth_chart: Dict[str, ChartData]
    drawdown_chart: Dict[str, ChartData]
    comparisons: List[str]