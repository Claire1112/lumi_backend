from typing import Optional
from pydantic import BaseModel, Field


class InitialProfile(BaseModel):
    # 初始問卷建立的使用者基本資料
    baselineState: Optional[str] = None
    longTermGoal: Optional[str] = None


class LearnedPreference(BaseModel):
    # 歷史偏好
    preferredScene: Optional[str] = None
    preferredBreathing: Optional[str] = None
    preferredGuidance: Optional[str] = None
    preferredDuration: Optional[int] = None

    # 歷史效果分數
    sceneEffect: dict[str, float] = Field(default_factory=dict)
    breathingEffect: dict[str, float] = Field(default_factory=dict)
    techniqueEffect: dict[str, float] = Field(default_factory=dict)
    guidanceEffect: dict[str, float] = Field(default_factory=dict)


class UserProfile(BaseModel):
    initial: InitialProfile = Field(default_factory=InitialProfile)
    learned: LearnedPreference = Field(default_factory=LearnedPreference)