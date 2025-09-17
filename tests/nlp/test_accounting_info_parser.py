import sys
import os

# 添加项目根目录到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.utils.nlp.accounting_info_parser import AccountingInfoParser

if __name__ == "__main__":
    import time
    
    # 初始化并测试
    start_total = time.time()
    parser = AccountingInfoParser()
    load_time = time.time() - start_total
    print(f"模型加载耗时: {load_time:.6f}秒\n")
    
    # 测试用例
    test_cases = [
        "买咖啡花了30元",
        "昨天早上打车花了50元",
        "10月1日下午3点吃饭花了80元",
        "前天晚上8点看电影花了120元",
        "今天18:30买衣服花了200元",
        "大概花了60元买零食",
        "今天下午打车"
    ]
    
    for i, case in enumerate(test_cases, 1):
        start = time.time()
        valid, result = parser.parse(case)
        cost = time.time() - start
        print(f"用例{i}: {case}")
        print(f"有效: {valid}, 结果: {result}")
        print(f"耗时: {cost:.6f}秒\n")
    
    total_cost = time.time() - start_total
    print(f"总耗时: {total_cost:.6f}秒")