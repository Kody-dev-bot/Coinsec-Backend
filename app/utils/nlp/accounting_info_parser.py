import re
import thulac
import datetime
from typing import Dict, Optional, Tuple, Union, List

# 预加载thulac模型
thu = thulac.thulac(seg_only=True)

class AccountingInfoParser:
    def __init__(self):
        # 消费类型关键词库
        self.category_keywords = {
            "餐饮": ["吃", "喝", "餐厅", "饭店", "外卖", "零食", "咖啡", "奶茶", "餐", "饭", "吃饭", "用餐"],
            "交通": ["公交", "地铁", "打车", "出租车", "火车", "高铁", "飞机", "油费", "停车", "出行", "乘车"],
            "购物": ["买", "购物", "衣服", "鞋子", "化妆品", "超市", "便利店", "商品", "购置", "服饰"],
            "住房": ["房租", "水电", "煤气", "物业", "网费", "住宿", "缴费"],
            "娱乐": ["电影", "游戏", "KTV", "旅游", "景点", "演唱会", "玩", "观影"],
            "医疗": ["医院", "药店", "看病", "买药", "医疗", "就诊"],
            "其他": []
        }
        
        # 模糊金额正则（拦截不明确的金额描述）
        self.fuzzy_amount_patterns = [
            r'[几]十[元块钱]',                  # 几十块、几十元
            r'[几]百[元块钱]',                  # 几百元、几百块
            r'[几]千[元块钱]',                  # 几千块
            r'大约.*?(\d+\.?\d*)[元块钱]',      # 大约花了30元
            r'大概.*?(\d+\.?\d*)[元块钱]',      # 大概50块
            r'差不多.*?(\d+\.?\d*)[元块钱]'    # 差不多20元
        ]
        
        # 模糊时间段默认时分映射
        self.time_period_mapping = {
            "早上": "08:00",
            "上午": "10:00",
            "中午": "12:00",
            "下午": "15:00",
            "晚上": "19:00",
            "夜里": "22:00"
        }

    def _extract_amount(self, text: str) -> Optional[float]:
        """提取精确金额，模糊金额返回None"""
        # 先检查是否为模糊金额
        for pattern in self.fuzzy_amount_patterns:
            if re.search(pattern, text):
                return None
        
        # 提取精确金额（数字+单位）
        amount_match = re.search(r'(\d+\.?\d*)[元块钱]', text)
        if amount_match:
            return float(amount_match.group(1))
        
        return None

    def _adjust_hour_by_period(self, hour: int, period: str) -> int:
        """根据时段（上午/下午）转换为24小时制小时"""
        if hour == 12:
            return 0 if period in ["上午", "早上"] else 12
        
        if period in ["下午", "晚上"] and hour < 12:
            return hour + 12
        
        return hour

    def _get_relative_date(self, text: str) -> Optional[str]:
        """处理相对日期（昨天/前天），返回YYYY-MM-DD或None"""
        today = datetime.date.today()
        if "昨天" in text:
            return (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif "前天" in text:
            return (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        return None

    def _extract_datetime(self, text: str) -> str:
        """提取完整日期时间，处理相对日期、绝对日期和时段"""
        today = datetime.date.today()
        now = datetime.datetime.now()
        default_date = today.strftime("%Y-%m-%d")
        default_time = now.strftime("%H:%M")

        # 1. 优先处理相对日期
        date_str = self._get_relative_date(text)
        if not date_str:
            # 2. 处理绝对日期（YYYY-MM-DD）
            iso_match = re.search(r'\d{4}-\d{2}-\d{2}', text)
            if iso_match:
                date_str = iso_match.group()
            else:
                # 3. 处理月日格式（MM月DD日）
                md_match = re.search(r'(\d+)月(\d+)日', text)
                if md_match:
                    month = int(md_match.group(1))
                    day = int(md_match.group(2))
                    if 1 <= month <= 12:  # 过滤无效月份
                        date_str = f"{today.year}-{month:02d}-{day:02d}"
                # 4. 若仍无匹配，使用默认日期
                if not date_str:
                    date_str = default_date

        # 提取时段（上午/下午/晚上）
        period = ""
        if "上午" in text:
            period = "上午"
        elif "下午" in text:
            period = "下午"
        elif "晚上" in text:
            period = "晚上"

        # 处理时间（时分）
        time_str = default_time
        
        # 匹配 10:30 格式
        time_match = re.search(r'(\d{1,2}):(\d{2})', text)
        if time_match:
            hour = self._adjust_hour_by_period(int(time_match.group(1)), period)
            time_str = f"{hour:02d}:{time_match.group(2)}"
        
        # 匹配 10点30分 格式
        else:
            time_match = re.search(r'(\d{1,2})点(\d{2})分', text)
            if time_match:
                hour = self._adjust_hour_by_period(int(time_match.group(1)), period)
                time_str = f"{hour:02d}:{time_match.group(2)}"
            
            # 匹配 10点半 格式
            else:
                time_match = re.search(r'(\d{1,2})点半', text)
                if time_match:
                    hour = self._adjust_hour_by_period(int(time_match.group(1)), period)
                    time_str = f"{hour:02d}:30"
                
                # 匹配 10点 格式
                else:
                    time_match = re.search(r'(\d{1,2})点', text)
                    if time_match:
                        hour = self._adjust_hour_by_period(int(time_match.group(1)), period)
                        time_str = f"{hour:02d}:00"
                    
                    # 匹配模糊时段（早上/中午等）
                    else:
                        for p, default_t in self.time_period_mapping.items():
                            if p in text:
                                time_str = default_t
                                break

        return f"{date_str} {time_str}"

    def _extract_category(self, text: str) -> Optional[str]:
        """基于关键词提取消费类型"""
        # 使用thulac进行分词
        words_result = thu.cut(text)
        words = [word[0] for word in words_result]
        for category, keywords in self.category_keywords.items():
            if any(keyword in words for keyword in keywords):
                return category
        return None

    def parse(self, text: str) -> Tuple[bool, Dict[str, Union[float, str, None, List[str]]]]:
        """解析入口：返回(是否有效, 结果字典)"""
        text = text.strip()
        if not text:
            return False, {"error": "输入不能为空", "missing": ["有效文本"]}
        
        # 提取核心信息
        amount = self._extract_amount(text)
        datetime_str = self._extract_datetime(text)
        category = self._extract_category(text)
        
        # 校验必选项
        missing: List[str] = []
        if amount is None:
            missing.append("金额（需明确具体数值，如30元，不能是几十块/大概50元）")
        if category is None:
            missing.append("消费类型（如餐饮、交通等）")
        
        # 返回结果
        if missing:
            return False, {
                "error": f"信息不完整，请补充：{', '.join(missing)}",
                "missing": missing,
                "original_text": text
            }
        
        return True, {
            "amount": amount,
            "datetime": datetime_str,
            "category": category,
            "original_text": text
        }

