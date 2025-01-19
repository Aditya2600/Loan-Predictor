import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model
model_pickle = open("./artifacts/classifier.pkl", "rb")
clf = pickle.load(model_pickle)

@app.route("/ping", methods=["GET"])
def ping():
    return {"message": "Hi there, I'm working!!"}

@app.route("/params", methods=["GET"])
def get_application_params():
    # Return the expected parameters for prediction
    parameters = {
        "Gender": "<Male/Female>",
        "Married": "<Unmarried/Married>",
        "Credit_History": "<Unclear Debts/Cleared Debts>",
        "ApplicantIncome": "<Amount>",
        "LoanAmount": "<Amount>"
    }
    return jsonify(parameters)

@app.route("/predict", methods=["POST"])
def prediction():
    try:
        # Get JSON data from the request
        loan_req = request.get_json()
        print(loan_req)

        # Pre-processing user input
        Gender = 0 if loan_req["Gender"] == "Male" else 1
        Married = 0 if loan_req["Married"] == "Unmarried" else 1
        Credit_History = 0 if loan_req["Credit_History"] == "Unclear Debts" else 1
        ApplicantIncome = loan_req["ApplicantIncome"]
        LoanAmount = loan_req["LoanAmount"]

        # Making predictions
        result = clf.predict(
            [[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]]
        )

        # Preparing the response
        pred = "Approved" if result[0] == 1 else "Rejected"
        return jsonify({"loan_approval_status": pred})

    except Exception as e:
        # Handle errors and return a meaningful message
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)