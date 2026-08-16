import random


def generate_technician_code() -> str:
    number = random.randint(1000, 9999)
    return f"FT-{number}"