from boto3.session import Session

session = Session(aws_access_key_id='AKIAJHG5MZOWVWJRJSJQ', aws_secret_access_key='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')
machine_learning = session.client('machinelearning', 'us-east-1')

model_id = 'ml-PydI1Cwh403'

labels = {
		"Max_Temp" : '57',
		"Min_Temp" : '44'
	}

model = machine_learning.get_ml_model(MLModelId=model_id)
predeiction_endpoint = model.get('EndpointInfo').get('EndpointUrl')

response = machine_learning.predict(MLModelId=model_id, Record = labels, PredictEndpoint=predeiction_endpoint)
print(response.get('Prediction').get('predictedValue'))
