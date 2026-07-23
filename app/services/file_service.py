from fastapi import HTTPException, UploadFile, status
import shutil
from pathlib import Path
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

from app.core.config import settings


class FileService:

    SOURCE_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".java",
        ".go",
        ".rs",
        ".cpp",
        ".c",
        ".cs",
        ".php",
        ".rb",
        ".swift",
        ".kt",
        ".sql",
        ".html",
        ".css",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".toml",
        ".md",
        ".sh",
    }

    IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
    }

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIRECTORY)
        self.upload_dir.mkdir(parents=True, exist_ok=True)


    def save_upload(self, file: UploadFile) -> Path:

        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file was uploaded")

        filename = f"{uuid4().hex}_{file.filename}"
        destination = self.upload_dir / filename

        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        except Exception:
            if destination.exists():
                destination.unlink()

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save uploaded file")

        return destination


    def read_uploaded_file(self, file: UploadFile) -> str:

        path = self.save_upload(file)

        try:

            if path.suffix.lower() not in self.SOURCE_EXTENSIONS:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported source file type")

            return path.read_text( encoding="utf-8")

        except UnicodeDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file encoding")

        finally:
            self.cleanup(path)



    def extract_archive(self,  archive_path: Path) -> Path:

        if archive_path.suffix.lower() != ".zip":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail="Only ZIP archives are supported")

        extract_dir = self.upload_dir / archive_path.stem
        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            with ZipFile(archive_path, "r") as archive:
                archive.extractall(extract_dir)

        except BadZipFile:
            self.cleanup(extract_dir)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid ZIP archive.",
            )

        return extract_dir

    def collect_source_files(self, project_path: Path) -> list[Path]:

        source_files: list[Path] = []

        for path in project_path.rglob("*"):

            if not path.is_file():
                continue

            if any(ignored in path.parts for ignored in self.IGNORED_DIRECTORIES):
                continue

            if path.suffix.lower() not in self.SOURCE_EXTENSIONS:
                continue

            source_files.append(path)

        source_files.sort()

        return source_files

    def combine_source_files(self, files: list[Path]) -> str:

        output: list[str] = []

        for file in files:

            try:
                content = file.read_text(encoding="utf-8")

            except UnicodeDecodeError:
                continue

            except Exception:
                continue

            relative_name = file.name

            output.append(
                f"""
    ==================================================
    FILE: {relative_name}
    ==================================================

    {content}
                """)


        return "\n".join(output)

    def cleanup(self, path: Path) -> None:

        if not path.exists():
            return

        if path.is_file():
            path.unlink()

        elif path.is_dir():
            shutil.rmtree(path, ignore_errors=True)


    def read_project(self, project_path: Path ) -> str:

        source_files = self.collect_source_files(project_path)

        if not source_files:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No supported source files were found")

        return self.combine_source_files(source_files)


    def read_archive(self, file: UploadFile) -> str:

        archive_path = self.save_upload(file)
        extract_path = None

        try:
            extract_path = self.extract_archive(archive_path)
            return self.read_project(extract_path)

        finally:
            self.cleanup(archive_path)
            if extract_path:
                self.cleanup(extract_path)

