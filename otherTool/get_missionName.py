def get_GiteeMission(PJ_name, needs: list):
    """
    把gitee需求 转为 自己的gitee任务
    """
    print(get_GiteeMission.__doc__.strip().center(60, '*'))
    missions = []
    missions.append('【测试】' + f'【{PJ_name}】 功能测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例执行')
    missions.append('【测试】' + f'【{PJ_name}】 回归测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例设计')
    missions += ['【测试】' + f"""【{PJ_name}】#{i} 功能测试""" for i in needs]

    print('\n'.join(missions))


def get_XmindMission(Model, needs: list):
    """
    把gitee需求 转为 xmind8标题
    """
    print(get_XmindMission.__doc__.strip().center(60, '*'))

    missions = [f"""{Model}#{i}""" for i in needs]
    print('\n'.join(missions))


if __name__ == '__main__':
    needs = """IMOH	全局增加登录用户安全水印
""".strip().replace('	', ' ').split('\n')
    get_GiteeMission('XC-Portal 2.2（私有化部署）', needs)
    get_XmindMission('Portal/2.2.0/', needs)
