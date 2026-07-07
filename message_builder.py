def build_message(decision, category, merchant, trigger, customer=None):

    merchant_name = merchant.identity.get("name", "Merchant")
    performance = merchant.performance or {}
    offers = merchant.offers or []

    ctr = performance.get("ctr")
    leads = performance.get("leads")

    offer_name = offers[0]["name"] if offers else "your offer"

    action = decision["action"]

    if action == "promote_offer":
        return (
            f"{merchant_name}, your CTR is {ctr}% which is below similar "
            f"{category.slug}. Your active offer '{offer_name}' is ready "
            "to promote. Would you like me to create a campaign?"
        )

    elif action == "refresh_listing":
        return (
            f"{merchant_name}, updating recent photos and posts can improve visibility."
        )

    elif action == "boost_growth":
        return (
            f"Great work {merchant_name}! You've generated {leads} leads. "
            "This is the right time to scale your campaigns."
        )

    elif action == "festival_offer":
        return (
            f"{merchant_name}, highlight '{offer_name}' during the festival "
            "to attract more customers."
        )

    elif action == "festival_campaign":
        return (
            f"{merchant_name}, create a festival offer to capture seasonal demand."
        )

    elif action == "share_research":
        return (
            f"New {category.slug} research is available. "
            "Would you like a 2-minute summary?"
        )

    elif action == "appointment_reminder":
        customer_name = (
            customer.identity.get("name", "Customer")
            if customer else "Customer"
        )

        return (
            f"{customer_name} is due for a follow-up appointment."
        )

    return f"{merchant_name}, I found a growth opportunity for your business."