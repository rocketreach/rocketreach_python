from collections import OrderedDict

from rocketreach.resource import Resource


class Person(Resource):
    """
    A class representing a Person Profile, returned in lookups, check status and search.
    Example attributes:

    {
        "id": 123456,
        "status": "complete",
        "name": "John Done",
        "profile_pic": "https://www.example.com/path/to/profile.jpg",
        "linkedin_url": "https://www.linkedin.com/in/john-doe-example",
        "links": {
            "crunchbase": "https://www.crunchbase.com/person/john-doe-example",
            "twitter": "https://twitter.com/john-doe-example",
            "linkedin": "https://www.linkedin.com/in/john-doe-example",
            "instagram": "https://www.instagram.com/john-doe-example"
        },
        "location": "Seattle, Washington, United States",
        "current_title": "Founder and CEO",
        "current_employer": "Example, Inc.",
        "current_work_email": "john.doe@example.com",
        "current_personal_email": john.doe@gmail.com,
        "emails": [
            {
                "email": "john.doe@example.com",
                "smtp_valid": "valid",
                "type": "professional"
            },
            {
                "email": "john.doe@gmail.com",
                "smtp_valid": "valid",
                "type": "personal"
            }
        ],
        "phones": [
            {
                "number": "+1235551221",
                "type": "office"
            },
            {
                "number": "+1235551222",
                "type": "mobile"
            }
        ]
    }
    """
    pass


class PersonCollection(list):
    """
    A collection of Person resources, returned in searches and check status.
    """
    pass
