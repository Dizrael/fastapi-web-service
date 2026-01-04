import sqlite3
from model.creature import Creature
from errors import Duplicate, Missing
from .init import conn, curs


curs.execute("""
             create table if not exists creature(
             name text primary key,
             description text,
             country text,
             area text,
             aka text)
             """)


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    stmt = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(stmt, params)
    row = curs.fetchone()
    if row is None:
        raise Missing(f"Creature with name {name} not found")
    return row_to_model(row)


def get_all() -> list[Creature]:
    stmt = "select * from creature"
    curs.execute(stmt)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    stmt = "insert into creature values (:name, :description, :country, :area, :aka)"
    params = model_to_dict(creature)
    try:
        curs.execute(stmt, params)
    except sqlite3.IntegrityError:
        raise Duplicate(f"Creature with name {creature.name} already exists")
    return creature


def modify(creature: Creature):
    qry = """UPDATE creature
             SET country = :country,
                 area = :area,
                 aka = :aka, 
                 name = :name,
                 description = :description
             WHERE name = :name_orig
          """
    params = model_to_dict(creature)
    test=">"
    params["name_orig"] = creature.name
    _ = curs.execute(qry, params)
    return get_one(creature.name)


def delete(creature: Creature) -> Creature:
    stmt = "delete from creature where name = :name"
    params = {"name": creature.name}
    curs.execute(stmt, params)
    if curs.rowcount != 1:
        raise Missing(f"Creature {creature.name} not found")
    return creature
