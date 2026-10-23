"""String options stay compatible with the existing C.ai questionnaire adapter."""
def build_acupressure_options(recommendation):
    symptom = recommendation['symptom']
    return list(dict.fromkeys(
        f"lumi:acupressure:{symptom}:{point['id']}"
        for point in recommendation.get('acupoints', [])
    ))
