from analyzer.static import analyze

code = """
class Solution {
public:
    int solve(int n) {
        for(int i=0; i<n; i++){
            int x = 5
        }
    
};
"""

results = analyze(code)
for r in results:
    print(r['type'], '-', r['message'], '| line:', r['line'])
