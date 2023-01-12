import datetime
from pathlib import Path

import pytest
import yaml
from sqlpyd import Connection

from corpus_pax import (
    Individual,
    Org,
    PersonCategory,
    PracticeArea,
    init_person_tables,
)

temppath = "tests/test.db"


def extract_files(shared_datadir, folder):
    details = shared_datadir.glob(f"{folder}/**/details.yaml")
    items = [yaml.safe_load(i.read_bytes()) for i in details]
    t = datetime.datetime.now().timestamp()
    return [
        {"id": f"id-{ctx}", "created": t, "modified": t} | i
        for ctx, i in enumerate(items)
    ]


@pytest.fixture
def individual_records(shared_datadir):
    return extract_files(shared_datadir, "members")


@pytest.fixture
def org_records(shared_datadir):
    return extract_files(shared_datadir, "orgs")


def setup_db(conn: Connection):
    init_person_tables(conn)  # add the tables
    return conn


def teardown_db(conn: Connection):
    conn.db.close()  # close the connection
    Path().cwd().joinpath(temppath).unlink()  # delete the file


@pytest.fixture
def session():
    c = Connection(DatabasePath=temppath)  # type: ignore
    db = setup_db(c)
    yield db
    teardown_db(db)


@pytest.fixture
def session_with_objs(individual_records, org_records):
    c = Connection(DatabasePath=temppath)  # type: ignore
    conn = setup_db(c)
    for i in individual_records:
        tbl = c.table(Individual)
        indiv_obj = Individual(**i)
        row = tbl.insert(indiv_obj.dict(), replace=True, pk="id")  # type: ignore
        if pk := row.last_pk:
            if indiv_obj.areas:
                PracticeArea.associate(tbl, pk, indiv_obj.areas)
            if indiv_obj.categories:
                PersonCategory.associate(tbl, pk, indiv_obj.categories)

    for i in org_records:
        tbl = c.table(Org)
        org_obj = Org(**i)
        row = tbl.insert(org_obj.dict(), replace=True, pk="id")  # type: ignore
        if pk := row.last_pk:
            if org_obj.areas:
                PracticeArea.associate(tbl, pk, org_obj.areas)
            if org_obj.categories:
                PersonCategory.associate(tbl, pk, org_obj.categories)
        org_obj.set_membership_rows(c)
    yield conn
    teardown_db(conn)
