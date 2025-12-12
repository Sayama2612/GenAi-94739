import requests

try:
    url = "https://nilesh-g.github.io/learn-web/data/novels.json"
    response = requests.get(url)
    print("Status Code:", response.status_code)

    data = response.json()
    print("Data:", data)
except:
    print("Some error occured")    