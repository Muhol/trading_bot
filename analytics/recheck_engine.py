from enum import Enum


class MarketState(str, Enum):
    TREND_MISMATCH = "TREND_MISMATCH"
    RANGING = "RANGING"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    OVEREXTENDED = "OVEREXTENDED"
    PULLBACK_PENDING = "PULLBACK_PENDING"
    BREAKOUT_SETUP = "BREAKOUT_SETUP"
    CHOPPY_HIGH_VOL = "CHOPPY_HIGH_VOL"


TIMEFRAME_MINUTES = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


STATE_TO_CANDLES = {
    MarketState.TREND_MISMATCH: 2,
    MarketState.RANGING: 3,
    MarketState.LOW_VOLATILITY: 4,
    MarketState.OVEREXTENDED: 2,
    MarketState.PULLBACK_PENDING: 1,
    MarketState.BREAKOUT_SETUP: 1,
    MarketState.CHOPPY_HIGH_VOL: 5,
}


class RecheckDecisionEngine:
    @staticmethod
    def determine_state(
        signal: str,
        trend: str,
        rsi: float,
        volatility: float,
        ema_slope: float,
        atr_threshold: float = 0.001
    ) -> MarketState:
        """
        Decide WHY there is no trade.
        Priority-based classification.
        """

        # 1️⃣ Choppy / high volatility chaos
        if volatility > atr_threshold * 3 and abs(ema_slope) < atr_threshold:
            return MarketState.CHOPPY_HIGH_VOL

        # 2️⃣ Trend mismatch
        if signal in ("BUY", "SELL") and (
            (signal == "BUY" and trend != "Bullish") or
            (signal == "SELL" and trend != "Bearish")
        ):
            return MarketState.TREND_MISMATCH

        # 3️⃣ Low volatility
        if volatility < atr_threshold:
            return MarketState.LOW_VOLATILITY

        # 4️⃣ Overextended momentum
        if rsi >= 70 or rsi <= 30:
            return MarketState.OVEREXTENDED

        # 5️⃣ Pullback pending
        if abs(ema_slope) > atr_threshold and signal == "NONE":
            return MarketState.PULLBACK_PENDING

        # 6️⃣ Ranging default
        return MarketState.RANGING

    @staticmethod
    def build_recheck_response(
        state: MarketState,
        timeframe: str
    ) -> dict:
        candles = STATE_TO_CANDLES[state]
        minutes = candles * TIMEFRAME_MINUTES.get(timeframe, 60)

        return {
            "market_state": state.value,
            "recheck_after_candles": candles,
            "recheck_timeframe": timeframe,
            "estimated_wait_minutes": minutes,
            "next_check_hint": RecheckDecisionEngine._hint_for_state(state)
        }

    @staticmethod
    def _hint_for_state(state: MarketState) -> str:
        hints = {
            MarketState.TREND_MISMATCH: "Wait for trend and signal alignment",
            MarketState.RANGING: "Wait for breakout or volatility expansion",
            MarketState.LOW_VOLATILITY: "Wait for momentum or session open",
            MarketState.OVEREXTENDED: "Wait for pullback toward EMA",
            MarketState.PULLBACK_PENDING: "Recheck after next candle close",
            MarketState.BREAKOUT_SETUP: "Monitor closely at candle close",
            MarketState.CHOPPY_HIGH_VOL: "Let market stabilize before trading",
        }
        return hints.get(state, "Wait for clearer market structure")
