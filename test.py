from models import Base, Band, Venue, Concert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up the database
engine = create_engine('sqlite:///concerts.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create instances
band1 = Band(name="The Rockers", hometown="Nairobi")
venue1 = Venue(title="Grand Arena", city="Nairobi")
session.add(band1)
session.add(venue1)
session.commit()

# Add a concert
band1.play_in_venue(venue1, "2024-09-30", session)

# Testing methods
first_band = session.query(Band).first()
print(first_band.venues(session))  # Should include the first venue
print(first_band.all_introductions(session))  # Should return introduction strings

first_venue = session.query(Venue).first()
print(first_venue.concert_on("2024-09-30", session))  # Should return the concert
print(first_venue.most_frequent_band(session))  # Should return the band with the most concerts

first_concert = session.query(Concert).first()
print(first_concert.hometown_show(session))  # Should be True
print(first_concert.introduction(session))  # Should print the introduction string
