from conversation_memory import extraction_input
from typing import Optional, Literal
from pydantic import BaseModel, Field
from llm import get_llm


from typing import Optional, Literal
from pydantic import BaseModel, Field


class CurrentContext(BaseModel):
    state: Optional[
        Literal[
            "stressed",
            "anxious",
            "fatigued",
            "overthinking",
            "calm"
        ]
    ] = None

    goal: Optional[
        Literal[
            "relax",
            "focus",
            "clear_mind",
            "sleep",
            "self_soothe"
        ]
    ] = None

    duration: Optional[int] = None

    guidancePreference: Optional[
        Literal[
            "gentle_companion",
            "structured_guidance",
            "environment_sound",
            "sparse_encouragement"
        ]
    ] = None

    scenePreference: Optional[
        Literal[
            "forest",
            "ocean",
            "mountain",
            "rice_field"
        ]
    ] = None

    avoidBreathHolding: bool = False

    explicitFields: list[str] = Field(default_factory=list)


llm = get_llm()
structured_llm = llm.with_structured_output(CurrentContext)


def extract_context(message: str) -> CurrentContext:
    prompt = f"""
你是 Lumi 冥想推薦系統中的資訊抽取模組。

請從使用者訊息中抽取推薦需要的資訊。

state：
- stressed：壓力大、事情很多、負擔很重
- anxious：焦慮、緊張、不安
- fatigued：身體疲勞、沒精神
- overthinking：思緒繁多、腦袋停不下來
- calm：目前平穩

goal：
- relax：想放鬆
- focus：想專注
- clear_mind：想放空、清空思緒
- sleep：想睡覺、準備睡眠
- self_soothe：想安撫自己

guidancePreference：
- gentle_companion：溫柔陪伴
- structured_guidance：清楚帶領
- environment_sound：環境聲為主
- sparse_encouragement：少量鼓勵

scenePreference：
- forest：森林
- ocean：海邊
- mountain：山群
- rice_field：稻田

duration：
如果使用者提到時間，轉成分鐘整數。

avoidBreathHolding：
如果使用者明確表示不想閉氣、不能閉氣、
不舒服或希望避免憋氣，設為 true。

explicitFields：
如果使用者明確說出某個資訊或偏好，
請把該欄位名稱加入 explicitFields。

例如：

「我最近壓力很大」
→ state = stressed
→ explicitFields 加入 "state"

「我想做十分鐘」
→ duration = 10
→ explicitFields 加入 "duration"

「我想要森林」
→ scenePreference = forest
→ explicitFields 加入 "scenePreference"

「不要閉氣」
→ avoidBreathHolding = true
→ explicitFields 加入 "avoidBreathHolding"

非常重要：
只抽取使用者有提供的資訊。
沒有提到的欄位請維持 null 或預設值。
不要自行猜測使用者偏好。

使用者訊息：
{extraction_input(message)}
"""

    return structured_llm.invoke(prompt)


def get_missing_fields(context: CurrentContext):
    missing = []

    if context.state is None:
        missing.append("state")

    if context.goal is None:
        missing.append("goal")

    if context.duration is None:
        missing.append("duration")

    if context.guidancePreference is None:
        missing.append("guidancePreference")

    return missing