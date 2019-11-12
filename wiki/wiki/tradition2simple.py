# coding:utf-8
import zhconv

# 繁体转简体


if __name__ == '__main__':
    print('主程序执行开始...')

    input_file_name = 'nodes.csv'
    output_file_name = 'nodes_new.csv'
    input_file = open(input_file_name, 'r', encoding='utf-8')
    output_file = open(output_file_name, 'w', encoding='utf-8')

    print('开始读入繁体文件...')
    lines = input_file.readlines()
    print('读入繁体文件结束！')

    print('转换程序执行开始...')
    count = 1
    for line in lines:
        output_file.write(zhconv.convert(line, 'zh-hans'))
        count += 1
        if count % 10000 == 0:
            print('目前已转换%d条数据' % count)
    print('转换程序执行结束！')

    print('主程序执行结束！')
