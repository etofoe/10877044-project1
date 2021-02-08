from flask import render_template, request

from manage import app, db,   mongo, Individual_GIS, Individual_EC, Individual_NHIA


def add_citizens(citizen_4=None):
    citizen_1 = Individual_EC(
        first_name="tetteh",
        middle_name="kwame",
        last_name="eric",
        age=22
    )
    citizen_2 = Individual_GIS(
        first_name="tetteh",
        middle_name="kwame",
        last_name="eric",
        age=22
    )
    # citizen_3 = Individual_NHIA(
    #     first_name="tetteh",
    #     middle_name="kwame",
    #     last_name="eric",
    #     age=22
    # )
    # citizen_4 = {
    #     "first_name": "tetteh",
    #     "middle_name": "kwame",
    #     "last_name": "eric",
    #     "age": "25",
    # }
    #
    db.session.add(citizen_1)  # Adds new User record to database
    db.session.add(citizen_2)  # Adds new User record to database
    # db.session.add(citizen_3)  # Adds new User record to database
    db.session.commit()
    mongo.db.individual_DVLA.insert(citizen_4)


def results_EC(args):
    pass


def results_GIS(args):
    pass


def results_NHIA(args):
    pass


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []

    add_citizens()
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if not first_name or not last_name:
            errors = {"error": "The request payload is not in JSON format"}
        else:
            results_ec = Individual_EC.query.filter_by(first_name=first_name, last_name=last_name).all()
            results_gis = Individual_GIS.query.filter_by(first_name=first_name, last_name=last_name).all()
            results_nia = Individual_NHIA.query.filter_by(first_name=first_name, last_name=last_name).all()

            citizens = mongo.db.individual_DVLA
            results_DVLA_1 = []
            for c in citizens.find():
                results_DVLA_1.append(
                    {'first_name': c['first_name'], 'middle_name': c['middle_name'], 'last_name': c['last_name'],
                     'age': c['age']})

            results_DVLA = []
            for citizen in results_DVLA_1:
                if citizen['first_name'] == first_name and citizen['last_name'] == last_name:
                    results_DVLA.append(
                        {'first_name': citizen['first_name'], 'middle_name': citizen['middle_name'],
                         'last_name': citizen['last_name'],
                         'age': citizen['age']})

            return render_template('results.html', results_ec=results_EC, results_gis=results_GIS,
                                   results_nhia=results_NHIA, results_dvla=results_DVLA)

    return render_template('index.html', errors=errors)


@app.route('/results', methods=['GET', ])
def results():
    return render_template('results.html')


if __name__ == "__main__":
    app.run()
