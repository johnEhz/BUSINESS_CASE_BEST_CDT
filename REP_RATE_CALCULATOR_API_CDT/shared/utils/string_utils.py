class StringUtils:
    @staticmethod
    def hide_chain(chain: str, visible_chars: int = 3) -> str:
        if len(chain) <= visible_chars:
            return chain
        return f"{chain[:visible_chars]}{'*' * (len(chain) - visible_chars)}"
