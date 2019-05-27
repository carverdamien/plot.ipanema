def update_rows(updates, df):
    for op in updates:
        df = __OP__[op["op"]](op, df)
    return df

def cas(op, df):
    assert(op["op"] == "cas")
    sel = df[op["key"]] == op["old"]
    df[op["key"]][sel] = op["new"]
    return df

def drop(op, df):
    assert(op["op"] == "drop")
    sel = df[op["key"]] != op["val"]
    return df[sel]

__OP__ = {
    'cas' : cas,
    'drop' : drop,
}
