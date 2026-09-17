def build_acupressure_response(
    missing_fields,
    context
):

    # =====================================================
    # 資料完整
    # =====================================================

    if not missing_fields:
        return {
            "route": "acupressure",
            "status": "ready",
            "missingField": None,
            "reply": "資訊已經足夠，可以開始推薦穴位。",
            "options": [],
            "action": None
        }


    next_field = missing_fields[0]


    # =====================================================
    # 1. 還不知道部位
    # =====================================================

    if next_field == "bodyPart":

        return {
            "route": "acupressure",
            "status": "need_more_info",
            "missingField": "bodyPart",
            "reply": "你現在比較想放鬆哪個部位？",
            "options": [
                "頭部",
                "肩頸",
                "手部",
                "其他"
            ],
            "action": None
        }


    # =====================================================
    # 2. 已知道部位，但還不知道狀況
    # =====================================================

    if next_field == "symptom":

        # -------------------------------------------------
        # 頭部
        # -------------------------------------------------

        if context.bodyPart == "head":

            return {
                "route": "acupressure",
                "status": "need_more_info",
                "missingField": "symptom",
                "reply": "請選擇更接近你的狀況。",
                "options": [
                    "頭部緊繃",
                    "眼睛疲勞",
                    "精神疲勞",
                    "壓力大",
                    "腦袋停不下來"
                ],
                "action": None
            }


        # -------------------------------------------------
        # 肩頸
        # -------------------------------------------------

        if context.bodyPart == "neck_shoulder":

            return {
                "route": "acupressure",
                "status": "need_more_info",
                "missingField": "symptom",
                "reply": "請選擇更接近你的狀況。",
                "options": [
                    "肩膀僵硬",
                    "脖子緊繃",
                    "久坐後不舒服",
                    "壓力造成的肩頸緊繃"
                ],
                "action": None
            }


        # -------------------------------------------------
        # 手部
        # -------------------------------------------------

        if context.bodyPart == "hand":

            return {
                "route": "acupressure",
                "status": "need_more_info",
                "missingField": "symptom",
                "reply": "請選擇更接近你的狀況。",
                "options": [
                    "手腕痠",
                    "手指疲勞",
                    "長時間滑手機或打字",
                    "想放鬆手部"
                ],
                "action": None
            }


        # -------------------------------------------------
        # 其他
        # -------------------------------------------------

        if context.bodyPart == "other":

            return {
                "route": "acupressure",
                "status": "need_more_info",
                "missingField": "symptom",
                "reply": "請選擇更接近你的狀況。",
                "options": [
                    "情緒焦躁",
                    "焦慮不安",
                    "睡前想放鬆",
                    "只是想舒緩一下"
                ],
                "action": None
            }


    # =====================================================
    # 防呆
    # =====================================================

    return {
        "route": "acupressure",
        "status": "error",
        "missingField": None,
        "reply": "目前無法判斷下一步需要的資訊。",
        "options": [],
        "action": None
    }