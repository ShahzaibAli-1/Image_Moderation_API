from google.cloud import vision
from PIL import Image
import io
import os
from typing import Dict, Any

class ImageModerator:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        
    async def analyze_image(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze an image for harmful content using Google Cloud Vision API."""
        try:
            # Create image object
            image = vision.Image(content=image_data)
            
            # Perform safe search detection
            safe_search = self.client.safe_search_detection(image=image).safe_search_annotation
            
            # Perform label detection for additional context
            labels = self.client.label_detection(image=image).label_annotations
            
            # Map Google's likelihood to probability scores
            likelihood_map = {
                vision.Likelihood.UNKNOWN: 0.0,
                vision.Likelihood.VERY_UNLIKELY: 0.1,
                vision.Likelihood.UNLIKELY: 0.3,
                vision.Likelihood.POSSIBLE: 0.5,
                vision.Likelihood.LIKELY: 0.7,
                vision.Likelihood.VERY_LIKELY: 0.9
            }
            
            # Calculate overall safety score
            safety_scores = {
                "violence": likelihood_map[safe_search.violence],
                "nudity": likelihood_map[safe_search.adult],
                "hate_symbols": self._check_hate_symbols(labels),
                "self_harm": self._check_self_harm(labels),
                "extremist_content": self._check_extremist_content(labels)
            }
            
            # Determine if image is safe (threshold at 0.7)
            is_safe = all(score < 0.7 for score in safety_scores.values())
            
            # Calculate overall confidence
            confidence = 1.0 - max(safety_scores.values())
            
            return {
                "safe": is_safe,
                "categories": safety_scores,
                "confidence": confidence,
                "labels": [label.description for label in labels[:5]]  # Top 5 labels
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
    
    def _check_hate_symbols(self, labels) -> float:
        """Check for hate symbols in image labels."""
        hate_indicators = {'hate', 'symbol', 'flag', 'gesture', 'sign'}
        return max(
            (label.score for label in labels 
             if any(indicator in label.description.lower() for indicator in hate_indicators)),
            default=0.0
        )
    
    def _check_self_harm(self, labels) -> float:
        """Check for self-harm indicators in image labels."""
        self_harm_indicators = {'self-harm', 'suicide', 'cut', 'wound', 'blood'}
        return max(
            (label.score for label in labels 
             if any(indicator in label.description.lower() for indicator in self_harm_indicators)),
            default=0.0
        )
    
    def _check_extremist_content(self, labels) -> float:
        """Check for extremist content indicators in image labels."""
        extremist_indicators = {'weapon', 'terrorism', 'extremist', 'radical', 'protest'}
        return max(
            (label.score for label in labels 
             if any(indicator in label.description.lower() for indicator in extremist_indicators)),
            default=0.0
        ) 