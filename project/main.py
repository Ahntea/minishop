import os
import csv
from project.post import Post
file_path = "./myenv/project/data.csv"
post_list = []

if os.path.exists(file_path):
    print("게시글 로딩중...")
    f = open(file_path, "r", encoding="utf8")
    reader = csv.reader(f)
    for i in reader:
        data = Post(int(i[0]),i[1],i[2],int(i[3]))
        post_list.append(data)
else:
    f = open(file_path, "w", encoding="utf8", newline="")
    f.close

#게시글 쓰기
def write_post():
    """게시글 쓰기 함수"""
    print("\n\n- 게시글 쓰기")
    title = input("제목을 입력해주세요\n")
    content = input("내용을 입력해주세요\n")
    if post_list == []:
        post = Post(1, title, content, 0)
        post_list.append(post)
    else:
        post = Post(post_list[-1].get_id() + 1, title, content, 0)
        post_list.append(post)
    print("게시글이 정상적으로 등록되었습니다.\n")

def view_list():
    id_list = []
    for i in post_list:
        print(f"번호 : {i.get_id()}, 제목 : {i.get_title()}, 조회수 : {i.get_view_count()}\n")
        id_list.append(i.get_id())
    while True:
        try :
            number = int(input("원하는 게시글을 입력하세요 (메뉴로 돌아가려면 -1)\n"))
            if number in id_list:
                view_post(number)
            elif number == -1:
                print("메뉴로 돌아갑니다.")
                break
            else:
                print("해당하는 글목록이 없습니다. 다시선택하세요")
        except ValueError:
            print("잘못된 값을 입력하셨습니다.")

def view_post(number):
    """게시글 불러오기 함수"""
    for post in post_list:
        if post.get_id() == number:
            post.add_view_count()
            print("번호 : ",post.get_id())
            print("제목 : ",post.get_title()) 
            print("본문 : ",post.get_content())
            print("조회수 : ",post.get_view_count())
            target_post = post

    while True:        
        try:
            select = int(input("Q) 수정: 1 삭제: 2 (메뉴로 돌아가려면 -1)"))
            if select == 1:
                print("\n\n- 게시글 수정하기")
                update_post(target_post)
                
            elif select == 2:
                delete_post(target_post)
                print("게시글이 삭제되었습니다.")
                break
            elif select == -1:
                break
            else :
                print("잘못된 번호입니다.")
        except Exception:
            print("잘못된 입력입니다.")

def update_post(target_post):
    id = target_post.get_id()
    title = input("제목을 입력해주세요\n")
    content = input("내용을 입력해주세요\n")
    view_count = target_post.get_view_count()
    target_post.set_post(id,title,content,view_count)


def save_file():
    """게시글 저장하는 함수"""
    f = open(file_path, "w", newline="", encoding="utf8")
    writer = csv.writer(f)
    for post in post_list:
        row = [post.get_id(), post.get_title(), post.get_content(),post.get_view_count()]
        writer.writerow(row)
    f.close()


def delete_post(target_post):
    post_list.remove(target_post)
    
while True:
    print(
    """
    - FASTCAMPUS BLOG -
    - 메뉴를 선택해 주세요 -
    1. 게시글 쓰기
    2. 게시글 목록
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
            write_post()
        elif a == "2":
            print("게시글 목록")
            view_list()
        elif a == "3":
            save_file()
            print("프로그램 종료합니다.")
            break

