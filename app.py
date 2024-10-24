from flask import Flask, request, render_template
from src.pipelines.prediction_pipelines import CustomData, PredictPipeline

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")  # Home page route


@app.route("/predict", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")  # Render the form on GET request

    else:
        # Collect data from the form
        data = CustomData(
            carat=float(request.form.get("carat")),
            depth=float(request.form.get("depth")),
            table=float(request.form.get("table")),
            x=float(request.form.get("x")),
            y=float(request.form.get("y")),
            z=float(request.form.get("z")),
            cut=request.form.get("cut"),
            color=request.form.get("color"),
            clarity=request.form.get("clarity"),
        )

        # Prepare the data for prediction
        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)

        # Round the prediction result
        results = round(pred[0], 2)

        # Render the form page again with the prediction result
        return render_template("form.html", final_result=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
