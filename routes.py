from extensions import app, db
from flask import render_template, request, redirect, flash, send_from_directory
from forms import AddProduct, RegisterForm, LoginForm
import os
from models import Product, Category, User
from flask_login import logout_user, login_user, login_required, current_user


products = [{"name": "Samsung", "file": "samsung.jpg",
             "price": 1000, "id":"1"
             },
             {"name": "iphone", "file": "iphone_15.jpg",
             "price": 500, "id":"2"
             },
             {"name": "Apple", "file": "apple_mc.jpg",
             "price": 900, "id":"3"
             }]

@app.route("/populate_data")
def populate_data():
    for product in products:
        product_to_add = Product(name=product["name"],
                                 price=product["price"],
                                 file=product["file"])
        db.session.add(product_to_add)
        db.session.commit()
    print(Product.query.all())
    return redirect("/")

        


@app.route("/")
def home():
    products = Product.query.all()
    # for product in products:
    #     print(product.name)
    #     print(product.file)
    #     print(product.price)

    return render_template("index.html", products=products)

@app.route("/hello")
def hello():
    name = request.args["name"]
    return f"Hello {name}"

    
    

@app.route("/test")
def test():
    users = {"tornike": 1,
             "giorgi": 2,
             "tekla": 3,
             "lasha": 4,
             "ilia": 5}

    return render_template("test.html", users=users)

@app.route('/detail/<int:id>')
def detail(id):
    current = Product.query.get(id)

    return render_template("details.html", product=current)

@app.route("/addproduct", methods=["GET", "POST"])
def add_product():
    form = AddProduct()
    if form.validate_on_submit():

        product = {"name": form.name.data,
                   "url": form.url.data,
                   "price": form.price.data,
                   "id": len(products) + 1}
        products.append(product)
        flash("You successfully added the product", category="success")
        
        return redirect("/")
    
    if form.errors:
        print(form.errors)
        for error in form.errors:
            print(error)

        flash("You didnt add product properly", category="danger")
        

    return render_template("addproduct.html", form=form)

@app.route("/uploadfile", methods=["GET", "POST"])
def upload_file():
    form = AddProduct()
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            obj = Product(name=form.name.data,
                          file=filename,
                          price = form.price.data)
            db.session.add(obj)
            db.session.commit()
            flash("You successfully added the product", category="success")
        
        return redirect("/")
    
    if form.errors:
        print(form.errors)
        for error in form.errors:
            print(error)

        flash("You didn't add the product properly", category="danger")
        

    return render_template("addproduct.html", form=form)

@app.route("/delete/<int:id>")
@login_required
def delete_product(id):
    if current_user.role == "admin":

        current = Product.query.get(id)
        print(current)
        db.session.delete(current)
        db.session.commit()
        return redirect("/")
    else:
        return "You are not authorized", 404


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    if current_user.role == "admin":

        current = Product.query.get(id)
        print(current)
        form = AddProduct(name=current.name,
                        price=current.price,
                        )
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            current.name = form.name.data
            print("name", current.name)
            current.file = filename
            current.price = form.price.data

            db.session.commit()
            flash("You successfully added the product", category="success")
            
            return redirect("/")
        
        if form.errors:
            print(form.errors)
            for error in form.errors:
                print(error)

            flash("You didn't add the product properly", category="danger")
        return render_template("addproduct.html", form=form)
    else:
        return "You are not authorized", 404
    


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/category/<int:category_id>")
def category_select(category_id):
    current_category = Category.query.get(category_id)
    print(current_category)
    products = current_category.product_id
    print(products)
    for product in products:
        print(product)

    return render_template("index.html", products=products)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You successgfully registered", category="success")
        redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        exists = User.query.filter(User.username==form.username.data).first()
        print(exists)
        if exists and exists.password == form.password.data:
            login_user(exists)
            flash("You successfully logged in", category="success")
            return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
