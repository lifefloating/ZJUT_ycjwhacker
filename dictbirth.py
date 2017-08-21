#!/usr/bin/env python3.5
# encoding:utf-8


year = ['1998', '1997', '1996', '1995', '1994', '1993', '98', '97', '96', '95', '94', '93']
mouth = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
       '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

dic = open("dictbirth.txt", "a")

for x in range(len(year)):
    for y in range(len(mouth)):
        for z in range(len(day)):
            birth = "".join(year[x])+"".join(mouth[y])+"".join(day[z])+'\n'
            dic.write(birth)
dic.close()
