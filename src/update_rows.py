def update_rows(updates, df):
    for op in updates:
        assert(op["op"] == "cas")
        sel = df[op["key"]] == op["old"]
        df[op["key"]][sel] = op["new"]
    return df
