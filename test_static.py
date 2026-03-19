from analyzer.static import analyze

code = """
for(int i=0; i<n; i++){
    for(int j=0; j<n; j++){
        cout << arr[i][j];
    }
}
"""

results = analyze(code)
for r in results:
    print(r)
