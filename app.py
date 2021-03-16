from flask import Flask, render_template, request, redirect, flash, url_for
import os, mlflow
import numpy as np
# import pandas as pd
import boto3, json, requests
from flask_cors import CORS, cross_origin
from mlflow.tracking import MlflowClient


app = Flask(__name__)
CORS(app)
app.secret_key='12345'


@app.route('/')
@cross_origin()
def index():
    # flash('File Uploaded')
    return render_template('index.html')


@app.route('/upload_file', methods= ['GET', 'POST'])
@cross_origin()
def upload_file():
    if 'myFile' not in request.files:
        flash('No file part')
        return redirect(request.url)
    uploaded_file = request.files['myFile']
    if uploaded_file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if uploaded_file.filename != '':
        print(os.getcwd())
        uploaded_file.save(os.path.join('csv_data',  uploaded_file.filename))
        s3_client = boto3.client('s3', aws_access_key_id='AKIAQLOZZIL6GGLX5PEF',
                          aws_secret_access_key='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')
        print('client name is.....', s3_client)
        s3_resource = boto3.resource('s3', aws_access_key_id='AKIAQLOZZIL6GGLX5PEF',
                                     aws_secret_access_key='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')
        print('client name is.....', s3_resource)
        my_bucket = s3_resource.Bucket('ml-flow01')
        # print('bucket name is....', bucket)
        #try:
        # response = s3_client.upload_file('README.md', my_bucket, 'README.md')
        response= s3_resource.Bucket('ml-flow01').put_object(Key=uploaded_file.filename, Body=uploaded_file)
        # with open(uploaded_file, "rb") as f:
        #     response= s3_resource.Bucket(my_bucket).put_object(Key=uploaded_file.filename, Body=f)
        # my_bucket = s3_resource.Bucket('distilbertmodel50epochs')
        # for s3_object in my_bucket.objects.all():
        #     filename = s3_object.key
        #     my_bucket.download_file(s3_object.key, filename)
        print('response is.....', response)
            # with open(uploaded_file, "rb") as f:
            #     s3_client.upload_fileobj(f, bucket, "OBJECT_NAME")
        # except Exception as e:
        #     # logging.error(e)
        #     return False
        # return True
        # return redirect(url_for('uploaded_file', filename= uploaded_file.filename))
        flash('File Uploaded', 'danger')
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/predict_data', methods=['GET', 'POST'])
@cross_origin()
def predict():
    all_col_ = ['fixed', 'acidity', 'volatile', 'acidity', 'citric', 'acid', 'residual', 'sugar',
                'chlorides', 'free', 'sulfur', 'dioxide', 'total', 'sulfur',
                'dioxide', 'density', 'pH', 'sulphates', 'alcohol']

    return render_template('inner-page.html', columns= all_col_)


@app.route('/result', methods=['GET', 'POST'])
@cross_origin()
def result():
    all_col_ = ['fixed', 'acidity', 'volatile', 'acidity', 'citric', 'acid', 'residual', 'sugar',
                'chlorides', 'free', 'sulfur', 'dioxide', 'total', 'sulfur',
                'dioxide', 'density', 'pH', 'sulphates', 'alcohol']
    input_data= {}
    for col in all_col_:
        col_val= request.form.get(col)
        input_data[col]= col_val

    print(input_data)
    ENDPOINT_NAME= 'https://jswaxdsra3.execute-api.us-east-1.amazonaws.com/sagemaker-004'
    # runtime = boto3.client('runtime.sagemaker')
    data= {
        "data": [[7.8, 0.88, 0, 2.6, 0.098, 25, 67, 0.9968, 3.2, 0.68, 9.8]]
    }

    # if isinstance(event['body'], (unicode, str)):
    #     body = json.loads(event['body'])
    payload = data['data']
    print(payload)

    # response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
    #                                    ContentType='text/csv',
    #                                    Accept='text/csv',
    #                                    Body=json.dumps(payload))

    # print(response)
    response = requests.post(
        ENDPOINT_NAME, data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    # result = json.loads(response['Body'].read().decode())
    print(response)
    print(response.status_code,response.content, response.reason, response.text)

    # model_name = "ElasticnetWineModel"

    # remote_server_uri = "http://0.0.0.0:5000"  # set to your server URI
    # mlflow.set_tracking_uri(remote_server_uri)
    #
    # client = MlflowClient()
    # for mv in client.search_model_versions(f"name='{model_name}'"):
    #     mv = dict(mv)
    #
    # logged_model = mv["source"]
    #
    # # Load model as a PyFuncModel.
    # loaded_model = mlflow.pyfunc.load_model(logged_model)
    # result = loaded_model.predict(input_data)
    # print(result)

    flash(f'Model prediction is {response.text}', 'danger')
    return redirect(url_for('predict'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)