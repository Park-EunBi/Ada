'''
Connect Database File
Edited by EunBi Park
8 Nov 2022
'''

import pymysql
import pandas as pd
# connect info (deleted)
conn = pymysql.connect(host='', user='', password='', db='scooter',charset='utf8', port=3306)
cur = conn.cursor(pymysql.cursors.DictCursor)

# all violations status
sql1 = '''SELECT * FROM violation'''
cur.execute(sql1)
result = cur.fetchall()
result = pd.DataFrame(result)

# users by number of violations
sql2 = '''select user_id, count(user_id) count from violation group by user_id order by count(user_id) desc;'''
cur.execute(sql2)
count_by_user = cur.fetchall()
count_by_user = pd.DataFrame(count_by_user)

# violations status by date
sql3 = '''SELECT DATE_FORMAT(time,'%Y-%m-%d') day, COUNT(*) count FROM violation GROUP BY day'''
cur.execute(sql3)
count_by_day = cur.fetchall()
count_by_day = pd.DataFrame(count_by_day)

# violations status by hour
sql4 = '''SELECT DATE_FORMAT(time,'%h') hour, COUNT(*) count FROM violation GROUP BY hour order by hour'''
cur.execute(sql4)
count_by_hour = cur.fetchall()
count_by_hour = pd.DataFrame(count_by_hour)

conn.close()

# make csv_files
# use absolute path in case of relative path error

# result_csv = result.to_csv('./csv_data/result.csv', index=False)
result_csv = result.to_csv(r'C:\pythonProject2\mydatabase\csv_data\result.csv', index=False)

# make csv file: users by number of violations
# count_by_user_csv = count_by_user.to_csv('./csv_data/count_by_user.csv', index=False, header = False)
count_by_user_csv = count_by_user.to_csv('C:\pythonProject2\mydatabase\csv_data\count_by_user.csv', index=False, header = False)

# make csv file: violations status by date
# count_by_day = count_by_day.to_csv('./csv_data/count_by_day.csv', index=False, header = False)
count_by_day = count_by_day.to_csv('C:\pythonProject2\mydatabase\csv_data\count_by_day.csv', index=False, header = False)

# make csv file: violations status by hour
# count_by_hour = count_by_hour.to_csv('./csv_data/count_by_hour.csv', index=False, header = False)
count_by_hour = count_by_hour.to_csv('C:\pythonProject2\mydatabase\csv_data\count_by_hour.csv', index=False, header = False)

# used for graph update
# my_data_analysis.make_graph()





