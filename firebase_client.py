import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore


# =====================================================
# Firebase 初始化
# =====================================================

if not firebase_admin._apps:

    cred = credentials.Certificate(
        "firebase-service-account.json"
    )

    firebase_admin.initialize_app(
        cred
    )


db = firestore.client()


# =====================================================
# Lumi Conversation
# =====================================================

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
        raise ValueError(
            "user_id 不可為空"
        )

    if not conversation_id:
        raise ValueError(
            "conversation_id 不可為空"
        )


    conversation_ref = (
        db
        .collection("users")
        .document(user_id)
        .collection("lumiConversations")
        .document(conversation_id)
    )


    # -------------------------------------------------
    # 判斷是不是第一次建立
    # -------------------------------------------------

    snapshot = conversation_ref.get()


    if snapshot.exists:

        # 已存在 → 更新
        conversation_data["updatedAt"] = (
            firestore.SERVER_TIMESTAMP
        )

        conversation_ref.set(
            conversation_data,
            merge=True
        )

        print(
            "Firestore Conversation Updated:",
            f"users/{user_id}/"
            f"lumiConversations/{conversation_id}"
        )


    else:

        # 第一次 → 建立
        conversation_data["createdAt"] = (
            firestore.SERVER_TIMESTAMP
        )

        conversation_data["updatedAt"] = (
            firestore.SERVER_TIMESTAMP
        )

        conversation_ref.set(
            conversation_data
        )

        print(
            "Firestore Conversation Created:",
            f"users/{user_id}/"
            f"lumiConversations/{conversation_id}"
        )