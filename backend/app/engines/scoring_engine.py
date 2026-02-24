"""
Scoring Engine - Core scoring logic.

Implements deterministic, config-driven lead scoring with:
- Weighted feature contributions
- Recency decay
- Normalization to 0-100 scale
- Full explainability

Architecture:
- Config-driven weights (YAML)
- Interface-based design for future ML replacement
- Deterministic scoring
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime, timedelta
import yaml
from app.core.config import settings
from app.core.logging import logger


class ScoringStrategy(ABC):
    """Abstract base class for scoring strategies."""
    
    @abstractmethod
    def score(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a lead.
        
        Returns:
            Dictionary with 'score', 'contributions', and 'raw_scores'
        """
        pass


class ConfigDrivenScoringEngine(ScoringStrategy):
    """
    Production scoring engine using YAML configuration.
    
    Features:
    - Loads weights from YAML config
    - Applies feature weights
    - Calculates recency score
    - Normalizes to 0-100
    - Returns detailed contribution breakdown
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the scoring engine with configuration."""
        if config_path is None:
            config_path = settings.config_path
        
        self.config = self._load_config(config_path)
        self.weights = self.config.get('weights', {})
        self.recency_config = self.config.get('recency', {})
        logger.info(f"Scoring engine initialized with config from {config_path}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def score(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate lead score based on features and weights.
        
        Args:
            lead_data: Dictionary with lead features and enquiry_date
            
        Returns:
            Dictionary containing:
                - score: Final score 0-100
                - contributions: List of feature contributions
                - raw_scores: Raw scores before normalization
        """
        
        raw_scores = {}
        total_raw_score = 0
        total_weight = 0
        contributions_detail = []
        
        # Calculate base weighted scores
        for feature, weight_config in self.weights.items():
            weight = weight_config.get('weight', 0)
            
            # Check if feature is present and true in lead data
            if lead_data.get(feature, False):
                raw_scores[feature] = weight
                total_raw_score += weight
            else:
                raw_scores[feature] = 0
            
            total_weight += weight
        
        # Calculate recency score if enquiry_date is provided
        recency_score = self._calculate_recency_score(lead_data.get('enquiry_date'))
        total_raw_score += recency_score
        total_weight += self.recency_config.get('max_score', 10)
        
        # Normalize score to 0-100
        if total_weight > 0:
            normalized_score = min(100, (total_raw_score / total_weight) * 100)
        else:
            normalized_score = 0
        
        # Build contribution details (top contributors)
        for feature, raw_score in raw_scores.items():
            if raw_score > 0:
                contribution_pct = (raw_score / total_weight) * 100
                weight_config = self.weights.get(feature, {})
                contributions_detail.append({
                    'feature': feature,
                    'impact': contribution_pct,
                    'reason': weight_config.get('description', '')
                })
        
        # Add recency contribution if applicable
        if recency_score > 0:
            recency_pct = (recency_score / total_weight) * 100
            contributions_detail.append({
                'feature': 'recency',
                'impact': recency_pct,
                'reason': self.recency_config.get('description', '')
            })
        
        # Sort by impact descending
        contributions_detail.sort(key=lambda x: x['impact'], reverse=True)
        
        return {
            'score': normalized_score,
            'contributions': contributions_detail,
            'raw_scores': raw_scores,
            'recency_score': recency_score,
        }
    
    def _calculate_recency_score(self, enquiry_date: datetime = None) -> float:
        """
        Calculate recency score based on enquiry date.
        
        Formula: max(0, 15 - days_since_enquiry)
        
        Args:
            enquiry_date: Date of enquiry
            
        Returns:
            Recency score (0 to max_score)
        """
        if enquiry_date is None:
            return 0
        
        days_since = (datetime.utcnow() - enquiry_date).days
        days_decay = self.recency_config.get('days_decay', 15)
        max_score = self.recency_config.get('max_score', 10)
        
        recency_score = max(0, (days_decay - days_since) / days_decay * max_score)
        
        logger.debug(
            f"Recency score calculated: days_since={days_since}, "
            f"score={recency_score:.2f}"
        )
        
        return recency_score


class MLScoringInterface(ScoringStrategy):
    """
    Interface for future ML-based scoring.
    Allows seamless replacement of rule-based with ML models.
    """
    
    def score(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score using ML model."""
        raise NotImplementedError(
            "ML scoring not yet implemented. "
            "Use ConfigDrivenScoringEngine."
        )


# Default scoring engine instance
_scoring_engine = None


def get_scoring_engine() -> ScoringStrategy:
    """Get or create singleton scoring engine."""
    global _scoring_engine
    if _scoring_engine is None:
        _scoring_engine = ConfigDrivenScoringEngine()
    return _scoring_engine
