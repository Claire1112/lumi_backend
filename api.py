from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag_service import answer_with_rag

from extractor import extract_context, get_missing_fields, CurrentContext
from response_builder import build_response
from context_manager import merge_context
from router import detect_route

from breathing_context import (
    BreathingContext,
    get_missing_breathing_fields
)

from breathing_extractor import extract_breathing_context
from breathing_context_manager import merge_breathing_context
from breathing_response_builder import build_breathing_response
from breathing_recommender import recommend_breathing

from meditation_recommender import recommend_meditation

from acupressure_context import (
    AcupressureContext,
    get_missing_acupressure_fields
)

from acupressure_extractor import extract_acupressure_context
from acupressure_context_manager import merge_acupressure_context
from acupressure_response_builder import build_acupressure_response
from acupressure_recommender import recommend_acupressure

from langchain_google_genai.chat_models import GoogleRateLimitError


app = FastAPI()

# =====================================================
# 暫存每個使用者最後一次 Meditation Recommendation
# 測試用，之後會改 Firestore
# =====================================================

class ChatRequest(BaseModel):
    message: str
    userId: str
    conversationId: str


# =====================================================
# 每個 Conversation 各自保存自己的多輪狀態
# =====================================================

conversation_states = {}


def create_conversation_state(user_id: str):
    return {
        "userId": user_id,

        # 各功能自己的多輪 Context
        "current_context": CurrentContext(),
        "breathing_context": BreathingContext(),
        "acupressure_context": AcupressureContext(),

        # 目前正在執行的流程
        "active_route": None,

        # 這個 Conversation 最新一次完成的 Meditation Recommendation
        "meditation_recommendation": None
    }


# =====================================================
# 明確切換功能判斷
# =====================================================

def detect_explicit_route_switch(message: str):
    """
    已經在多輪流程中時，
    只有使用者明確表示「要換功能」才允許切換 route。
    """

    text = message.strip().lower()

    explicit_switch_keywords = {
        "meditation": [
            "我要冥想",
            "我想做冥想",
            "改成冥想",
            "改做冥想",
            "換成冥想"
        ],

        "breathing": [
            "我要做呼吸練習",
            "我想做呼吸練習",
            "改成呼吸練習",
            "改做呼吸練習",
            "換成呼吸練習"
        ],

        "acupressure": [
            "我要穴位放鬆",
            "我要穴位按摩",
            "我想做穴位放鬆",
            "改成穴位放鬆",
            "改做穴位按摩",
            "換成穴位放鬆"
        ],

        "app_help": [
            "app怎麼用",
            "app 怎麼用",
            "我要看使用說明",
            "告訴我app怎麼用"
        ]
    }

    for route, keywords in explicit_switch_keywords.items():
        if any(keyword in text for keyword in keywords):
            return route

    return None


# =====================================================
# Lumi Chat API
# =====================================================
# @app.get("/lumi/")
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Lumi Backend"
    }

@app.post("/lumi/chat")
def lumi_chat(request: ChatRequest):

    user_id = request.userId
    conversation_id = request.conversationId

    print("\n============================")
    print("Firebase UID：", user_id)
    print("Conversation ID：", conversation_id)
    print("收到叡揚訊息：", repr(request.message))
    print("============================\n")


    # =====================================================
    # 第一次收到這個 Conversation
    # → 建立獨立的多輪狀態
    # =====================================================

    if conversation_id not in conversation_states:

        conversation_states[
            conversation_id
        ] = create_conversation_state(
            user_id
        )

        print(
            "建立新的 Conversation State：",
            conversation_id
        )


    state = conversation_states[
        conversation_id
    ]


    # =====================================================
    # Firebase UID 檢查
    # 同一個 conversation 不應該突然換人
    # =====================================================

    if state["userId"] != user_id:

        return {
            "route": "system",
            "status": "user_mismatch",
            "missingField": None,
            "reply": "聊天使用者資料不一致。",
            "options": [],
            "action": None,
            "context": {}
        }


    # =====================================================
    # 取得這個 Conversation 自己的 Context
    # =====================================================

    current_context = state[
        "current_context"
    ]

    breathing_context = state[
        "breathing_context"
    ]

    acupressure_context = state[
        "acupressure_context"
    ]

    active_route = state[
        "active_route"
    ]


    # 記住進來之前正在跑什麼流程
    previous_active_route = active_route

    print("\n============================")
    print("收到叡揚訊息：", repr(request.message))
    print("============================\n")

    # =====================================================
    # 1. Route 判斷
    # =====================================================

    detected_route = detect_route(request.message)

    # =====================================================
    # 使用者取消目前流程
    # =====================================================

    if detected_route == "cancel":

        print("Cancel Current Flow")

        state["current_context"] = (
            CurrentContext()
        )

        state["breathing_context"] = (
            BreathingContext()
        )

        state["acupressure_context"] = (
            AcupressureContext()
        )

        state["active_route"] = None

        return {
            "route": "system",
            "status": "cancelled",
            "missingField": None,
            "reply": "好，已經停止目前的流程。你可以重新告訴我現在想做什麼。",
            "options": [
                "幫我推薦",
                "我想放鬆",
                "我想睡覺",
                "呼吸練習",
                "穴位放鬆"
            ],
            "action": None,
            "context": {}
        }


    # =====================================================
    # Route 判斷 / 中途切換
    # =====================================================

    switchable_routes = [
        "meditation",
        "breathing",
        "acupressure",
        "app_help"
    ]


    # -----------------------------------------------------
    # 沒有正在執行多輪流程
    # -----------------------------------------------------

    if active_route is None:

        route = detected_route


    # -----------------------------------------------------
    # 已經在某個多輪流程
    # -----------------------------------------------------

    else:

        explicit_switch_route = detect_explicit_route_switch(
            request.message
        )

        # 只有明確要求換功能才切換
        if (
            explicit_switch_route in switchable_routes
            and explicit_switch_route != active_route
        ):

            print(
                f"Explicit Route Switch: "
                f"{active_route} -> {explicit_switch_route}"
            )

            # 清除原本尚未完成的流程資料
            if active_route == "meditation":

                state["current_context"] = (
                    CurrentContext()
                )

            elif active_route == "breathing":

                state["breathing_context"] = (
                    BreathingContext()
                )

            elif active_route == "acupressure":

                state["acupressure_context"] = (
                    AcupressureContext()
                )


            active_route = explicit_switch_route

            state["active_route"] = (
                explicit_switch_route
            )

            route = explicit_switch_route


        # 沒有明確要求換功能
        # → 一律繼續目前流程
        else:

            route = active_route


    print("Detected Route:")
    print(detected_route)

    print("Active Route:")
    print(active_route)

    print("Final Route:")
    print(route)


    # =====================================================
    # 2. Meditation
    # =====================================================

    if route == "meditation":

        # =====================================================
        # 判斷是不是「新的一次」Meditation Flow
        # =====================================================

        if previous_active_route != "meditation":

            # 開始新 Meditation Flow 時，
            # 舊的 Recommendation 不應該再被當成這次結果
            state["meditation_recommendation"] = None


        active_route = "meditation"

        state["active_route"] = "meditation"


        try:
            new_context = extract_context(
                request.message
            )

        except GoogleRateLimitError:

            return {
                "route": "system",
                "status": "error",
                "missingField": None,
                "reply": "目前 Lumi 的 AI 服務使用量較高，請稍後再試一次。",
                "options": [],
                "action": None,
                "context": current_context.model_dump()
            }


        print("New Context:")
        print(
            new_context.model_dump()
        )


        # =====================================================
        # Merge 多輪資料
        # =====================================================

        current_context = merge_context(
            current_context,
            new_context
        )


        # 非常重要：
        # Merge 完要放回這個 Conversation
        state["current_context"] = (
            current_context
        )


        print("Merged Context:")
        print(
            current_context.model_dump()
        )


        missing_fields = get_missing_fields(
            current_context
        )


        print("Missing Fields:")
        print(
            missing_fields
        )


        # =====================================================
        # 還缺資料
        # → 保留 Context，下一輪繼續
        # =====================================================

        if missing_fields:

            response = build_response(
                missing_fields
            )

            return {
                **response,
                "context":
                    current_context.model_dump()
            }


        # =====================================================
        # 資料完整 → Meditation Recommendation
        # =====================================================

        recommendation = recommend_meditation(
            current_context
        )


        print(
            "Meditation Recommendation:"
        )

        print(
            recommendation
        )


        # =====================================================
        # 保存這個 Conversation 最新一次 Meditation Recommendation
        # =====================================================

        state[
            "meditation_recommendation"
        ] = recommendation


        print(
            "Meditation Recommendation 已保存"
        )

        print(
            "Firebase UID：",
            user_id
        )

        print(
            "Conversation ID：",
            conversation_id
        )


        finished_context = (
            current_context.model_dump()
        )


        # =====================================================
        # Meditation Flow 完成
        #
        # active_route Reset
        # Context Reset
        #
        # 但是 recommendation 保留給 GET
        # =====================================================

        state["active_route"] = None

        state["current_context"] = (
            CurrentContext()
        )


        return {
            "route": "meditation",
            "status": "ready",
            "missingField": None,
            "reply": "好，我已經幫你準備好適合現在狀態的冥想。",
            "options": [],
            "action": {
                "type": "start_meditation",
                "data": recommendation
            },
            "context": finished_context
        }


    # =====================================================
    # 3. Breathing
    # =====================================================

    if route == "breathing":

        active_route = "breathing"

        state["active_route"] = (
            "breathing"
        )

        try:
            new_breathing_context = (
                extract_breathing_context(
                    request.message
                )
            )

        except GoogleRateLimitError:
            return {
                "route": "system",
                "status": "error",
                "missingField": None,
                "reply": "目前 Lumi 的 AI 服務使用量較高，請稍後再試一次。",
                "options": [],
                "action": None,
                "context": breathing_context.model_dump()
            }


        print("New Breathing Context:")
        print(
            new_breathing_context.model_dump()
        )


        breathing_context = merge_breathing_context(
            breathing_context,
            new_breathing_context
        )

        state["breathing_context"] = (
            breathing_context
        )


        print("Merged Breathing Context:")
        print(
            breathing_context.model_dump()
        )


        missing_fields = (
            get_missing_breathing_fields(
                breathing_context
            )
        )


        print("Missing Breathing Fields:")
        print(missing_fields)


        # -------------------------------------------------
        # 還缺資料
        # -------------------------------------------------

        if missing_fields:

            response = build_breathing_response(
                missing_fields
            )

            return {
                **response,
                "context": breathing_context.model_dump()
            }


        # -------------------------------------------------
        # 資料完整 → 推薦呼吸練習
        # -------------------------------------------------

        recommendation = recommend_breathing(
            breathing_context
        )


        print("Breathing Recommendation:")
        print(recommendation)


        finished_context = (
            breathing_context.model_dump()
        )

        finished_duration = (
            breathing_context.duration
        )


        # 結束流程
        state["active_route"] = None

        state["breathing_context"] = (
            BreathingContext()
        )


        return {
            "route": "breathing",
            "status": "ready",
            "missingField": None,
            "reply": "好，我已經幫你選好適合的呼吸練習。",
            "options": [],
            "action": {
                "type": "start_breathing",
                "data": {
                    "duration": finished_duration,
                    **recommendation
                }
            },
            "context": finished_context
        }


    # =====================================================
    # 4. Acupressure
    # =====================================================

    if route == "acupressure":

        active_route = "acupressure"

        state["active_route"] = (
            "acupressure"
        )

        try:
            new_acupressure_context = (
                extract_acupressure_context(
                    request.message
                )
            )

        except GoogleRateLimitError:
            return {
                "route": "system",
                "status": "error",
                "missingField": None,
                "reply": "目前 Lumi 的 AI 服務使用量較高，請稍後再試一次。",
                "options": [],
                "action": None,
                "context": acupressure_context.model_dump()
            }


        print("New Acupressure Context:")
        print(
            new_acupressure_context.model_dump()
        )


        acupressure_context = merge_acupressure_context(
            acupressure_context,
            new_acupressure_context
        )

        state["acupressure_context"] = (
            acupressure_context
        )


        print("Merged Acupressure Context:")
        print(
            acupressure_context.model_dump()
        )


        missing_fields = (
            get_missing_acupressure_fields(
                acupressure_context
            )
        )


        print("Missing Acupressure Fields:")
        print(missing_fields)


        # -------------------------------------------------
        # 還缺資料
        # -------------------------------------------------

        if missing_fields:

            response = build_acupressure_response(
                missing_fields,
                acupressure_context
            )

            return {
                **response,
                "context": acupressure_context.model_dump()
            }


        # -------------------------------------------------
        # 資料完整 → 推薦穴位
        # -------------------------------------------------

        recommendation = recommend_acupressure(
            acupressure_context
        )


        print("Acupressure Recommendation:")
        print(recommendation)


        # -------------------------------------------------
        # 防呆
        # -------------------------------------------------

        if recommendation is None:

            finished_context = (
                acupressure_context.model_dump()
            )

            state["active_route"] = None

            state["acupressure_context"] = (
                AcupressureContext()
            )

            return {
                "route": "acupressure",
                "status": "error",
                "missingField": None,
                "reply": "目前找不到符合這個狀況的穴位推薦。",
                "options": [],
                "action": None,
                "context": finished_context
            }


        finished_context = (
            acupressure_context.model_dump()
        )


        # 結束流程
        state["active_route"] = None

        # Reset
        state["acupressure_context"] = (
            AcupressureContext()
        )


        return {
            "route": "acupressure",
            "status": "ready",
            "missingField": None,
            "reply": "好，我已經幫你找到適合目前狀況的穴位。",
            "options": [],
            "action": {
                "type": "start_acupressure",
                "data": recommendation
            },
            "context": finished_context
        }


    # =====================================================
    # 5. App Help
    # =====================================================

    if route == "app_help":

        state["active_route"] = None

        return {
            "route": "app_help",
            "status": "answered",
            "missingField": None,
            "reply": (
                "你可以透過 Lumi 進行冥想推薦、"
                "呼吸練習和穴位按摩，"
                "也可以直接跟我說你現在的狀態。"
            ),
            "options": [],
            "action": None,
            "context": current_context.model_dump()
        }
    # =====================================================
    # 6. Knowledge / RAG
    # =====================================================

    if route == "knowledge":

        try:
            rag_result = answer_with_rag(
                request.message
            )

        except GoogleRateLimitError:
            return {
                "route": "system",
                "status": "error",
                "missingField": None,
                "reply": "目前 Lumi 的 AI 服務使用量較高，請稍後再試一次。",
                "options": [],
                "action": None,
                "context": {}
            }


        # RAG 有找到相關知識
        if rag_result["answer"]:

            print("RAG Knowledge Found:")
            print(rag_result["sources"])

            return {
                "route": "knowledge",
                "status": "answered",
                "missingField": None,
                "reply": rag_result["answer"],
                "options": [],
                "action": None,
                "context": {},
                "sources": rag_result["sources"]
            }


        # 問題看起來是知識問題，
        # 但 Lumi Knowledge Base 沒有相關內容
        return {
            "route": "knowledge",
            "status": "no_knowledge",
            "missingField": None,
            "reply": "目前我的知識庫裡還沒有足夠的相關資訊。",
            "options": [],
            "action": None,
            "context": {},
            "sources": []
        }

    # # =====================================================
    # # 6. General Chat
    # # =====================================================

    # return {
    #     "route": "general_chat",
    #     "status": "answered",
    #     "missingField": None,
    #     "reply": "我有收到你的訊息，之後這裡會接一般聊天功能。",
    #     "options": [],
    #     "action": None,
    #     "context": current_context.model_dump()
    # }
    # =====================================================
    # 6. General Chat / RAG Knowledge
    # =====================================================

    try:
        rag_result = answer_with_rag(
            request.message
        )

    except GoogleRateLimitError:
        rag_result = {
            "answer": None,
            "sources": []
        }


    # -----------------------------------------------------
    # RAG 找到相關知識
    # -----------------------------------------------------

    if rag_result["answer"]:

        print("RAG Knowledge Found:")
        print(rag_result["sources"])

        return {
            "route": "knowledge",
            "status": "answered",
            "missingField": None,
            "reply": rag_result["answer"],
            "options": [],
            "action": None,
            "context": {},
            "sources": rag_result["sources"]
        }


    # -----------------------------------------------------
    # RAG 也找不到
    # → 才是真正 General Chat
    # -----------------------------------------------------

    print("No Relevant RAG Knowledge")

    return {
        "route": "general_chat",
        "status": "answered",
        "missingField": None,
        "reply": "我有收到你的訊息，之後這裡會接一般聊天功能。",
        "options": [],
        "action": None,
        "context": current_context.model_dump()
    }

@app.get(
    "/lumi/recommendation/{user_id}/{conversation_id}"
)
def get_recommendation(
    user_id: str,
    conversation_id: str
):

    state = conversation_states.get(
        conversation_id
    )


    # =====================================================
    # Conversation 不存在
    # =====================================================

    if state is None:

        return {
            "status": "not_found",
            "userId": user_id,
            "conversationId": conversation_id,
            "recommendation": None
        }


    # =====================================================
    # Firebase UID 不符合
    # =====================================================

    if state["userId"] != user_id:

        return {
            "status": "user_mismatch",
            "userId": user_id,
            "conversationId": conversation_id,
            "recommendation": None
        }


    # =====================================================
    # 取得最新 Meditation Recommendation
    # =====================================================

    recommendation = state.get(
        "meditation_recommendation"
    )


    # Meditation Flow 還沒完成
    if recommendation is None:

        return {
            "status": "not_ready",
            "userId": user_id,
            "conversationId": conversation_id,
            "recommendation": None
        }


    return {
        "status": "success",
        "userId": user_id,
        "conversationId": conversation_id,
        "recommendation": recommendation
    }