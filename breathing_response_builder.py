def build_breathing_response(missing_fields):
    if not missing_fields:
        return {
            "route": "breathing",
            "status": "ready",
            "missingField": None,
            "reply": "資訊已經足夠，可以開始呼吸練習。",
            "options": [],
            "action": None
        }

    next_field = missing_fields[0]

    if next_field == "state":
        return {
            "route": "breathing",
            "status": "need_more_info",
            "missingField": "state",
            "reply": "你現在比較接近哪一種狀態？",
            "options": [
                "壓力很大",
                "焦慮緊張",
                "身體疲勞",
                "思緒繁多",
                "目前平穩"
            ],
            "action": None
        }

    if next_field == "goal":
        return {
            "route": "breathing",
            "status": "need_more_info",
            "missingField": "goal",
            "reply": "你希望這次呼吸練習主要幫助你什麼？",
            "options": [
                "放鬆一下",
                "重新專注",
                "放空一下",
                "準備睡覺",
                "安撫自己"
            ],
            "action": None
        }

    if next_field == "duration":
        return {
            "route": "breathing",
            "status": "need_more_info",
            "missingField": "duration",
            "reply": "你想做多久的呼吸練習？",
            "options": [
                "3分鐘",
                "5分鐘",
                "10分鐘"
            ],
            "action": None
        }

    return {
        "route": "breathing",
        "status": "error",
        "missingField": None,
        "reply": "目前無法判斷下一步需要的資訊。",
        "options": [],
        "action": None
    }