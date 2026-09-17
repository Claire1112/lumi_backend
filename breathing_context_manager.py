from breathing_context import BreathingContext
from breathing_extractor import BreathingExtraction


def merge_breathing_context(
    old_context: BreathingContext,
    new_context: BreathingExtraction
) -> BreathingContext:

    data = old_context.model_dump()

    # 只有這一輪明確提供的欄位才覆蓋
    if "state" in new_context.explicitFields:
        data["state"] = new_context.state

    if "goal" in new_context.explicitFields:
        data["goal"] = new_context.goal

    if "duration" in new_context.explicitFields:
        data["duration"] = new_context.duration

    if "avoidBreathHolding" in new_context.explicitFields:
        data["avoidBreathHolding"] = new_context.avoidBreathHolding

    if "breathingPreference" in new_context.explicitFields:
        data["breathingPreference"] = new_context.breathingPreference

    # 合併 explicitFields，避免之前紀錄消失
    data["explicitFields"] = list(
        dict.fromkeys(
            old_context.explicitFields
            + new_context.explicitFields
        )
    )

    return BreathingContext(**data)