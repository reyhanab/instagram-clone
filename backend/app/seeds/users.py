from app.models import db, User, Post, environment, SCHEMA

users = [
    {
        "username": "Demo_User",
        "full_name": "Demo User",
        "gender": "Prefer not to say",
        "email": "demo_user@email.com",
        "password": "demouserpw",
        "phone_number": "1111111111",
        "profile_picture": "https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2015/3/31/1427823466140/1fe69f2c-59d6-4e07-ab3a-8b60dbe35db2-1020x1020.jpeg?width=700&quality=85&auto=format&fit=max&s=488d904c14758c38d8010de62c742e4b",
        "is_verified": True,
        "is_private": True
    },
    {
        "username": "Marnie_Demo",
        "full_name": "Marnie Demo",
        "gender": "Prefer not to say",
        "email": "marnie_demo@email.com",
        "password": "marniedemopw",
        "phone_number": "2222222222",
        "profile_picture": "https://www.crystalknows.com/hubfs/API/celebrities/mark_zuckerberg.jpg",
        "is_verified": False,
        "is_private": False
    },
    {
        "username": "Bobbie_Demo",
        "full_name": "Bobbie Demo",
        "gender": "Prefer not to say",
        "email": "bobbie_demo@email.com",
        "password": "bobbiedemopw",
        "phone_number": "3333333333",
        "profile_picture": "https://img.i-scmp.com/cdn-cgi/image/fit=contain,width=1098,format=auto/sites/default/files/styles/1200x800/public/d8/images/canvas/2022/05/19/4eb393f3-d671-4d58-8680-89ccd6607acf_5e3be874.jpg?itok=CEBu_LXQ&v=1652966452",
        "is_verified": False,
        "is_private": False
    },
    {
        "username": "Stan_Demo",
        "full_name": "Stanley Demo",
        "gender": "Male",
        "email": "stanley_demo@email.com",
        "password": "stanleydemopw",
        "phone_number": "4444444444",
        "profile_picture": "data:image/jpeg;base64,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",
        "is_verified": True,
        "is_private": True
    },
    {
        "username": "Rey_Demo",
        "full_name": "Reyhaneh Demo",
        "gender": "Female",
        "bio": "It's Rey",
        "email": "reyhaneh_demo@email.com",
        "password": "reyhanehdemopw",
        "phone_number": "5555555555",
        "profile_picture": "https://www.animalhospitalofspringfield.com/sites/default/files/styles/large/public/golden-retriever-dog-breed-info.jpg?itok=mFt6R_EN",
        "is_verified": True,
        "is_private": False
    },
    {
        "username": "Dan_Demo",
        "full_name": "Daniel Demo",
        "gender": "Male",
        "email": "daniel_demo@email.com",
        "password": "danieldemopw",
        "phone_number": "6666666666",
        "profile_picture": "",
        "is_verified": True,
        "is_private": True
    },
]


def seed_users():
    db.session.add_all([User(**user) for user in users])
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM users")

    db.session.commit()
