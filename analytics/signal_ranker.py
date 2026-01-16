class SignalRanker:

    @staticmethod
    def score(signal: dict) -> float:
        score = 0

        score += signal.get("confidence_percent", 0) * 0.4
        score += signal.get("rr_ratio", 0) * 20
        score += min(signal.get("volatility", 0.0), 0.02) * 1000

        return round(score, 2)

    @staticmethod
    def is_high_profit(signal: dict) -> bool:
        return (
            signal.get("confidence_percent", 0) >= 80
            and signal.get("rr_ratio", 0) >= 3
        )
