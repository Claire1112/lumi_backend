from acupressure_context import AcupressureContext
from acupressure_extractor import AcupressureExtraction


def merge_acupressure_context(
    old_context: AcupressureContext,
    new_context: AcupressureExtraction
):

    data = old_context.model_dump()

    # 只有使用者這一輪明確提供的欄位才更新
    if "bodyPart" in new_context.explicitFields:
        data["bodyPart"] = new_context.bodyPart

    if "symptom" in new_context.explicitFields:
        data["symptom"] = new_context.symptom

    if "duration" in new_context.explicitFields:
        data["duration"] = new_context.duration

    # 合併 explicitFields，並去除重複
    data["explicitFields"] = list(
        dict.fromkeys(
            old_context.explicitFields
            + new_context.explicitFields
        )
    )

    return AcupressureContext(**data)