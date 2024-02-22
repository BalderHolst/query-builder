
def make_sql(history: list[str]) -> str:
    return " > ".join(history)

if __name__ == "__main__":
    s = make_sql(["SELECT", "FROM"])
