from conversation_memory import conversation, use_memory, remember, ConversationBusy
from fastapi import HTTPException

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from rag.rag_service import answer_with_rag

from extractor import extract_context, get_missing_fields, CurrentContext
from response_builder import build_response
from context_manager import merge_context
from router import detect_route, wants_personal_data, wants_breathing_settings, wants_acupressure_entry

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


from firebase_client import save_conversation

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    body = await request.body()

    print("\n")
    print("========== FASTAPI 422 DEBUG ==========")
    print("URL:", request.url)
    print("Content-Type:", request.headers.get("content-type"))
    print("Raw Body:", body.decode("utf-8", errors="replace"))
    print("Validation Errors:", exc.errors())
    print("=======================================")
    print("\n")

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        }
    )


class ChatRequest(BaseModel):
    userId: str | None = None
    conversationId: str | None = None
    caiConversationId: str | None = None
    message: str | None = None

@app.get("/firebase/test")
def firebase_test():

    test_user_id = "test_user"

    test_conversation_id = "test_conversation"

    test_data = {
        "userId": test_user_id,
        "conversationId": test_conversation_id,
        "sessionId": None,
        "activeRoute": None,
        "status": "test",

        "meditationContext": {},
        "breathingContext": {},
        "acupressureContext": {},

        "recommendationInput": None
    }

    save_conversation(
        user_id=test_user_id,
        conversation_id=test_conversation_id,
        conversation_data=test_data
    )

    return {
        "status": "ok",
        "message": "Firestore test success"
    }

    
# =====================================================
# Context
# =====================================================

# 冥想 Context

# 呼吸 Context

# 穴位 Context

# 目前正在執行的多輪流程

# =====================================================
# 給 Firebase / 組員使用的 Conversation Data
# =====================================================

def build_conversation_data(
    user_id,
    conversation_id,
    active_route,
    status,
    meditation_context=None,
    breathing_context=None,
    acupressure_context=None,
    recommendation_input=None,
    session_id=None
):
    return {
        "userId": user_id,
        "conversationId": conversation_id,
        "sessionId": session_id,

        "activeRoute": active_route,
        "status": status,

        "meditationContext": (
            meditation_context.model_dump()
            if meditation_context is not None
            else {}
        ),

        "breathingContext": (
            breathing_context.model_dump()
            if breathing_context is not None
            else {}
        ),

        "acupressureContext": (
            acupressure_context.model_dump()
            if acupressure_context is not None
            else {}
        ),

        "recommendationInput": recommendation_input
    }

def persist_conversation(request: ChatRequest, conversation_data: dict):
    if not request.userId or not request.conversationId:
        print("Skip Firestore save: missing userId or conversationId")
        return

    save_conversation(
        user_id=request.userId,
        conversation_id=request.conversationId,
        conversation_data=conversation_data
    )


def save_lumi_conversation(
    user_id: str | None,
    conversation_id: str | None,
    conversation_data: dict
):
    if not user_id or not conversation_id:
        print("Skip Firestore save: missing userId or conversationId")
        return

    try:
        save_conversation(
            user_id=user_id,
            conversation_id=conversation_id,
            conversation_data=conversation_data
        )

        print(
            "Lumi conversation saved:",
            f"users/{user_id}/lumiConversations/{conversation_id}"
        )

    except Exception as e:
        print("Firestore save failed:", e)


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
    if not request.userId or not request.userId.strip() or not request.conversationId or not request.conversationId.strip():
        raise HTTPException(status_code=422, detail="userId 與 conversationId 不可為空")
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=422, detail="message 不可為空")
    try:
        with conversation(request.userId, request.conversationId) as session:
            with use_memory(session):
                response = _lumi_chat_turn(request, session)
            remember(session, request.message, response)
            return response
    except ConversationBusy:
        raise HTTPException(status_code=409, detail="上一則訊息仍在處理，請稍後再送出")


def _lumi_chat_turn(request: ChatRequest, session):
    current_context = CurrentContext(**session.get('meditation_context', {}))
    breathing_context = BreathingContext(**session.get('breathing_context', {}))
    acupressure_context = AcupressureContext(**session.get('acupressure_context', {}))
    active_route = session.get('active_route')
    try:

        # =====================================================
        # Request 基本資料
        # =====================================================

        user_id = request.userId
        conversation_id = request.conversationId
        message = request.message or ""

        print("\n============================")
        print("收到 Lumi Request")
        print("User ID:", user_id)
        print("Conversation ID:", conversation_id)
        print("C.ai Conversation ID:", request.caiConversationId)
        print("Message:", repr(message))
        print("============================\n")

        # =====================================================
        # 1. Route 判斷
        # =====================================================

        detected_route = detect_route(message)

        if detected_route != "cancel" and wants_acupressure_entry(message):
            return {
                "route": "navigation",
                "status": "answered",
                "missingField": None,
                "reply": "點下方按鈕，就能前往穴道按摩頁。",
                "options": ["lumi:navigate:acupressure"],
                "action": None,
                "context": {}
            }

        if detected_route != "cancel" and wants_breathing_settings(message):
            return {
                "route": "navigation",
                "status": "answered",
                "missingField": None,
                "reply": "點下方按鈕開啟呼吸進階設定，就能調整吸氣、停留與吐氣秒數。",
                "options": ["lumi:navigate:breathing_settings"],
                "action": None,
                "context": {}
            }

        # Offer a local navigation button without consuming recommendation slots.
        if detected_route != "cancel" and wants_personal_data(message):
            return {
                "route": "navigation",
                "status": "answered",
                "missingField": None,
                "reply": "可以，點下方按鈕查看你的個人數據與練習紀錄。",
                "options": ["lumi:navigate:personal_records"],
                "action": None,
                "context": {}
            }


        # =====================================================
        # 使用者取消目前流程
        # =====================================================

        if detected_route == "cancel":

            print("Cancel Current Flow")

            current_context = CurrentContext()
            breathing_context = BreathingContext()
            acupressure_context = AcupressureContext()

            active_route = None

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

        elif detected_route in {"knowledge", "social"}:

            # 暫時回答問題或問候，保留原本的推薦進度。
            # social 也走現有 RAG 入口，由 simple_social_reply 回覆。
            route = "knowledge"

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
                    current_context = CurrentContext()

                elif active_route == "breathing":
                    breathing_context = BreathingContext()

                elif active_route == "acupressure":
                    acupressure_context = AcupressureContext()

                active_route = explicit_switch_route
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

            active_route = "meditation"

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
            print(new_context.model_dump())


            current_context = merge_context(
                current_context,
                new_context
            )


            print("Merged Context:")
            print(current_context.model_dump())


            missing_fields = get_missing_fields(
                current_context
            )


            print("Missing Fields:")
            print(missing_fields)


            # -------------------------------------------------
            # 還缺資料
            # -------------------------------------------------

            if missing_fields:

                response = build_response(
                    missing_fields
                )

                conversation_data = build_conversation_data(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    active_route="meditation",
                    status="collecting",
                    meditation_context=current_context,
                    breathing_context=breathing_context,
                    acupressure_context=acupressure_context
                )
                save_lumi_conversation(
                    user_id,
                    conversation_id,
                    conversation_data
                )

                print("\n========== Conversation Data ==========")
                print(conversation_data)
                print("=======================================\n")

                return {
                    **response,
                    "context": current_context.model_dump(),
                    "conversationData": conversation_data
                }

            # -------------------------------------------------
            # 資料完整 → 推薦冥想
            # -------------------------------------------------

            recommendation = recommend_meditation(
                current_context
            )


            print("Meditation Recommendation:")
            print(recommendation)


            finished_context = (
                current_context.model_dump()
            )

            # =====================================================
            # 整理 Recommendation Input
            # =====================================================

            recommendation_input = {
                "type": "meditation",
                "context": finished_context,
                "recommendation": recommendation
            }

            # =====================================================
            # 整理給組員 / Firebase 的資料
            # =====================================================

            conversation_data = build_conversation_data(
                user_id=user_id,
                conversation_id=conversation_id,
                active_route=None,
                status="ready",
                meditation_context=current_context,
                breathing_context=breathing_context,
                acupressure_context=acupressure_context,
                recommendation_input=recommendation_input
            )

            save_lumi_conversation(
                user_id,
                conversation_id,
                conversation_data
            )

            print("\n========== Conversation Data ==========")
            print(conversation_data)
            print("=======================================\n")

            # 結束流程
            active_route = None

            # Reset
            current_context = CurrentContext()


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
                "context": finished_context,
                "conversationData": conversation_data
            }


        # =====================================================
        # 3. Breathing
        # =====================================================

        if route == "breathing":

            active_route = "breathing"

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

                # 整理目前 Conversation Data
                conversation_data = build_conversation_data(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    active_route="breathing",
                    status="collecting",
                    meditation_context=current_context,
                    breathing_context=breathing_context,
                    acupressure_context=acupressure_context
                )

                # 儲存到 Firestore
                save_lumi_conversation(
                    user_id,
                    conversation_id,
                    conversation_data
                )
                print("\n========== Breathing Response ==========")
                print("Reply:", response.get("reply"))
                print("Options:", response.get("options"))
                print("========================================\n")

                print("\n========== Conversation Data ==========")
                print(conversation_data)
                print("=======================================\n")

                return {
                    **response,
                    "context": breathing_context.model_dump(),
                    "conversationData": conversation_data
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


            # =====================================================
            # 整理 Recommendation Input
            # =====================================================

            recommendation_input = {
                "type": "breathing",
                "context": finished_context,
                "recommendation": {
                    "duration": finished_duration,
                    **recommendation
                }
            }


            # =====================================================
            # 整理給 Firebase / 組員的 Conversation Data
            # =====================================================

            conversation_data = build_conversation_data(
                user_id=user_id,
                conversation_id=conversation_id,
                active_route=None,
                status="ready",
                meditation_context=current_context,
                breathing_context=breathing_context,
                acupressure_context=acupressure_context,
                recommendation_input=recommendation_input
            )


            # =====================================================
            # 儲存到 Firestore
            # =====================================================

            save_lumi_conversation(
                user_id,
                conversation_id,
                conversation_data
            )


            print("\n========== Conversation Data ==========")
            print(conversation_data)
            print("=======================================\n")


            # =====================================================
            # 結束流程
            # =====================================================

            active_route = None


            # Reset
            # 注意：一定要在 Firestore 儲存完成之後才能 Reset

            breathing_context = BreathingContext()


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
                "context": finished_context,
                "conversationData": conversation_data
            }


        # =====================================================
        # 4. Acupressure
        # =====================================================

        if route == "acupressure":

            active_route = "acupressure"

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

                # 整理目前 Conversation Data
                conversation_data = build_conversation_data(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    active_route="acupressure",
                    status="collecting",
                    meditation_context=current_context,
                    breathing_context=breathing_context,
                    acupressure_context=acupressure_context
                )

                # 儲存到 Firestore
                save_lumi_conversation(
                    user_id,
                    conversation_id,
                    conversation_data
                )

                print("\n========== Acupressure Response ==========")
                print("Reply:", response.get("reply"))
                print("Options:", response.get("options"))
                print("==========================================\n")

                print("\n========== Conversation Data ==========")
                print(conversation_data)
                print("=======================================\n")

                return {
                    **response,
                    "context": acupressure_context.model_dump(),
                    "conversationData": conversation_data
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
            # 防呆：找不到推薦
            # -------------------------------------------------

            if recommendation is None:

                finished_context = (
                    acupressure_context.model_dump()
                )

                conversation_data = build_conversation_data(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    active_route=None,
                    status="error",
                    meditation_context=current_context,
                    breathing_context=breathing_context,
                    acupressure_context=acupressure_context,
                    recommendation_input={
                        "type": "acupressure",
                        "context": finished_context,
                        "recommendation": None
                    }
                )

                save_lumi_conversation(
                    user_id,
                    conversation_id,
                    conversation_data
                )

                active_route = None
                acupressure_context = AcupressureContext()

                return {
                    "route": "acupressure",
                    "status": "error",
                    "missingField": None,
                    "reply": "目前找不到符合這個狀況的穴位推薦。",
                    "options": [],
                    "action": None,
                    "context": finished_context,
                    "conversationData": conversation_data
                }


            # -------------------------------------------------
            # 正常找到推薦
            # -------------------------------------------------

            finished_context = (
                acupressure_context.model_dump()
            )

            # =====================================================
            # 整理 Recommendation Input
            # =====================================================

            recommendation_input = {
                "type": "acupressure",
                "context": finished_context,
                "recommendation": recommendation
            }

            # =====================================================
            # 整理給 Firebase / 組員的 Conversation Data
            # =====================================================

            conversation_data = build_conversation_data(
                user_id=user_id,
                conversation_id=conversation_id,
                active_route=None,
                status="ready",
                meditation_context=current_context,
                breathing_context=breathing_context,
                acupressure_context=acupressure_context,
                recommendation_input=recommendation_input
            )

            # =====================================================
            # 儲存到 Firestore
            # =====================================================

            save_lumi_conversation(
                user_id,
                conversation_id,
                conversation_data
            )

            print("\n========== Conversation Data ==========")
            print(conversation_data)
            print("=======================================\n")

            # =====================================================
            # 結束流程
            # =====================================================

            active_route = None

            # Firestore 儲存完成後再 Reset
            acupressure_context = AcupressureContext()

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
                "context": finished_context,
                "conversationData": conversation_data
            }


        # =====================================================
        # 5. App Help
        # =====================================================

        if route == "app_help":

            active_route = None

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
    finally:
        session['meditation_context'] = current_context.model_dump()
        session['breathing_context'] = breathing_context.model_dump()
        session['acupressure_context'] = acupressure_context.model_dump()
        session['active_route'] = active_route
