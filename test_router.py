from router import detect_route

test_cases = [
    ("我最近壓力很大", "meditation"),
    ("我好累，我想休息五分鐘", "meditation"),
    ("我腦袋一直停不下來", "meditation"),
    ("我今天很焦慮", "meditation"),
    ("我想專心一下", "meditation"),
    ("我睡不著", "meditation"),

    ("我想做呼吸練習", "breathing"),
    ("帶我深呼吸一下", "breathing"),
    ("有什麼呼吸法可以放鬆", "breathing"),

    ("肩膀好痠", "acupressure"),
    ("脖子很痛", "acupressure"),
    ("有什麼穴位可以按", "acupressure"),

    ("什麼是冥想", "knowledge"),
    ("腹式呼吸是什麼", "knowledge"),

    ("嗨", "general_chat"),
    ("謝謝", "general_chat"),

    ("算了", "cancel"),
    ("停止", "cancel"),
]

failed = []

for message, expected in test_cases:
    actual = detect_route(message)

    if actual != expected:
        failed.append((message, expected, actual))

total = len(test_cases)
passed = total - len(failed)

print(f"\nResult: {passed}/{total} passed")
print(f"Accuracy: {passed / total * 100:.1f}%")

if failed:
    print("\nFailed cases:")
    for message, expected, actual in failed:
        print(
            f"- {message}"
            f" | expected={expected}"
            f" | actual={actual}"
        )
else:
    print("\nAll tests passed!")