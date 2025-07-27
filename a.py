import json

json_input = '''
```json
{
  "Cal": 300
}
```
'''

# JSON文字列を辞書に変換
data = json.loads(json_input)

print(data)        # {'Cal': 300}
print(type(data))  # <class 'dict'>