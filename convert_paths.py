import os
import re

def get_rel_prefix(file_rel_path):
    parts = file_rel_path.replace("\\", "/").split("/")
    depth = len(parts) - 1
    if depth == 0:
        return ""
    elif depth == 1:
        return "../"
    elif depth == 2:
        return "../../"
    else:
        return "../" * depth

def fix_html_content(content, file_rel_path):
    rel_norm = file_rel_path.replace("\\", "/").lower()
    depth = len(rel_norm.split("/")) - 1
    prefix = get_rel_prefix(file_rel_path)
    
    # Replacement rules for href and src starting with "/"
    # 1. /index.html
    if depth == 0:
        content = re.sub(r'href=["\']/index\.html(["\'])', r'href="index.html\1', content)
    else:
        content = re.sub(r'href=["\']/index\.html(["\'])', f'href="{prefix}index.html\\1', content)
        
    # 2. /pages/...
    if depth == 0:
        content = re.sub(r'href=["\']/pages/([^"\']*)["\']', r'href="pages/\1"', content)
    elif depth == 1 and rel_norm.startswith("pages/"):
        content = re.sub(r'href=["\']/pages/([^"\']*)["\']', r'href="\1"', content)
    else:
        content = re.sub(r'href=["\']/pages/([^"\']*)["\']', f'href="{prefix}pages/\\1"', content)

    # 3. /course_details.html/...
    if depth == 0:
        content = re.sub(r'href=["\']/course_details\.html/([^"\']*)["\']', r'href="course_details.html/\1"', content)
    elif depth == 1:
        content = re.sub(r'href=["\']/course_details\.html/([^"\']*)["\']', r'href="../course_details.html/\1"', content)
    elif depth == 2:
        content = re.sub(r'href=["\']/course_details\.html/([^"\']*)["\']', r'href="../../course_details.html/\1"', content)

    # 4. /images/...
    if depth == 0:
        content = re.sub(r'(src|href)=["\']/images/([^"\']*)["\']', r'\1="images/\2"', content)
    else:
        content = re.sub(r'(src|href)=["\']/images/([^"\']*)["\']', f'\\1="{prefix}images/\\2"', content)

    # 5. /icons/...
    if depth == 0:
        content = re.sub(r'(src|href)=["\']/icons/([^"\']*)["\']', r'\1="icons/\2"', content)
    else:
        content = re.sub(r'(src|href)=["\']/icons/([^"\']*)["\']', f'\\1="{prefix}icons/\\2"', content)

    # 6. /css/...
    if depth == 0:
        content = re.sub(r'href=["\']/css/([^"\']*)["\']', r'href="css/\1"', content)
    else:
        content = re.sub(r'href=["\']/css/([^"\']*)["\']', f'href="{prefix}css/\\1"', content)

    # 7. /js/...
    if depth == 0:
        content = re.sub(r'src=["\']/js/([^"\']*)["\']', r'src="js/\1"', content)
    else:
        content = re.sub(r'src=["\']/js/([^"\']*)["\']', f'src="{prefix}js/\\1"', content)

    # 8. /demo.html, /blog1.html, /blog2.html
    for pg in ["demo.html", "blog1.html", "blog2.html"]:
        if depth == 0:
            content = re.sub(rf'href=["\']/{pg}(["\'])', rf'href="{pg}\1', content)
        else:
            content = re.sub(rf'href=["\']/{pg}(["\'])', f'href="{prefix}{pg}\\1', content)

    return content

def process_all_html(root_dir="."):
    skip_dirs = {".git", ".vscode", "node_modules", ".gemini"}
    modified_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for filename in filenames:
            if not filename.lower().endswith(".html"):
                continue
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            new_content = fix_html_content(content, rel_path)
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[FIXED] {rel_path}")
                modified_count += 1
            else:
                print(f"[UNCHANGED] {rel_path}")
                
    print(f"\nTotal files updated: {modified_count}")

if __name__ == "__main__":
    process_all_html(".")
