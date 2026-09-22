from conversation_memory import extraction_input
from typing import Optional, Literal, List
from pydantic import BaseModel, Field

from llm import get_llm


class BreathingExtraction(BaseModel):
    state: Optional[
        Literal[
            "stressed",
            "anxious",
            "fatigued",
            "overthinking",
            "calm"
        ]
    ] = Field(
        default=None,
        description="使用者目前的身心狀態"
    )

    goal: Optional[
        Literal[
            "relax",
            "focus",
            "clear_mind",
            "sleep",
            "self_soothe"
        ]
    ] = Field(
        default=None,
        description="使用者希望透過呼吸練習達成的目標"
    )

    duration: Optional[int] = Field(
        default=None,
        description="使用者希望進行呼吸練習的分鐘數"
    )

    avoidBreathHolding: bool = Field(
        default=False,
        description="使用者是否明確表示不要閉氣、憋氣或停留呼吸"
    )

    breathingPreference: Optional[str] = Field(
        default=None,
        description="使用者明確指定的呼吸方法，例如 box breathing、4-6 呼吸等"
    )

    explicitFields: List[str] = Field(
        default_factory=list,
        description="這一輪使用者明確提供了哪些欄位"
    )


def extract_breathing_context(message: str) -> BreathingExtraction:
    llm = get_llm()

    structured_llm = llm.with_structured_output(BreathingExtraction)

    prompt = f"""
你是 Lumi 的呼吸練習資訊抽取器。

請從使用者訊息中，只抽取使用者明確表達的資訊。

使用者訊息：
{extraction_input(message)}

欄位規則：

state：
- stressed = 壓力大、壓力很大
- anxious = 焦慮、緊張、不安
- fatigued = 疲勞、很累、身體累
- overthinking = 想很多、思緒很多、腦袋停不下來
- calm = 平靜、目前狀態穩定

goal：
- relax = 放鬆
- focus = 專注
- clear_mind = 放空、清空思緒
- sleep = 睡覺、幫助入睡
- self_soothe = 安撫自己、穩定情緒

duration：
只輸出分鐘數，例如：
「五分鐘」→ 5
「10分鐘」→ 10

avoidBreathHolding：
只有使用者明確表示「不要閉氣」、「不想憋氣」、
「不舒服不要停住呼吸」等情況才設為 true。
否則為 false。

breathingPreference：
只有使用者明確指定某種呼吸方式時才填寫，
否則為 null。

explicitFields：
只列出這一輪訊息中，使用者明確提供的欄位名稱。
例如：
「我很焦慮，想做五分鐘，不要閉氣」
應為：
["state", "duration", "avoidBreathHolding"]

不要自行猜測沒有說出的資訊。
"""

    result = structured_llm.invoke(prompt)

    return result