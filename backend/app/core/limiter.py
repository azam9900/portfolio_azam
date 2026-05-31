"""
Rate Limiting — slowapi se powered
Contact form aur login pe spam se bachata hai
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

# IP address se rate limit karta hai
limiter = Limiter(key_func=get_remote_address)
