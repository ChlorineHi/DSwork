import json

# 测试元组作为键的问题
def test_tuple_keys():
    # 这会导致错误
    bad_dict = {
        ("午门", "太和殿"): "从午门出发，沿着中轴线向北步行约10分钟即可到达太和殿。",
        ("太和殿", "乾清宫"): "从太和殿出发，穿过中和殿、保和殿，继续向北步行约5分钟即可到达乾清宫。"
    }
    
    try:
        json_str = json.dumps(bad_dict)
        print("成功序列化（意外）:", json_str)
    except Exception as e:
        print("预期的错误:", str(e))
    
    # 正确的方式
    good_dict = {
        "午门_太和殿": "从午门出发，沿着中轴线向北步行约10分钟即可到达太和殿。",
        "太和殿_乾清宫": "从太和殿出发，穿过中和殿、保和殿，继续向北步行约5分钟即可到达乾清宫。"
    }
    
    try:
        json_str = json.dumps(good_dict)
        print("成功序列化:", json_str)
    except Exception as e:
        print("意外错误:", str(e))

if __name__ == "__main__":
    test_tuple_keys() 