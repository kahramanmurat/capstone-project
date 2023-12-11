import requests

# url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
url="https://5oph9792mi.execute-api.us-east-1.amazonaws.com/test/predict"

data = {'url': 'https://images.theconversation.com/files/513157/original/file-20230302-28-r91z9l.jpg?ixlib=rb-1.1.0&rect=10%2C0%2C6699%2C4466&q=45&auto=format&w=926&fit=clip'}

result = requests.post(url, json=data).json()
print(result)