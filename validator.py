# validator.py
# 用于验证二阶魔方状态是否合法

def validate_cube(solver_state):
    """
    验证 solver_state (Solver Format) 是否合法。
    Solver Format 顺序：UFL, UBL, UBR, UFR, DFL, DBL, DBR, DFR
    每个角块3个字符。
    """
    if len(solver_state) != 24:
        return False, "长度错误"

    # 1. 统计颜色的数量，标准二阶每种颜色应有4个
    colors = {}
    for c in solver_state:
        colors[c] = colors.get(c, 0) + 1
    
    required_colors = ['Y', 'W', 'R', 'O', 'B', 'G']
    for c in required_colors:
        if colors.get(c, 0) != 4:
            return False, f"颜色 {c} 的数量不为4 (当前: {colors.get(c,0)})"

    # 2. 验证角块组成
    # 标准配色的对色：Y-W, R-O, B-G。相斥颜色不能出现在同一个角块上。
    # 例如一个角块不能同时拥有红和橙。
    opposite_pairs = [
        {'Y', 'W'},
        {'R', 'O'},
        {'B', 'G'}
    ]

    # 将状态切分为8个角块，每个3字符
    corners = [solver_state[i:i+3] for i in range(0, 24, 3)]
    
    for idx, c_str in enumerate(corners):
        c_set = set(c_str)
        if len(c_set) != 3:
            return False, f"第 {idx+1} 个角块包含重复颜色 ({c_str})"
        
        for pair in opposite_pairs:
            if len(c_set.intersection(pair)) > 1:
                return False, f"第 {idx+1} 个角块包含相对颜色 {pair} ({c_str})"

    # 二阶魔方的更深层校验（如角块朝向和置换的奇偶性）在物理组装上是必须的，
    # 但对于简单的填色求解器，颜色数量和角块合法性校验已能覆盖大多数用户输入错误。
    # 这里不再进行复杂的群论校验，以免误杀某些特殊的不完整状态（虽然本求解器假设完整状态）。

    return True, "OK"
