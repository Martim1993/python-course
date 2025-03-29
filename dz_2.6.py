import re


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9]+[a-zA-Z0-9._-]*@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+$'
    return bool(re.fullmatch(pattern, email))


print(is_valid_email("example@example.com"))
print(is_valid_email("invalid-email@com"))
print()


def extract_urls(text: str) -> list:
    pattern = r'(?:https?://|www\.)[a-zA-Z0-9.-]+(?:\/[a-zA-Z0-9.-]*)*'
    urls = re.findall(pattern, text)
    return urls


text = "Visit our website at https://example.com or http://www.example.org for more info."
print(extract_urls(text))
print()


def replace_date_format(text: str) -> str:
    replaced_text = re.sub(
        r'(\d{2})/(\d{2})/(\d{4})',
        r'\3-\1-\2',
        text
    )
    return replaced_text


text = "The event will be held on 08/25/2024. Please RSVP by 07/30/2024."
print(replace_date_format(text))
print()


def is_valid_phone_number(phone: str) -> bool:
    pattern = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return bool(re.fullmatch(pattern, phone))

print(is_valid_phone_number("(123) 456-7890"))
print(is_valid_phone_number("123-456-7890"))
print(is_valid_phone_number("123.456.7890"))
print(is_valid_phone_number("1234567890"))
print(is_valid_phone_number("123-4567-890"))
