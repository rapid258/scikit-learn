# Flask API for scikit learn
A Flask application that can serve predictions from a scikit-learn model.
Reads a pickled sklearn model into memory when the Flask app is started and returns predictions through the /predict endpoint. 
Any sklearn model can be used for prediction.

## Dependencies
- Flask==1.0.2
- numpy==1.16.3
- pandas==0.24.2
- scikit-learn==0.20.3

```
pip install -r requirements.txt
```

### Running API
```
python main.py <port>
```

# Endpoints
### /predict (POST)
Returns an array of predictions given a JSON object representing independent variables. Here's a sample input:
```
[
{"Name": "andrea erika"},
{"Name": "erik"} 
]

```

and sample output:
```
{
  "prediction": [
    "female", 
    "male"
  ]
}
```
## Example of use in curl

```
curl -d '[{"Name": "andrea erika"},{"Name": "erik"} ]' -H "Content-Type: application/json"      -X POST http://35.225.223.196:5000/predict &&     echo -e "\n -> predict OK"
```


