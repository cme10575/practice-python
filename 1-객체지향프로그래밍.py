ItemList = ['A상품', 'B상품', 'C상품', 'D상품', 'E상품']

class User :
    def __init__(self, NAME, ID, PASS):
        self.name = NAME
        self.id = ID
        self.Pass = PASS
        self.BuyList = []
    def BuyItem(self):
        print("**********************")
        print(" [로그인]%s님 반갑습니다" % (self.name))
        print("**********************")
        for idx, item in enumerate(ItemList):
            print('%d : %s' % (idx, item))
        print("구매 :", end='')
        buying = int(input())
        if 0 <= buying and buying <= 4:
            self.BuyList.append(ItemList[buying])
        else:
            print("상품 없음")

    def CheckItemList(self):
        for item in self.BuyList:
            print(item)
    def ShowUser(self):
        print("[이름 : %s, 아이디 : %s, 비밀번호 : %s]" % (self.name, self.id, self.Pass))

class UserManager:
    def __init__(self):
        self.UserTable = []
        self.login_index = -1
        self.isLogin = False
        self.current_user = User('','','')
    def UserRegister(self):
        print("이름 : ", end="")
        NAME = input()
        print("아이디 : ", end="")
        ID = input()
        print("패스워드 : ", end="")
        PASS = input()
        print("패스워드 확인 : ", end="")
        PASS_CONFIRM = input()
        if PASS != PASS_CONFIRM:
            print("패스워드가 다릅니다")
            return
        user = User(NAME, ID, PASS)
        self.UserTable.append(user)
    def CheckUserList(self):
        for user in self.UserTable:
            user.ShowUser()
    def AfterLogin(self):
        while True:
            print("/****************/")
            print("     반갑습니다")
            print("/****************/")
            print("1. 장바구니 확인")
            print("2. 상품 장바구니에 넣기")
            print("3. 돌아가기")

            selection = int(input())
            if selection == 1:
                self.current_user.CheckItemList()
            elif selection == 2:
                self.current_user.BuyItem()
            else:
                return
    def UserLogin(self):
        print("아이디 :", end="")
        ID = input()
        print("비밀번호 :", end="")
        PASS = input()
        self.login_index = -1
        for idx, user in enumerate(self.UserTable):
            if ID == user.id and PASS == user.Pass:
                print("success")
                self.current_user = self.UserTable[idx]
                self.isLogin = True
                break
        if self.isLogin == False:
            print("실패")
        else:
            self.AfterLogin()

manager = UserManager()

def ProgramHome():
    while True:
        print("/*************************/")
        print("     쇼핑몰 프로그램")
        print("/*************************/")
        print("1. 회원 가입")
        print("2. 회원 리스트 확인")
        print("3. 회원 로그인")

        selection = int(input())
        if selection == 1:
            manager.UserRegister()
        elif selection == 2:
            manager.CheckUserList()
        elif selection == 3:
            manager.UserLogin()
        else:
            return

ProgramHome()
