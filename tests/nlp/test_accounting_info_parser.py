import pytest
from app.utils.nlp.accounting_info_parser import AccountingInfoParser

class TestAccountingInfoParser:
    @pytest.fixture(scope="class")
    def parser(self):
        """初始化AccountingInfoParser实例"""
        return AccountingInfoParser()
    
    def test_parser_initialization(self):
        """测试解析器初始化"""
        parser = AccountingInfoParser()
        assert parser is not None
        assert hasattr(parser, 'category_keywords')
        assert hasattr(parser, 'fuzzy_amount_patterns')
        assert hasattr(parser, 'time_period_mapping')
    
    @pytest.mark.parametrize("text,expected_valid,expected_category", [
        ("买咖啡花了30元", True, "餐饮"),
        ("昨天早上打车花了50元", True, "交通"),
        ("今天下午打车", False, "交通"),  # 缺少金额
        ("大概花了60元买零食", False, "餐饮"),  # 模糊金额
    ])
    def test_parse_cases(self, parser, text, expected_valid, expected_category):
        """测试解析器处理不同输入"""
        valid, result = parser.parse(text)
        assert valid == expected_valid
        if expected_category:
            if valid:
                assert result["category"] == expected_category
            else:
                # 即使无效，也应该能识别出分类
                assert result.get("category") == expected_category or "category" not in result
    
    def test_extract_amount(self, parser):
        """测试金额提取功能"""
        # 精确金额
        assert parser._extract_amount("花了30元") == 30.0
        assert parser._extract_amount("花费100块钱") == 100.0
        assert parser._extract_amount("支出50.5元") == 50.5
        
        # 模糊金额应该返回None
        assert parser._extract_amount("大概几十块钱") is None
        assert parser._extract_amount("大约花了100元") is None
    
    def test_extract_datetime(self, parser):
        """测试日期时间提取功能"""
        result = parser._extract_datetime("昨天早上打车花了50元")
        assert "20" in result and "-" in result and ":" in result
        
        result = parser._extract_datetime("今天18:30买衣服")
        assert ":30" in result
    
    def test_extract_category(self, parser):
        """测试分类提取功能"""
        assert parser._extract_category("买咖啡") == "餐饮"
        assert parser._extract_category("打车去机场") == "交通"
        assert parser._extract_category("买衣服") == "购物"
        assert parser._extract_category("看电影") == "娱乐"