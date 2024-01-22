
# Flask Rest-X Template

This repository is a template that can be used for everyone to start making API using Flask Rest-X.

See the [license](https://github.com/Enricko/Flask-Restx-Template/blob/main/LICENSE) file for more information, I reserve the right to take down any repository that does not meet these requirements.

## FAQ

#### Why i make this template?
I make this template so everyone can easily organize the file and usage. However there is none or i didn't search that deep for Flask Rest-X Template. So i decide make this my on 

#### Why the template is so basic and bla-bla...

Well i just make it with my experience as junior programmer and my majority is not python.


## How To Setup

To setup the Flask Rest-X i made.

#### First clone the repository
```
git clone https://github.com/Enricko/Flask-Restx-Template.git
```

#### Go to the file directory and then install python virtual env
```
pip install virtualenv
```

#### Activate the virtual env
```
.\env\scripts\activate
```

#### Copy paste the `.env.example`
```
cp .env.example .env
```

#### In `.env` setup your database and you can setup the other in there
```
DB_CONNECTION=<db connection>
DB_DATABASE=<db name>
DB_USERNAME=<db username>
DB_PASSWORD=<db password>
```

#### And then just run it 
```
python main.py
```

## Example

Here the example

#### Database Model create file in folder `app/model/<your_filename>`
```
from app.extensions import db


class ExampleModel(db.Model):
    __tablename__ = "example_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @validates("name") # Validating DB model
    def validate_name(self, key, name):
        if not name:
            raise AssertionError("Name field is required")
        return name

    def __repr__(self):
        return f"<ExampleModel(id={self.id}, name={self.name}, created_at={self.created_at}, updated_at={self.updated_at})>"
```

#### Api Model
```
from flask_restx import fields, reqparse
from app.extensions import api

# For form input 
input_parser = reqparse.RequestParser()
input_parser.add_argument("id", type=int)
input_parser.add_argument("name", type=str)

# For fetching data
example_api_model = api.model(
    "Api Model",
    {
        "id": fields.Integer,
        "name": fields.String,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime
    },
)
```

#### Route Get Post Put Delete
```
from app.resources import ns
from flask_restx import Resource
from app.extensions import api_handle_exception, db

@ns.route("/example")
class Example(Resource):

    # Get
    @ns.marshal_list_with(example_api_model) # Get Api Model
    @api_handle_exception # Error handler
    def get(self):
        data = ExampleModel.query.all()

        return data

    # Post
    @ns.expect(input_parser) # Input Parser Model
    @api_handle_exception # Error handler
    def post(self):
        args = input_parser.parse_args()
        
        id = args["id"]
        name = args["name"]

        data = ExampleModel(
            id=id,
            name=name,
        )

        db.session.add(data)
        db.session.commit()
        return {"message":"Data Inserted."}

# With id parameter
@ns.route("/example/<integer:id>")
class ExampleSingle(Resource):
    # Get
    @ns.marshal_list_with(example_api_model) # Get Api Model
    @api_handle_exception # Error handler
    def get(self,id):
        data = ExampleModel.query.get(id)

        return data

    # Put or usually used for Update
    @ns.expect(input_parser) # Input Parser Model
    @api_handle_exception # Error handler
    def put(self,id):
        args = input_parser.parse_args()
        
        id = args["id"]
        name = args["name"]

        data = ExampleModel.query.get(id)

        data.id = id
        data.name = name
        
        db.session.commit()
        return {"message":"Data Updated."}

    # Delete
    @ns.expect(input_parser) # Input Parser Model
    @api_handle_exception # Error handler
    def delete(self,id):

        data = ExampleModel.query.get(id)

        db.session.delete(data)
        
        db.session.commit()
        return {"message":"Data Deleted."}



```

## Lisence
This project is lisenced under the MIT Lisence - See the [Licence](https://github.com/Enricko/Flask-Restx-Template/blob/main/LICENSE) for the details
