from query_builder.query import Query

__all__ = [
        Query
]

if __name__ == "__main__":
    q = Query().SELECT("*").ALL.FROM("table")
    print(q.sql())
