from typing import Dict, List


class AnalysisService:

    def analyze(self, tests:List[Dict]) -> Dict:
        """
        Deterministic analysis: compute status (low/normal/high), collect warnings and build facts.
        Returns dict with:
         - warnings: list[str]
         - facts: { "high": [...], "low": [...], "normal": [...] }
         - results: list[per-test detailed dict]
        """

        warnings = []
        high = []
        low = []
        normal = []
        results = []

        for t in tests:
            analyte = t.get('analyte') or "unknown"
            value = t.get("value")
            low_bound = t.get("normal_low")
            high_bound = t.get("normal_high")
            status = "unknown"
            interpretation = "No interpretation available."

            try:
                if low_bound is not None and value < low_bound:
                    status ="low"
                    low.append(analyte)
                    interpretation = f"{analyte} is below normal ({value} < {low_bound})."
                    warnings.append(f"{analyte}: {value}{t.get('unit', '')} is below normal ({low_bound}-{high_bound})")
                elif high_bound is not None and value > high_bound:
                    status ="high"
                    high.append(analyte)
                    interpretation = f"{analyte} is above normal ({value} > {high_bound})."
                    warnings.append(f"{analyte}: {value}{t.get('unit', '')} is above normal ({low_bound}-{high_bound})")
                else:
                    status = "normal"
                    normal.append(analyte)
                    interpretation = f"{analyte} is within normal range."
            except Exception:
                status = "unknown"
                interpretation = "Unable to determine status."
            
            results.append({
                "analyte": analyte,
                "value": value,
                "unit": t.get("unit"),
                "normal_range": {"low": low_bound, "high": high_bound},
                "status": status,
                "interpretation": interpretation
            })

        abnormal_count = len(low) + len(high)
        if abnormal_count == 0:
            risk = "low"
        elif abnormal_count <= 2:
            risk = "moderate"
        else:
            risk = "elevated"

        facts = {"high": high, "low": low, "normal": normal}
        return {
            "warnings": warnings,
            "analysis": {"abnormal_count": abnormal_count, "risk_level": risk},
            "facts": facts,
            "results": results
        }


