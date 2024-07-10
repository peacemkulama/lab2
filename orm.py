from pony.orm import *

# Define the database and bind it to the SQLite provider with the specified filename
db = Database()
db.bind(provider='sqlite', filename='static/RiskDB.db', create_db=True)


class Photo(db.Entity):
    _table_ = "photo"
    time = PrimaryKey(str)
    description = Required(str)
    path = Required(str)
    name = Required(str)


# Generate the mapping and create the tables if they don't exist
db.generate_mapping(create_tables=True)


def add_photo(time, desc, path, name):
    with db_session:
        # Create a new Photo object and add it to the database session
        Photo(
            time=time,
            description=desc,
            path=path,
            name=name
        )


def get_photos():
    with db_session:
        # Fetch all photos from the database and order them by descending time
        photo_list = [p.to_dict() for p in Photo.select().order_by(desc(Photo.time))]
        return photo_list
