from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    surname: str
    loginname: str
    email: str
