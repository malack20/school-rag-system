import logging

logger = logging.getLogger("chat_queries")

def log_query(user, query, response):
    logger.info(f"user={getattr(user, 'id', None)} query={query} response_len={len(response or '')}")
