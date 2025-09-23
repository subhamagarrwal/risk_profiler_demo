from pydantic import BaseModel, Field, model_validator, ConfigDict, field_validator
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

# class RiskProfile(BaseModel):
#     goal: str
#     timeline_years: float
#     loss_aversion: LossAversion
#     liquidity_need: LiquidityNeed
#     income_stability: IncomeStability
#     knowledge_level: KnowledgeLevel
#     notes: str
#     confidences: Optional[Dict[str, float]] = None
from typing import Optional
from pydantic import BaseModel, Field

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pydantic_core import PydanticUndefined

class Confidences(BaseModel):
    timeline_years: float = Field(default=3.0)
    loss_aversion: float = Field(default=0.5)
    liquidity_need: float = Field(default=0.5)

    model_config = ConfigDict(validate_default=True)

    @model_validator(mode='before')
    def none_to_default(cls, values):
        # values is the raw input (likely a dict) before parsing
        if not isinstance(values, dict):
            return values
        for name, field in cls.model_fields.items():
            if name in values and values[name] is None:
                # respect default/default_factory
                values[name] = field.get_default(call_default_factory=True)
        return values


# --- RiskProfile: per-field normalization for Enums (None → enum default) ---
class RiskProfile(BaseModel):
    goal: Optional[str] = Field(default="steady growth")
    timeline_years: Optional[float] = Field(default=5.0)

    loss_aversion: LossAversion = Field(default=LossAversion.moderate)
    liquidity_need: LiquidityNeed = Field(default=LiquidityNeed.moderate)
    income_stability: IncomeStability = Field(default=IncomeStability.variable)
    knowledge_level: KnowledgeLevel = Field(default=KnowledgeLevel.novice)

    notes: Optional[str] = Field(default="")
    confidences: Confidences = Field(default_factory=Confidences)

    model_config = ConfigDict(validate_default=True)

    # For enum fields, intercept None BEFORE enum coercion:
    @field_validator("loss_aversion", mode="before")
    def _loss_aversion_default(cls, v):
        return v or LossAversion.moderate

    @field_validator("liquidity_need", mode="before")
    def _liquidity_need_default(cls, v):
        return v or LiquidityNeed.moderate

    @field_validator("income_stability", mode="before")
    def _income_stability_default(cls, v):
        return v or IncomeStability.variable

    @field_validator("knowledge_level", mode="before")
    def _knowledge_level_default(cls, v):
        return v or KnowledgeLevel.novice

    # (Optional) keep this if you want dict-wide cleanup for other fields
    @model_validator(mode='before')
    def none_to_default(cls, values):
        if not isinstance(values, dict):
            return values
        for name, field in cls.model_fields.items():
            if name in values and values[name] is None:
                # for non-enum fields, let defaults apply
                values[name] = field.get_default(call_default_factory=True)
        return values


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
