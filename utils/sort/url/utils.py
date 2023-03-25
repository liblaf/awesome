def escape_markdown(text: str) -> str:
    text = text.replace(r"|", r"\|")
    return text
