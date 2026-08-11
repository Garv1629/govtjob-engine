from typing import List
from app.modules.ai.schemas import StructuredJobExtraction, ExtractionConfidence
from app.core.logging import logger


class ConfidenceScoringEngine:
    """Computes objective confidence scores (0.0 to 1.0) based on field completeness and rule validation."""

    @staticmethod
    def compute_confidence(
        extraction: StructuredJobExtraction,
        errors: List[str],
        warnings: List[str]
    ) -> ExtractionConfidence:
        # 1. Base Score starts at 1.0
        score = 1.0

        # Critical errors heavily penalize score
        if len(errors) > 0:
            score -= 0.3 * len(errors)

        # Warnings lightly penalize score
        if len(warnings) > 0:
            score -= 0.05 * len(warnings)

        # Field completeness evaluation
        total_fields = 32
        filled_fields = 0

        data_dict = extraction.model_dump()
        for k, v in data_dict.items():
            if v is not None and v != "" and v != [] and v != {}:
                filled_fields += 1

        completeness_ratio = filled_fields / total_fields
        
        # Combine completeness ratio (40% weight) and validation score (60% weight)
        final_score = round(max(0.0, min(1.0, (score * 0.6) + (completeness_ratio * 0.4))), 2)

        mandatory_valid = len(errors) == 0

        logger.info(f"Confidence score computed: {final_score:.2f} (Completeness: {completeness_ratio*100:.1f}%)")

        return ExtractionConfidence(
            score=final_score,
            mandatory_fields_valid=mandatory_valid,
            validation_warnings=warnings,
            validation_errors=errors
        )
