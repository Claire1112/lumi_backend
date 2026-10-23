"""Reviewed manual UI paths and feature-guide replies (no AI/network required)."""
import re

GUIDE_PREFIX = "lumi:guide:"
FEATURES = {
    "meditation": {
        "name": "冥想",
        "content": "想留一點時間靜下來，可以從地圖選擇「森林、海邊、高山或小麥田」，再設定練習並點「START」。還不確定怎麼選？也可以點下方「幫我推薦冥想」按鈕，讓我陪你挑選～",
        "option": "幫我推薦冥想",
        "aliases": ("冥想",),
    },
    "breathing": {
        "name": "呼吸練習",
        "content": "想跟著節奏練習呼吸，可以從地圖點「小木屋」，進入後點「查看罐子功能」，再選右邊的「呼吸模式」。也可以點下方「前往呼吸練習」按鈕，直接開啟呼吸介面，慢慢練習就好～",
        "option": "lumi:navigate:breathing_practice",
        "aliases": ("呼吸練習", "呼吸訓練"),
    },
    "acupressure": {
        "name": "穴位按摩",
        "content": "想看看適合的穴位，可以從地圖點「小木屋」，進入後點「查看罐子功能」，再選左邊的「穴道按摩」，依部位與狀況查看資料和引導。也可以點下方「前往穴道按摩」按鈕，直接進入按摩介面看看喔。",
        "option": "lumi:navigate:acupressure",
        "aliases": ("穴位按摩", "穴道按摩", "穴位教學", "穴道教學"),
    },
    "music": {
        "name": "音樂創作",
        "content": "想做一首自己的放鬆音樂，可以從地圖點「小木屋」，進入後點「查看罐子功能」，選中間的「個人紀錄」，再到「我的收藏」找到音樂生成入口。也可以點下方「前往音樂創作」按鈕，開始試試喜歡的風格吧～",
        "option": "lumi:navigate:music_generation",
        "aliases": ("音樂創作", "音樂生成", "生成音樂", "製作音樂"),
    },
    "records": {
        "name": "個人紀錄",
        "content": "想回顧練習或查看收藏，可以從地圖點「小木屋」，進入後點「查看罐子功能」，再選中間的「個人紀錄」。也可以點下方「查看我的數據」按鈕，看看自己累積的練習與收藏喔。",
        "option": "lumi:navigate:personal_records",
        "aliases": ("個人紀錄", "個人記錄", "個人數據", "我的紀錄"),
    },
}


def guide_topic(message, allow_other=False):
    text = re.sub(r"[\s，。！？,.!?～~]", "", (message or "").lower())
    selections = {'冥想要從哪裡開始': 'meditation', '呼吸練習在哪裡': 'breathing', '穴位按摩在哪裡': 'acupressure', '要去哪裡製作自己的音樂': 'music', '我的練習紀錄在哪裡看': 'records', '我想看看其他功能': 'menu'}
    if text in selections:
        return selections[text]
    if allow_other and text == "其他":
        return "menu"
    if text.startswith(GUIDE_PREFIX):
        key = text[len(GUIDE_PREFIX):]
        return key if key == "menu" or key in FEATURES else None
    if any(word in text for word in ("取消", "不要", "不想", "不用")):
        return None
    if text in ("功能", "我想看功能導覽", "我想看看功能導覽", "我想了解功能導覽", "有哪些功能",
                "功能導覽", "返回功能導覽", "app怎麼用", "app怎麼使用", "如何使用app",
                "功能介紹", "使用方法", "怎麼使用", "如何使用", "功能在哪裡", "功能在哪"):
        return "menu"
    # Explicit guide selections and location/help requests, not health questions.
    explicit = text.startswith("功能導覽：") or text.startswith("功能導覽:")
    location = any(word in text for word in ("在哪裡", "在哪", "哪邊", "怎麼找到", "如何找到", "怎麼點", "如何點"))
    if explicit or location:
        for key, feature in FEATURES.items():
            if any(alias in text for alias in feature["aliases"]):
                return key
    return None


def get_feature_guide(message, allow_other=False):
    topic = guide_topic(message, allow_other=allow_other)
    if topic is None:
        return None
    if topic == "menu":
        reply = "想了解哪個功能？我可以告訴你在哪裡找到。"
        options = [GUIDE_PREFIX + key for key in FEATURES]
    else:
        feature = FEATURES[topic]
        reply = feature["content"]
        options = [feature["option"], GUIDE_PREFIX + "menu"]
    return {"route": "app_help", "status": "answered", "missingField": None,
            "reply": reply, "options": options, "action": None, "context": {}}
