
if __name__ == '__main__':
    print('主程序执行开始...')

    input_file_name = 'nodes_new.csv'
    output_file_name = 'nodes_new_new.csv'
    input_file = open(input_file_name, 'r', encoding='utf-8')
    output_file = open(output_file_name, 'w', encoding='utf-8')
    index = 0
    for line in input_file.readlines():
        index += 1
        if line.count(',') > 2:
            print(index)

    # print('开始读入繁体文件...')
    # lines = input_file.readlines()
    # print('读入繁体文件结束！')
    #
    # print('转换程序执行开始...')
    # str = "是覅违法,sfjie,feag,grag,label"
    # str_list = str.split(",")
    # print(str_list)
    # print(str_list[0],str_list[-1])
    # print(str_list[1:len(str) - 2])
    #
    #
    # # count = 1
    # # for line in lines:
    # #     str = line.split(",")
    # #     for s in range(2,len(str)):
    # #         result = ""
    # #         result = result.join(".").join(str[s])
    # #     output_file.write(str[0]+"," + str[1] + "," + result)
    # #     count += 1
    # #     if count % 10000 == 0:
    # #         print('目前已转换%d条数据' % count)
    # print('转换程序执行结束！')
    #
    # print('主程序执行结束！')
