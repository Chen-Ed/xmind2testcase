import os

if __name__ == '__main__':
    # urlfliter = r"https://1p-portal-k11-uat.nwplatform.com.cn/portal-uat/"
    # urlfliter = r"https://1p-portal-testk11-uat.nwplatform.com.cn/portal-uat/*"
    # requestType = r"!(CSS | Javascript | Flash | images)"
    os.system('chcp 65001')
    os.system(r'cd .\otherTool\mitmProxy')

    order = f'mitmweb.exe -s myAddon.py -p 8080 '
    # order = f'mitmdump.exe -s myAddon.py -p 8080 ~u mattch {urlfliter}'
    # print(order)
    os.system(order)