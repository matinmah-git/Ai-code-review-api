import shutil
from pathlib import Path
from uuid import uuid4
from urllib.parse import urlparse
from git import Repo, GitCommandError
from app.services.file_service import FileService


class GithubService:

    def __init__(self):
        self.repository_dir = Path("repositories")
        self.repository_dir.mkdir(parents=True, exist_ok=True)
        self.file_service = FileService()

    def get_repository_name(self, repository_url: str) -> str:

        parsed = urlparse(repository_url)
        path = parsed.path.strip("/")
        if path.endswith(".git"):
            path = path[:-4]
        return path


    def validate_repository_url(self, repository_url: str) -> None:

        parsed = urlparse(repository_url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError("Invalid repository URL")

        if parsed.netloc.lower() != "github.com":
            raise ValueError("Only GitHub repositories are supported")

        path = parsed.path.strip("/")

        if len(path.split("/")) < 2:
            raise ValueError("Invalid GitHub repository URL")


    def _cleanup_repository(self, repository_path: Path) -> None:

        if repository_path.exists():
            shutil.rmtree(repository_path, ignore_errors=True)


    def clone_repository(self, repository_url: str)-> Path:

        self.validate_repository_url(repository_url)
        repository_name = (f"{uuid4().hex}")
        destination = (self.repository_dir / repository_name)
        try:
            Repo.clone_from(url=repository_url, to_path=destination, depth=1)
            return destination

        except GitCommandError as exc:
            if destination.exists():
                shutil.rmtree(destination, ignore_errors=True)
            raise RuntimeError(f"Failed to clone repository: {exc}")


    def read_repository(self, repository_url: str) -> str:

        repository_path = self.clone_repository(repository_url)

        try:
            return self.file_service.read_project(repository_path)

        finally:
            self._cleanup_repository(repository_path)


