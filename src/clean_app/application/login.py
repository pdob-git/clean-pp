class LoginUseCase:
    def execute(self, host: str, user: str, password: str) -> None:
        # store credentials or validate connection
        print("Login successful")
        print(f"Host: {host}, User: {user}, Password: {password}")