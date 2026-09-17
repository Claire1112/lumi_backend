from extractor import CurrentContext


def merge_context(
    old_context: CurrentContext,
    new_context: CurrentContext
) -> CurrentContext:

    merged_explicit_fields = list(
        set(
            old_context.explicitFields
            + new_context.explicitFields
        )
    )

    return CurrentContext(
        state=new_context.state or old_context.state,
        goal=new_context.goal or old_context.goal,
        duration=new_context.duration or old_context.duration,

        guidancePreference=(
            new_context.guidancePreference
            or old_context.guidancePreference
        ),

        scenePreference=(
            new_context.scenePreference
            or old_context.scenePreference
        ),

        avoidBreathHolding=(
            old_context.avoidBreathHolding
            or new_context.avoidBreathHolding
        ),

        explicitFields=merged_explicit_fields
    )