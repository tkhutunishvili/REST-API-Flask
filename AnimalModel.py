from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app


#################################################
# Database Setup
#################################################


db = SQLAlchemy(app)

class Animals(db.Model):
    __tablename__='animals'
    unique_id = db.Column(db.Integer, primary_key=True)
    centerid = db.Column(db.Integer)
    name = db.Column(db.String(256))
    description = db.Column(db.String(256), nullable=False)
    age = db.Column(db.Integer)
    species = db.Column(db.String(256))
    price = db.Column(db.Float, nullable=False) 

    def json(self):
    	return {
    	    'centerid': self.centerid,
    		'name': self.name, 
    		'description': self.description, 
    		'age': self.age, 
    		'species': self.species, 
    		'price': self.price
    	}

    def json_name_id(self):
    	return {
    	    'centerid': self.centerid,
    		'name': self.name, 
    	}

    def json_name_id_species(self):
    	return {
    	    'centerid': self.centerid,
    		'name': self.name, 
    		'species': self.species, 
    	}

    def add_animal(_centerid, _name, _description, _age, _species, _price):
    	new_animal = Animals(centerid=_centerid, name=_name, description=_description, age=_age, species=_species, price=_price)
    	db.session.add(new_animal)
    	db.session.commit()

    def get_all_animals():
    	return [Animals.json(animal) for animal in Animals.query.all()]

    def get_animal(_centerid):
    	return [Animals.json(Animals.query.filter_by(centerid=_centerid).first())]

    def get_centers():
    	name_id = db.session.query(Animals.name, Animals.centerid)
    	return [Animals.json_name_id(center) for center in name_id.all()]

    def get_centers_id(_centerid):
    	name_id_species = db.session.query(Animals.name, Animals.centerid, Animals.species).filter_by(centerid=_centerid)
    	return [Animals.json_name_id_species(name_id_species.first())]
   
    def get_species():
    	species_count_db = {}
    	species_count = db.session.query(Animals.species)
    	for specie in species_count.all():
    		if specie[0] not in species_count_db:
	    		species_count_db[specie[0]]=1
	    	species_count_db.update({specie[0]: int(species_count_db[specie[0]])+1})
    	return [species_count_db]   	

    def get_species_id(_species):
    	name_id_species = db.session.query(Animals.name, Animals.centerid, Animals.species).filter_by(species=_species)
    	return [Animals.json_name_id_species(specie) for specie in name_id_species.all()]   	

    def get_all_centers():
    	all_centers = Animals.query.all()
    	return Animals.query.all(name)

    def animal_name_update(_centerid, _name):
    	update_animal_name = Animals.query.filter_by(centerid=_centerid).first()
    	update_animal_name.name = _name
    	db.session.commit()

    def animal_description_update(_centerid, _description):
    	update_animal_description = Animals.query.filter_by(centerid=_centerid).first()
    	update_animal_description.description = _description
    	db.session.commit()

    def animal_age_update(_centerid, _age):
    	update_animal_age = Animals.query.filter_by(centerid=_centerid).first()
    	update_animal_age.age = _age
    	db.session.commit()

    def animal_species_update(_centerid, _species):
    	update_animal_species = Animals.query.filter_by(centerid=_centerid).first()
    	update_animal_species.species = _species
    	db.session.commit()

    def animal_price_update(_centerid, _price):
    	update_animal_price = Animals.query.filter_by(centerid=_centerid).first()
    	update_animal_price.price = _price
    	db.session.commit()

    def replace_animals(_centerid, _name, _description, _age, _species, _price):
        animal_to_replace = Animals.query.filter_by(centerid=_centerid).first()
        animal_to_replace.name = _name
        animal_to_replace.price = _description
        animal_to_replace.name = _age
        animal_to_replace.price = _species
        animal_to_replace.price = _price
        db.session.commit() #save changes

    def delete_animal(_centerid):
    	is_successful = Animals.query.filter_by(centerid=_centerid).delete()
    	db.session.commit()
    	return bool(is_successful)


    def __repr__(self):
    	animal_object = {
    		'centerid': self.centerid,
    		'name': self.name, 
    		'description': self.description, 
    		'age': self.age, 
    		'species': self.species, 
    		'price': self.price
    	}
    	return json.dumps(animal_object)