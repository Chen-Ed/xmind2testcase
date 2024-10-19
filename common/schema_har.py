SCHEMA_HAR={
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HAR Log Format Schema",
  "description": "A schema defining the structure of a HTTP Archive (HAR) log.",
  "type": "object",
  "properties": {
    "log": {
      "type": "object",
      "properties": {
        "version": {
          "type": "string",
          "pattern": "^\\d+(\\.\\d+)?$"
        },
        "creator": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "version": {"type": "string"},
            "comment": {"type": ["string", "null"]}
          },
          "required": ["name", "version"]
        },
        "pages": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "startedDateTime": {"type": "string", "format": "date-time"},
              "id": {"type": "string"},
              "title": {"type": "string"}
            },
            "required": ["startedDateTime", "id", "title"]
          }
        },
        "entries": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "startedDateTime": {"type": "string", "format": "date-time"},
              "time": {"type": "number"},
              "request": {
                "$ref": "#/definitions/requestObject"
              },
              "response": {
                "$ref": "#/definitions/responseObject"
              },
              "cache": {"type": "object"},
              "timings": {
                "type": "object",
                "properties": {
                  "connect": {"type": "number"},
                  "ssl": {"type": "number"},
                  "send": {"type": "number"},
                  "receive": {"type": "number"},
                  "wait": {"type": "number"},
                  # // Additional timing fields can be added as needed
                }
              },
              "serverIPAddress": {"type": "string", "format": "ipv4"}
            },
            "required": ["startedDateTime", "time", "request", "response", "cache", "timings", "serverIPAddress"]
          }
        }
      },
      "required": ["version", "creator", "pages", "entries"]
    }
  },
  "required": ["log"],
  "definitions": {
    "requestObject": {
      "type": "object",
      "properties": {
        "method": {"type": "string"},
        "url": {"type": "string", "format": "uri"},
        "httpVersion": {"type": "string", "pattern": "^HTTP/\d+.\d+$"},
        "cookies": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "value": {"type": "string"}
            },
            "required": ["name", "value"]
          }
        },
        "headers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "value": {"type": "string"}
            },
            "required": ["name", "value"]
          }
        },
        # // Other request properties like 'queryString', 'headersSize', etc.
      },
      "required": ["method", "url", "httpVersion", "cookies", "headers"]
    },
    "responseObject": {
      "type": "object",
      "properties": {
        "status": {"type": "integer"},
        "statusText": {"type": "string"},
        "httpVersion": {"type": "string", "pattern": "^HTTP/\d+.\d+$"},
        "cookies": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "value": {"type": "string"}
            },
            "required": ["name", "value"]
          }
        },
        "headers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "value": {"type": "string"}
            },
            "required": ["name", "value"]
          }
        },
        # // Other response properties like 'content', 'headersSize', etc.
      },
      "required": ["status", "statusText", "httpVersion", "cookies", "headers"]
    }
  }
}

if  __name__ == "__main__":
    import json
    import jsonschema
    with open(r'D:\pythonProject\myMitmProxy\cache\har_20240704_174409.har','r',encoding='utf8') as f:
        a = json.load(f)
    # 执行验证
    try:
        jsonschema.validate(a, SCHEMA_HAR)
        print("验证通过")
    except jsonschema.exceptions.ValidationError as e:
        print(f"验证失败: {e.message}")
