import requests
# url = 'http://localhost:9696/predict'
# url = 'http://localhost:8080/predict'
url='http://af5e6c6cde2fb47efbfc82e50a4b612c-58691788.us-east-1.elb.amazonaws.com/predict'

data = {'url': 'https://images.theconversation.com/files/513157/original/file-20230302-28-r91z9l.jpg?ixlib=rb-1.1.0&rect=10%2C0%2C6699%2C4466&q=45&auto=format&w=926&fit=clip'}

result = requests.post(url, json=data).json()
print(result)

