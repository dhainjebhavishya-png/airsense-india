CATEGORIES = [
    (30, "Good", "#2ecc71"),
    (60, "Satisfactory", "#a3d977"),
    (90, "Moderate", "#f1c40f"),
    (120, "Poor", "#e67e22"),
    (250, "Very Poor", "#e74c3c"),
    (float("inf"), "Severe", "#a4204a"),
]
ADVICE_GROUPS = ["Children", "Elderly", "Asthma / heart patients", "Runners / outdoor workers"]

ADVICE = {
    "Good": [
        "Outdoor play is fine.",
        "Normal activity is fine.",
        "No special precautions needed.",
        "Great day for outdoor exercise.",
    ],
    "Satisfactory": [
        "Outdoor play is fine.",
        "Fine for most. Take it easy if you feel discomfort.",
        "Keep your reliever medication with you.",
        "Exercise is fine. Sensitive people may notice mild effects.",
    ],
    "Moderate": [
        "Limit long, intense outdoor play.",
        "Shorten long walks. Prefer parks away from traffic.",
        "Keep medication handy. Avoid prolonged outdoor exertion.",
        "Reduce intensity and duration of workouts.",
    ],
    "Poor": [
        "Avoid outdoor sports. Keep windows closed near busy roads.",
        "Stay indoors where possible. Wear an N95 outside.",
        "Stay indoors, keep medication close, watch for symptoms.",
        "Move workouts indoors. Wear an N95 if you must be outside.",
    ],
    "Very Poor": [
        "Keep children indoors. Cancel outdoor school activities.",
        "Stay indoors. Use an air purifier if available.",
        "Avoid outdoor exposure. See a doctor if symptoms worsen.",
        "No outdoor exercise. N95 is a must for outdoor work.",
    ],
    "Severe": [
        "Keep children indoors with windows shut.",
        "Do not go out unless essential. Wear an N95.",
        "Health emergency level. Stay in and seek medical help early.",
        "Outdoor work only with an N95 and for short shifts.",
    ],
}


def categorize(pm):
    for limit, name, color in CATEGORIES:
        if pm <= limit:
            return name, color


if __name__ == "__main__":
    for v in [20, 75, 146.7, 300]:
        print(v, categorize(v))