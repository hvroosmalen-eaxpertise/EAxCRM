"""try/except inside a function is fine — the smell is only at module scope."""
import ea_session


def do_work() -> bool:
    try:
        with ea_session.ea_repository("M:\\some.qea") as repo:
            return repo.Models.Count > 0
    except Exception:
        return False


if __name__ == "__main__":
    print(do_work())
