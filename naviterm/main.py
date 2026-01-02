"""Entry point for Naviterm application."""

from .app import NavitermApp


def main():
    """Run the Naviterm application."""
    app = NavitermApp()
    app.run()


if __name__ == "__main__":
    main()

