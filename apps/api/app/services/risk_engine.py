"""Risk engine with deterministic checks"""
from typing import List, Dict, Any


class RiskEngine:
    """Risk management engine"""
    
    def __init__(self, 
                 min_confidence: float = 0.6,
                 max_candidates: int = 20,
                 max_position_pct: float = 0.1):
        self.min_confidence = min_confidence
        self.max_candidates = max_candidates
        self.max_position_pct = max_position_pct
    
    def check_candidate(self, candidate: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check a single trade candidate"""
        flags = []
        
        # Check confidence threshold
        if candidate.get("conviction", 0) < self.min_confidence:
            flags.append(f"low_confidence_{candidate.get('conviction', 0):.2f}")
        
        # Check for missing required fields
        if not candidate.get("asset_id"):
            flags.append("missing_asset_id")
        
        if not candidate.get("thesis"):
            flags.append("missing_thesis")
        
        # Check conviction is reasonable
        conviction = candidate.get("conviction", 0)
        if conviction > 1.0 or conviction < 0:
            flags.append("invalid_conviction")
        
        return len(flags) == 0, flags
    
    def filter_candidates(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Filter candidates through risk checks"""
        accepted = []
        rejected = []
        all_flags = []
        
        for candidate in candidates:
            is_valid, flags = self.check_candidate(candidate)
            
            if is_valid:
                accepted.append(candidate)
            else:
                rejected.append({
                    "candidate": candidate,
                    "flags": flags
                })
                all_flags.extend(flags)
        
        # Apply max candidates limit
        if len(accepted) > self.max_candidates:
            # Sort by conviction and take top N
            accepted = sorted(accepted, 
                            key=lambda x: x.get("conviction", 0), 
                            reverse=True)[:self.max_candidates]
        
        return {
            "accepted": accepted,
            "rejected": rejected,
            "flags": list(set(all_flags)),
            "summary": {
                "total": len(candidates),
                "accepted_count": len(accepted),
                "rejected_count": len(rejected),
            }
        }
