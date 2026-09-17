from acupressure_extractor import extract_acupressure_context


tests = [
    "我肩膀很僵硬",
    "最近眼睛很疲勞",
    "我最近很焦慮",
    "滑手機太久手很痠",
    "腦袋一直停不下來",
    "我想按摩手部"
]


for text in tests:

    print("\n====================")
    print("Input:")
    print(text)

    result = extract_acupressure_context(text)

    print("Result:")
    print(result.model_dump())
    