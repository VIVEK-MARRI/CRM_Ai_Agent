"""
Next Best Action Engine - Recommends actions based on lead score.

Implements score-to-action mapping:
- 80-100: Immediate sales call
- 60-79: Pricing + Follow-up
- 40-59: Nurture campaign
- <40: Automated drip

Design: Service layer with configurable mappings
"""

from typing import Dict, Any
import yaml
from app.core.config import settings
from app.core.logging import logger


class NextActionEngine:
    """
    Recommends next best action based on lead score.
    
    Provides:
    - Action recommendation
    - Urgency classification
    - Conversion probability
    - Rationale
    """
    
    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = settings.config_path
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.actions = self.config.get('recommended_actions', {})
        self.probabilities = self.config.get('conversion_probabilities', {})
        logger.info("Next action engine initialized")
    
    def get_action(self, score: float) -> Dict[str, Any]:
        """
        Get recommended action for a score.
        
        Args:
            score: Lead score (0-100)
            
        Returns:
            Dictionary with:
                - action: Recommended next action
                - urgency: Urgency level
                - probability: Conversion probability
                - rationale: Explanation
        """
        
        action_key = self._get_action_key(score)
        action_config = self.actions.get(action_key, {})
        prob_config = self.probabilities.get(action_key, {})
        
        recommendation = {
            'action': action_config.get('action', 'No action'),
            'urgency': action_config.get('urgency', 'Low'),
            'probability_label': action_config.get('probability_label', '<20%'),
            'probability': prob_config.get('probability', 0),
            'score_bracket': action_key,
            'rationale': self._generate_rationale(score, action_config)
        }
        
        logger.debug(f"Action recommended for score {score}: {action_config.get('action')}")
        
        return recommendation
    
    def _get_action_key(self, score: float) -> str:
        """Determine action bucket based on score."""
        if score >= 80:
            return 'score_80_100'
        elif score >= 60:
            return 'score_60_79'
        elif score >= 40:
            return 'score_40_59'
        else:
            return 'score_below_40'
    
    def _generate_rationale(
        self,
        score: float,
        action_config: Dict[str, Any]
    ) -> str:
        """Generate explanation for the recommended action."""
        
        urgency = action_config.get('urgency', 'Low')
        
        rationales = {
            'Immediate': f"Lead shows strong buying signals (Score: {score:.0f}). "
                        "High conversion probability. Prioritize immediate engagement.",
            'High': f"Lead demonstrates significant interest (Score: {score:.0f}). "
                   "Schedule follow-up to advance sales cycle.",
            'Medium': f"Lead shows moderate intent (Score: {score:.0f}). "
                     "Continue nurturing through targeted content.",
            'Low': f"Lead is in early awareness stage (Score: {score:.0f}). "
                  "Build relationship through educational content."
        }
        
        return rationales.get(urgency, "Continue with appropriate action")
    
    def get_bulk_actions(self, leads_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Get actions for multiple leads.
        
        Args:
            leads_scores: Dictionary of lead_id -> score
            
        Returns:
            Dictionary of lead_id -> action recommendation
        """
        result = {}
        for lead_id, score in leads_scores.items():
            result[lead_id] = self.get_action(score)
        
        return result


def get_action_engine() -> NextActionEngine:
    """Get or create singleton action engine."""
    return NextActionEngine()
