"""
复杂3x5老虎机模拟器
- 8种普通符号: 9, 10, J, Q, K, A, Dia, Crown
- 1种Wild (W): 可替代除 Scatter 外的所有符号
- 1种Scatter (S): 触发免费游戏并支付散布赔率
- 25条奖励线
- 免费游戏: 3个S得10次, 4个S得15次, 5个S得20次
  免费游戏中所有赢取×2, 且每个非S非W符号有10%概率变为Wild
- 每局总投注=25单位 (线注=1)
"""

import numpy as np
from collections import Counter

# ==================== 基础配置 ====================
SYMBOLS = ['9', '10', 'J', 'Q', 'K', 'A', 'Dia', 'Crown', 'W', 'S']
NORMAL_SYMBOLS = ['9', '10', 'J', 'Q', 'K', 'A', 'Dia', 'Crown']

# 每个卷轴(列)的符号权重 (可分别设定，此处统一)
REEL_WEIGHTS = {
    '9': 18, '10': 16, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2
}
TOTAL_WEIGHT = sum(REEL_WEIGHTS.values())

# 赔付表 (线注1) - 对每个符号: [3连, 4连, 5连] 的倍率
PAYTABLE = {
    '9':      [2, 10, 50],
    '10':     [4, 20, 80],
    'J':      [6, 30, 120],
    'Q':      [8, 40, 160],
    'K':      [10, 50, 200],
    'A':      [15, 75, 300],
    'Dia':    [25, 100, 400],
    'Crown':  [50, 250, 1000],
    'W':      [100, 500, 2000]   # 纯Wild组合 (不替代时)
}

# Scatter 散布赔率 (乘以总投注)
SCATTER_PAY = [2, 10, 100]  # 索引0->3个S, 1->4个S, 2->5个S

# 免费游戏配置
FREE_SPINS_AWARD = {3: 10, 4: 15, 5: 20}  # 触发获得的免费旋转次数
FREE_MULTIPLIER = 2                        # 免费旋转中所有赢取乘数
WILD_UPGRADE_PROB = 0.1                    # 免费旋转中普通符号变Wild的概率

# 25条经典奖励线 (行索引0-2, 列0-4)
LINES = [
    # 水平线
    [(1,0),(1,1),(1,2),(1,3),(1,4)],  # 1: 中横线
    [(0,0),(0,1),(0,2),(0,3),(0,4)],  # 2: 上横线
    [(2,0),(2,1),(2,2),(2,3),(2,4)],  # 3: 下横线
    # V形 / 倒V
    [(0,0),(1,1),(2,2),(1,3),(0,4)],  # 4
    [(2,0),(1,1),(0,2),(1,3),(2,4)],  # 5
    # 其他常见线
    [(1,0),(2,1),(2,2),(2,3),(1,4)],  # 6
    [(1,0),(0,1),(0,2),(0,3),(1,4)],  # 7
    [(0,0),(0,1),(1,2),(2,3),(2,4)],  # 8
    [(2,0),(2,1),(1,2),(0,3),(0,4)],  # 9
    [(0,0),(1,1),(1,2),(1,3),(0,4)],  # 10
    [(2,0),(1,1),(1,2),(1,3),(2,4)],  # 11
    [(0,0),(0,1),(1,2),(0,3),(0,4)],  # 12
    [(2,0),(2,1),(1,2),(2,3),(2,4)],  # 13
    [(0,0),(1,1),(0,2),(1,3),(0,4)],  # 14
    [(2,0),(1,1),(2,2),(1,3),(2,4)],  # 15
    [(1,0),(1,1),(0,2),(1,3),(1,4)],  # 16
    [(1,0),(1,1),(2,2),(1,3),(1,4)],  # 17
    [(0,0),(1,1),(1,2),(1,3),(2,4)],  # 18
    [(2,0),(1,1),(1,2),(1,3),(0,4)],  # 19
    [(1,0),(0,1),(1,2),(0,3),(1,4)],  # 20
    [(1,0),(2,1),(1,2),(2,3),(1,4)],  # 21
    [(0,0),(1,1),(2,2),(2,3),(2,4)],  # 22
    [(2,0),(1,1),(0,2),(0,3),(0,4)],  # 23
    [(0,0),(0,1),(2,2),(0,3),(0,4)],  # 24
    [(2,0),(2,1),(0,2),(2,3),(2,4)],  # 25
]

# ==================== 核心函数 ====================
def generate_screen():
    """生成一个3x5的符号矩阵 (行, 列)"""
    # 每个单元格独立按权重随机抽取
    weights = [REEL_WEIGHTS[s] for s in SYMBOLS]
    return np.random.choice(SYMBOLS, size=(3, 5), p=np.array(weights)/TOTAL_WEIGHT)

def apply_wild_upgrade(screen):
    """对免费旋转屏幕进行Wild升级: 非S非W的符号以WILD_UPGRADE_PROB变为W"""
    new_screen = screen.copy()
    for i in range(3):
        for j in range(5):
            if screen[i, j] != 'S' and screen[i, j] != 'W':
                if np.random.rand() < WILD_UPGRADE_PROB:
                    new_screen[i, j] = 'W'
    return new_screen

def eval_line(line_symbols):
    """计算一条线的赢取额 (线注1)"""
    max_pay = 0
    # 测试所有可能匹配的符号 (普通符号 + Wild自身)
    for symbol in NORMAL_SYMBOLS + ['W']:
        length = 0
        for s in line_symbols:
            if s == symbol or s == 'W':
                length += 1
            else:
                break
        if length >= 3:
            pay = PAYTABLE[symbol][length - 3]
            if pay > max_pay:
                max_pay = pay
    return max_pay

def calc_screen_win(screen):
    """计算一屏的总赢取 (线赢 + scatter赢)"""
    total_win = 0

    # 线赢
    for line in LINES:
        symbols = [screen[r, c] for (r, c) in line]
        total_win += eval_line(symbols)

    # scatter赢 (散布)
    s_count = min(np.sum(screen == 'S'),5)
    if s_count >= 3:
        total_win += SCATTER_PAY[s_count - 3] * 25   # 乘以总投注(25)

    return total_win

def play_one_round():
    """
    执行一局完整游戏 (基础 + 可能的免费旋转)
    返回: (总赢取, 是否中奖>0)
    总赢取单位为投注单位 (总投注=25)
    """
    win = 0

    # ---- 基础游戏 ----
    screen = generate_screen()
    win += calc_screen_win(screen)

    s_count = min(np.sum(screen == 'S'),5)
    if s_count >= 3:
        free_spins_remaining = FREE_SPINS_AWARD[s_count]

        while free_spins_remaining > 0:
            free_spins_remaining -= 1

            # 免费旋转屏幕 + Wild升级
            fs_screen = generate_screen()
            fs_screen = apply_wild_upgrade(fs_screen)

            # 免费游戏赢取 (含乘数)
            fs_win = calc_screen_win(fs_screen) * FREE_MULTIPLIER
            win += fs_win

            # 再触发检测
            fs_s_count = np.sum(fs_screen == 'S')
            if fs_s_count >= 3:
                free_spins_remaining += FREE_SPINS_AWARD[fs_s_count]

    return win, (win > 0)

# ==================== 模拟与统计 ====================
def simulate(num_games=500000):
    wins = np.zeros(num_games, dtype=np.float64)
    hits = 0

    for i in range(num_games):
        win, hit = play_one_round()
        wins[i] = win
        if hit:
            hits += 1

        # 进度提示 (可选)
        if (i + 1) % (num_games // 10) == 0:
            print(f"  进度: {i+1}/{num_games}")

    total_bet = 25.0
    avg_win = np.mean(wins)
    rtp = (avg_win / total_bet) * 100
    std_win = np.std(wins)        # 每局赢取的标准差 (单位)
    hit_rate = hits / num_games

    return rtp, std_win, hit_rate

if __name__ == "__main__":
    import time

    start = time.time()

    print("=" * 50)
    print("复杂3x5老虎机模拟器")
    print("符号: 9,10,J,Q,K,A,Dia,Crown, W(Wild), S(Scatter)")
    print("25线, 线注=1, 总投注=25")
    print("=" * 50)
    GAMES = 500000
    print(f"模拟局数: {GAMES}")
    rtp, std, hr = simulate(GAMES)
    print("\n================ 统计结果 =================")
    print(f"平均RTP:       {rtp:.2f}%")
    print(f"赢取标准差:     {std:.2f} (每局赢取金额)")
    print(f"中奖率:         {hr*100:.2f}%")
    print("============================================")
    print(f"总耗时: {time.time() - start:.4f} 秒")
