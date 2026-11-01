import os

repo_root = os.getcwd()
found = []
for root, dirs, files in os.walk(repo_root):
    # skip .git or artifacts directory outside
    for f in files:
        if f.endswith(('.md', '.py', '.txt', '.json', '.html')):
            p = os.path.join(root, f)
            try:
                content = open(p, encoding='utf-8').read()
                if "file://" in content:
                    count = content.count("file://")
                    rel = os.path.relpath(p, repo_root)
                    print(f"{rel}: {count} occurrences")
                    found.append((rel, count))
            except Exception as e:
                pass
print(f"Total files with file:// : {len(found)}")
