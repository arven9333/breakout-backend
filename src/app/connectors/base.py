from dataclasses import dataclass


@dataclass
class DatabaseSettings:
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str

    def get_dsn(self):
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
