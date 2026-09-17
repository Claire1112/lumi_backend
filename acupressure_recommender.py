def recommend_acupressure(context):

    symptom = context.symptom

    recommendations = {

        # =================================================
        # 頭部區
        # =================================================

        "head_tension": {
            "bodyPart": "head",
            "symptom": "head_tension",
            "acupoints": [
                {
                    "id": "baihui",
                    "name": "百會",
                    "location": "頭頂正中央",
                    "effect": "放鬆頭部、舒緩頭部緊繃感"
                },
                {
                    "id": "taiyang",
                    "name": "太陽",
                    "location": "眉尾與眼尾外側凹陷處",
                    "effect": "緩解頭痛、太陽穴緊繃"
                },
                {
                    "id": "fengchi",
                    "name": "風池",
                    "location": "後頸兩側、髮際凹陷處",
                    "effect": "放鬆頸肩、改善頭部壓力"
                }
            ]
        },

        "eye_fatigue": {
            "bodyPart": "head",
            "symptom": "eye_fatigue",
            "acupoints": [
                {
                    "id": "taiyang",
                    "name": "太陽",
                    "location": "眉尾與眼尾外側凹陷處",
                    "effect": "緩解頭痛、太陽穴緊繃"
                },
                {
                    "id": "jingming",
                    "name": "睛明",
                    "location": "內眼角旁",
                    "effect": "緩解眼睛疲勞、乾澀"
                },
                {
                    "id": "cuanzhu",
                    "name": "攢竹",
                    "location": "眉頭內側凹陷處",
                    "effect": "舒緩眼壓、眉間緊繃"
                }
            ]
        },

        "mental_fatigue": {
            "bodyPart": "head",
            "symptom": "mental_fatigue",
            "acupoints": [
                {
                    "id": "baihui",
                    "name": "百會",
                    "location": "頭頂正中央",
                    "effect": "放鬆頭部、舒緩頭部緊繃感"
                },
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "舒緩疲勞、促進循環"
                },
                {
                    "id": "zusanli",
                    "name": "足三里",
                    "location": "膝蓋下約四指、脛骨外側",
                    "effect": "提升元氣、改善疲勞感"
                }
            ]
        },

        "high_stress": {
            "bodyPart": "head",
            "symptom": "high_stress",
            "acupoints": [
                {
                    "id": "baihui",
                    "name": "百會",
                    "location": "頭頂正中央",
                    "effect": "放鬆頭部、舒緩頭部緊繃感"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "緩解焦慮、舒緩壓力"
                },
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "安定情緒、放鬆身心"
                }
            ]
        },

        "racing_thoughts": {
            "bodyPart": "head",
            "symptom": "racing_thoughts",
            "acupoints": [
                {
                    "id": "yintang",
                    "name": "印堂",
                    "location": "兩眉之間",
                    "effect": "平靜思緒、舒緩緊張"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "緩解焦慮、舒緩壓力"
                },
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "安定情緒、放鬆身心"
                }
            ]
        },

        # =================================================
        # 肩頸區
        # =================================================

        "shoulder_stiffness": {
            "bodyPart": "neck_shoulder",
            "symptom": "shoulder_stiffness",
            "acupoints": [
                {
                    "id": "jianjing",
                    "name": "肩井",
                    "location": "肩膀最高點中央",
                    "effect": "放鬆肩膀肌肉、改善僵硬"
                },
                {
                    "id": "fengchi",
                    "name": "風池",
                    "location": "後頸兩側、髮際凹陷處",
                    "effect": "放鬆頸肩、改善頭部壓力"
                },
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "舒緩肩頸痠痛、促進循環"
                }
            ]
        },

        "neck_tension": {
            "bodyPart": "neck_shoulder",
            "symptom": "neck_tension",
            "acupoints": [
                {
                    "id": "jianjing",
                    "name": "肩井",
                    "location": "肩膀最高點中央",
                    "effect": "改善肩頸僵硬與痠痛"
                },
                {
                    "id": "fengchi",
                    "name": "風池",
                    "location": "後頸兩側、髮際凹陷處",
                    "effect": "放鬆頸部肌肉、減輕緊繃"
                },
                {
                    "id": "tianzhu",
                    "name": "天柱",
                    "location": "後頸髮際兩側",
                    "effect": "舒緩頸部僵硬、疲勞"
                }
            ]
        },

        "sitting_discomfort": {
            "bodyPart": "neck_shoulder",
            "symptom": "sitting_discomfort",
            "acupoints": [
                {
                    "id": "jianjing",
                    "name": "肩井",
                    "location": "肩膀最高點中央",
                    "effect": "放鬆肩膀肌肉、改善僵硬"
                },
                {
                    "id": "zusanli",
                    "name": "足三里",
                    "location": "膝蓋下約四指、脛骨外側",
                    "effect": "促進循環、減輕疲勞"
                },
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "舒緩肌肉緊繃、放鬆身體"
                }
            ]
        },

        "stress_neck_tension": {
            "bodyPart": "neck_shoulder",
            "symptom": "stress_neck_tension",
            "acupoints": [
                {
                    "id": "jianjing",
                    "name": "肩井",
                    "location": "肩膀最高點中央",
                    "effect": "放鬆肩膀肌肉、改善僵硬"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "緩解焦慮、舒緩壓力"
                },
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "安定情緒、放鬆身心"
                }
            ]
        },

        # =================================================
        # 手部區
        # =================================================

        "wrist_soreness": {
            "bodyPart": "hand",
            "symptom": "wrist_soreness",
            "acupoints": [
                {
                    "id": "yangchi",
                    "name": "陽池",
                    "location": "手腕背側橫紋中央",
                    "effect": "舒緩手腕痠痛、改善活動度"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "放鬆手腕、減輕痠脹"
                },
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "緩解手腕緊繃、放鬆身心"
                }
            ]
        },

        "finger_fatigue": {
            "bodyPart": "hand",
            "symptom": "finger_fatigue",
            "acupoints": [
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "放鬆手部肌肉、改善疲勞"
                },
                {
                    "id": "baxie",
                    "name": "八邪",
                    "location": "手指根部指縫間",
                    "effect": "緩解手指僵硬、促進循環"
                },
                {
                    "id": "laogong",
                    "name": "勞宮",
                    "location": "手掌中央",
                    "effect": "放鬆手掌、減輕疲勞感"
                }
            ]
        },

        "phone_typing_fatigue": {
            "bodyPart": "hand",
            "symptom": "phone_typing_fatigue",
            "acupoints": [
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "舒緩手部疲勞與痠痛"
                },
                {
                    "id": "yangchi",
                    "name": "陽池",
                    "location": "手腕背側橫紋中央",
                    "effect": "改善手腕僵硬與不適"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "放鬆手腕與前臂肌肉"
                }
            ]
        },

        "hand_relaxation": {
            "bodyPart": "hand",
            "symptom": "hand_relaxation",
            "acupoints": [
                {
                    "id": "laogong",
                    "name": "勞宮",
                    "location": "手掌中央",
                    "effect": "放鬆手掌、舒緩緊繃"
                },
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "安定情緒、放鬆身心"
                },
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "促進循環、舒緩手部疲勞"
                }
            ]
        },

        # =================================================
        # 其他
        # =================================================

        "irritability": {
            "bodyPart": "other",
            "symptom": "irritability",
            "acupoints": [
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "安定情緒、減少煩躁"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "舒緩焦慮、放鬆身心"
                },
                {
                    "id": "yintang",
                    "name": "印堂",
                    "location": "兩眉之間",
                    "effect": "平靜思緒、放鬆精神"
                }
            ]
        },

        "anxiety": {
            "bodyPart": "other",
            "symptom": "anxiety",
            "acupoints": [
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "緩解焦慮、穩定情緒"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "放鬆神經、舒緩壓力"
                },
                {
                    "id": "baihui",
                    "name": "百會",
                    "location": "頭頂正中央",
                    "effect": "放鬆思緒、減輕精神壓力"
                }
            ]
        },

        "bedtime_relaxation": {
            "bodyPart": "other",
            "symptom": "bedtime_relaxation",
            "acupoints": [
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "幫助放鬆、舒緩情緒"
                },
                {
                    "id": "yintang",
                    "name": "印堂",
                    "location": "兩眉之間",
                    "effect": "平靜心情、幫助入睡"
                },
                {
                    "id": "neiguan",
                    "name": "內關",
                    "location": "手腕橫紋上三指、兩筋之間",
                    "effect": "放鬆神經、舒緩緊張"
                }
            ]
        },

        "general_relaxation": {
            "bodyPart": "other",
            "symptom": "general_relaxation",
            "acupoints": [
                {
                    "id": "hegu",
                    "name": "合谷",
                    "location": "手背虎口處",
                    "effect": "促進循環、舒緩全身疲勞"
                },
                {
                    "id": "shenmen",
                    "name": "神門",
                    "location": "手腕小指側橫紋凹陷處",
                    "effect": "放鬆身心、安定情緒"
                },
                {
                    "id": "baihui",
                    "name": "百會",
                    "location": "頭頂正中央",
                    "effect": "舒緩壓力、提振精神"
                }
            ]
        }
    }

    recommendation = recommendations.get(symptom)

    if recommendation is None:
        return None

    return {
        **recommendation,

        # 對應你們計畫書推薦頁固定資訊
        "massageMethod": "以指腹輕輕按壓，搭配慢慢呼吸。",
        "suggestedPressTime": "約30秒至1分鐘，可依舒適程度調整。"
    }