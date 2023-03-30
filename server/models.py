from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    serialize_rules = ('-vendor_sweets.vendor',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_sweets = db.relationship('VendorSweet', back_populates='vendor')

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    serialize_rules = ('-vendor_sweets.sweet',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_sweets = db.relationship('VendorSweet', back_populates='sweet')

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)

    vendor = db.relationship('Vendor', back_populates='vendor_sweets')
    sweet = db.relationship('Sweet', back_populates='vendor_sweets')

    @validates('price')
    def validates_price(self, key, value):
        if not value:
            raise ValueError("Price cannot be blank!")
        elif value < 0:
            raise ValueError("Price cannot be a negative number!")
        return value

# for relationships between tables, name these "vendor_sweets"



#i originally included put this in each class but the tests would not pass i do realize that this data needs to be there:
# "created_at = db.Column(db.DateTime, server_default = db.func.now())
    #updated_at = db.Column(db.DateTime, onupdate = db.func.now())" 