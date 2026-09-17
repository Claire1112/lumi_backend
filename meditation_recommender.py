# 還沒加入推薦系統的推薦邏輯

from user_profile import UserProfile

def recommend_meditation(context):
    state = context.state
    goal = context.goal
    duration = context.duration
    guidance = context.guidancePreference
    scene_preference = context.scenePreference
    avoid_hold = context.avoidBreathHolding

    # =====================================================
    # 1. Scene 場景
    # 使用者明確指定 > 系統推薦
    # =====================================================

    if scene_preference:
        scene = scene_preference

    elif goal == "sleep":
        scene = "night"

    elif state in ["stressed", "anxious"]:
        scene = "forest"

    elif state == "fatigued":
        scene = "rice_field"

    elif state == "overthinking":
        scene = "mountain"

    else:
        scene = "rice_field"

    # =====================================================
    # 2. Breathing 呼吸方式
    # =====================================================

    # 不希望閉氣 → 一律避開需要 hold 的呼吸
    if avoid_hold:
        breathing = "slow_4_6"

    elif goal == "sleep":
        breathing = "slow_4_6"

    elif state in ["stressed", "anxious"]:
        breathing = "slow_4_6"

    elif state == "overthinking" and goal == "focus":
        breathing = "box_breathing"

    elif state == "calm":
        breathing = "equal_breathing"

    else:
        breathing = "slow_4_6"

    # =====================================================
    # 3. Meditation Technique
    # =====================================================

    # 短時間避免太複雜的技巧
    if duration <= 5:
        technique = "breath_awareness"

    elif goal == "sleep":
        technique = "body_scan"

    elif state == "overthinking":
        technique = "breath_awareness"

    elif state == "fatigued" and goal == "relax":
        technique = "body_scan"

    elif goal == "clear_mind":
        technique = "breath_awareness"

    elif duration >= 10:
        technique = "body_scan"

    else:
        technique = "breath_awareness"

    # =====================================================
    # 4. Guidance → Voice
    # =====================================================

    if guidance == "gentle_companion":
        voice_tone = "warm_gentle"
        voice_speed = "slow"
        guidance_density = "medium"
        silence_ratio = 0.325

    elif guidance == "structured_guidance":
        voice_tone = "calm_clear"
        voice_speed = "medium_slow"
        guidance_density = "high"
        silence_ratio = 0.175

    elif guidance == "environment_focused":
        voice_tone = "soft"
        voice_speed = "slow"
        guidance_density = "very_low"
        silence_ratio = 0.75

    elif guidance == "sparse_encouragement":
        voice_tone = "warm_gentle"
        voice_speed = "slow"
        guidance_density = "low"
        silence_ratio = 0.60

    else:
        # 防呆
        voice_tone = "warm_gentle"
        voice_speed = "slow"
        guidance_density = "medium"
        silence_ratio = 0.325

    # =====================================================
    # 5. Sleep 相容性限制
    # =====================================================

    if goal == "sleep":
        voice_speed = "slow"

        # 睡眠時引導密度不能太高
        if guidance_density == "high":
            guidance_density = "medium"

    # =====================================================
    # 6. Music
    # =====================================================

    if goal == "sleep":
        music_mood = "sleep"

    elif goal == "focus":
        music_mood = "focused_calm"

    elif state in ["stressed", "anxious"]:
        music_mood = "calm"

    elif state == "fatigued":
        music_mood = "restorative"

    else:
        music_mood = "calm"

    # =====================================================
    # 7. Environment Sound
    # =====================================================

    if scene == "forest":
        environment_sound = "forest"

    elif scene == "night":
        environment_sound = "night"

    elif scene == "rice_field":
        environment_sound = "nature_breeze"

    elif scene == "mountain":
        environment_sound = "mountain_wind"

    else:
        environment_sound = "nature"

    # =====================================================
    # Personalized Meditation Plan
    # =====================================================

    return {
        "state": state,
        "goal": goal,
        "duration": duration,

        "scene": scene,

        "breathing": breathing,
        "technique": technique,

        "guidanceStyle": guidance,

        "voiceTone": voice_tone,
        "voiceSpeed": voice_speed,
        "guidanceDensity": guidance_density,
        "silenceRatio": silence_ratio,

        "musicMood": music_mood,
        "environmentSound": environment_sound
    }