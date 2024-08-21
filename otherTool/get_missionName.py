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
    needs = """IN08	应用展示增加关闭显示选项
IN0H	项目配置增加非营业时间和假期日历信息
INIQ	处理A.Connect中WS切换XigmaCloud接口问题
INJ9	处理A.Connect 引用 WS页面替换
INJH	XC-UAT登录，增加lease开发人员接收验证码邮件白名单
""".strip().replace('	', ' ').split('\n')
    get_GiteeMission('XC-Portal 2.3', needs)
    get_XmindMission('Portal/2.3.0/', needs)
