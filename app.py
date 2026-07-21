from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, Owner, Pet, Booking, Contact
from datetime import datetime
app = Flask(__name__)
app.secret_key = "petcarestay123"
app.config.from_object(Config)

# Inisialisasi database
db.init_app(app)

# Membuat database jika belum ada
with app.app_context():
    db.create_all()

    # Membuat akun admin pertama
    if User.query.filter_by(username="admin").first() is None:

        admin = User(username="admin")
        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()


# ==========================
# ROUTE HOME
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# ROUTE LOGIN
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            return redirect(url_for("dashboard"))

        flash("Username atau password salah!")

    return render_template("login.html")


# ==========================
# ROUTE DASHBOARD
# ==========================
@app.route("/dashboard")
def dashboard():

    total_owner = Owner.query.count()
    total_pet = Pet.query.count()
    total_booking = Booking.query.count()
    total_contact = Contact.query.count()

    return render_template(
        "dashboard.html",
        total_owner=total_owner,
        total_pet=total_pet,
        total_booking=total_booking,
        total_contact=total_contact
    )

# ==========================
# DATA PEMILIK
# ==========================

@app.route("/owners")
def owners():

    data_owner = Owner.query.all()

    return render_template(
        "owner/list.html",
        owners=data_owner
    )

@app.route("/owners/add", methods=["GET", "POST"])
def add_owner():

    if request.method == "POST":

        owner = Owner(
            name=request.form["name"],
            phone=request.form["phone"],
            email=request.form["email"],
            address=request.form["address"]
        )

        db.session.add(owner)
        db.session.commit()

        return redirect(url_for("owners"))

    return render_template("owner/add.html")

@app.route("/owners/edit/<int:id>", methods=["GET","POST"])
def edit_owner(id):

    owner = Owner.query.get_or_404(id)

    if request.method == "POST":

        owner.name = request.form["name"]
        owner.phone = request.form["phone"]
        owner.email = request.form["email"]
        owner.address = request.form["address"]

        db.session.commit()

        return redirect(url_for("owners"))

    return render_template(
        "owner/edit.html",
        owner=owner
    )
@app.route("/owners/delete/<int:id>")
def delete_owner(id):

    owner = Owner.query.get_or_404(id)

    db.session.delete(owner)

    db.session.commit()

    return redirect(url_for("owners"))

@app.route("/pets")
def pets():

    data_pet = Pet.query.all()

    return render_template(
        "pet/list.html",
        pets=data_pet
    )

@app.route("/pets/add", methods=["GET", "POST"])
def add_pet():

    owners = Owner.query.all()

    if request.method == "POST":

        pet = Pet(
            name=request.form["name"],
            species=request.form["species"],
            breed=request.form["breed"],
            age=request.form["age"],
            gender=request.form["gender"],
            weight=request.form["weight"],
            owner_id=request.form["owner_id"]
        )

        db.session.add(pet)
        db.session.commit()

        return redirect(url_for("pets"))

    return render_template(
        "pet/add.html",
        owners=owners
    )

@app.route("/pets/edit/<int:id>", methods=["GET", "POST"])
def edit_pet(id):

    pet = Pet.query.get_or_404(id)
    owners = Owner.query.all()

    if request.method == "POST":

        pet.name = request.form["name"]
        pet.species = request.form["species"]
        pet.breed = request.form["breed"]
        pet.age = request.form["age"]
        pet.gender = request.form["gender"]
        pet.weight = request.form["weight"]
        pet.owner_id = request.form["owner_id"]

        db.session.commit()

        return redirect(url_for("pets"))

    return render_template(
        "pet/edit.html",
        pet=pet,
        owners=owners
    )

@app.route("/pets/delete/<int:id>")
def delete_pet(id):

    pet = Pet.query.get_or_404(id)

    db.session.delete(pet)
    db.session.commit()

    return redirect(url_for("pets"))

@app.route("/bookings")
def bookings():

    data_booking = Booking.query.all()

    return render_template(
        "booking/list.html",
        bookings=data_booking
    )

@app.route("/bookings/add", methods=["GET","POST"])
def add_booking():

    pets = Pet.query.all()

    if request.method == "POST":

        booking = Booking(
    pet_id=request.form["pet_id"],
    check_in=datetime.strptime(
        request.form["check_in"], "%Y-%m-%d"
    ).date(),

    check_out=datetime.strptime(
        request.form["check_out"], "%Y-%m-%d"
    ).date(),

    room_type=request.form["room_type"],
    note=request.form["note"],
    status=request.form["status"]
)

        db.session.add(booking)
        db.session.commit()

        return redirect(url_for("bookings"))

    return render_template(
        "booking/add.html",
        pets=pets
    )

@app.route("/bookings/edit/<int:id>", methods=["GET", "POST"])
def edit_booking(id):

    booking = Booking.query.get_or_404(id)
    pets = Pet.query.all()

    if request.method == "POST":

        booking.pet_id = request.form["pet_id"]

        booking.check_in = datetime.strptime(
            request.form["check_in"], "%Y-%m-%d"
        ).date()

        booking.check_out = datetime.strptime(
            request.form["check_out"], "%Y-%m-%d"
        ).date()

        booking.room_type = request.form["room_type"]
        booking.note = request.form["note"]
        booking.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("bookings"))

    return render_template(
        "booking/edit.html",
        booking=booking,
        pets=pets
    )

@app.route("/bookings/delete/<int:id>")
def delete_booking(id):

    booking = Booking.query.get_or_404(id)

    db.session.delete(booking)
    db.session.commit()

    return redirect(url_for("bookings"))

@app.route("/contacts")
def contacts():

    data_contact = Contact.query.all()

    return render_template(
        "contact/list.html",
        contacts=data_contact
    )

@app.route("/contacts/add", methods=["GET","POST"])
def add_contact():

    if request.method == "POST":

        contact = Contact(
            name=request.form["name"],
            email=request.form["email"],
            message=request.form["message"]
        )

        db.session.add(contact)
        db.session.commit()

        return redirect(url_for("contacts"))

    return render_template("contact/add.html")

@app.route("/contacts/edit/<int:id>", methods=["GET","POST"])
def edit_contact(id):

    contact = Contact.query.get_or_404(id)

    if request.method == "POST":

        contact.name = request.form["name"]
        contact.email = request.form["email"]
        contact.message = request.form["message"]

        db.session.commit()

        return redirect(url_for("contacts"))

    return render_template(
        "contact/edit.html",
        contact=contact
    )

@app.route("/contacts/delete/<int:id>")
def delete_contact(id):

    contact = Contact.query.get_or_404(id)

    db.session.delete(contact)
    db.session.commit()

    return redirect(url_for("contacts"))


# ==========================
# MENJALANKAN FLASK
# ==========================
if __name__ == "__main__":
    app.run(debug=True)

