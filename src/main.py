"""TheContenator — CLI Entry Point"""

import sys
import os

# Add src/ to path so modules can import each other
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main_menu():
    """Display the main interactive menu."""
    print("\n" + "=" * 50)
    print("  TheContenator")
    print("  Creator Research & Content Intelligence")
    print("=" * 50)
    print()
    print("  [1] Discover — Search niches & find top creators")
    print("  [2] Analyze  — Video stats & script extraction")
    print("  [3] Download — Grab videos from any platform")
    print("  [4] Compare  — Side-by-side account/video comparison")
    print("  [0] Exit")
    print()

    choice = input("  Select an option: ").strip()
    return choice


def run():
    """Main application loop."""
    while True:
        choice = main_menu()

        if choice == "1":
            print("\n  [Discovery module — not yet implemented]")
        elif choice == "2":
            print("\n  [Analyzer module — not yet implemented]")
        elif choice == "3":
            print("\n  [Download module — not yet implemented]")
        elif choice == "4":
            print("\n  [Comparator module — not yet implemented]")
        elif choice == "0":
            print("\n  Goodbye.\n")
            sys.exit(0)
        else:
            print("\n  Invalid option. Try again.")


if __name__ == "__main__":
    run()
