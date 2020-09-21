from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String())
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)


    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
    def __str__(self):
        return self.name

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#Create product
@app.route('/product/create',methods=['POST'])
def add_product():
    # Post Data comes in as Rawjson 
    name = request.json['name']
    description = request.json['description']
    price= request.json['price']
    qty = request.json['qty']

    # instantiate a new product
    new_product = Product(name,description,price,qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)
# Get all products
@app.route('/products',methods=['GET'])
def get_products():
    products = Product.query.all()
    all_products = products_schema.dump(products)
    return jsonify(all_products)

#Get Single Product
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)

@app.route('/product/<id>/update',methods=['PUT'])
def update_product(id):
    # Post Data comes in as Rawjson
    # get that object to update
    product = Product.query.get(id)
    # Data from the Request

    name = request.json['name']
    description = request.json['description']
    price= request.json['price']
    qty = request.json['qty']

    # change product 's attribute

    product.name = name
    product.price=price
    product.qty = qty
    product.description = description
    db.session.commit()

    return product_schema.jsonify(product)

@app.route('/product/<id>/delete',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)




if __name__ == "__main__":
    app.run(debug=True)