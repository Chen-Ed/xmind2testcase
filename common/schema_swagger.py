SCHEMA_SWAGGER = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "openapi": {
            "type": "string",
            "pattern": "^3\\.0\\.\\d+$"
        },
        "info": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "version": {"type": "string"}
            },
            "required": ["title", "version"]
        },
        "servers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "format": "uri"}
                },
                "required": ["url"]
            }
        },
        "paths": {
            "type": "object",
            "patternProperties": {
                "^/.+": {
                    "type": "object",
                    "properties": {
                        "[get|post|delect|patch]+": {
                            "type": "object",
                            "properties": {
                                "summary": {"type": "string"},
                                "description": {"type": "string"},
                                "tags": {"type": "array", "items": {"type": "string"}},
                                "parameters": {"type": "array"},
                                "operationId": {"type": "string"},
                                "requestBody": {
                                    "type": "object",
                                    "properties": {
                                        "content": {
                                            "type": "object",
                                            "properties": {
                                                "application/json": {
                                                    "type": "object",
                                                    "properties": {
                                                        "schema": {},
                                                        "example": {}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "responses": {
                                    "type": "object",
                                    "patternProperties": {
                                        "^[2-5]\\d{2}$": {
                                            "type": "object",
                                            "properties": {
                                                "description": {"type": "string"},
                                                "content": {
                                                    "type": "object",
                                                    "properties": {
                                                        "application/json": {
                                                            "type": "object",
                                                            "properties": {
                                                                "schema": {},
                                                                "example": {}
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "type": "object",
            "properties": {
                "schemas": {"type": "object"}
            }
        }
    },
    "required": ["openapi", "info", "servers", "paths", "components"]
}
if __name__ == '__main__':
    import json
    import jsonschema
    with open(r'D:\pythonProject\myMitmProxy\cache\new_swagger.json','r',encoding='utf8') as f:
        a = json.load(f)
    # 执行验证
    try:
        jsonschema.validate(a, SCHEMA_SWAGGER)
        print("验证通过")
    except jsonschema.exceptions.ValidationError as e:
        print(f"验证失败: {e.message}")