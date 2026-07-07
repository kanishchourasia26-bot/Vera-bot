from decision_engine import decision_engine
from models import ReplyResponse

from context.category_context import CategoryContext
from context.merchant_context import MerchantContext
from context.trigger_context import TriggerContext
from context.customer_context import CustomerContext


def compose(category, merchant, trigger, customer=None):

    # -------------------------
    # Build Context Objects
    # -------------------------

    category_ctx = CategoryContext.from_request(category)
    merchant_ctx = MerchantContext.from_request(merchant)
    trigger_ctx = TriggerContext.from_request(trigger)
    customer_ctx = CustomerContext.from_request(customer)

    # -------------------------
    # Decision Engine
    # -------------------------

    decision = decision_engine.decide(
        category_ctx,
        merchant_ctx,
        trigger_ctx,
        customer_ctx
    )

    merchant_name = merchant_ctx.identity.get("name", "Merchant")

    performance = merchant_ctx.performance or {}
    offers = merchant_ctx.offers or []

    ctr = performance.get("ctr")
    leads = performance.get("leads")
    views = performance.get("views")

    offer_name = ""
    offer_price = ""

    if offers:
        offer_name = offers[0].get("name", "")
        offer_price = offers[0].get("price", "")

    body = ""

    # --------------------------------------------------

    if decision["action"] == "promote_offer":

        body = (
            f"{merchant_name}, "
            f"your CTR is {ctr}% which is below similar "
            f"{category_ctx.slug} businesses in your area. "
        )

        if views:
            body += f"You received {views} profile views recently. "

        if offer_name:
            body += (
                f"Your active offer '{offer_name}'"
            )

            if offer_price:
                body += f" (₹{offer_price})"

            body += (
                " is already live. "
                "Promoting this offer now can improve visibility "
                "and bring more customers. "
            )

        body += "I can generate the campaign in one click."

    # --------------------------------------------------

    elif decision["action"] == "refresh_listing":

        body = (
            f"{merchant_name}, your listing looks inactive. "
            "Updating recent posts and photos can improve discovery."
        )

    # --------------------------------------------------

    elif decision["action"] == "boost_growth":

        body = f"Great work {merchant_name}! "

        if leads:
            body += f"You've already generated {leads} leads. "

        body += (
            "Now is a great time to scale campaigns and reach more customers."
        )

    # --------------------------------------------------

    elif decision["action"] == "festival_offer":

        body = (
            f"{merchant_name}, festivals usually bring higher customer demand. "
        )

        if offer_name:
            body += f"Promote your '{offer_name}' offer "

        body += "to attract more bookings."

    # --------------------------------------------------

    elif decision["action"] == "festival_campaign":

        body = (
            f"{merchant_name}, festivals usually bring higher customer demand. "
            "Creating a limited-time offer now can improve conversions."
        )

    # --------------------------------------------------

    elif decision["action"] == "share_research":

        body = (
            f"This week's {category_ctx.slug} research is ready. "
            "It includes trends and recommendations for your business."
        )

    # --------------------------------------------------

    elif decision["action"] == "appointment_reminder":

        customer_name = "Customer"

        if customer_ctx:
            customer_name = customer_ctx.identity.get("name", "Customer")

        body = (
            f"{customer_name} is due for a follow-up. "
            "Sending a reminder today can improve repeat visits."
        )

    # --------------------------------------------------

    else:

        body = (
            f"{merchant_name}, I found an opportunity to improve your business."
        )

    return ReplyResponse(
        body=body,
        cta=decision["cta"],
        send_as="merchant_on_behalf" if customer_ctx else "vera",
        suppression_key=trigger_ctx.suppression_key,
        rationale=decision["reason"]
    )