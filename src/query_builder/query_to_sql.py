def class_to_sql(c: any) -> str:
    return str(c)

def make_sql(history: list[str]) -> str:
    history = map(class_to_sql, history)
    return " ".join(history)

if __name__ == "__main__":
    s = make_sql(["SELECT", "FROM"])
