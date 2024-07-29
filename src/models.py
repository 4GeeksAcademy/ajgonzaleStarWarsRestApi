from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    climate= db.Column(db.String())
    diameter= db.Column(db.Integer)
    gravity= db.Column(db.Integer)
    name= db.Column(db.String(100))
    orbital_period= db.Column(db.Integer)
    population= db.Column(db.Integer)
    rotation_period= db.Column(db.Integer)
    surface_water= db.Column(db.Integer)
    terrain= db.Column(db.String)
    characters = db.relationship("Character", back_populates="homeworld")
    favorites = db.relationship("Favorite", back_populates="planet")

    def __repr__(self):
        return f"""<Planet %r>' id: {self.id} climate: {self.climate} diameter: {self.diameter} "
          "gravity: {self.gravity} name: {self.name} orbital_period: {self.orbital_period} "
          "population: {self.population} rotation_period: {self.rotation_period} "
          "surface_water: {self.surface_water} terrain: {self.terrain}"""

    def serialize(self):
        return {
            "id": self.id,
            "climate" : self.climate,
            "diameter" : self.diameter,
            "gravity" : self.gravity,
            "name" : self.name,
            "orbital_period" : self.orbital_period,
            "population" : self.population,
            "rotation_period" : self.rotation_period,
            "surface_water" : self.surface_water,
            "terrain" : self.terrain
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    birth_year = db.Column(db.String(20)) 
    eye_color = db.Column(db.String(30)) 
    gender = db.Column(db.String(20))
    hair_color = db.Column(db.String(30))
    height = db.Column(db.Integer) 
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(50)) 
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    homeworld = db.relationship("Planet", back_populates="characters")
    favorites = db.relationship("Favorite", back_populates="character")

    def __repr__(self):
        return f"""<Character %r>' id: {self.id} name: {self.name}  birth_year: {self.birth_year} "
        "eye_color: {self.eye_color} gender: {self.gender} hair_color: {self.hair_color} "
        "height: {self.height} homeworld_id: {self.homeworld_id} mass: {self.mass} skin_color: {self.skin_color}"""

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "birth_year" : self.birth_year,
            "eye_color" : self.eye_color,
            "gender" : self.gender,
            "hair_color" : self.hair_color,
            "height" : self.height,
            "homeworld_id" : self.homeworld_id,
            "mass" : self.mass,
            "skin_color" : self.skin_color
        }

class Vehicule(db.Model):
    __tablename__ = 'vehicules'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100))
    weight = db.Column(db.DECIMAL)
    year = db.Column(db.Integer)
    make = db.Column(db.String(100))
    favorites = db.relationship("Favorite", back_populates="vehicule")

    def __repr__(self):
        return f"<Vehicule %r>' model: {self.model}  year: {self.year} make: {self.make}"

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "weight": self.weight,
            "year": self.year,
            "make": self.make
        }

class Favorite(db.Model) :
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    vehicule_id = db.Column(db.Integer, db.ForeignKey('vehicules.id'))
    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planet", back_populates="favorites")
    character = db.relationship("Character", back_populates="favorites")
    vehicule = db.relationship("Vehicule", back_populates="favorites")

    def __repr__(self):
        return f"""<Favorites %r>' id : {self.id} user_id : {self.user_id} planet_id : {self.planet_id} "
        "character_id : {self.character_id} vehicule_id: {self.vehicule_id}"""

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "planet_id" : self.planet_id,
            "character_id" : self.character_id,
            "vehicule_id" : self.vehicule_id
        }