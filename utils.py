import os
from git import Repo

INCLUDE_EXTENSIONS = (
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".ts", ".tsx",
    ".py", ".java", ".c", ".cpp", ".cs", ".h", ".hpp",
    ".sh", ".bash", ".zsh", ".ini", ".cfg", ".toml", ".yaml", ".yml",
    ".php", ".rb", ".pl", ".pm", ".rake",
    ".go", ".rs",
    ".swift", ".kt", ".kts", ".scala",
    ".dart", ".sql",
    ".xml", ".json", ".vue", ".svelte", ".md"
)

INCLUDE_FILENAMES = {"Makefile", "Dockerfile", "CMakeLists.txt"}

EXCLUDE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", ".vscode", ".idea", "build", "dist", "target", ".next", ".cache"
}

EXCLUDE_FILES = {
    ".gitignore", ".gitattributes", ".env", ".env.local",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "requirements.txt"
}

MIN_FILE_SIZE_BYTES = 20

def clone_repo(repo_url, dest="./repos"):
    repo_name = repo_url.rstrip('/').split("/")[-1]
    path = os.path.join(dest, repo_name)
    os.makedirs(dest, exist_ok=True)
    if not os.path.exists(path):
        Repo.clone_from(repo_url, path)
    return path

def is_valid_file(file):
    return (
        file in INCLUDE_FILENAMES or
        file.endswith(INCLUDE_EXTENSIONS)
    )

def summarize_codebase(path):
    summary = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDE_DIRS]

        for file in files:
            if file in EXCLUDE_FILES or file.startswith("."):
                continue
            if not is_valid_file(file):
                continue

            file_path = os.path.join(root, file)

            if os.path.getsize(file_path) < MIN_FILE_SIZE_BYTES:
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                rel_path = os.path.relpath(file_path, path)
                summary.append(f"\n# File: {rel_path}\n\n{content}\n")
            except Exception as e:
                print(f"Skipped {file_path}: {e}")

    return "\n".join(summary)
