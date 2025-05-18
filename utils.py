import os
from git import Repo

def clone_repo(repo_url, dest="./repos"):
    repo_name = repo_url.rstrip('/').split("/")[-1]
    path = os.path.join(dest, repo_name)
    os.makedirs(dest, exist_ok=True)
    if not os.path.exists(path):
        Repo.clone_from(repo_url, path)
    return path

def summarize_codebase(path):
    summary = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".cpp")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    rel_path = os.path.relpath(file_path, path)
                    summary.append(f"\n# File: {rel_path}\n\n{content}\n")
                except Exception as e:
                    print(f"Skipped {file_path}: {e}")
    return "\n".join(summary)