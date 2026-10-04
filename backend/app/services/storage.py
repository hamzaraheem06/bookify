from pathlib import Path
from ..core.config import settings

class LocalStorage:
    def __init__(self, root: Path | None = None):
        self.root = root or settings.storage_root
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, data: bytes) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return key

    def read(self, key: str) -> bytes:
        return (self.root / key).read_bytes()

    def delete(self, key: str) -> None:
        path = self.root / key
        if path.exists(): path.unlink()

    def path(self, key: str) -> Path:
        return self.root / key

storage = LocalStorage()
