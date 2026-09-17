from router import detect_route


tests = [
    "幫我推薦",
    "我想放鬆",
    "我想睡覺",
    "呼吸練習",
    "穴位放鬆",
    "我肩頸很緊",
    "我手腕很痠",
    "App怎麼用",
    "今天天氣不錯",
    "取消"
]


for text in tests:
    print(
        text,
        "=>",
        detect_route(text)
    )