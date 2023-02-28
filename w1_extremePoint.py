import math
def input_cons():
    M = int(input("Nhap M: "))
    conditions = []
    for i in range(M):
        input_str=input()
        a,b,d=map(int,input_str.split())
        conditions.append((a, b, d))
    input_str=input()
    c1,c2=map(int,input_str.split())
    return M,conditions,c1,c2

#giai he phuong trinh bac nhat 2 an
def solve_eqs(a1, b1, c1, a2, b2, c2):
    D = a1 * b2 - a2 * b1
    if D == 0:
        if b1 * c2 == b2 * c1:
            return None,None
        else:
            return None,None
    else:
        x = (b2 * c1 - b1 * c2) / D
        y = (a1 * c2 - a2 * c1) / D
    
    return x, y

#kiem tra 1 diem co phai diem bien khong
def check_extremePoint(x,y,con):
    for i in con:
        if i[0]*x+i[1]*y>i[2]:
            return False
    return True

#kiem tra 2 duong thang co giao nhau khong va tra ve diem giao
def check_lines(a,b,con):
    x,y=solve_eqs(a[0],a[1],a[2],b[0],b[1],b[2])
    if x==None:
        return False
    return False if check_extremePoint(x,y,con)==False else (x,y)

def orientation(p, q, r):
    # Tính hướng của tam giác pqr
    # Trả về 0 nếu p, q, r thẳng hàng
    # Trả về 1 nếu p, q, r theo chiều kim đồng hồ
    # Trả về 2 nếu p, q, r ngược chiều kim đồng hồ
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def convex_hull(points):
    # Sắp xếp các điểm theo tọa độ y tăng dần, nếu bằng nhau thì theo x tăng dần
    n = len(points)
    points = sorted(points, key=lambda p: (p[1], p[0]))

    # Tìm các điểm nằm trên bao lồi bên trái
    hull = []
    for i in range(n):
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], points[i]) != 2:
            hull.pop()
        hull.append(points[i])

    # Tìm các điểm nằm trên bao lồi bên phải
    for i in range(n - 2, -1, -1):
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], points[i]) != 2:
            hull.pop()
        hull.append(points[i])

    # Loại bỏ điểm trùng nhau trong danh sách bao lồi
    hull = list(set(hull))
    return hull

# Hàm tính góc tạo bởi điểm A và B với trục hoành
def angle(A, B):
    return math.atan2(B[1] - A[1], B[0] - A[0])

# Hàm tính khoảng cách giữa hai điểm A và B
def distance(A, B):
    return math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)

# Hàm sắp xếp các điểm bao lồi theo chiều kim đồng hồ
def sort_convex_hull(points):
    # Tìm điểm trái nhất trong số các điểm
    leftmost = min(points, key=lambda x: x[0])
    # Tạo danh sách các điểm còn lại
    rest = [p for p in points if p != leftmost]
    # Sắp xếp các điểm còn lại theo góc tạo bởi đường thẳng nối điểm trái nhất và điểm đó với trục hoành
    sorted_points = sorted(rest, key=lambda x: angle(leftmost, x))
    # Nếu có hai điểm có cùng góc tạo với điểm trái nhất thì sắp xếp theo khoảng cách của chúng với điểm trái nhất
    for i in range(1, len(sorted_points)):
        if angle(leftmost, sorted_points[i-1]) == angle(leftmost, sorted_points[i]):
            if distance(leftmost, sorted_points[i-1]) > distance(leftmost, sorted_points[i]):
                sorted_points[i-1], sorted_points[i] = sorted_points[i], sorted_points[i-1]
    # Trả về danh sách các điểm đã được sắp xếp
    return [leftmost] + sorted_points

def check_lines_hull(a,b,cons): # kiem tra 2 diem ke nhau co nam tren mot duong thang (dieu kien)
    axisX=(1,0,0)
    axisY=(0,1,0)
    if a[0]*axisX[0]+a[1]*axisX[1]==axisX[2] and b[0]*axisX[0]+b[1]*axisX[1]==axisX[2]:
        return True
    elif a[0]*axisY[0]+a[1]*axisY[1]==axisY[2] and b[0]*axisY[0]+b[1]*axisY[1]==axisY[2]:
        return True
    for con in cons:
        if a[0]*con[0]+a[1]*con[1]==con[2] and b[0]*con[0]+b[1]*con[1]==con[2]:
            return True
    return False

def main():
    M,conditions,c1,c2 = input_cons()
    i=j=0
    ex_point=[]
    # kiem tra goc toa do co phai diem bien khong
    if check_extremePoint(0,0,conditions) == True: ex_point.append((0,0))
    for i in range(M):            
        axis=check_lines(conditions[i],(1,0,0),conditions) # kiem tra duong thang co cat truc hoanh khong
        if axis != False:
            ex_point.append(axis)
        axis=check_lines(conditions[i],(0,1,0),conditions) # kiem tra duong thang co cat truc tung khong
        if axis != False:
            ex_point.append(axis)
        for j in range(i+1,M):
            t=check_lines(conditions[i],conditions[j],conditions)
            if t != False:
                ex_point.append(t)
    print("1/ Diem cuc bien: ",ex_point)
    ex_point=sort_convex_hull(convex_hull(ex_point))
    prevent = True
    ex_point.append(ex_point[0])
    i=0
    for i in range(len(ex_point)-1):
        if check_lines_hull(ex_point[i],ex_point[i+1],conditions)==False:
            prevent = False
        
    print("2/ Mien rang buoc bi chan" if prevent else "2/ Mien rang buoc khong bi chan")
    max = c1*ex_point[0][0]+c2*ex_point[0][1]
    min = c1*ex_point[0][0]+c2*ex_point[0][1]
    point_max=[]
    point_min=[]
    if prevent==False:
        print("3/ GTLN khong ton tai")
        for point in ex_point:
            if min >= c1*point[0]+c2*point[1]:
                min=c1*point[0]+c2*point[1]
                point_min=point
    else:
        for point in ex_point:
            if max <= c1*point[0]+c2*point[1]:
                max=c1*point[0]+c2*point[1]
                point_max=point
            if min >= c1*point[0]+c2*point[1]:
                min=c1*point[0]+c2*point[1]
                point_min=point
        print("3/ GTLN: ",max," tai x1=",point_max[0],", x2=",point_max[1])
    print("GTNN: ",min," tai x1=",point_min[0],", x2=",point_min[1])
    return

main()