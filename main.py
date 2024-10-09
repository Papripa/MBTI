import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
question_dict = {"I": [6,15,21,26,41,51],"E":[1,11,16,31,36,43,53]};

def click_inputs():

    wd.implicitly_wait(3)
    elements = wd.find_elements(By.TAG_NAME, "input")
    for i in range(0, len(elements), 7):
        group = elements[i:i + 7]  # 切片取出七个元素
        try:
            # 滚动到元素可见
            input = group[1]
            wd.execute_script("arguments[0].scrollIntoView(true);", input )
            # 使用 JavaScript 点击元素
            wd.execute_script("arguments[0].click();", input )
            print("Clicked " + input.get_attribute("aria-label"))
        except Exception as e:
            print(f"Error clicking the input element: {e}")


if __name__ == "__main__":
    wd = webdriver.Chrome()
    wd.get('https://www.16personalities.com/free-personality-test')
    i = 1
    while True:
        # 初始点击输入框
        click_inputs()
        next_buttons = wd.find_elements(By.XPATH, "//button[@aria-label='Go to next set of questions']")
        if next_buttons:  # 如果找到了 Next 按钮
            next_button = next_buttons[0]  # 取第一个找到的按钮
            next_button.click()  # 点击 Next 按钮
            print("Clicked the Next button.")
        else:
            print("No Next button found. Exiting loop.")
            break
        print("-----------------------------PAGE\n-----------------------------")

        # 等待并尝试点击 Next 按钮
    try:
        submit_button = wd.find_element(By.XPATH, "//button[@aria-label='Submit the test and see results.']")
        submit_button.click()  # 点击提交按钮
        print("Clicked the Submit button.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")

    try:
        # 等待 traitbox__text 类的 div 元素可见
        trait_elements = WebDriverWait(wd, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "traitbox__text"))
        )

        # 提取每个 traitbox__text 元素的信息
        values = []
        for element in trait_elements:
            # 获取 Nature 和值
            value = element.find_element(By.CLASS_NAME, "traitbox__value").text.strip()
            # 存入字典中
            values.append(value)

        # 创建 DataFrame

        column_names = ["Energy", "Mind", "Nature", "Tactics", "Identity"]
        new_row = pd.DataFrame([values], columns=column_names)
        # 根据提取的结果填充 DataFrame

        file_path = "result.xlsx"
        # 保存到 Excel 文件
        try:
            # 使用 append 模式打开文件
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

    # 关闭浏览器
    wd.quit()