from extensions import app, db
from flask_login import UserMixin
from extensions import login_manager


class Product(db.Model):
    name = db.Column(db.String)
    file = db.Column(db.String)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __str__(self):
        return f"{self.name}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    product_id = db.relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return f"{self.name}"
    
class User(db.Model, UserMixin):
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"{self.username}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
        

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Adding sample categories
        electronics = Category(name='Electronics')
        clothing = Category(name='Clothing')
        groceries = Category(name='Groceries')
        books = Category(name='Books')

        admin = User(username="admin", password="password123", role="admin")
        user = User(username="test1", password="pass123")


        db.session.add_all([electronics, clothing, groceries, books, user, admin])
        db.session.commit()

        # Adding sample products with image filenames
        products = [
            Product(name='AirPods', file='airpods.jpg', price=199, category=electronics),
            Product(name='Apple MacBook', file='apple_mc.jpg', price=1299, category=books),
            Product(name='iPhone 13', file='iphone_13.jpg', price=999, category=clothing),
            Product(name='iPhone 15', file='iphone_15.jpg', price=1099, category=clothing),
            Product(name='Samsung Galaxy', file='samsung_galaxy.jpg', price=899, category=electronics),
            Product(name='Samsung Phone', file='samsung.jpg', price=799, category=electronics)
        ]

        db.session.add_all(products)
        db.session.commit()