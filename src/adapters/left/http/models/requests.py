from pydantic import BaseModel


class ConnectNodes(BaseModel):
    nodes: list[str]

    def IsEmpty(self) -> bool:
        for node in self.nodes:
            if node:
                return False

        return True

    def GetNodes(self) -> list[str]:
        return [_ for _ in self.nodes if _]
