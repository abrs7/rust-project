"""Obvious implementation derived only from task.yaml's stated three fixes."""

from pathlib import Path
import sys


root = Path(sys.argv[1] if len(sys.argv) > 1 else "/app")
settings = root / "api_service" / "settings.py"
text = settings.read_text(encoding="utf-8")
text = text.replace(
    '    # "corsheaders",  # Missing - CORS won\'t work',
    '    "corsheaders",',
)
text = text.replace(
    '    # "corsheaders.middleware.CorsMiddleware",  # Missing - must be here before CommonMiddleware',
    '    "corsheaders.middleware.CorsMiddleware",',
)
text = text.replace(
    "# CORS_ALLOW_ALL_ORIGINS = True  # Missing - needed to allow all origins",
    "CORS_ALLOW_ALL_ORIGINS = True",
)
settings.write_text(text, encoding="utf-8")
