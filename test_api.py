import requests

code = """
for(int i=0; i<n; i++){
    for(int j=0; j<n; j++){
        cout << arr[i][j];
    }
}
"""

response = requests.post("http://127.0.0.1:8000/analyze", json={"code": code})
print(response.json())
