from .init import curs, conn, IntegrityError
from model.explorer import Explorer
from errors import Missing, Duplicate

curs.execute("""create table if not exists explorer(
                name text primary key,
                country text,
                description text)""")


def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    qry = "select * from explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> Explorer:
    qry = """insert into explorer (name, country, description)
             values (:name, :country, :description)"""
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Explorer {explorer.name} already exists")
    return get_one(explorer.name)


def modify(explorer: Explorer) -> Explorer:
    qry = """UPDATE explorer
             SET country=:country,
                 name=:name,
                 description=:description
             WHERE name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(f"Explorer {explorer.name} not found")


def delete(explorer: Explorer) -> Explorer:
    qry = "delete from explorer where name = :name"
    params = {"name": explorer.name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Explorer {explorer.name} not found")
    return explorer
