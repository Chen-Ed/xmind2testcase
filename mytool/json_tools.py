import json
import jsonpath_ng
from loguru import logger

def replace_json_elements(json_str, json_path, target_str):
    """
    使用jsonpath_ng查询并替换JSON字符串中指定路径的值。

    :param json_str: JSON格式的字符串
    :param json_path: jsonpath表达式
    :param target_str: 目标字符串，用于替换
    :return: 替换后的JSON字符串
    """
    # 将JSON字符串转换为字典
    data = json.loads(json_str)

    # 解析jsonpath表达式
    path_expr = jsonpath_ng.parse(json_path)

    # 执行查询
    matches = path_expr.find(data)

    # 检查是否有匹配项
    if matches:
        logger.info(f"找到匹配项:{[match.value for match in matches]}")
        # 遍历匹配项并进行替换
        for i,match in enumerate(matches):
            # 替换值
            matches[i].full_path.update(data, target_str)

    # 将修改后的字典转换回JSON字符串
    result_json_str = json.dumps(data, indent=2,ensure_ascii=False)

    return result_json_str


def find_json_value(json_str, json_path):
    """
    使用jsonpath_ng查询JSON字符串中指定路径的元素并打印。

    :param json_str: JSON格式的字符串
    :param json_path: jsonpath表达式
    """
    # 将JSON字符串转换为字典
    data = json.loads(json_str)

    # 解析jsonpath表达式
    path_expr = jsonpath_ng.parse(json_path)

    # 执行查询
    matches = path_expr.find(data)

    # 检查是否有匹配项
    if matches:
        # 遍历匹配项并打印
        return [match.value for match in matches]


if __name__ == '__main__':
    # 示例调用
    json_str = '{"name": "Alice", "details": {"age": 30, "city": "New York"}}'
    json_path = '$..city'
    target_str = "佛山"
    logger.info(find_json_value(json_str, json_path))
    logger.info(replace_json_elements(json_str, json_path, target_str))


