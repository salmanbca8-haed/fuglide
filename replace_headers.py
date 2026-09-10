import os
import re

HEADER_TEMPLATE = """<header class="site-header animate-in">
  <div class="announcement-bar" role="region" aria-label="Fu-Glide announcements">
    <div class="announcement-bar__contact">
      <a class="announcement-bar__phone" href="tel:+919150792336">+91 91507 92336</a>
      <a class="announcement-bar__instagram" href="https://www.instagram.com/fu_glide_iin/?hl=en" target="_blank"
        rel="noopener noreferrer" aria-label="Follow Fu-Glide on Instagram">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path
            d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.79 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" />
        </svg>
      </a>
      <a class="announcement-bar__email" href="mailto:fuglide@gmail.com" aria-label="Email Fu-Glide">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M3 5h18a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zm0 2v.5l9 6 9-6V7H3zm18 10V9.9l-8.45 5.63a1 1 0 0 1-1.1 0L3 9.9V17h18z" />
        </svg>
      </a>
    </div>
    <div class="announcement-bar__marquee">
      <div class="announcement-bar__viewport">
        <div class="announcement-bar__track">
          <div class="announcement-bar__group">
            <span class="announcement-bar__item">Best AI Course in Dindigul</span>
            <span class="announcement-bar__item">Practical Generative AI Training</span>
            <span class="announcement-bar__item">Robotics &amp; Automation Programs Open</span>
          </div>
          <div class="announcement-bar__group" aria-hidden="true">
            <span class="announcement-bar__item">Best AI Course in Dindigul</span>
            <span class="announcement-bar__item">Practical Generative AI Training</span>
            <span class="announcement-bar__item">Robotics &amp; Automation Programs Open</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <nav class="navbar container">
    <a class="brand" href="/index.html">
      <img src="/images/logo.png" alt="Fu-Glide Logo" class="brand-logo" />
    </a>

    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <div class="nav-links">
      __HOME_LINK__
      __ABOUT_LINK__

      <div class="dropdown">
        __COURSES_TOGGLE__
        <div class="dropdown-menu">
          <a href="/pages/tutoring.html">IT courses & Technology Training</a>
          <a href="/pages/software-achievements.html">Non-IT Courses</a>
        </div>
      </div>

      <div class="dropdown">
        __SERVICES_TOGGLE__
        <div class="dropdown-menu">
          <!-- Added distinct hashes so dropdown selections can jump to specific areas -->
          <a href="/pages/services2.html#seo">SEO</a>
          <a href="/pages/services2.html#smo">SMO</a>
          <a href="/pages/services2.html#ads">Meta and Google Ads</a>
          <a href="/pages/services2.html#webdev">Website Development</a>
          <a href="/pages/services2.html#branding">Branding and Marketing</a>
          <a href="/pages/services2.html#robotics">Robotic Services</a>
          <a href="/pages/services2.html#proposals">Business Proposals and Writing</a>
          <a href="/pages/services2.html#growth">Business Growth Development</a>
        </div>
      </div>

      __BLOG_LINK__
      __APPLY_LINK__
      __CONTACT_LINK__
    </div>
  </nav>
</header>"""

def get_header_for_page(rel_path):
    rel_norm = rel_path.replace("\\", "/").lower()
    
    # Check what is active on this page
    is_home = rel_norm in ["index.html", "./index.html"]
    is_about = "about" in rel_norm
    is_blog = "blog" in rel_norm
    is_apply = "apply" in rel_norm
    is_contact = "contact" in rel_norm
    is_courses = ("tutoring" in rel_norm or "software-achievements" in rel_norm or "course_details" in rel_norm)
    is_services = ("service" in rel_norm)
    
    home_style = ' style="color: #f6b84b;"' if is_home else ''
    about_style = ' style="color: #f6b84b;"' if is_about else ''
    blog_style = ' style="color: #f6b84b;"' if is_blog else ''
    apply_style = ' style="color: #f6b84b;"' if is_apply else ''
    contact_style = ' style="color: #f6b84b;"' if is_contact else ''
    courses_style = ' style="color: #f6b84b;"' if is_courses else ''
    services_style = ' style="color: #f6b84b;"' if is_services else ''
    
    h = HEADER_TEMPLATE
    h = h.replace('__HOME_LINK__', f'<a href="/index.html"{home_style}>Home</a>')
    h = h.replace('__ABOUT_LINK__', f'<a href="/pages/about.html"{about_style}>About</a>')
    
    courses_btn = f'''<button class="dropdown-toggle" type="button"{courses_style}>
          Courses
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>'''
    h = h.replace('__COURSES_TOGGLE__', courses_btn)
    
    services_btn = f'''<button class="dropdown-toggle" type="button"{services_style}>
          Services
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>'''
    h = h.replace('__SERVICES_TOGGLE__', services_btn)
    
    h = h.replace('__BLOG_LINK__', f'<a href="/pages/blog.html"{blog_style}>Blog</a>')
    h = h.replace('__APPLY_LINK__', f'<a href="/pages/apply.html"{apply_style}>Apply</a>')
    h = h.replace('__CONTACT_LINK__', f'<a href="/pages/contact.html"{contact_style}>Contact</a>')
    
    return h

def batch_replace_headers(root_dir="."):
    """
    Scans all HTML files in root_dir, extracts hardcoded <header class="site-header">...</header>
    or placeholder containers, and updates them with the unified site header.
    """
    skip_files = {"header.html", "footer.html"}
    skip_dirs = {".git", ".vscode", "node_modules", ".gemini", "dist", "build"}
    
    header_regex = re.compile(r"<header\b[^>]*class=[\"'][^\"']*site-header[^\"']*[\"'][^>]*>.*?</header>", re.DOTALL | re.IGNORECASE)
    placeholder_regex = re.compile(r"<div\s+id=[\"']header-placeholder[\"']\s*>\s*</div>", re.IGNORECASE)
    
    modified_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        for filename in filenames:
            if not filename.lower().endswith(".html") or filename in skip_files:
                continue
                
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            page_header = get_header_for_page(rel_path)
            updated = False
            
            if header_regex.search(content):
                content = header_regex.sub(page_header, content)
                updated = True
            elif placeholder_regex.search(content):
                content = placeholder_regex.sub(page_header, content)
                updated = True
            elif rel_path.replace("\\", "/") == "blog1.html":
                if "<body>" in content:
                    content = content.replace("<body>", f"<body>\n  {page_header}\n")
                    if "css/style.css" not in content:
                        content = content.replace('</head>', '  <link rel="stylesheet" href="css/style.css" />\n</head>')
                    if "js/main.js" not in content:
                        content = content.replace('</body>', '  <script src="js/main.js"></script>\n</body>')
                    updated = True
            elif "service.html" in rel_path.lower() and "redirect" in content.lower():
                pass
                
            if updated:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"[MODIFIED] Updated header in: {rel_path}")
                modified_count += 1
            else:
                print(f"[SKIPPED] No header update needed for: {rel_path}")
                
    print(f"\nDone! Successfully updated {modified_count} HTML file(s).")

if __name__ == "__main__":
    batch_replace_headers(".")
