from rules import CATEGORY_TONES, TRIGGER_PRIORITY


class DecisionEngine:
    """
    Deterministic Decision Engine

    Same input -> Same output
    No AI
    No Randomness
    """

    def decide(self, category, merchant, trigger, customer=None):

        trigger_kind = trigger.kind.lower()
        category_slug = category.slug.lower()

        signals = merchant.signals or []
        offers = merchant.offers or []
        performance = merchant.performance or {}
        history = merchant.conversation_history or []

        ctr = performance.get("ctr")
        views = performance.get("views")
        views_delta = performance.get("views_delta")
        leads = performance.get("leads")

        # -----------------------------
        # CATEGORY STRATEGY
        # -----------------------------

        category_strategy = {
            "dentists": {
                "tone": "clinical",
                "focus": "patient_recall"
            },
            "restaurants": {
                "tone": "friendly",
                "focus": "offers"
            },
            "salons": {
                "tone": "visual",
                "focus": "beauty"
            },
            "gyms": {
                "tone": "motivational",
                "focus": "membership"
            },
            "pharmacies": {
                "tone": "utility",
                "focus": "health"
            }
        }

        tone = CATEGORY_TONES.get(category_slug, "professional")
        priority = TRIGGER_PRIORITY.get(trigger_kind, 10)

        decision = {
    "priority": priority,
    "tone": tone,
    "action": "generic",
    "cta": "Learn More",
    "reason": "General recommendation"
}

        # -----------------------------
        # PRIORITY MAP
        # -----------------------------

        priority_map = {
            "recall_due": 120,
            "festival": 110,
            "perf_spike": 100,
            "perf_dip": 90,
            "research_digest": 60
        }
        strategy = category_strategy.get(
    category_slug,
    {
        "tone": "professional",
        "focus": "growth"
    }
)
        priority = priority_map.get(trigger_kind, 10)

        decision = {
            "priority": priority,
            "tone": strategy["tone"],
            "action": "generic",
            "cta": "Learn More",
            "reason": "General recommendation"
        }

        # -----------------------------
        # PERFORMANCE DIP
        # -----------------------------

        if trigger_kind == "perf_dip":
            ctr = performance.get("ctr", 0)
            views = performance.get("views", 0)

            if "ctr_below_peer_median" in signals:

                decision.update({
            "priority": 100,
            "action": "promote_offer",
            "cta": "Generate Campaign",
            "reason": f"CTR is {ctr}, below expected benchmark"
               })


            elif "stale_posts" in signals:

                decision.update({
                    "priority":90,
                    "action": "refresh_listing",
                    "cta": "Refresh Listing",
                    "reason": "Recent posts are outdated"
                })

            elif views < 100:

                 decision.update({
            "priority": 85,
            "action": "improve_visibility",
            "cta": "Improve Listing",
            "reason": f"Only {views} profile views detected"
        })

            else:

                decision.update({
                    "priority":80,
                    "action": "improve_visibility",
                    "cta": "Improve Listing",
                    "reason": "performance trend declining"
                })

        # -----------------------------
        # PERFORMANCE SPIKE
        # -----------------------------

        elif trigger_kind == "perf_spike":

            if leads is not None and leads > 50:

                decision.update({
                    "action": "boost_growth",
                    "cta": "Scale Campaign",
                    "reason": "Lead generation is strong"
                })

            else:

                decision.update({
                    "action": "boost_growth",
                    "cta": "Boost Campaign",
                    "reason": "Business performance is improving"
                })

        # -----------------------------
        # FESTIVAL
        # -----------------------------

        elif trigger_kind == "festival":

            if offers:

                decision.update({
                    "action": "festival_offer",
                    "cta": "Promote Offer",
                    "reason": "Festival traffic + Active offer"
                })

            else:

                decision.update({
                    "action": "festival_campaign",
                    "cta": "Create Festival Offer",
                    "reason": "Festival opportunity"
                })

        # -----------------------------
        # RESEARCH
        # -----------------------------

        elif trigger_kind == "research_digest":

            decision.update({
                "action": "share_research",
                "cta": "Read Research",
                "reason": f"Weekly {category_slug} research available"
            })

        # -----------------------------
        # CUSTOMER RECALL
        # -----------------------------

        elif trigger_kind == "recall_due":

            if customer:

                visits = customer.relationship.get("visits_total", 0)

                if visits >= 5:

                    decision.update({
                        "action": "appointment_reminder",
                        "cta": "Book Follow-up",
                        "reason": "Loyal customer recall"
                    })

                else:

                    decision.update({
                        "action": "appointment_reminder",
                        "cta": "Book Appointment",
                        "reason": "Customer recall due"
                    })

        # -----------------------------
        # CONVERSATION HISTORY
        # -----------------------------

        if history:

            last = history[-1]

            if isinstance(last, dict):

                if last.get("status") == "ignored":

                    decision["cta"] = "Quick Reminder"

                elif last.get("status") == "replied":

                    if decision["cta"] == "Learn More":
                        decision["cta"] = "Continue"

        return decision


decision_engine = DecisionEngine()