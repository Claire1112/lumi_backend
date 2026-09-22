from conversation_memory import extraction_input
from typing import Optional, Literal, List
from pydantic import BaseModel, Field

from llm import get_llm


class AcupressureExtraction(BaseModel):

    bodyPart: Optional[
        Literal[
            "head",
            "neck_shoulder",
            "hand",
            "other"
        ]
    ] = None

    symptom: Optional[
        Literal[
            # 頭部
            "head_tension",
            "eye_fatigue",
            "mental_fatigue",
            "high_stress",
            "racing_thoughts",

            # 肩頸
            "shoulder_stiffness",
            "neck_tension",
            "sitting_discomfort",
            "stress_neck_tension",

            # 手部
            "wrist_soreness",
            "finger_fatigue",
            "phone_typing_fatigue",
            "hand_relaxation",

            # 其他
            "irritability",
            "anxiety",
            "bedtime_relaxation",
            "general_relaxation"
        ]
    ] = None

    duration: Optional[int] = None

    explicitFields: List[str] = Field(
        default_factory=list
    )


def extract_acupressure_context(
    message: str
) -> AcupressureExtraction:

    text = message.strip()

    # =====================================================
    # 功能入口文字
    # 這些文字只代表「進入穴位放鬆流程」，
    # 不應該直接推斷 bodyPart / symptom
    # =====================================================

    entry_messages = [
        "穴位放鬆",
        "身體放鬆",
        "身體疲勞／痠痛",
        "身體疲勞/痠痛"
    ]

    if text in entry_messages:
        return AcupressureExtraction(
            bodyPart=None,
            symptom=None,
            duration=None,
            explicitFields=[]
        )

    # =====================================================
    # 其餘訊息再交給 Gemini 抽取
    # =====================================================

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        AcupressureExtraction
    )

    prompt = f"""
你是 Lumi 身心放鬆 App 的穴位資訊抽取器。

請從使用者訊息中，只抽取使用者明確表達的資訊。

使用者訊息：
{extraction_input(message)}


【bodyPart】

head：
頭部相關狀況

neck_shoulder：
肩膀、肩頸、脖子相關狀況

hand：
手、手指、手腕相關狀況

other：
沒有特定身體部位，而是情緒、焦慮、睡前放鬆、
或只是想舒緩一下


【symptom】

頭部：
head_tension
= 頭部緊繃

eye_fatigue
= 眼睛疲勞

mental_fatigue
= 精神疲勞

high_stress
= 壓力大

racing_thoughts
= 腦袋停不下來、想很多、思緒很多


肩頸：
shoulder_stiffness
= 肩膀僵硬

neck_tension
= 脖子緊繃

sitting_discomfort
= 久坐後不舒服

stress_neck_tension
= 壓力造成的肩頸緊繃


手部：
wrist_soreness
= 手腕痠

finger_fatigue
= 手指疲勞

phone_typing_fatigue
= 長時間滑手機或打字造成疲勞

hand_relaxation
= 想放鬆手部


其他：
irritability
= 情緒焦躁

anxiety
= 焦慮不安

bedtime_relaxation
= 睡前想放鬆

general_relaxation
= 不知道哪裡不舒服，只是想舒緩一下


【duration】

只有使用者明確提到時間時才填入分鐘數。
否則為 null。


【explicitFields】

只記錄使用者這一句話中明確提供的欄位。

例如：

「我頭很緊」
bodyPart = head
symptom = head_tension
explicitFields = ["bodyPart", "symptom"]

「最近一直盯電腦，眼睛很累」
bodyPart = head
symptom = eye_fatigue
explicitFields = ["bodyPart", "symptom"]

「我肩膀超僵硬」
bodyPart = neck_shoulder
symptom = shoulder_stiffness
explicitFields = ["bodyPart", "symptom"]

「最近滑手機滑太久，手很痠」
bodyPart = hand
symptom = phone_typing_fatigue
explicitFields = ["bodyPart", "symptom"]

「我最近很焦慮」
bodyPart = other
symptom = anxiety
explicitFields = ["bodyPart", "symptom"]

「睡前想放鬆一下」
bodyPart = other
symptom = bedtime_relaxation
explicitFields = ["bodyPart", "symptom"]

不要自行加入使用者沒有說出的資訊。
"""

    result = structured_llm.invoke(prompt)

    return result