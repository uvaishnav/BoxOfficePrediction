from flask import Flask, request, render_template, jsonify
import numpy as np
from BoxOfficePrediction.pipeline.prediction_pipeline import CustomData, PredictPipeline
from BoxOfficePrediction import logger

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_revenue():
    try:
        data = request.get_json()
        
        custom_data = CustomData(
            budget=int(data['budget']),
            runtime=int(data['runtime']),
            crew=data['director_name'],
            hero=data['hero_name'],
            heroine=data['heroine_name'],
            release_month=data['release_month'],
            production_countries=data['production_company'],
            spoken_languages=data['spoken_languages'],
            genres=str(request.form.getlist('genres[]'))
        )

        pred_df = custom_data.get_data_as_dataframe()
        logger.info("Predicting user data")

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)
        logger.info("Prediction Done")

        footfall = np.exp(result[0])
        predicted_revenue = 11.75 * footfall

        return jsonify(results=predicted_revenue, expected_budget=data['budget'])
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify(error=str(e)), 500
    


if __name__ == '__main__':
    app.run(host="0.0.0.0")
