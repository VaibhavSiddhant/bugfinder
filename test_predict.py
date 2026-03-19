from model.predict import ml_predict

code1 = 'void foo(char *str) { char buf[10]; strcpy(buf, str); }'
code2 = 'int add(int a, int b) { return a + b; }'

print('Test 1 (should be bug):', ml_predict(code1))
print('Test 2 (should be clean):', ml_predict(code2))
