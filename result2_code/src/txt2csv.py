
fr = open('../data/result6.txt', 'r')
fw = open('../data/result6.csv', 'w')
for line in fr.readlines():
    for data in line.strip().split(' '):
        print(data)
        fw.write(data+',')
    fw.write('\n')
fr.close()
fw.close()