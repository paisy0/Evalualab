class EvalLabError(Exception):
    pass


class ConnectionFailed(EvalLabError):
    def __init__(self, db_type: str, host: str, port: int, reason: str):
        self.db_type = db_type
        self.host = host
        self.port = port
        super().__init__(
            f"{db_type} connection failed → {host}:{port}. "
            f"Check .env credentials. Reason: {reason}"
        )


class QueryFailed(EvalLabError):
    def __init__(self, query_preview: str, reason: str):
        self.query_preview = query_preview
        super().__init__(f"Query failed: {reason}\n  → {query_preview}")


class NotConnected(EvalLabError):
    def __init__(self):
        super().__init__(
            "Not connected. Use `with get_loader('postgres') as db:` "
            "or call .connect() first."
        )


class UnknownLoader(EvalLabError):
    def __init__(self, db_type: str, available: list[str]):
        self.db_type = db_type
        super().__init__(
            f"Unknown db_type '{db_type}'. Pick one: {available}"
        )


class UnknownEvalType(EvalLabError):
    def __init__(self, eval_type: str, query: str = "?"):
        self.eval_type = eval_type
        super().__init__(
            f"No evaluator for type '{eval_type}' (query: '{query}')"
        )
