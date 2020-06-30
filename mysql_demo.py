from pymysql import cursors,connect
#连接数据库
conn =connect(host='127.0.0.1',
              user='root',
              password='root',
              db='guest',
              charset='utf8mb4',
              cursorsclass=cursors.DictCursor)
try:
    with conn.cursor() as cursors:
        #创建嘉宾数据
        sql = 'insert into sign_guest (realname,pgone,email,sign,event_id,create_time) values ("tom",18800110002,"tom@mail.com",0,1,NOW());'
        cursors.execute(sql)
    #提交事务
    conn.commit()

    with conn.cursor() as cursor:
        #查询添加的嘉宾
        sql = "select realname,phone,email,aign from sign_gues where phone=%s"
        cursor.execute(sql,('18800110002',))
        result = cursor.fetchone()
        print(result)
finally:
    conn.close()

