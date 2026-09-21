import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


# =========================================================
# Firebase 初始化
# 本機：使用 Application Default Credentials
# Render：使用 FIREBASE_CREDENTIALS 環境變數
# =========================================================

try:
    firebase_admin.get_app()

except ValueError:

    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

    if firebase_credentials:
        # =================================================
        # Render 環境
        # =================================================
        service_account_info = json.loads(firebase_credentials)

        cred = credentials.Certificate(service_account_info)

        firebase_admin.initialize_app(
            cred,
            options={
                "projectId": "ming-advisor-ff390"
            }
        )

        print("Firebase initialized using FIREBASE_CREDENTIALS")

    else:
        # =================================================
        # 本機環境
        # 使用 Application Default Credentials
        # =================================================
        firebase_admin.initialize_app(
            options={
                "projectId": "ming-advisor-ff390"
            }
        )

        print("Firebase initialized using Application Default Credentials")


db = firestore.client()


# =========================================================
# Lumi Conversation
# =========================================================

def save_conversation(
    user_id: str,
    conversation_id: str,
    conversation_data: dict
):
    """
    儲存 Lumi conversation。

    Firestore path:

    users/{userId}/
        lumiConversations/{conversationId}
    """

    if not user_id:
        raise ValueError("user_id 不可為空")

    if not conversation_id:
        raise ValueError("conversation_id 不可為空")

    conversation_ref = (
        db
        .collection("users")
        .document(user_id)
        .collection("lumiConversations")
        .document(conversation_id)
    )

    # -------------------------------------------------
    # 建立 Firestore 專用副本
    # 不直接修改 FastAPI 原本的 conversation_data
    # -------------------------------------------------

    payload = dict(conversation_data)

    # -------------------------------------------------
    # 判斷是不是第一次建立
    # -------------------------------------------------

    snapshot = conversation_ref.get()

    if snapshot.exists:

        # 已存在 → 更新
        payload["updatedAt"] = firestore.SERVER_TIMESTAMP

        conversation_ref.set(
            payload,
            merge=True
        )

        print(
            "Firestore Conversation Updated:",
            f"users/{user_id}/"
            f"lumiConversations/{conversation_id}"
        )

    else:

        # 第一次 → 建立
        payload["createdAt"] = firestore.SERVER_TIMESTAMP
        payload["updatedAt"] = firestore.SERVER_TIMESTAMP

        conversation_ref.set(payload)

        print(
            "Firestore Conversation Created:",
            f"users/{user_id}/"
            f"lumiConversations/{conversation_id}"
        )