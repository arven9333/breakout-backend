from dataclasses import dataclass


@dataclass
class DatabaseSettings:
    plugin: str
    user: str
    password: str
    host: str
    port: int
    name: str

    def get_dsn(self):
        return f"{self.plugin}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
