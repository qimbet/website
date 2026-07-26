from pathlib import Path


class SidebarManager:
    SIDEBAR_SCRIPT = (
        '<script type="module" src="/website_js/sidebar.js"></script>'
    )

    MARKERS = {
        "html": (
            "<!-- SIDEBAR START -->",
            "<!-- SIDEBAR END -->"
        )
    }

    EXCLUDED_DIRS = {
        "100_haikus",
        "website_components",
        ".git",
        "__pycache__",
    }

    def __init__(self, site):
        self.site = site
        self.sidebar_file = (
            site.components / "sidebar.html"
        )

        self.sidebar_source = (
            self.sidebar_file
            .read_text(encoding="utf-8")
        )

        self.sidebar_html = (
            self.sidebar_file
            .read_text(encoding="utf-8")
            .strip()
        )


    def extract_section(self, name):
        start_marker, end_marker = self.MARKERS[name]
        start = self.sidebar_source.find(start_marker)
        end = self.sidebar_source.find(end_marker)

        if start == -1 or end == -1:
            return ""

        start += len(start_marker)

        return self.sidebar_source[start:end].strip()


    def is_excluded(self, path: Path) -> bool:
        return any(
            part in self.EXCLUDED_DIRS
            for part in path.parts
        )


    def replace_section(self, html, name, content):
        start_marker, end_marker = self.MARKERS[name]
        start = html.find(start_marker)
        end = html.find(end_marker)

        if start == -1 or end == -1:
            return html

        start += len(start_marker)

        return (
            html[:start]
            + "\n\n"
            + content
            + "\n\n"
            + html[end:]
        )


    def inject(self, html):
        html = self.replace_section(
            html,
            "html",
            self.sidebar_html
        )
        return html


    def build(self):

        total_pages = 0
        processed_pages = 0
        updated_pages = 0

        for page in self.site.site_root.rglob("*.html"):

            total_pages += 1

            if page == self.sidebar_file:
                continue

            if self.is_excluded(page):
                continue

            processed_pages += 1

            original = page.read_text(
                encoding="utf-8"
            )

            updated = self.inject(original)

            if updated != original:

                page.write_text(
                    updated,
                    encoding="utf-8"
                )

                updated_pages += 1
                print(f"Updated sidebar: {page}")

        print("\nSidebar update complete")
        print(f"Total HTML pages found: {total_pages}")
        print(f"Pages processed: {processed_pages}")
        print(f"Pages updated: {updated_pages}")