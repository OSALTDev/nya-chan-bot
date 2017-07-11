import re

"""
Intended for helper functions which are needed in multiple places but to small to warrant their own file.
"""

def filterTextForSqlInjection(text: str):
    """Remove all potentially unsafe characters from a text so it is safe to be injected into an SQL statement."""
    unsafe_characters = re.compile(r"[^a-zA-Z0-9 \-_:]*")
    return unsafe_characters.sub('', text).strip()
