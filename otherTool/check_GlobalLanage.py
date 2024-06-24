import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver_path=ChromeDriverManager().install() #下载latest release版本的chromedriver，并返回其在本机的下载存储路径
# 指定要访问的页面列表
url_list = ["https://open-uat.nwplatform.com.cn/",
"https://open-uat.nwplatform.com.cn/appStore",
"https://open-uat.nwplatform.com.cn/open-capability",
"https://open-uat.nwplatform.com.cn/developer/doc",
"https://open-uat.nwplatform.com.cn/developer/search",
"https://open-uat.nwplatform.com.cn/account/notify-message",
"https://open-uat.nwplatform.com.cn/account/info",
"https://open-uat.nwplatform.com.cn/developer/console",
"https://open-uat.nwplatform.com.cn/appStore/f13d6a9626ea4b25aaf46819616c14b6",
"https://open-uat.nwplatform.com.cn/developer/doc?docCode=b5798f2e&category=GENERAL_ABILITY"]

result_list = []

# 创建Chrome驱动

# 创建ChromeOptions对象
# options = webdriver.ChromeOptions()
# # 设置请求头参数
# options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"')

driver = webdriver.Chrome(service=Service(driver_path)) 



# 遍历访问所有页面

driver.get("https://open-uat.nwplatform.com.cn/login")
driver.set_window_size(1936, 1056)
driver.find_element(By.NAME, "password").send_keys("Qq123456")
driver.find_element(By.NAME, "email").send_keys("alanxu@nwcs.com.hk")
driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .el-button").click()
time.sleep(3)
driver.find_element(By.XPATH, "//div[2]/div/div/i").click()
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/ul/div[1]/p[2]/span").click()
driver.find_element(By.XPATH, "//li[4]/span/span").click()

for url in url_list:
    driver.get(url)
    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//body')))
    # 获取页面上的所有元素
    elements = driver.find_elements(By.XPATH,"//*")
    thisUrl_reasult = {'url': url, 'has_chinese': False,"content":[]}
    # 检查页面中是否包含中文 遍历每个元素并输出其content属性
    for element in elements:
        try:
            content = element.getText()
            if re.findall('[\u4e00-\u9fa5]+', content):
                # ele_source =  driver.execute_script("return arguments[0].outerHTML;", element)
                thisUrl_reasult["content"].append({element.getTagName():content})
                thisUrl_reasult["has_chinese"] = True
        except:
            print(f"查看元素内容出现错误！{element.getTagName()}")

    result_list.append(thisUrl_reasult)
    time.sleep(0.5)

# 关闭Chrome驱动
driver.quit()

# 输出所有结果
print(result_list)

with open(r'.\check_GlobalLanage.json',encoding='utf8',mode='w+') as f:
    
    print(json.dumps(result_list),file=f)

