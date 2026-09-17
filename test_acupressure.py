from acupressure_context import AcupressureContext
from acupressure_recommender import recommend_acupressure


tests = [
    AcupressureContext(
        bodyPart="head",
        symptom="eye_fatigue"
    ),

    AcupressureContext(
        bodyPart="neck_shoulder",
        symptom="shoulder_stiffness"
    ),

    AcupressureContext(
        bodyPart="hand",
        symptom="wrist_soreness"
    ),

    AcupressureContext(
        bodyPart="other",
        symptom="anxiety"
    )
]


for context in tests:

    print("\n====================")
    print("Context:")
    print(context.model_dump())

    result = recommend_acupressure(
        context
    )

    print("Recommendation:")
    print(result)