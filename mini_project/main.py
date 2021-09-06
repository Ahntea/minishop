import os
import datetime
import sqlite3
from product import Product

## 주문일자 regdate 입력을 위한 시간값 생성
now = datetime.datetime.now()
nowDatetime = now.strftime("%Y-%m-%d %H:%M:%S")

print("메뉴 로딩중...")

# DB 접속 및 테이블 생성
#file_path = "./myenv/mini_project/database.db"
file_path = "C:/Users/user/bytedgree/myenv/mini_project/database.db"
conn= sqlite3.connect(file_path, isolation_level=None)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY, product_name text,price INTEGER, remains INTEGER, regdate text)")
c.execute("CREATE TABLE IF NOT EXISTS orders(order_number INTEGER PRIMARY KEY, product_name text, price INTEGER, count INTEGER, regdate text)")

# 테스트 활용을 위한 기본 데이터
default_product = (
    (1, 'apple', 1000, 100,nowDatetime),
    (2, 'banana', 2000, 150,nowDatetime),
    (3, 'tomato', 3000, 300,nowDatetime),
)

default_orders = (
    (1, 'banana', 2000, 20, nowDatetime),
    (2, 'tomato', 3000, 30, nowDatetime),
)

#c.executemany("INSERT INTO products(id , product_name ,price, remains ,regdate) Values (?,?,?,?,?)", default_product)
#c.executemany("INSERT INTO orders(order_number, product_name, price, count, regdate) Values (?,?,?,?,?)", default_orders)

# Product 객체를 담을 List
product_list = []
c.execute("SELECT * FROM products")
for row in c:
    product = Product(row[0],row[1],row[2],row[3],row[4])
    product_list.append(product)

# 주문을 받는 함수
def insert_order(product_name, count):
    c.execute("SELECT count(*) FROM ORDERS")
    order_num = int(c.fetchone()[0]) + 1
    c.execute("SELECT price,id,remains FROM products WHERE product_name=?",(product_name,))
    price,id_,remains = c.fetchone()
    order_var = (order_num, product_name, price, int(count), nowDatetime)

    if int(remains) >= int(count): 
        selected_product = product_list[id_-1]
        selected_product.order(int(count))
        c.execute("UPDATE products SET remains = ? WHERE id=?",(selected_product.get_remains(),id_))
        c.execute("INSERT INTO orders(order_number, product_name, price, count, regdate) VALUES (?,?,?,?,?)", order_var)
        print("주문이 완료되었습니다.\n")
    else:
        print("수량이 부족합니다.")

# 상품 목록을 보여주는 함수
def show_product():
    print("상품목록")
    c.execute("SELECT * FROM products")
    for row in c:
        print(row)

    while True:
        try:
            code = int(input("주문을 원하시는 상품 번호를 입력하세요(메뉴로 돌아가시려면 -1)"))
            if code in range(1,len(product_list)+1):
                print("주문페이지로 이동 합니다.\n")
            elif code == -1:
                break
            else:
                print("상품정보를 다시 확인하세요\n")
                continue
        except Exception:
            print("올바른 값을 입력하세요")

        selected_product = product_list[code -1].get_product_name()
        print(f"------상품 {selected_product}을 주문합니다.-----\n")
        try:
            count = int(input("주문수량을 입력하세요\n"))
            if count <=1 :
                raise Exception
        except Exception:
            print("올바른 값을 입력하세요")    
        else:
            insert_order(selected_product, count)
            
# 주문 목록을 보여주는 함수
def show_orders():
    print("주문 목록")
    c.execute("SELECT * FROM orders")
    for order in c:
        print(order)

# 머드 쇼핑몰 메뉴 구현
while True:
    print(
    """
    - mini shopping -
    - 메뉴를 선택해 주세요 -
    1. 상품 목록
    2. 주문 목록 확인
    3. 프로그램 종료
    """
    )
    a = input("선택: ")
    try:
        if a not in ["1","2","3"]:
            raise Exception
            
    except:
        print("올바른 번호를 입력하세요")

    else:       
        if a == "1":
            show_product()
        elif a == "2":
            show_orders()
        elif a == "3":
            c.close()
            print("프로그램 종료합니다.")
            break



