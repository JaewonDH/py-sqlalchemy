from database.db import Session, init_db
from sample_data.data import address, citys, countrys, category, customer

# actors,
from model.model import Actor, Address, City, Country, Customer
from sqlalchemy import Select, text, and_, or_, func
from sqlalchemy.orm import aliased
import datetime

init_db()


# def insert_actor():
#     with Session() as session:
#         session.add_all(actors)
#         session.commit()
#         session.close()


def insert_address():
    with Session() as session:
        session.execute(text(customer))
        session.commit()
        session.close()


def select_actor():
    with Session() as session:
        stmt = Select(Actor)
        result = session.execute(stmt)
        for row in result:
            print(row)


def select_address():
    with Session() as session:
        stmt = Select(Address).where(Address.district == "Alberta")
        print(stmt)
        result = session.execute(stmt)
        print(result)
        for row in result.scalars():
            print(row)


def update_actor():
    with Session() as session:
        actor = session.query(Actor).filter(Actor.last_name == "JAEWON").first()
        if actor:
            actor.first_name = "dddddddddddddddddddddd"
            session.commit()


def add_actor():
    print("!!!!!!!!!!!!!!!!!!!!")
    with Session() as session:
        actor = Actor(first_name="test", last_name="test test")
        session.add(actor)
        session.commit()


def delete_actor():
    with Session() as session:
        actor = session.query(Actor).filter(Actor.actor_id == 144).one()
        if actor:
            session.delete(actor)
            session.commit()


def update_actor():
    with Session() as session:
        actor = session.query(Actor).filter(Actor.last_name == "JAEWON").first()
        if actor:
            actor.first_name = "dddddddddddddddddddddd"
            session.commit()


def update_actor2():
    with Session() as session:
        actor = session.query(Actor).filter(Actor.actor_id == 144).first()
        if actor:
            actor.first_name = "dddddddddddddddddddddd"
            session.commit()


#  SELECT address.address_id AS id, address.address, address.district, city.city_id, city.city, country.country
# FROM address JOIN city ON address.city_id = city.city_id JOIN country ON country.country_id = city.country_id
# WHERE address.district = ? AND (city.city_id = ? OR city.city_id = ?) ORDER BY address.address
def select_address1():
    with Session() as session:
        stmt = (
            Select(
                Address.address_id.label("id"),  # as
                Address.address,
                Address.district,
                City.city_id,
                City.city,
                Country.country,
            )
            .where(
                and_(
                    Address.district == "Buenos Aires",
                    or_(City.city_id == 334, City.city_id == 567),
                )
            )
            .join(City, Address.city_id == City.city_id)
            .join(Country, Country.country_id == City.country_id)
            .order_by(Address.address)
        )
        result = session.execute(stmt)
        for row in result:
            print(f"address_id={row.id}")
            print(f"address={row.address}")
            print(f"district={row.district}")
            print(f"city_id={row.city_id}")
            print(f"city={row.city}")
            print(f"country={row.country}")
            print("-----" * 20)


def select_address_group_having():
    with Session() as session:
        stmt = (
            Select(Customer.store_id, func.count(Customer.store_id).label("count"))
            .group_by(Customer.store_id)
            .having(func.count(Customer.store_id) > 300)
        )
        result = session.execute(stmt)
        for row in result:
            print(f"store_id={row.store_id} count={row.count}")
            print("-----" * 20)


# SELECT customer.address_id AS id, customer.first_name, customer.last_name, customer.email, anon_1.address, anon_1.district
# FROM customer JOIN (SELECT address.address_id AS address_id, address.address AS address, address.district AS district
# FROM address
# WHERE address.address LIKE ?) AS anon_1 ON customer.address_id = anon_1.address_id
def select_address_cte_sub_query():
    with Session() as session:
        subq = (
            Select(Address.address_id, Address.address, Address.district)
            .where(Address.address.like("%Cuernavaca%"))
            .subquery()
        )
        address_subq = aliased(Address, subq)
        stmt = Select(
            Customer.address_id.label("id"),
            Customer.first_name,
            Customer.last_name,
            Customer.email,
            address_subq.address,
            address_subq.district,
        ).join(address_subq, Customer.address_id == address_subq.address_id)
        result = session.execute(stmt)
        for row in result:
            print(f"id: {row.id}")
            print(f"First Name: {row.first_name}")
            print(f"Last Name: {row.last_name}")
            print(f"Email: {row.email}")
            print(f"Address: {row.address}")
            print(f"District: {row.district}")
            print("-" * 20)  # Print separator between records


# (SELECT address.address_id AS address_id, address.address AS address, address.district AS district
# FROM address
# WHERE address.address LIKE ?)
#  SELECT customer.address_id AS id, customer.first_name, customer.last_name, customer.email, anon_1.address, anon_1.district
# FROM customer JOIN anon_1 ON customer.address_id = anon_1.address_id


def select_address_cte_query():
    with Session() as session:
        subq = (
            Select(Address.address_id, Address.address, Address.district)
            .where(Address.address.like("%Cuernavaca%"))
            .cte()
        )
        address_cte = aliased(Address, subq)
        stmt = Select(
            Customer.address_id.label("id"),
            Customer.first_name,
            Customer.last_name,
            Customer.email,
            address_cte.address,
            address_cte.district,
        ).join(address_cte, Customer.address_id == address_cte.address_id)
        result = session.execute(stmt)
        for row in result:
            print(f"id: {row.id}")
            print(f"First Name: {row.first_name}")
            print(f"Last Name: {row.last_name}")
            print(f"Email: {row.email}")
            print(f"Address: {row.address}")
            print(f"District: {row.district}")
            print("-" * 20)  # Print separator between records


def select_address_join_test():
    with Session() as session:
        subq = (
            Select(Address.address_id, Address.address, Address.district)
            .where(Address.address.like("%Cuernavaca%"))
            .cte()
        )
        address_cte = aliased(Address, subq)
        stmt = Select(
            Customer.address_id.label("id"),
            Customer.first_name,
            Customer.last_name,
            Customer.email,
            address_cte.address,
            address_cte.district,
        ).join(Customer, Customer.address_id == address_cte.address_id)
        result = session.execute(stmt)
        for row in result:
            print(f"id: {row.id}")
            print(f"First Name: {row.first_name}")
            print(f"Last Name: {row.last_name}")
            print(f"Email: {row.email}")
            print(f"Address: {row.address}")
            print(f"District: {row.district}")
            print("-" * 20)  # Print separator between records


# 컬럼과 , where에서 서브 쿼리 사용법
def select_address_column_scalar_subquery():
    with Session() as session:
        subq = Select(func.count(Address.address)).scalar_subquery()
        stmt = Select(Address.address, subq.label("count")).where(300 < subq)
        result = session.execute(stmt)
        for row in result:
            print(f"address: {row.address}")
            print(f"count: {row.count}")
            print("-" * 20)  # Print separator between records


if __name__ == "__main__":
    # insert_actor()
    # select_actor()
    # insert_address()
    # select_actor()
    # select_address_group_having()
    # select_address1()
    # select_address_cte_sub_query()
    # select_address_join_test()
    # select_address_column_scalar_subquery()
    # update_actor()
    add_actor()
    # update_actor2()
    delete_actor()
