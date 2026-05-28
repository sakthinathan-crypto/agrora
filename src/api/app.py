from flask import Flask
from src.api.routes import predict_disease

app = Flask(__name__)

@app.route("/")
def home():
    return "API Running"

@app.route("/upload")
def upload_page():
    return '''
    <h2>Plant Disease Detection</h2>

    <form action="/predict" method="post" enctype="multipart/form-data">
    
        <input type="file" name="image">
        
        <br><br>
        
        <button type="submit">Predict Disease</button>

    </form>
    '''

app.add_url_rule(
    "/predict",
    "predict",
    predict_disease,
    methods=["POST"]
)

if __name__ == "__main__":
    app.run(debug=True)