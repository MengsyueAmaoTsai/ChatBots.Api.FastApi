class CurrentUser:
    """"""

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def user_id(self) -> str:
        return "1"

    @property
    def email(self) -> str:
        return "mengsyue.tsai@outlook.com"
