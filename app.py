from flask import Flask, request, render_template
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

with open('model_pickle.pkl', 'rb') as file:
    model = pickle.load(file)

scaler = StandardScaler()

@app.route('/analysis')
def analysis():
    return render_template("stroke.html")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        gender = request.form["gender"]
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        disease = int(request.form['disease'])
        married = request.form['married']
        work = request.form['work']
        residence = request.form['residence']
        glucose = float(request.form['glucose'])
        bmi = float(request.form['bmi'])
        smoking = request.form['smoking']

        # Encoding gender
        gender_male = 0
        gender_other = 0
        if gender == "Male":
            gender_male = 1
        elif gender == "Other":
            gender_other = 1

        # Encoding married
        married_yes = 0
        if married == "Yes":
            married_yes = 1

        # Encoding work type
        work_type_Never_worked = 0
        work_type_Private = 0
        work_type_Self_employed = 0
        work_type_children = 0
        if work == 'Self-employed':
            work_type_Self_employed = 1
        elif work == 'Private':
            work_type_Private = 1
        elif work == 'children':
            work_type_children = 1
        elif work == 'Never_worked':
            work_type_Never_worked = 1

        # Encoding residence type
        Residence_type_urban = 0
        if residence == "Urban":
            Residence_type_urban = 1

        # Encoding smoking status
        smoking_status_formerly_smoked = 0
        smoking_status_never_smoked = 0
        smoking_status_smokes = 0
        if smoking == 'formerly smoked':
            smoking_status_formerly_smoked = 1
        elif smoking == 'smokes':
            smoking_status_smokes = 1
        elif smoking == 'never smoked':
            smoking_status_never_smoked = 1

        feature = scaler.fit_transform([[age, hypertension, disease, glucose, bmi,
                                         gender_male, gender_other, married_yes,
                                         work_type_Never_worked, work_type_Private,
                                         work_type_Self_employed, work_type_children,
                                         Residence_type_urban, smoking_status_formerly_smoked,
                                         smoking_status_never_smoked, smoking_status_smokes]])

        prediction = model.predict(feature)[0]

        if prediction == 0:
            prediction_text = "NO"
        else:
            prediction_text = "YES"

        return render_template("index.html", prediction_text="Chance of Strokes Prediction is --> {}".format(prediction_text))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()
