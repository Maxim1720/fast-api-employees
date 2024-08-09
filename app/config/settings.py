import os
from dotenv import load_dotenv

load_dotenv()
print(os.environ)


def env(key):
    return os.getenv(key)
