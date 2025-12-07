'''
定位块：白橙蓝

填色方法：由高级面到中级面再到低级面（上下、前后、左右）

目标状态表示方法：
[0][1][2]  [3][4][5]  [6][7][8]  [9][10][11]  [12][13][14]  [15][16][17]  [18][19][20] [21][22][23]

旋转操作：

1.R
[0][1][2]  [3][4][5]  [10][9][11]  [22][21][23]  [12][13][14]  [15][16][17]  [7][6][8] [19][18][20]

2.R’
R*3

3.R2
R*2

4.U
[9][11][10]  [0][2][1]  [3][5][4]  [6][8][7]  [12][13][14]  [15][16][17]  [18][19][20] [21][22][23]

5.U’
U*3

6.U2
U*2

7.F
[14][12][13]  [3][4][5]  [6][7][8]  [2][1][0]  [23][22][21]  [15][16][17]  [18][19][20] [11][10][9]

8.F’
F*3

9.F2
F*2


填色方法：
把白橙蓝的角块朝左后下摆放, 然后进行填色
顺序：
上前左的角块
上后左的角块
上后右的角块
上前右的角块
下前左的角块
下后左的角块(即白橙蓝的角块)
下后右的角块
下前右的角块

由此组成长度为24的字符串(包含YWBGOR, 代表英文颜色的首字母), 三个三个依次表示一个角块

'''
def R(st):
    
    parts = [
        st[:6], st[10], st[9],
        st[11], st[22], st[21],
        st[23], st[12:18], st[7],
        st[6], st[8], st[19],
        st[18], st[20]
    ]
    
    return ''.join(parts)

def R_star(st):

    # R * 3

    for i in range(3):
        st = R(st)

    return st

def R2(st):

    # R * 2

    for i in range(2):
        st = R(st)

    return st

def U(st):
    parts = [
        st[9], st[11], st[10],
        st[0], st[2], st[1],
        st[3], st[5], st[4],
        st[6], st[8], st[7],
        st[12:24]
    ]

    return ''.join(parts)

def U_star(st):
    
    # U * 3

    for i in range(3):
        st = U(st)

    return st

def U2(st):

    # U * 2

    for i in range(2):
        st = U(st)

    return st

def F(st):
    parts = [
        st[14], st[13], st[12],
        st[3:9],
        st[2], st[1], st[0],
        st[23], st[22], st[21],
        st[15:21],
        st[11], st[10], st[9]
    ]

    return ''.join(parts)

def F_star(st):

    # F * 3

    for i in range(3):
        st = F(st)

    return st

def F2(st):

    # F * 2

    for i in range(2):
        st = F(st)

    return st

'''
st = "YRBYOBYOGYRGWRBWOBWOGWRG"
print(F(st))
'''
