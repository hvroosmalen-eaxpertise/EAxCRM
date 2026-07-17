"""Same body as the positive fixture, but properly wrapped."""
import sys
import ea_session

QEA = r"M:\some.qea"


def main() -> None:
    try:
        with ea_session.ea_repository(QEA) as repo:
            root = repo.Models.GetAt(0)
            print(root.Name)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
