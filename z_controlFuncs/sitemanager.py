from pathlib import Path

class Website:
    ROOT_MARKER = ".webroot"

    def __init__(self, start: Path | None = None):
        self.site_root = self._find_site_root(start or Path(__file__))

    @classmethod
    def _find_site_root(cls, start: Path) -> Path:
        current = start.resolve()

        if current.is_file():
            current = current.parent

        while True:
            if (current / cls.ROOT_MARKER).exists():
                return current

            if current.parent == current:
                raise FileNotFoundError(
                    f"Could not locate '{cls.ROOT_MARKER}'."
                )

            current = current.parent

    @property
    def components(self) -> Path:
        return self.site_root / "website_components"

    @property
    def javascript(self) -> Path:
        return self.site_root / "website_js"

    @property
    def static(self) -> Path:
        return self.site_root / "static"
