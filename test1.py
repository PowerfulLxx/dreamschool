from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

import time
import sys


rate_url = "https://www.boc.cn/sourcedb/whpj/"
symbol_url = "https://www.11meigui.com/tools/currency"


# 从输入符号获取对应货币名
def get_currency_name(standard_symbol):
    driver.get(symbol_url)
    # 等待加载时间，并获取html源码并获取对应表格
    driver.implicitly_wait(10)
    symbolHtml = driver.page_source
    soup = BeautifulSoup(symbolHtml,'html.parser')
    contents = soup.find(id='desc')

    # 查找标准符号对应的货币名称
    currency_name = None

    for row in contents.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 5 and cells[4].text.strip() == standard_symbol:
            currency_name = cells[1].text.strip()
            break

    # 标准符号输入错误的异常处理
    if currency_name:
        return currency_name
    else:
        print('未找到对应的货币名称')
        sys.exit()


# 根据货币名以及日期获取对应的外汇卖出价格
def get_forex_sell_price(currency_name,date):
    driver.get(rate_url)
    
    # 输入日期以及货币名进行查询
    driver.find_element(By.NAME,value='erectDate').clear()
    driver.find_element(By.NAME,value='erectDate').send_keys(date)
    driver.find_element(By.NAME,value='nothing').clear()
    driver.find_element(By.NAME,value='nothing').send_keys(date)

    # 通过下拉菜单选择货币
    element = driver.find_element(By.ID,value='pjname')
    select = Select(element)
    driver.implicitly_wait(10)
    select.select_by_value(currency_name)
    search_btns = driver.find_elements(By.CLASS_NAME,value='search_btn')
    search_btns[1].click()
    time.sleep(5)

    flag = True
    # 初始化数据字典
    data = []
    # 最后要输出的外汇卖出价
    forex_sell_price = None

    # 利用soup读取html文件
    page_num = 1
    while(flag):
        rate_html = driver.page_source
        soup = BeautifulSoup(rate_html,'html.parser')

        table = soup.find('div',attrs={'class':'BOC_main publish'})

        # 从文本内容中提取总页数
        
        total_pages_element = driver.find_element(By.XPATH, "//li[contains(text(), '共') and contains(text(), '页')]")
        total_pages_text = total_pages_element.text
        total_pages = int(total_pages_text.split('共')[-1].split('页')[0])
        
        # 遍历表格行
        for row in table.find_all('tr')[1:]:  # 跳过第一行表头
            cells = row.find_all('td')
            if len(cells) >= 7:
                item = {
                    "货币名称": cells[0].text.strip(),
                    "现汇买入价": cells[1].text.strip(),
                    "现钞买入价": cells[2].text.strip(),
                    "现汇卖出价": cells[3].text.strip(),
                    "现钞卖出价": cells[4].text.strip(),
                    "中行折算价": cells[5].text.strip(),
                    "发布时间": cells[6].text.strip()
                }
                #print(item)
                forex_sell_price = item['现汇卖出价']
                data.append(item)
        
        # 寻找下一页按钮
        next_page = None
        try:
            next_page = driver.find_element(By.CLASS_NAME,'turn_next')
        except Exception as e:
            print(e)
            pass
        if next_page:
            try:
                next_page.click()
                page_num += 1
                time.sleep(2) # 控制间隔时间，等待浏览器反映
            except Exception as e:
                print ('next_page could not be clicked')
                print (e)
                flag = False
        else:
            flag = False

        if (page_num > total_pages):
            flag = False

    # 保存数据到txt文件
    with open('result.txt', 'w') as file:
        for item in data:
            file.write(f"货币名称: {item['货币名称']}, 现汇买入价: {item['现汇买入价']}, 现钞买入价: {item['现钞买入价']}, 现汇卖出价: {item['现汇卖出价']}, 现钞卖出价: {item['现钞卖出价']}, 中行折算价: {item['中行折算价']}, 发布时间: {item['发布时间']}\n")
    if forex_sell_price:
        return forex_sell_price
    else:
        print('没有找到对应日期外汇卖出价')

#print(symbol_name_driver('HKD'))
# 获取命令行参数
args = sys.argv
if (len(args) > 1):
    date = args[1]
    symbol = args[2]
driver = webdriver.Firefox()
currency_name = get_currency_name(symbol)
forex_sell_price = get_forex_sell_price(currency_name=currency_name,date=date)
print(forex_sell_price)
#print(contents)
