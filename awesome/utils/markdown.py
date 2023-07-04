def escape(text: str) -> str:
    """Escape markdown special characters"""
    text = text.replace(r"_", r"\_")
    text = text.replace(r"*", r"\*")
    text = text.replace(r"`", r"\`")
    text = text.replace(r"|", r"\|")
    return text
