# from extractor import extract_context, get_missing_fields
# from response_builder import build_response

# message = "我最近事情很多壓力很大，想做十分鐘放鬆一下"

# result = extract_context(message)
# missing_fields = get_missing_fields(result)
# response = build_response(missing_fields)

# print("Current Context:")
# print(result.model_dump())

# print("\nMissing Fields:")
# print(missing_fields)

# print("\nResponse:")
# print(response)

from extractor import extract_context, get_missing_fields
from response_builder import build_response
from context_manager import merge_context


# -------------------------
# 第一輪
# -------------------------

message1 = "我最近事情很多壓力很大，想做十分鐘放鬆一下"

context = extract_context(message1)

missing_fields = get_missing_fields(context)
response = build_response(missing_fields)

print("=== 第一輪 ===")
print("Current Context:")
print(context.model_dump())

print("\nResponse:")
print(response)


# -------------------------
# 第二輪
# -------------------------

message2 = "溫柔陪伴"

new_context = extract_context(message2)

context = merge_context(
    context,
    new_context
)

missing_fields = get_missing_fields(context)
response = build_response(missing_fields)

print("\n\n=== 第二輪 ===")
print("New Extracted Context:")
print(new_context.model_dump())

print("\nMerged Context:")
print(context.model_dump())

print("\nMissing Fields:")
print(missing_fields)

print("\nResponse:")
print(response)