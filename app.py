from fastapi import FastAPI
from models import ReplyRequest
from composer import compose
from models import Category, Merchant, Trigger, Customer
from datetime import datetime, UTC

app = FastAPI(
    title="Vera Message Engine",
    version="1.0"
)

# ------------------------------------------------------------------
# In-memory Context Store
# ------------------------------------------------------------------

CONTEXT = {
    "categories": {},
    "merchants": {},
    "customers": {},
    "triggers": {}
}

# ------------------------------------------------------------------
# HEALTH
# ------------------------------------------------------------------

@app.get("/healthz")
@app.get("/v1/healthz")
def healthz():
    return {
        "status": "ok"
    }

# ------------------------------------------------------------------
# METADATA
# ------------------------------------------------------------------
@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Kanishq",
        "model": "Rule-Based + Gemini",
        "version": "1.0"
    }

# ------------------------------------------------------------------
# CONTEXT
# ------------------------------------------------------------------
@app.post("/context")
@app.post("/v1/context")
def context(payload: dict):

    scope = payload.get("scope")
    context_id = payload.get("context_id")
    data = payload.get("payload")

    # judge sends: category / merchant / trigger / customer
    scope_map = {
        "category": "categories",
        "merchant": "merchants",
        "trigger": "triggers",
        "customer": "customers",
    }

    key = scope_map.get(scope)

    if key is None:
        return {
            "accepted": False
        }

    CONTEXT[key][context_id] = data

    return {
        "accepted": True
    }
# ------------------------------------------------------------------
# TICK
# ------------------------------------------------------------------

@app.post("/tick")
@app.post("/v1/tick")
def tick(payload: dict):

    return {
        "status": "ok",
        "categories_loaded": len(CONTEXT["categories"]),
        "merchants_loaded": len(CONTEXT["merchants"]),
        "customers_loaded": len(CONTEXT["customers"]),
        "triggers_loaded": len(CONTEXT["triggers"])
    }

# ------------------------------------------------------------------
# REPLY (Original API)
# ------------------------------------------------------------------

@app.post("/reply")
def reply(request: ReplyRequest):

    return compose(
        request.category,
        request.merchant,
        request.trigger,
        request.customer
    )
# ------------------------------------------------------------------
# JUDGE COMPATIBILITY ENDPOINT
# ------------------------------------------------------------------

@app.post("/v1/reply")
def judge_reply(payload: dict):

    merchant_id = payload.get("merchant_id")
    message = (payload.get("message") or "").lower()

    merchant = CONTEXT["merchants"].get(merchant_id)

    if merchant is None:
        return {
            "action": "end",
            "body": "Merchant context not found."
        }

    category_slug = merchant.get("category_slug")
    category = CONTEXT["categories"].get(category_slug)

    if category is None:
        return {
            "action": "end",
            "body": "Category context not found."
        }

    # Hostile handling
    if any(x in message for x in [
        "stop",
        "spam",
        "leave me",
        "don't message",
        "dont message",
        "unsubscribe"
    ]):
        return {
            "action": "end",
            "body": "Understood. I won't send any more messages. Feel free to reach out anytime."
        }

    # Intent transition
    if any(x in message for x in [
        "yes",
        "ok",
        "okay",
        "sure",
        "do it",
        "lets do it",
        "let's do it",
        "next",
        "what next"
    ]):
        return {
            "action": "send",
            "body": "Done. I'm preparing the campaign now and will generate the draft for your review.",
            "done": True
        }

    # Dummy trigger expected by compose()
    trigger = {
        "kind": "conversation",
        "urgency": 1,
        "suppression_key": "",
        "payload": {},
        "source": "judge",
        "scope": "merchant"
    }

    customer = None

    # Convert dict -> Pydantic models
    category_model = Category(**category)
    merchant_model = Merchant(**merchant)
    trigger_model = Trigger(**trigger)
    customer_model = Customer(**customer) if customer else None
    auto_reply_patterns = [
    "thank you for contacting us",
    "our team will respond shortly",
    "we will respond shortly",
    "auto reply",
    "automated message",
    "away message",
    "out of office"
]

    if any(p in message for p in auto_reply_patterns):
      return {
        "action": "end",
        "body": ""
    }
    response = compose(
        category_model,
        merchant_model,
        trigger_model,
        customer_model
    )

    return  {
    "action": "end"
}