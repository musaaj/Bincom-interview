#!/usr/bin/python3
"""helper module"""
from models.tables import *
from sqlalchemy import text, func, insert
from datetime import datetime


def get_polling_units():
    """get all polling units that have name"""
    with Session(my_engine) as session:
        results = session.execute(
                select(polling_unit.c
                .uniqueid,
                polling_unit.c
                .polling_unit_name).where(
                    polling_unit.c.polling_unit_name != ''))
        return results.all()


def get_pu_results(pu_id):
    """get results of a single poling unit"""
    with Session(my_engine) as session:
        sql = select(announced_pu_results.c.party_score).where(
                announced_pu_results.
                c.polling_unit_uniqueid == pu_id).order_by(
                        announced_pu_results.c.party_abbreviation)
        results = session.execute(sql)
        return results.all()


def get_pu_info(pu_id):
    """get information about a poling unit"""
    with Session(my_engine) as session:
        sql = select(polling_unit.c.polling_unit_name,
                polling_unit.c.polling_unit_description,
                polling_unit.c.polling_unit_number,
                polling_unit.c.entered_by_user).where(
                        polling_unit.c.uniqueid == pu_id)
        results = session.execute(sql)
        results = results.mappings()
        return results.one()


def get_lgas():
    """get all lga"""
    with Session(my_engine) as session:
        sql = select(lgas.c.uniqueid, lgas.c.lga_name)
        results = session.execute(sql)
        return results.all()


def get_lga_info(lga_id):
    """get info of an lga"""
    with Session(my_engine) as session:
        sql = select(lgas.c.lga_name,
                lgas.c.lga_id).where(
                        lgas.c.uniqueid == lga_id)
        results = session.execute(sql)
        return results.mappings().one()


def get_lga_results(lga_id):
    """get total vote cast for an lga"""
    lg = []
    txt = text("select sum(party_score)\
            from announced_pu_results\
            where polling_unit_uniqueid\
            in (select uniqueid\
            from polling_unit\
            where lga_id = {});".format(lga_id))
    with Session(my_engine) as session:
        pu = session.execute(txt)
        return pu.one()[0]


def get_parties():
    """get all parties"""
    with Session(my_engine) as session:
        sql = select(party.c.partyname
                ,party.c.partyid)\
                        .order_by(party.c.partyname)
        results = session.execute(sql).all()
        return results


def get_wards():
    """get all wards"""
    with Session(my_engine) as session:
        sql = select(ward.c.uniqueid,
                ward.c.ward_name)
        results = session.execute(sql)
        return results.all()
 
def insert_new_result(obj, **args):
    """add new polling unit and result

    Args:
        obj: dict
        args: dict
    """
    with Session(my_engine) as session:
        sql = polling_unit.insert().values(**args)
        session.execute(sql)
        session.commit()
        smt = select(polling_unit.c.uniqueid)\
                .where(polling_unit.c.polling_unit_name\
                == args['polling_unit_name'])
        result = session.execute(smt).fetchone()
        smt2 = announced_pu_results.insert()\
                .values(polling_unit_uniqueid=\
                result[0]
                ,party_abbreviation=\
                        obj['party']
                ,party_score=obj['party_score']
                ,entered_by_user=''
                ,date_entered=datetime.isoformat()
                ,user_ip_address=''
                )
        session.execute(smt2)
        session.commit()
