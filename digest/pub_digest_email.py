import requests

from django.conf import settings


def get_api_header():
    return {
        "X-Secure-Token": settings.MAILHANDLER_RU_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def get_url(url):
    return f"http://api.mailhandler.ru/{url}"


def send_email(subject, html_body):
    """
    Send email with requests python library.
    """
    headers = get_api_header()

    emails = get_user_emails(settings.MAILHANDLER_RU_USER_LIST_ID)

    for email in emails:
        data = {
            "from": "mail@pythondigest.ru",
            "to": [email],
            "subject": subject,
            "html_body": html_body,
        }
        try:
            response = requests.post(
                get_url("message/send/"), json=data, headers=headers
            )
        except Exception as e:
            print(e)
    return "Ok"


def req(url, get=True, data=None):
    if get:
        func = requests.get
    else:
        func = requests.post

    return func(url, headers=get_api_header(), json=data)


def get_lists():
    response = req(get_url("sub/lists/"))

    items = []
    items.extend(response.json()["results"])
    while response.json()["next"] is not None:
        response = req(response.json()["next"])
        items.extend(response.json()["results"])

    return items


def get_id_list_by_name(lists, name):
    for item in lists:
        if item.get("name", "") == name:
            return item["id"]
    else:
        raise NotImplemented


def get_user_emails(list_id):
    users = []
    response = req(get_url(f"sub/lists/{list_id}/subscribers/"))
    users.extend(
        [
            x
            for x in response.json()["results"]
            if x["is_active"] and x["is_email_verified"]
        ]
    )
    while response.json()["next"] is not None:
        response = req(response.json()["next"])
        users.extend(
            [
                x
                for x in response.json()["results"]
                if x["is_active"] and x["is_email_verified"]
            ]
        )

    return [x["email"] for x in users if x]
