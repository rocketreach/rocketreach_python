from rocketreach.resource import Resource


class Account(Resource):
    """
    A class representing a RocketReach User's account.

    Example attributes:

        {
            "id": 12345,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "state": "registered",
            "lookup_credit_balance": 123,
            "plan": {
                "id": 221,
                "name": "Pro",
                "lookup_limit": 600
            },
            "lifetime_credits_spent": 1234,
            "api_key": "3e7k0123456789abcdef0123456789abcdef",
            "api_key_domain": "*",
            "daily_api_num_calls": 0,
            "daily_api_limit": 0,
            "lifetime_api_num_calls": 0
        }

    Note the daily_api_num_calls, daily_api_limit and lifetime_api_num_calls are no
    longer maintained and will likely be removed in a future version of the API.
    """
    pass
