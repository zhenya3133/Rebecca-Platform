from logger import log_event


def log(message: str) -> None:
    log_event(f"knowledge_curator: {message}")
