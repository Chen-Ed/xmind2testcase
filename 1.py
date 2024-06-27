import re

# 原始字符串
input_string = '''
"parameters": [
    {
        "name": "auth-token",
        "in": "header",
        "description": "",
        "required": true,
        "example": "{{auth-token}}",
        "schema": {
            "type": "string"
        }
    }
],
'''

# 定义正则表达式
pattern = re.compile(r'"parameters": $$\s*{([^}]*)}\s*]', re.DOTALL)

# 使用正则表达式进行匹配
match = re.search(pattern, input_string)

if match:
    parameters_content = match.group(1)
    print(parameters_content)
else:
    print("No match found.")
