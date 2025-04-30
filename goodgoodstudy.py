import os
import time
import traceback

all_words = {}


def standard(eng, chin):
    return f"{eng} --- {chin}"

def read_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = {}
        for line in f.readlines():
            if line.strip():
                single = line.strip().replace("---", '-')
            if single.count('-') == 1:
                eng, chin = single.split('-')
            else:
                eng, chin = special_split(single)
            eng = eng.lower().strip()
            chin = chin.strip()
            words[eng] = chin
    return words


def get_date_range(date_str):
    if ',' in date_str:
        data_range = [date.strip() for date in date_str.split(',')]
    else:
        data_range = date_str.split()
    if len(data_range) == 2 and data_range[0].split('.')[0] == data_range[1].split('.')[0]:
        month = data_range[0].split('.')[0]
        min_day = int(data_range[0].split('.')[1])
        max_day = int(data_range[1].split('.')[1])
        if min_day <= max_day:
            print(f"填写的日期为{data_range}，是相同月份下的两个日期，视作范围")
            res = []
            for day in range(min_day, max_day + 1):
                res.append(f"{month}.{day}")
            print(f"生成日期如下：{res}")
            return res
        else:
            print(f"填写的日期为{data_range}，第一个日期大于第二个，视作枚举")
            return [date.strip() for date in data_range]
    else:
        print(f"填写的日期为{data_range}，视作枚举")
        return [date.strip() for date in data_range]


def special_split(string, pattern='-'):
    """
    我是万万没想到单词里面也能有'-'的，是我浅薄无知了
    :return:
    """
    string = string[::-1]
    line = string.find(pattern)
    chin, eng = string[:line].strip()[::-1], string[line+1:].strip()[::-1]
    return eng, chin


def find_word_dict(eng):
    """
    查询单词的汉语意思
    :param eng:
    :return:
    """
    for every_day in all_words.values():
        if eng in every_day:
            return every_day[eng]
    else:
        return ''


def find_chinese_dict(chin):
    """
    找出所有包含单词近似中文意思的词
    :param chin:
    :return:
    """
    res_words = []
    for every_day in all_words.values():
        for eng, value in every_day.items():
            if chin in value:
                res_words.append(standard(eng, value))
    return res_words


def read_all_words(path):
    for txt in os.listdir(path):
        if txt.endswith('.txt'):
            now_file = os.path.join(path, txt)
            all_words[txt] = read_words(now_file)


def main():
    words_path = input("请输入词库所在路径（默认C:\\Users\\Administrator\\Desktop\\考研\\words）：")
    if not words_path.strip():
        words_path = "C:\\Users\\Administrator\\Desktop\\考研\\words"
    read_all_words(words_path)
    while True:
        ability = int(input(
            "请输入功能序号：\n背单词（1），\n写全拼（2），\n写中文（3），\n英文查中文（4），\n中文查英文（5），\n退出(-1)\n序号："
        ))
        if ability == -1:
            print("本日单词练习完成！5秒后退出")
            time.sleep(5)
            break
        aim_words = {}
        while ability in [1, 2, 3] and not aim_words:
            aim_date_str = input("请输入想重复的日期，用空格分隔多个日期。填写相同月份的两个日期视作范围，否则视作枚举）:")
            aim_date_list = get_date_range(aim_date_str)
            for aim_date in aim_date_list:
                if f"{aim_date}.txt" in all_words.keys():
                    aim_words.update(all_words[f"{aim_date}.txt"])
        if ability == 1:
            print("开始单词不间断循环播放，请手动关闭程序")
            while aim_words:
                for eng, chin in aim_words.items():
                    print(standard(eng, chin))
                    print()
                    time.sleep(5)
        elif ability == 2:
            count = 0
            while aim_words:
                set_error = set()
                aim_engs = list(set(aim_words.keys()))
                for eng in aim_engs:
                    chin = aim_words[eng]
                    value = input(f"{chin}\n请输入英文全拼：").lower()
                    while value != eng:
                        set_error.add(eng)
                        print(f"错误！这个单词的全拼是：{eng}，")
                        error_meaning = find_word_dict(value)
                        if error_meaning:
                            print(f"（你所输入单词的意思:\n{standard(value, error_meaning)}\n注意不要搞混了）")
                        print("写错了，重写一遍！")
                        value = input(f"{chin}\n请输入英文全拼：")
                    print("正确！请看下一题：")
                    print()
                aim_words = list(set(aim_words.keys()) & set_error)
                count += 1
                print(f"非常棒！您已经练习了【{count}】轮，错误的单词已经归档并乱序，请加油！")
            print("练习完成，请继续选择")
        elif ability == 3:
            count = 0
            while aim_words:
                set_error = set()
                aim_engs = list(set(aim_words.keys()))
                for eng in aim_engs:
                    chin = aim_words[eng]
                    value = input(f"{eng}\n请输入中文含义：")
                    while not (value and value in chin.strip()):
                        set_error.add(eng)
                        print(f"错误！这个单词的意思是：{chin}，请看下一题：")
                        value = input(f"{eng}\n请输入中文含义：")
                    print(f"正确！这个单词的意思是：{chin}, 请看下一题：")
                aim_words = list(set(aim_words.keys()) & set_error)
                count += 1
                print(f"非常棒！您已经练习了【{count}】轮，错误的单词已经归档并乱序，请加油！")
            print("练习完成，请继续选择")
        elif ability == 4:
            eng = input("请输入单词的英语全拼，输入-1返回：").strip()
            while eng != '-1':
                meaning = find_word_dict(eng)
                if meaning:
                    print(standard(eng, meaning))
                else:
                    print("当前词库中不存在该单词。")
                eng = input("请输入单词的英语全拼，输入-1返回：").strip()
            print("查询完成，请继续选择")
        elif ability == 5:
            chin = input("请输入单词的汉语意思，输入-1返回：").strip()
            while chin != '-1':
                similar_words = find_chinese_dict(chin)
                if similar_words:
                    for item in similar_words:
                        print(item)
                else:
                    print("当前词库中不存在该汉语意思的单词。")
                print()
                chin = input("请输入单词的汉语意思，输入-1返回：")
            print("查询完成，请继续选择")
        else:
            print("输入无法识别，请重新输入")


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        traceback.print_exc()
        print(f"报错：{ex},20秒后退出程序")
        time.sleep(20)
