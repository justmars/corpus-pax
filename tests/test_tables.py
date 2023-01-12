from sqlpyd import Connection

from corpus_pax import Individual, Org, OrgMember


def test_individuals_made(session_with_objs: Connection):
    assert len(list(session_with_objs.tbl(Individual.__tablename__).rows)) == 4


def test_orgs_made(session_with_objs: Connection):
    assert len(list(session_with_objs.tbl(Org.__tablename__).rows)) == 4


def test_org_members_made(session_with_objs: Connection):
    """Note one item is None (which counts as one item in the set);
    not all members are included in the data/members table (missing mv).
    mv is a member of 3 organizations, no id exists since not included
    in the data/members folder but the email address of
    mv is included in the data/orgs folder"""
    org_mem = session_with_objs.tbl(OrgMember.__tablename__)
    assert len(list(org_mem.rows)) == 9
    assert len({m["individual_id"] for m in org_mem.rows}) == 5
    assert len(list(org_mem.rows_where("individual_id is null"))) == 3
