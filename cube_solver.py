# cube_solver.py
from face_move import R, R_star, R2, U, U_star, U2, F, F_star, F2
from collections import deque

moves = {
    'R': R, "R'": R_star, 'R2': R2,
    'U': U, "U'": U_star, 'U2': U2,
    'F': F, "F'": F_star, 'F2': F2,
}

def opposite_move(move):
    """
    返回给定一步操作的逆操作，如R -> R'，U2 -> U2，F' -> F
    用于双向搜索中快速检测剪枝
    """
    if move.endswith("2"):
        return move  # R2逆操作还是R2
    if move.endswith("'"):
        return move[:-1]
    else:
        return move + "'"

def solve(start, target):
    """
    双向 BFS 搜索，从start和target同时向中间搜索
    以减少状态空间和时间。
    剪枝策略：
    - 相邻步骤不能来自同一转动面（R/U/F）
    - 避免重复访问相同状态和最后操作面组合
    - 双向搜索中遇到重合状态时拼接路径返回结果
    """
    if start == target:
        return []

    # 定义队列元素 (状态, 路径, 上一步操作面)
    queue_start = deque()
    queue_end = deque()

    visited_start = dict()  # key: state, value: (path, last_move_face)
    visited_end = dict()

    queue_start.append((start, [], None))
    visited_start[start] = ([], None)

    queue_end.append((target, [], None))
    visited_end[target] = ([], None)

    while queue_start and queue_end:
        # 从起点方向扩展
        state_s, path_s, last_face_s = queue_start.popleft()
        for move_name, move_func in moves.items():
            face = move_name[0]
            if face == last_face_s:
                continue

            next_state = move_func(state_s)
            if next_state in visited_start:
                prev_path, prev_last = visited_start[next_state]
                if prev_last == face:
                    continue
            # 如果next_state在终点方向已访问，说明找到路径
            if next_state in visited_end:
                path_e, last_face_e = visited_end[next_state]
                # 终点方向路径需要倒序且转为逆操作
                path_e_rev = [opposite_move(m) for m in reversed(path_e)]
                return path_s + [move_name] + path_e_rev

            visited_start[next_state] = (path_s + [move_name], face)
            queue_start.append((next_state, path_s + [move_name], face))

        # 从终点方向扩展
        state_e, path_e, last_face_e = queue_end.popleft()
        for move_name, move_func in moves.items():
            face = move_name[0]
            if face == last_face_e:
                continue

            next_state = move_func(state_e)
            if next_state in visited_end:
                prev_path, prev_last = visited_end[next_state]
                if prev_last == face:
                    continue

            if next_state in visited_start:
                path_s, last_face_s = visited_start[next_state]
                path_e_new = path_e + [move_name]
                # 终点方向路径需要倒序且转为逆操作
                path_e_rev = [opposite_move(m) for m in reversed(path_e_new)]
                return path_s + path_e_rev

            visited_end[next_state] = (path_e + [move_name], face)
            queue_end.append((next_state, path_e + [move_name], face))

    return None

'''
if __name__ == '__main__':
    start_state = 'YRBYRGYOGYOBWRBWOBWOGWRG'
    target_state = 'YRBYOBYOGYRGWRBWOBWOGWRG'
    steps = solve(start_state, target_state)
    if steps:
        print(' '.join(steps))
    else:
        print('')
'''
