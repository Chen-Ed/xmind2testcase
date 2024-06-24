# 把需求 转为 自己的任务
def get_mission(PJ_name,needs:list):
    missions = []
    missions.append(f'【{PJ_name}】 功能测试')
    missions.append(f'【{PJ_name}】 回归测试')
    missions.append(f'【{PJ_name}】 用例设计')
    
    for i in needs:
        template = f"""【{PJ_name}】 #{i} 功能测试"""
        missions.append(template)
    print('\n'.join(missions))



if __name__ == '__main__':
    needs = """IK97	AD账号手机号码自动带出
IKPS	应用开放权限问题设置
IL0D	应用列表补充应用分类
IL8T	应用列表补充搜素功能，搜索应用名称
ILAS	应用列表补充两个HR弹窗应用迁移
ILAV	旧WordSpace需要更换接口显示内容
ILAX	角色权限配置，由于应用量较多，需要进行分区进行查看
""".strip().replace('	',' ').split('\n')
    get_mission('XC-Portal 2.1.6',needs)