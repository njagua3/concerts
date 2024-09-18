from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for declarative model definitions
Base = declarative_base()

# Band model representing a musical group
class Band(Base):
    __tablename__ = 'bands'

    # Primary key for the band table
    id = Column(Integer, primary_key=True)
    
    # The band's name (cannot be null)
    name = Column(String, nullable=False)
    
    # The band's hometown (cannot be null)
    hometown = Column(String, nullable=False)
    
    # Relationship to the Concert model, back_populates is used to define the inverse relationship from Concert to Band
    concerts = relationship('Concert', back_populates='band')

    # Method to fetch all concerts for the current band
    def get_concerts(self, session):
        """Returns all concerts where the band performed."""
        return session.query(Concert).filter_by(band_id=self.id).all()

    # Method to fetch all venues where the band has performed
    def venues(self, session):
        """Returns a list of venues where the band has performed."""
        return [concert.venue for concert in self.get_concerts(session)]

    # Method to add a new concert for the band
    def play_in_venue(self, venue, date, session):
        """
        Creates a new concert for the band in the specified venue on the given date.
        Adds the concert to the session and commits it to the database.
        """
        new_concert = Concert(date=date, band=self, venue=venue)
        session.add(new_concert)
        session.commit()

    # Method to generate an introduction for each concert the band performed
    def all_introductions(self, session):
        """
        Returns a list of introduction strings for all the band's concerts.
        Example: "Hello {city}!!!!! We are {band_name} and we're from {hometown}"
        """
        return [
            f"Hello {concert.venue.city}!!!!! We are {self.name} and we're from {self.hometown}"
            for concert in self.get_concerts(session)
        ]

# Venue model representing a location where concerts take place
class Venue(Base):
    __tablename__ = 'venues'

    # Primary key for the venue table
    id = Column(Integer, primary_key=True)
    
    # The venue's name (cannot be null)
    title = Column(String, nullable=False)
    
    # The city where the venue is located (cannot be null)
    city = Column(String, nullable=False)

    # Relationship to the Concert model, back_populates defines the inverse relationship from Concert to Venue
    concerts = relationship('Concert', back_populates='venue')

    # Method to fetch all concerts held at this venue
    def get_concerts(self, session):
        """Returns all concerts held at this venue."""
        return session.query(Concert).filter_by(venue_id=self.id).all()

    # Method to fetch all bands that have performed at this venue
    def bands(self, session):
        """Returns a list of bands that have performed at this venue."""
        return [concert.band for concert in self.get_concerts(session)]

    # Method to find a concert held on a specific date
    def concert_on(self, date, session):
        """Finds and returns the concert on the specified date at the venue."""
        return session.query(Concert).filter_by(venue_id=self.id, date=date).first()

    # Method to find the band that has performed most frequently at this venue
    def most_frequent_band(self, session):
        """
        Returns the band with the most concerts at this venue.
        In case of a tie, the first band with the most performances is returned.
        """
        band_count = {}
        for concert in self.get_concerts(session):
            band_count[concert.band] = band_count.get(concert.band, 0) + 1
        # Return the band with the highest concert count
        return max(band_count, key=band_count.get, default=None)

# Concert model representing a performance by a band at a venue on a specific date
class Concert(Base):
    __tablename__ = 'concerts'

    # Primary key for the concert table
    id = Column(Integer, primary_key=True)
    
    # The date of the concert (cannot be null)
    date = Column(String, nullable=False)
    
    # Foreign key referring to the band that performed in the concert
    band_id = Column(Integer, ForeignKey('bands.id'), nullable=False)
    
    # Foreign key referring to the venue where the concert took place
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)

    # Relationship to Band, back_populates defines the inverse relationship from Band to Concert
    band = relationship('Band', back_populates='concerts')
    
    # Relationship to Venue, back_populates defines the inverse relationship from Venue to Concert
    venue = relationship('Venue', back_populates='concerts')

    # Method to check if the concert was a "hometown show" for the band
    def hometown_show(self, session):
        """
        Returns True if the concert was held in the band's hometown, False otherwise.
        A hometown show occurs if the concert venue's city matches the band's hometown.
        """
        return self.venue.city == self.band.hometown

    # Method to generate an introduction string for the concert
    def introduction(self, session):
        """
        Returns the introduction string for the concert.
        Example: "Hello {city}!!!!! We are {band_name} and we're from {hometown}"
        """
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
