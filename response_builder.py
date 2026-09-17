def build_response(missing_fields):
    if not missing_fields:
        return {
            "route": "meditation",
            "status": "ready",
            "missingField": None,
            "reply": "資訊已經足夠，可以開始推薦。",
            "options": [],
            "action": None
        }

    next_field = missing_fields[0]

    if next_field == "state":
        return {
            "route": "meditation",
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
            "route": "meditation",
            "status": "need_more_info",
            "missingField": "goal",
            "reply": "你現在最希望改善什麼？",
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
            "route": "meditation",
            "status": "need_more_info",
            "missingField": "duration",
            "reply": "這次想做多久？",
            "options": [
                "3分鐘",
                "5分鐘",
                "10分鐘",
                "15分鐘",
                "20分鐘以上"
            ],
            "action": None
        }

    if next_field == "guidancePreference":
        return {
            "route": "meditation",
            "status": "need_more_info",
            "missingField": "guidancePreference",
            "reply": "你比較希望我怎麼陪你進行這次冥想？",
            "options": [
                "溫柔陪伴",
                "清楚帶領",
                "環境聲為主",
                "少量鼓勵"
            ],
            "action": None
        }

    return {
        "route": "meditation",
        "status": "error",
        "missingField": None,
        "reply": "目前無法判斷下一步需要的資訊。",
        "options": [],
        "action": None
    }

# def build_response(missing_fields):
#     if not missing_fields:
#         return {
#             "status": "ready",
#             "reply": "資訊已經足夠，可以開始推薦。",
#             "options": []
#         }

#     next_field = missing_fields[0]

#     if next_field == "state":
#         return {
#             "status": "need_more_info",
#             "missingField": "state",
#             "reply": "你現在比較接近哪一種狀態？",
#             "options": [
#                 "壓力很大",
#                 "焦慮緊張",
#                 "身體疲勞",
#                 "思緒繁多",
#                 "目前平穩"
#             ]
#         }

#     if next_field == "goal":
#         return {
#             "status": "need_more_info",
#             "missingField": "goal",
#             "reply": "你現在最希望改善什麼？",
#             "options": [
#                 "放鬆一下",
#                 "重新專注",
#                 "放空一下",
#                 "準備睡覺",
#                 "安撫自己"
#             ]
#         }

#     if next_field == "duration":
#         return {
#             "status": "need_more_info",
#             "missingField": "duration",
#             "reply": "這次想做多久？",
#             "options": [
#                 "3分鐘",
#                 "5分鐘",
#                 "10分鐘",
#                 "15分鐘",
#                 "20分鐘以上"
#             ]
#         }

#     if next_field == "guidancePreference":
#         return {
#             "status": "need_more_info",
#             "missingField": "guidancePreference",
#             "reply": "你比較希望我怎麼陪你進行這次冥想？",
#             "options": [
#                 "溫柔陪伴",
#                 "清楚帶領",
#                 "環境聲為主",
#                 "少量鼓勵"
#             ]
#         }