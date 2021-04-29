# import os
# from selenium.webdriver import Chrome, ChromeOptions
from selenium import  webdriver
import time
import pandas as pd

# 課題７　ログファイル出力　まだ良く分かっていませんので、引き続き調べます。
import logging
logging.basicConfig(filename="app.log",level=logging.WARNING)
logging.debug('debug')
logging.info('info')
logging.warning('warnig')
logging.error('error')
logging.critical('critical')

def main():
        # 課題４　キーワードをコンソールから入力
    search_keyword = input("検索キーワードを入力してください >>> ")
        # search_keyword = "高収入"
    driver = webdriver.Chrome()
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

        # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
        # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()


    exp_only_name_list = []
    exp_status_list = []
    exp_condition_list = []

        # 課題６　エラー処理
    try:
        # 課題３　全ページの情報を取得（
        while True:

            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

                #課題１　キャッチコピーを除いた会社名のみを表示
            for name in name_list:
                only_name = name.text
                exp_only_name_list.append(only_name.split('|')[0])

                # 課題２　正社員・契約社員　情報取得   
            status_list = driver.find_elements_by_class_name("cassetteRecruit__copy")

            for status_label in status_list:
                status = status_label.find_element_by_class_name("labelEmploymentStatus")
                exp_status_list.append(status.text)

                #課題２　初年度年収/給与　情報取得 "cassetteRecruit__main"の属性が"cassetteRecruit__mainM" と入力されている場合があり、データが取得できない場合が発生するので、検索ワードをランダムに変更する場合は、情報取得を見送りました。  
            # condition_list = driver.find_elements_by_class_name("cassetteRecruit__main")

            # for condition_body in condition_list:
            #     conditions = condition_body.find_elements_by_class_name("tableCondition__body")
            #     conditions.reverse()
            #     exp_condition_list.append(conditions[0].text)

            try:
                next_button = driver.find_element_by_css_selector("a.iconFont--arrowLeft").get_attribute("href")
                driver.get(next_button)
                time.sleep(1)
            except Exception:
            #     driver.quit()
                break

            # 課題５　csvファイルに出力
            # 課題６　エラー処理

        df = pd.DataFrame()
        df['会社名'] = exp_only_name_list
        df['雇用形態'] = exp_status_list
        # df['年収/給与'] = exp_condition_list

        df.to_csv('table_totals.csv')
        df.to_csv('table_totals2.csv',index=False)
    except:
        pass

if __name__ == "__main__":
    main()