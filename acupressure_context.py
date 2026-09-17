from typing import Optional, List
from pydantic import BaseModel, Field


class AcupressureContext(BaseModel):
    # 不舒服的部位
    bodyPart: Optional[str] = None

    # 症狀，例如痠痛、僵硬、疲勞
    symptom: Optional[str] = None

    # 想進行多久（分鐘）
    duration: Optional[int] = None

    # 記錄哪些資訊是使用者明確說的
    explicitFields: List[str] = Field(default_factory=list)


def get_missing_acupressure_fields(
    context: AcupressureContext
):
    missing_fields = []

    if context.bodyPart is None:
        missing_fields.append("bodyPart")

    if context.symptom is None:
        missing_fields.append("symptom")

    # duration 暫時設定為非必要
    # 沒有提供的話，之後推薦器可以給預設值

    return missing_fields