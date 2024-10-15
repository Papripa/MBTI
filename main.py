import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
#question_dict = {"IE": [6,15,21,26,41,51,1,11,16,31,36,43,53]};

def click_inputs(wd,susp,degree,cnt):

    wd.implicitly_wait(3)
    elements = wd.find_elements(By.TAG_NAME, "input")
    for i in range(0, len(elements)-1, 7):
        if i + 7 <= len(elements):  # 确保有足够的元素构成完整的组
            group = elements[i:i + 7]
            try:
                # 滚动到元素可见
                if cnt[0] == susp:
                    input  = group[degree]
                    print( "Susp: " + str(susp) + " "+ input.get_attribute("aria-label"))
                else:
                    input = group[0]
                    label = input.get_attribute("aria-label")
                wd.execute_script("arguments[0].scrollIntoView(true);", input )
                # 使用 JavaScript 点击元素
                wd.execute_script("arguments[0].click();", input )
                #print("Clicked " + str(cnt[0]))
                cnt[0] += 1
            except Exception as e:
                print(f"Error clicking the input element: {e}")

def once(susp,degree,cnt):
    try:
        wd.get("http://localhost:65256")  # 确保端口号正确
    except Exception as e:
        print(f"Failure: {e}")
    while True:
        # 初始点击输入框
        click_inputs(wd,susp,degree,cnt)
        next_buttons = wd.find_elements(By.XPATH, "//button[@aria-label='Go to next set of questions']")
        if next_buttons:  # 如果找到了 Next 按钮
            next_button = next_buttons[0]  # 取第一个找到的按钮
            next_button.click()  # 点击 Next 按钮
        else:
            #print("No Next button found. Exiting loop.")
            break

        # 等待并尝试点击 Next 按钮
    try:
        submit_button = wd.find_element(By.XPATH, "//button[@aria-label='Submit the test and see results.']")
        submit_button.click()  # 点击提交按钮
        print("Submitted")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")

    try:
        # 等待 traitbox__text 类的 div 元素可见
        trait_elements = WebDriverWait(wd, 4).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "traitbox__text"))
        )

        # 提取每个 traitbox__text 元素的信息
        values = []
        traits = []
        for element in trait_elements:
            # 获取 Nature 和值
            value = element.find_element(By.CLASS_NAME, "traitbox__value").text.strip()
            percentage, trait = value.split(" ", 1)
            traits.append(trait)
            # 存入字典中
            values.append(percentage)
        type = ""
        if  'I' in traits[0]:
            type += 'I'
        else:
            type += 'E'
        if  'S' in traits[1]:
            type += 'S'
        else:
            type += 'N'
        if  'T' in traits[2]:
            type += 'T'
        else:
            type += 'F'
        if  'J' in traits[3]:
            type += 'J'
        else:
            type += 'P'
        # 创建 DataFrame
        values.append(type)
        column_names = ["Energy", "Mind", "Nature", "Tactics", "Identity","Type"]
        new_row = pd.DataFrame([values], columns=column_names)
        file_path = "result3.xlsx"
        # 根据提取的结果填充 DataFrame
        try:
            existing_df = pd.read_excel(file_path, sheet_name='Sheet1')
            # 将新行追加到现有数据的底部
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            # 保存更新后的 DataFrame 到 Excel 文件
            with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer:
                updated_df.to_excel(writer, sheet_name='Sheet1', index=False)
        except FileNotFoundError:
            # 如果文件不存在，创建一个新文件
            new_row.to_excel(file_path, sheet_name='Sheet1', index=False)

    except Exception as e:
        print(f"Error occurred: {e}")

    # refresh web browser
    wd.quit()

if __name__ == "__main__":
    print(list(range(1, 7)))
    num = 1
    wd = webdriver.Chrome()
    wd.get('https://www.16personalities.com/free-personality-test')

    for m in list(range(1, 61)):
        for degree in list(range(2, 3)):
            cnt = [1]
            print(str(num) + " try " + "question:" +str(m) + " degree: " +str(degree) )
            num += 1
            once(m,degree,cnt)

    ## Tasks
    ## 1: individual check -- each question only contribute to one dimension

    ## 2: each question contribute equally
    ## 3: even different but the same

