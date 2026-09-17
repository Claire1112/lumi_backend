def recommend_breathing(context):
    state = context.state
    goal = context.goal
    duration = context.duration
    avoid_hold = context.avoidBreathHolding
    preference = context.breathingPreference

    # -------------------------------------------------
    # 1. 使用者有明確指定呼吸法
    # -------------------------------------------------

    if preference:
        if preference == "slow_4_6":
            return {
                "breathing": "slow_4_6",
                "inhaleSeconds": 4,
                "holdSeconds": 0,
                "exhaleSeconds": 6
            }

        if preference == "box_breathing" and not avoid_hold:
            return {
                "breathing": "box_breathing",
                "inhaleSeconds": 4,
                "holdSeconds": 4,
                "exhaleSeconds": 4
            }

        if preference == "equal_breathing":
            return {
                "breathing": "equal_breathing",
                "inhaleSeconds": 4,
                "holdSeconds": 0,
                "exhaleSeconds": 4
            }

    # -------------------------------------------------
    # 2. 明確不要閉氣
    # -------------------------------------------------

    if avoid_hold:
        if goal == "sleep":
            return {
                "breathing": "slow_4_6",
                "inhaleSeconds": 4,
                "holdSeconds": 0,
                "exhaleSeconds": 6
            }

        if state in ["anxious", "stressed"]:
            return {
                "breathing": "slow_4_6",
                "inhaleSeconds": 4,
                "holdSeconds": 0,
                "exhaleSeconds": 6
            }

        return {
            "breathing": "equal_breathing",
            "inhaleSeconds": 4,
            "holdSeconds": 0,
            "exhaleSeconds": 4
        }

    # -------------------------------------------------
    # 3. 睡眠
    # -------------------------------------------------

    if goal == "sleep":
        return {
            "breathing": "slow_4_6",
            "inhaleSeconds": 4,
            "holdSeconds": 0,
            "exhaleSeconds": 6
        }

    # -------------------------------------------------
    # 4. 焦慮 / 壓力
    # -------------------------------------------------

    if state in ["anxious", "stressed"]:
        return {
            "breathing": "slow_4_6",
            "inhaleSeconds": 4,
            "holdSeconds": 0,
            "exhaleSeconds": 6
        }

    # -------------------------------------------------
    # 5. 思緒繁多 + 專注
    # -------------------------------------------------

    if state == "overthinking" and goal == "focus":
        return {
            "breathing": "box_breathing",
            "inhaleSeconds": 4,
            "holdSeconds": 4,
            "exhaleSeconds": 4
        }

    # -------------------------------------------------
    # 6. 疲勞 + 放鬆
    # -------------------------------------------------

    if state == "fatigued" and goal == "relax":
        return {
            "breathing": "slow_4_6",
            "inhaleSeconds": 4,
            "holdSeconds": 0,
            "exhaleSeconds": 6
        }

    # -------------------------------------------------
    # 7. 平穩 / 預設
    # -------------------------------------------------

    return {
        "breathing": "equal_breathing",
        "inhaleSeconds": 4,
        "holdSeconds": 0,
        "exhaleSeconds": 4
    }