from random import randint
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random():
    # Get total rows in cafe cb
    row_count = Cafe.query.count()
    # Place cursor at random offset and grab only that record
    cafe = Cafe.query.offset(randint(0, row_count-1)).first()
    return jsonify(cafe=cafe.to_dict())


@app.route("/all", methods=["GET"])
def get_all():
    # Get all rows in cafe cb
    cafes = Cafe.query.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/search", methods=["GET"])
def get_cafe_from_location():
    location = request.args.get("loc")
    cafe = Cafe.query.filter_by(location=location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Unable to find cafe at provided location."})


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    try:
        cafe = Cafe(
            name = request.form.get("name"),
            map_url = request.form.get("map_url"),
            img_url = request.form.get("img_url"),
            location = request.form.get("location"),
            has_sockets = bool(request.form.get("has_sockets")),
            has_toilet = bool(request.form.get("has_toilet")),
            has_wifi = bool(request.form.get("has_wifi")),
            can_take_calls = bool(request.form.get("can_take_calls")),
            seats = request.form.get("seats"),
            coffee_price = request.form.get("coffee_price"),
        )
        db.session.add(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    except Exception as e:
        print(f"{e}")
        return jsonify(response={"failure": "Unable to process request."})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_cafe_price(cafe_id):
    new_price = request.args.get("new_price")
    print(f"{new_price}")
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(
            response={
                "success": f"Successfully updated price at {cafe.name}"
            }
        )
    else:
        return jsonify(
            error={
                "failure": f"Cafe with id {cafe_id} not found."
            }
        ), 404


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    cafe = Cafe.query.get(cafe_id)
    if api_key == "TopSecretAPIKey":
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(
                response={
                    "success": f"Successfully deleted cafe: {cafe.name}"
                }
            ), 200
        else:
            return jsonify(
                error={
                    "failure": f"Cafe with id {cafe_id} not found."
                }
            ), 404
    else:
        return jsonify(
            error={
                "failure": "Invalid API Key"
            }
        ), 401


if __name__ == '__main__':
    app.run(debug=True)
