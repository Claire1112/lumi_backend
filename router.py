import re

def detect_route(message: str) -> str:
    text = message.strip().lower()

    # =====================================================
    # 1. 取消目前流程
    # =====================================================

    cancel_keywords = [
        "取消",
        "算了",
        "不要了",
        "停止",
        "重新開始"
    ]

    if any(keyword in text for keyword in cancel_keywords):
        return "cancel"


        # 單純問候：不要被尚未完成的推薦流程攔住
    normalized = re.sub(r"[\s，。！？,.!?～~]", "", text)

    if normalized in {
        "你好", "您好", "嗨", "哈囉", "哈啰",
        "hi", "hello", "謝謝", "謝謝你", "感謝"
    }:
        return "social"

    # 適用性追問，例如「那它適合睡前嗎？」
    suitability_question = re.search(
        r"(適合|可以|能不能|可不可以).*(嗎|呢|[？?])$",
        text
    )

    # 延續上一個主題，例如「那它怎麼做？」
    reference_question = (
        any(word in text for word in (
            "那它", "這個", "那個", "剛剛", "這種", "那種"
        ))
        and any(word in text for word in (
            "怎麼", "如何", "多久", "什麼", "嗎", "呢", "？", "?"
        ))
    )

    if suitability_question or reference_question:
        return "knowledge"
        
    # =====================================================
    # 2. 知識 / 說明型問題
    # =====================================================

    knowledge_patterns = [
        # Privacy questions are explanations, not recommendation slots.
        "我的資料",
        "隱私",
        "個資",
        "資料保存",
        "資料儲存",
        "資料使用",
        "資料安全",
        "什麼是",
        "是什麼",
        "什麼意思",
        "怎麼運作",
        "原理",
        "有什麼作用",
        "有什麼效果",
        "有什麼好處",
        "為什麼",
        "介紹一下",
        "解釋",
        "告訴我什麼是",

        # 適用性問題
        "適合嗎",
        "適不適合",
        "適合什麼",
        "適合哪些",
        "什麼時候適合",
    ]

    if any(pattern in text for pattern in knowledge_patterns):
        return "knowledge"

    # =====================================================
    # 2. 呼吸
    # =====================================================

    breathing_keywords = [
        "呼吸",
        "呼吸練習",
        "breathing"
    ]

    if any(keyword in text for keyword in breathing_keywords):
        return "breathing"


    # =====================================================
    # 3. 穴位 / 身體放鬆
    # =====================================================

    acupressure_keywords = [
        # 功能入口
        "穴位",
        "穴位放鬆",
        "身體放鬆",
        "身體疲勞",
        "按摩",

        # 頭部
        "頭部緊繃",
        "頭很緊",
        "眼睛疲勞",
        "眼睛很累",
        "精神疲勞",
        "腦袋停不下來",

        # 肩頸
        "肩頸",
        "肩膀",
        "肩膀僵硬",
        "脖子",
        "脖子緊繃",
        "久坐後不舒服",
        "肩頸緊繃",

        # 手部
        "手腕",
        "手腕痠",
        "手腕酸",
        "手指疲勞",
        "手很累",
        "滑手機",
        "打字",

        # 常見身體不適
        "痠痛",
        "酸痛"
    ]

    if any(keyword in text for keyword in acupressure_keywords):
        return "acupressure"


    # =====================================================
    # 4. App 使用說明
    # =====================================================

    app_help_keywords = [
        "app怎麼用",
        "app 怎麼用",
        "怎麼使用",
        "如何使用",
        "功能介紹",
        "使用方法"
    ]

    if any(keyword in text for keyword in app_help_keywords):
        return "app_help"


    # =====================================================
    # 5. 冥想
    # =====================================================

    meditation_keywords = [
        # 功能入口
        "幫我推薦",
        "推薦",
        "冥想",

        # 使用者可能直接描述需求
        "放鬆",
        "睡覺",
        "睡眠",
        "專注",
        "放空",
        "安撫"
    ]

    if any(keyword in text for keyword in meditation_keywords):
        return "meditation"


    # =====================================================
    # 6. 一般聊天
    # =====================================================

    return "general_chat"

def wants_personal_data(message: str) -> bool:
    text = re.sub(r"[\s，。！？,.!?～~]", "", message.lower())
    if any(word in text for word in ("不要", "不想", "不用", "取消", "刪除", "隱私", "安全", "保存", "儲存", "什麼是", "是什麼", "別人", "他人")):
        return False
    targets = ("個人數據", "個人資料頁", "個人紀錄", "我的數據", "我的紀錄", "練習紀錄", "個人記錄", "我的記錄", "練習記錄")
    return any(word in text for word in targets) and (
        text in targets or any(word in text for word in ("看", "查", "打開", "開啟", "前往", "帶我", "哪裡", "在哪", "進入"))
    )


def wants_breathing_settings(message: str) -> bool:
    text = re.sub(r"[\s，。！？,.!?～~]", "", message.lower())
    if any(word in text for word in ("不要", "不想", "不用", "取消", "什麼是", "是什麼", "原理", "安全嗎", "適合嗎", "為什麼")):
        return False
    if text in ("呼吸法進階設定", "呼吸進階設定", "呼吸設定", "呼吸滑桿", "呼吸滑杆"):
        return True
    subject = any(word in text for word in ("呼吸", "吸氣", "吐氣", "憋氣"))
    setting = any(word in text for word in ("設定", "滑桿", "滑杆", "秒數", "進階", "自訂", "調整"))
    request = any(word in text for word in ("打開", "開啟", "帶我", "前往", "在哪", "哪裡", "怎麼調", "如何調", "想調", "要調", "想改", "要改", "設定"))
    return subject and setting and request


def wants_acupressure_entry(message: str) -> bool:
    text = re.sub(r"[\s，。！？,.!?～~]", "", message.lower())
    if any(word in text for word in ("不要", "不想", "不用", "取消", "推薦", "什麼是", "是什麼", "原理", "功效", "好處", "適合", "安全", "怎麼按", "如何按", "怎麼做", "如何做")):
        return False
    targets = ("穴道按摩", "穴位按摩", "穴位放鬆", "穴道放鬆", "按摩區", "穴位教學", "穴道教學")
    if not any(word in text for word in targets):
        return False
    return text in targets or any(word in text for word in (
        "入口", "在哪", "哪裡", "哪邊", "打開", "開啟", "前往", "帶我", "進入", "想去", "要去", "怎麼去"
    ))
