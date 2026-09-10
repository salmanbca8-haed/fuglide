import os
import re

def process_html_files(root_dir="."):
    # Matches any opening <footer ...> to closing </footer> (multi-line, case-insensitive)
    footer_pattern = re.compile(r"<footer\b[^>]*>.*?</footer>", re.DOTALL | re.IGNORECASE)
    
    # Files/folders to skip
    skip_files = {"footer.html"}
    skip_dirs = {".git", ".vscode", "node_modules", ".gemini"}

    modified_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove skipped directories in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            if not filename.lower().endswith(".html") or filename in skip_files:
                continue

            filepath = os.path.join(dirpath, filename)
            
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Check if there is a <footer> to replace
            if footer_pattern.search(content):
                # Replace the footer with placeholder
                new_content = footer_pattern.sub('<div id="footer-placeholder"></div>', content)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                rel_path = os.path.relpath(filepath, root_dir)
                print(f"[MODIFIED] Replaced hardcoded footer in: {rel_path}")
                modified_count += 1
            else:
                rel_path = os.path.relpath(filepath, root_dir)
                print(f"[SKIPPED] No hardcoded footer found in: {rel_path}")

    print(f"\nDone! Successfully updated {modified_count} HTML file(s).")

if __name__ == "__main__":
    process_html_files(".")
