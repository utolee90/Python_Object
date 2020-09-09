import numpy as np #numpy 사용

class Omok:
    def __init__(self, _num, _list_black =[], _list_white = [], _game='gomoku'):
        self.num = _num #숫자. 바둑판 크기
        self.list_black = _list_black # 흑돌 배치, 튜플 형태로 저장
        self.list_white = _list_white # 백돌 배치, 튜플 형태로 저장
        self.bw_turn = '흑' # 초기값은 흑이 먼저 두기
        self.dict_list = {'흑': self.list_black , '백' : self.list_white }
        self.win_lose = 'n' # 흑백 승패 변수
        self.game = _game #게임 종류
    
    def count_stone(self): #돌의 갯수 확인
        cnt = len(self.list_black+self.list_white)
        return cnt

    def take_turn(self): #흑백 바꾸기
        self.bw_turn = '백' if self.bw_turn == '흑' else '흑'
    
    def place_stone(self, _tup): #tup 입력하면 리스트 추가
        res = False #놓는지 확인
        _num=  self.num
        _dict = self.dict_list
        _bw = self.bw_turn
        if _tup not in _dict['흑']+_dict['백']: #이미 둔 곳은 두지 않기
            if _tup[0]<=_num and _tup[0]>=1 and _tup[1]<=_num and _tup[1] >=1: #보드판 안에 있을 때
                _dict[_bw].append(_tup)
                res = True #배열 성공!
            elif _tup[0] == 0 and _tup [1] <=0 and len(self.list_black)>0 and len(self.list_white)>0: 
                #이미 알 둔 상태에서 강제로 알 하나씩 제거
                _dict['흑'].pop(-1)
                _dict['백'].pop(-1)
                res = True
            elif _tup[0] == 0 and _tup [1] >0: #Pass
                res = True
            elif _tup[0]>_num: #give up
                res = True
        
        return res #작업 수행시 True, 작업 미수행시 False 출력

    def empty(self, _row, _col): #빈 오목판을 위해 문자 입력
        _num = self.num
        
        if _row == 1 and _col == 1: return '┌ ' #왼쪽 위
        elif _row == 1 and _col == _num: return '┐ ' #오른쪽 위
        elif _row == _num and _col == 1: return '└ ' #왼쪽 아래
        elif _row == _num and _col == _num: return '┘ '  #오른쪽 아래
        elif _row == 1: return '┬ ' #맨 윗줄
        elif _row == _num: return '┴ ' #맨 아랫줄
        elif _col == 1: return '├ ' #맨 왼쪽
        elif _col == _num: return '┤ ' #맨 오른쪽
        else: return '┼ ' #한가운데

    def showmatrix(self): #matrix 형태로
        _num = self.num
        mat_stone = np.zeros((_num,_num), dtype=np.int16) #정수 행렬
        for _tup in self.list_black: #흑 배치
            mat_stone[_tup[0]-1, _tup[1]-1] =1
        for _tup in self.list_white: #백 배치
            mat_stone[_tup[0]-1, _tup[1]-1] = -1

        return mat_stone   

    def show(self): #보여주기
        _num = self.num
        res='' #빈 텍스트 두 칸 출력.
        lab = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J '
        , 'K ', 'L ', 'M ', 'N ', 'O ', 'P ', 'Q ', 'R ', 'S ', 'T ', 'U ', 'V ', 'W ', 'X ', 'Y ', 'Z '] #라벨 붙이기
        for i in range(0, _num+1):
            for j in range(0, _num+1):
                if (i,j) == (0,0): res +='  '
                elif i == 0 : res +=lab[j-1]
                elif j == 0 : res +=lab[i-1]
                else :
                    if (i,j) in self.list_black:
                        res += '● '
                    elif (i,j) in self.list_white:
                        res += '○ '
                    else:
                        res += self.empty(i,j)
            res +='\n'
        return res
    
    def five_row(self): #list에서 오목 여부 확인
        _num = self.num
        res = ['n', []] #아무것도 없음
        mat_stone = self.showmatrix() #정수 행렬

        for i in range(1,_num+1):
            if res[0] !='n':
                break
            else:
                for j in range(1, _num-3): 
                    if np.sum(mat_stone[i-1,j-1:j+4]) == 5: #세로로 5개 일치
                        res = ['흑', [(i,k) for k in range(j, j+5)]]
                        break
                    elif np.sum(mat_stone[i-1,j-1:j+4]) ==-5: #세로로 백 일치
                        res = ['백', [(i,k) for k in range(j, j+5)]]
                        break
        for i in range(1,_num-3):
            if res[0] !='n':
                break
            else: 
                for j in range(1, _num+1): 
                    if np.sum(mat_stone[i-1:i+4, j-1]) == 5: #가로로 흑 5개 일치
                        res = ['흑', [(k,j) for k in range(i, i+5)]]
                        break
                    elif np.sum(mat_stone[i-1:i+4, j-1]) == -5: #가로로 5개 일치
                        res = ['백', [(k,j) for k in range(i, i+5)]]
                        break
        for i in range(1, _num-3):
            if res[0] != 'n':
                break
            else:
                for j in range(1, _num-3):
                    if sum([mat_stone[i+k-1, j+k-1] for k in range(5)]) == 5: #우하강 대각선 5개 일치
                        res = ['흑', [(i+k, j+k) for k in range(5)]]
                        break
                    elif sum([mat_stone[i+k-1, j+k-1] for k in range(5)]) == -5: #우하강 대각선 5개 일치
                        res = ['백', [(i+k, j+k) for k in range(5)]]
                        break
        for i in range(5,_num+1):
            if res[0] != 'n':
                break
            else:
                for j in range(1, _num-3): 
                    if sum([mat_stone[i-k-1,j+k-1] for k in range(5)]) == 5: #좌하강 대각선 5개 일치
                        res = ['흑', [(i-k, j+k) for k in range(5)]]
                        break
                    elif sum([mat_stone[i-k-1,j+k-1] for k in range(5)]) == -5: #좌하강 대각선 5개 일치
                        res = ['백', [(i-k, j+k) for k in range(5)]]
                        break
        
        return res
        
    def sixinrow(self): #흑 육목 금지
        res = False
        mat_stone = self.showmatrix()
        if self.five_row()[0] == '흑': #흑에서
            row1 = self.five_row()[1]
            row_diff = np.array(row1[4])-np.array(row1[0])

            if row_diff.tolist() == [0,4] and mat_stone[row1[4][0]-1, row1[4][1]] == 1:
                res = True
            elif row_diff.tolist() == [4,0] and mat_stone[row1[4][0], row1[4][1]-1] == 1 :
                res = True
            elif row_diff.tolist() == [4,4] and mat_stone[row1[4][0], row1[4][1]] == 1 :
                res = True
            elif row_diff.tolist() == [-4,4] and mat_stone[row1[4][0]-2, row1[4][1]] == 1 :
                res = True
        
        if res == True:
            msg = '육목 금지!'
            return ['백' , msg]
        else:
            return ['n', '']
    
    def fourcheck(self): #4-in-row 배열
        _num= self.num
        res_black_1 = [] #세로
        res_black_2 = [] #가로
        res_black_3 = [] #대각선1
        res_black_4 = [] #대각선2
        mat_stone = self.showmatrix()
        
        for i in range(1,_num+1):
            for j in range(1, _num-3): 
                if mat_stone[i-1, j-1] == 1 and np.sum(mat_stone[i-1,j-1:j+4]) == 4: #가로로 흑 4개
                    res_black_1.append([(i, j+k) for k in range(5)])
                elif mat_stone[i-1, j-1] == 0 and np.sum(mat_stone[i-1,j:j+4]) == 4 and (j==_num-4 or mat_stone[i-1, j+4]==-1): #빈칸 + 4개 연속일 때
                    res_black_1.append([(i, j+k) for k in range(5)])
        for i in range(1,_num-3):
            for j in range(1, _num+1): 
                if mat_stone[i-1, j-1]==1 and np.sum(mat_stone[i-1:i+4, j-1]) == 4: #세로로 흑 4개 일치
                    res_black_2.append([(i+k, j) for k in range(5)])
                elif mat_stone[i-1, j-1] == 0 and np.sum(mat_stone[i:i+4,j-1]) == 4 and (i==_num-4 or mat_stone[i+4, j-1]==-1): #빈칸 + 4개 연속일 때
                    res_black_2.append([(i+k, j) for k in range(5)])
        for i in range(1, _num-3):
            for j in range(1, _num-3):
                if mat_stone[i-1, j-1] == 1 and sum([mat_stone[i+k-1, j+k-1] for k in range(5)]) == 4: #우하강 대각선 4개 일치
                    res_black_3.append([(i+k, j+k) for k in range(5)])
                elif mat_stone[i-1, j-1] == 0 and sum([mat_stone[i+k, j+k] for k in range(4)]) == 4 and (i==_num-4 or j==_num-4 or mat_stone[i+4, j+4] == -1):
                    res_black_3.append([(i+k, j+k) for k in range(5)])
        for i in range(5,_num+1):
            for j in range(1, _num-3): 
                if mat_stone[i-1, j-1] == 1 and sum([mat_stone[i-k-1,j+k-1] for k in range(5)]) == 4: #좌하강 대각선 4개 일치
                    res_black_4.append([(i-k, j+k) for k in range(5)])
                elif mat_stone[i-1, j-1] == 0 and sum([mat_stone[i-k-2,j+k] for k in range(4)]) == 4 and (i==5 or j==_num-4 or mat_stone[i-6, j+4] == -1):
                    res_black_4.append([(i-k, j+k) for k in range(5)])
                
        return [res_black_1 , res_black_2, res_black_3, res_black_4]
    
    def doublefour(self): #44 금수조건 찾기
        res = ['n' , '']
        _num = self.num
        res_black_set=self.fourcheck()
        for i in res_black_set[0]:
            if res[0] == 'n':
                for j in res_black_set[1]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 44 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[0]:
            if res[0] == 'n':
                for j in res_black_set[2]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 44 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[0]:
            if res[0] == 'n':
                for j in res_black_set[3]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 44 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[1]:
            if res[0] == 'n':
                for j in res_black_set[2]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 44 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[1]:
            if res[0] == 'n':
                for j in res_black_set[3]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 44 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[2]:
            if res[0] == 'n':
                for j in res_black_set[3]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 44 걸림.'
                        res = ['백', msg]
                        break
        
        return res
    
    def threecheck(self): #33 금수조건 찾기
        _num= self.num
        res_black_1 = []
        res_black_2 = []
        res_black_3 = []
        res_black_4 = []
        mat_stone = self.showmatrix()
        for i in range(1,_num+1):
            for j in range(1, _num-4): 
                if mat_stone[i-1, j-1] == 0 and mat_stone[i-1,j] == 1 and np.sum(mat_stone[i-1,j:j+4]) == 3 and mat_stone[i-1, j+4] == 0: #세로로 흑 4개
                    res_black_1.append([(i, j+k) for k in range(1,5)])
        for i in range(1,_num-4):
            for j in range(1, _num+1): 
                if mat_stone[i-1, j-1]== 0 and mat_stone[i, j-1] == 1 and np.sum(mat_stone[i:i+4, j-1]) == 3 and mat_stone[i+4, j-1] == 0: #가로로 흑 5개 일치
                    res_black_2.append([(i+k, j) for k in range(1,5)])
        for i in range(1, _num-4):
            for j in range(1, _num-4):
                if mat_stone[i-1, j-1] == 0 and mat_stone[i,j] == 1 and sum([mat_stone[i+k, j+k] for k in range(4)]) == 3 and mat_stone[i+4, j+4]==0: #우하강 대각선 5개 일치
                    res_black_3.append([(i+k, j+k) for k in range(1,5)])
        for i in range(6,_num+1):
            for j in range(1, _num-4): 
                if mat_stone[i-1, j-1] == 0 and mat_stone[i-2, j] == 1 and sum([mat_stone[i-k-1,j+k-1] for k in range(1,5)]) == 3 and mat_stone[i-5, j+3] ==0 : #좌하강 대각선 5개 일치
                    res_black_4.append([(i-k, j+k) for k in range(1,5)])
        
        return [res_black_1 , res_black_2, res_black_3, res_black_4]

    def doublethree(self):
        res = ['n', '']
        _num = self.num
        res_black_set = self.threecheck()
        for i in res_black_set[0]:
            if res[0] == 'n':
                for j in res_black_set[1]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 33 걸림.'
                        res = ['백', msg]
                        break

        for i in res_black_set[0]:
            if res[0] == 'n':
                for j in res_black_set[2]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 33 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[0]:
            if res[0] == 'n':
                for j in res_black_set[3]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 33 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[1]:
            if res[0] == 'n':
                for j in res_black_set[2]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 33 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[1]:
            if res[0] == 'n':
                for j in res_black_set[3]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 33 걸림.'
                        res = ['백', msg]
                        break
        for i in res_black_set[2]:
            if res[0] == 'n':
                for j in res_black_set[3]:
                    if len(set(i).intersection(set(j))) !=0: #교집합이 있음.
                        msg = '흑 33 걸림.'
                        res = ['백', msg]
                        break

        return res

    def winloss(self, _var='n'): #승패 결정
        isprohibit= False #처음에는 금수 안 걸림.
        res = _var #흑백 강제 승패 결정
        if res != '흑' and res != '백' and self.game == 'renju':
            list_prohibit = [self.sixinrow()[0], self.doublefour()[0], self.doublethree()[0] ]
            list_prohibit2 = [self.sixinrow(), self.doublefour(), self.doublethree()]
            for num, res1 in enumerate(list_prohibit):
                if res1 == '백':
                    print(list_prohibit2[num][1])
                    res = '백'
                    isprohibit = True

        if isprohibit == False and _var == 'n':
            res = self.five_row()[0] #흑백 승패 

        self.win_lose = res
    
    def do_omok(self): #알 두는 장면. 승패 결정
        isplaced = False # 일단 
        while isplaced == False and self.win_lose == 'n': #알을 확실히 둘 때까지만 
            msg = '{0}번째 오목 알({1} 차례)을 놓을 곳 : [행수 열수]로 입력 :'
            if self.count_stone()>0:
                msg +='\n0 0으로 입력하면 한 수 무를 수 있음. 0 1로 입력하면 건너뛰기.\n게임 포기하고 싶으면 앞 숫자에 큰 수 입력. :' 
            x = input(msg.format(self.count_stone()+1, self.bw_turn))
                
            lx = x.split(' ') #리스트 분석
            tx = []
            for i in lx:
                try:
                    tx.append(int(i))
                except:
                    pass
            tx = tuple(tx)
            print(tx)
            if len(tx)>=2: #길이 2 이상일때만 검사
                try:
                    if int(lx[0])>0 and int(lx[0])<=self.num: #00에서 nn까지 - 직접 바둑판에 배치할 때
                        isplaced = self.place_stone(tx)
                        if isplaced == True:
                            self.take_turn()
                            print('({0},{1})에 알 배치 중'.format(lx[0], lx[1]))
                            y = input('상황 보기? [y]/n :')
                            if y.upper() in ['N', 'NO']:
                                pass
                            else:
                                print(self.show())
                            if self.game == 'renju':
                                z = input('흑 금수 체크? y/[n] : ')
                                if z.upper() in ['Y', 'YES']:
                                    print('33체크 (가로) : ', board.threecheck()[0])
                                    print('33체크 (세로) : ', board.threecheck()[1])
                                    print('33체크 (우하향) : ', board.threecheck()[2])
                                    print('33체크 (좌하향) : ', board.threecheck()[3])
                                    print('44체크 (가로) : ', board.fourcheck()[0])
                                    print('44체크 (세로) : ', board.fourcheck()[1])
                                    print('44체크 (우하향) : ', board.fourcheck()[2])
                                    print('44체크 (좌하향) : ', board.fourcheck()[3])
                                else:
                                    pass
                                
                            
                    elif int(lx[0])==0 and int(lx[1])==0: #int(lx[0])<=0 and int(lx[1])<0 - 수를 무를 때 사용
                        isplaced = self.place_stone(tx)
                        if isplaced == True:
                            print('알 하나씩 무르는 중')
                            y = input('상황 보기? [y]/n')
                            if y.upper() in ['N', 'NO']:
                                pass
                            else:
                                print(self.show())
                    
                    elif int(lx[0])==0 and int(lx[1])>0: #패스!
                        isplaced=self.place_stone(tx)
                        if isplaced == True:
                            print('{0} 패스!'.format(self.bw_turn))
                            self.take_turn()
                            y = input('상황 보기? [y]/n')
                            if y.upper() in ['N', 'NO']:
                                pass
                            else:
                                print(self.show())

                            
                    else: #int (ln[0])>num - 포기 선언할 때 사용
                        isplaced = self.place_stone(tx)
                        if isplaced == True:
                            print('{0} 포기했음'.format(self.bw_turn))
                            if self.bw_turn == '백':#흑턴 
                                self.win_lose = '흑'
                                break
                            else:
                                self.win_lose = '백'
                                break

                except:
                    pass
        

print('오목 두기')
n = 0
while n<=6 or n>36: # 7 이상 36 이하
    try:
        n = int(input('오목판 사이즈 (7~36까지): '))
    except:
        pass
x ='0'
while x not in ['1','2']: #게임 종류 결정.
    x = input('게임 종류 결정 (1. 고모쿠, 2.렌주) : ')

if x == '1':
    board = Omok(n) #고모쿠 룰로 오목판 생성
elif x == '2':
    board = Omok(n, _game='renju')

board.winloss('n')


while board.win_lose == 'n' and board.count_stone()<n**2: #흑백 어느쪽도 이기지 못하면서 알이 채워지지 않음.
    board.do_omok() #오목 한수 두기. 흑백 승패 출력
    board.winloss(board.win_lose) #승패 결정
    
    
if board.win_lose == '흑':
    print('흑 승리!')
elif board.win_lose == '백':
    print('백 승리!')
elif board.count_stone() == n**2: #알이 채워졌을 때 
    print('무승부!')
