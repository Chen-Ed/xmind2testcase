from common.comm import *
from common.schema_swagger import *
import json


class ParseOpenApi(object):
    def __init__(self, file_path: str):
        self.openapi_obj = self.parse_swagger(file_path)

    @staticmethod
    def parse_swagger(file_path: str) -> dict:
        """Parses a Swagger 3.0 JSON file and returns an OpenAPI object."""
        with open(file_path, 'r', encoding='utf8') as file:
            json_data = json.load(file)

            # 验证并解析json
            vailidata_OpenAPI(json_data, SCHEMA_SWAGGER)

            return json_data

    def __len__(self):
        return len(self.openapi_obj.get('paths'))

    def __str__(self):
        return json.dumps(openapi_obj, indent=2)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.openapi_obj.get('paths')):
            path = list(self.openapi_obj.get('paths').keys())[self.index]
            operation = self.openapi_obj.get('paths')[path]
            self.index += 1
            return path, operation
        else:
            raise StopIteration


    def get_AllApi(self):
        api_list = []
        for path, operation in self:
            api_list.append({path: operation})
        return api_list

    def count_api(self):
        sum_GET = 0
        sum_POST = 0
        sum_PUT = 0
        sum_DELETE = 0
        sum_other = 0
        for path, operation in self:
            if operation.get('get'):
                sum_GET += 1
            elif operation.get('post'):
                sum_POST += 1
            elif operation.get('put'):
                sum_PUT += 1
            elif operation.get('delete'):
                sum_DELETE += 1
            else:
                sum_other += 1
        return {'sum_GET': sum_GET, 'sum_POST': sum_POST, 'sum_PUT': sum_PUT, 'sum_DELETE': sum_DELETE,
                'sum_other': sum_other, 'count': len(self.openapi_obj.get('paths'))}

    def to_dict(self):
        return self.openapi_obj

if __name__ == '__main__':
    openapi_obj = ParseOpenApi(os.path.join(CACHE,'new_swagger.json'))
    # print(openapi_obj)
    for path, operation in openapi_obj:
        logger.info('-' * 60)
        logger.info(path)
        # logger.info(json.dumps(operation, indent=2, ensure_ascii=False))
    # print(openapi_obj.count_api())
