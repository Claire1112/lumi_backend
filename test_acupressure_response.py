from acupressure_context import AcupressureContext
from acupressure_response_builder import build_acupressure_response


tests = [
    (
        ["bodyPart", "symptom"],
        AcupressureContext()
    ),

    (
        ["symptom"],
        AcupressureContext(
            bodyPart="head"
        )
    ),

    (
        ["symptom"],
        AcupressureContext(
            bodyPart="neck_shoulder"
        )
    ),

    (
        ["symptom"],
        AcupressureContext(
            bodyPart="hand"
        )
    ),

    (
        ["symptom"],
        AcupressureContext(
            bodyPart="other"
        )
    )
]


for missing_fields, context in tests:

    print("\n====================")
    print("Context:")
    print(context.model_dump())

    print("Missing:")
    print(missing_fields)

    result = build_acupressure_response(
        missing_fields,
        context
    )

    print("Response:")
    print(result)