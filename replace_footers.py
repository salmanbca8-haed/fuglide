import os
import re

def generate_footer(rel_path):
    # Normalize path separators
    rel_norm = rel_path.replace("\\", "/").lstrip("./")
    
    # Calculate depth and appropriate relative prefix
    parts = [p for p in rel_norm.split("/") if p]
    depth = len(parts) - 1
    
    if depth == 0:
        prefix = ""
        pages_prefix = "pages/"
        home_href = "index.html"
    elif depth == 1 and rel_norm.startswith("pages/"):
        prefix = "../"
        pages_prefix = ""
        home_href = "../index.html"
    elif depth == 1:
        prefix = "../"
        pages_prefix = "../pages/"
        home_href = "../index.html"
    else:
        prefix = "../../"
        pages_prefix = "../../pages/"
        home_href = "../../index.html"

    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <!-- Column 1: Brand Info -->
    <div class="footer-col footer-brand">
      <a class="footer-logo-wrap" href="{home_href}" aria-label="Fu-Glide Home">
        <img src="{prefix}images/logo.png" alt="Fu-Glide Logo" class="footer-logo" />
        <span class="footer-brand-name">Fu-Glide</span>
      </a>
      <p class="footer-about-text">
        At Fu-Glide, we’re entirely focused on helping you succeed. We provide modern digital tools and hands-on guidance for teams and students with big goals. Whether you’re trying to land your first job or level up your current skills, we’re here to help you get where you want to be.
      </p>
      <div class="footer-social-row">
        <a href="https://www.instagram.com/fu_glide_iin/?hl=en" target="_blank" rel="noopener noreferrer"
          class="footer-social-btn" aria-label="Instagram">
          <svg viewBox="0 0 24 24">
            <path
              d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" />
          </svg>
        </a>
        <a href="https://wa.me/9150792336" target="_blank" rel="noopener noreferrer" class="footer-social-btn"
          aria-label="WhatsApp">
          <svg viewBox="0 0 24 24">
            <path
              d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L0 24l6.335-1.662c1.746.953 3.71 1.456 5.711 1.457h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
          </svg>
        </a>
        <a href="mailto:fuglide@gmail.com" class="footer-social-btn" aria-label="Email Fu-Glide">
          <svg viewBox="0 0 24 24">
            <path d="M3 5h18a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zm0 2v.5l9 6 9-6V7H3zm18 10V9.9l-8.45 5.63a1 1 0 0 1-1.1 0L3 9.9V17h18z" />
          </svg>
        </a>
      </div>
    </div>

    <!-- Column 2: Quick Links -->
    <div class="footer-col footer-links-col">
      <h4 class="footer-heading">Quick Links</h4>
      <ul class="footer-nav-list">
        <li class="footer-nav-item">
          <a href="{home_href}" class="footer-nav-link">
            <svg class="footer-link-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>Home</span>
          </a>
        </li>
        <li class="footer-nav-item">
          <a href="{pages_prefix}about.html" class="footer-nav-link">
            <svg class="footer-link-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>About Us</span>
          </a>
        </li>
        <li class="footer-nav-item">
          <a href="{pages_prefix}tutoring.html" class="footer-nav-link">
            <svg class="footer-link-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>Our Courses</span>
          </a>
        </li>
        <li class="footer-nav-item">
          <a href="{pages_prefix}blog.html" class="footer-nav-link">
            <svg class="footer-link-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>Blog</span>
          </a>
        </li>
        <li class="footer-nav-item">
          <a href="{pages_prefix}services2.html" class="footer-nav-link">
            <svg class="footer-link-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>Our Services</span>
          </a>
        </li>
        <li class="footer-nav-item">
          <a href="{pages_prefix}contact.html" class="footer-nav-link">
            <svg class="footer-link-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <span>Contact Us</span>
          </a>
        </li>
      </ul>
    </div>

    <!-- Column 3: Contact Us -->
    <div class="footer-col footer-contact-col">
      <h4 class="footer-heading">Contact Us</h4>
      <ul class="footer-contact-list">
        <li class="footer-contact-item">
          <div class="footer-contact-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
            </svg>
          </div>
          <div class="footer-contact-info">
            <span class="footer-contact-label">Location</span>
            <span class="footer-contact-val">
              <strong>Fu-Glide Innovation Intelligence Network</strong>
              38B RMV Complex, Palani Road, Dindigul 624003.
            </span>
          </div>
        </li>
        <li class="footer-contact-item">
          <div class="footer-contact-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" />
            </svg>
          </div>
          <div class="footer-contact-info">
            <span class="footer-contact-label">Email Support</span>
            <a class="footer-contact-val" href="mailto:fuglide@gmail.com">fuglide@gmail.com</a>
          </div>
        </li>
        <li class="footer-contact-item">
          <div class="footer-contact-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-2.2 2.2a15.053 15.053 0 01-6.59-6.59l2.2-2.21a.96.96 0 00.25-1.01A11.36 11.36 0 018.5 3.99c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.61c0-.55-.45-1-.99-1z" />
            </svg>
          </div>
          <div class="footer-contact-info">
            <span class="footer-contact-label">Direct Line</span>
            <a class="footer-contact-val" href="tel:+919150792336">+91 91507 92336</a>
          </div>
        </li>
      </ul>
    </div>

    <!-- Column 4: Our Location -->
    <div class="footer-col footer-map-col">
      <h4 class="footer-heading">Our Location</h4>
      <div class="footer-map-card">
        <div class="footer-map-badge">
          <span class="footer-map-dot"></span>
          <span>Live HQ Campus</span>
        </div>
        <div class="footer-map-wrapper">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d62804.04400047483!2d77.90463166305959!3d10.321646438874492!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b00ab004b59b95d%3A0x1382bb12b1642380!2sFu-Glide%20Innovation%20Intelligence%20Network!5e0!3m2!1sen!2sin!4v1785505014608!5m2!1sen!2sin"
            width="100%" height="175" style="border:0;" allowfullscreen="" loading="lazy"
            referrerpolicy="strict-origin-when-cross-origin" title="Fu-Glide Innovation Network Location Map">
          </iframe>
        </div>
      </div>
    </div>
  </div>

  <div class="container footer-bottom">
    <p>&copy; 2026 Fu-Glide Innovation Intelligence Network. All rights reserved.</p>
    <div class="footer-tagline-pill">
      <span>Empowering Next-Gen Innovators &amp; Students</span>
    </div>
  </div>
</footer>'''

def process_html_files(root_dir="."):
    footer_pattern = re.compile(r"<footer\b[^>]*>.*?</footer>", re.DOTALL | re.IGNORECASE)
    
    skip_files = {"footer.html", "header.html"}
    skip_dirs = {".git", ".vscode", "node_modules", ".gemini", "brain"}

    modified_count = 0

    # Also update footer.html explicitly
    footer_html_content = generate_footer("index.html")
    with open("footer.html", "w", encoding="utf-8") as f:
        f.write(footer_html_content + "\n")
    print("[UPDATED] footer.html")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            if not filename.lower().endswith(".html") or filename in skip_files:
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            new_footer = generate_footer(rel_path)

            if footer_pattern.search(content):
                new_content = footer_pattern.sub(new_footer, content)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[MODIFIED] Updated footer in: {rel_path}")
                modified_count += 1
            else:
                print(f"[SKIPPED] No footer found in: {rel_path}")

    print(f"\nDone! Successfully updated {modified_count} HTML file(s).")

if __name__ == "__main__":
    process_html_files(".")
