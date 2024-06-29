import stripe
stripe.api_key = "sk_test_51PATYu089JUuVWC5gd49xLoAkxyGGVYgPevTFjOYpRCaTodm7Fr12sfLvpQXHWzkxcxHvjB8fsRa0UAy7jsgJ9BV00AFn9GUfL"


all_payment_intent_events = stripe.Event.list(
    limit=10,
    # type="payment_intent.*"  # Fetch all types of payment_intent events
)

for event in all_payment_intent_events:
    # if event['data']['object'].get('id') == payment_id:
    print("--------------------------------------")
    print(event)

# print(events)