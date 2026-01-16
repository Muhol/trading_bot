class SignalValidator:

    MIN_RR = 2.0

    @staticmethod
    def validate(signal_data: dict) -> tuple[bool, str]:
        if not signal_data.get("stop_loss"):
            return False, "Missing stop loss"

        if not signal_data.get("take_profit"):
            return False, "Missing take profit"

        entry = signal_data["entry_price"]
        sl = signal_data["stop_loss"]
        tp = signal_data["take_profit"]

        risk = abs(entry - sl)
        reward = abs(tp - entry)

        if risk <= 0:
            return False, "Invalid stop loss distance"

        rr = reward / risk

        if rr < SignalValidator.MIN_RR:
            return False, f"RR too low ({round(rr,2)})"

        return True, "VALID"
