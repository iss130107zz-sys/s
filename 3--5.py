import numpy as np
from matplotlib.pyplot import scatter
from numpy import dtype
from openpyxl.styles.builtins import total

# 滚轮权重
BASE_REEL_WEIGHTS = {
    'reel1_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel2_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel3_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel4_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel5_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2}
}

BASE_WEIGHTS = [np.array(list(w.values()),dtype=float) for w in BASE_REEL_WEIGHTS.values()]
BASE_PROBS = [w/ sum(w) for w in BASE_WEIGHTS]


FREE_REEL_WEIGHTS = {
    'reel1_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel2_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel3_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel4_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2},

    'reel5_weights' : {'9': 30, '10': 25, 'J': 14, 'Q': 12, 'K': 10,
    'A': 8, 'Dia': 6, 'Crown': 4, 'W': 3, 'S': 2}
}

FREE_WEIGHTS = [np.array(list(w.values()),dtype=float) for w in FREE_REEL_WEIGHTS.values()]
FREE_PROBS = [w/ sum(w) for w in FREE_WEIGHTS]




# 赔付表
PAYTABLE = {
    '9':      [5, 10, 50],
    '10':     [8, 20, 80],
    'J':      [10, 30, 120],
    'Q':      [15, 40, 160],
    'K':      [20, 50, 200],
    'A':      [25, 75, 300],
    'Dia':    [40, 100, 400],
    'Crown':  [50, 250, 1000],
    'W':      [100, 500, 2000]   # 纯Wild组合 (不替代时)
}
PAYTABLE_list = []
for val in PAYTABLE.values():
    PAYTABLE_list.append([0,0,0] + val)
PAYTABLE_ARR = np.array(PAYTABLE_list,dtype=float)

SCATTER_PAY_MAP = np.array([0,0,0,2,10,100],dtype=float)
FREE_SPIN_AWARD = {3:10,4:15,5:20}

# 奖励线(转化为一维坐标)
RAW_LINES = [
    [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
    [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)],
    [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
    [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
    [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],
    [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],
    [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],
    [(0, 0), (1, 1), (1, 2), (1, 3), (0, 4)],
    [(2, 0), (1, 1), (1, 2), (1, 3), (2, 4)],
    [(0, 0), (0, 1), (1, 2), (0, 3), (0, 4)],
    [(2, 0), (2, 1), (1, 2), (2, 3), (2, 4)],
    [(0, 0), (1, 1), (0, 2), (1, 3), (0, 4)],
    [(2, 0), (1, 1), (2, 2), (1, 3), (2, 4)],
    [(1, 0), (1, 1), (0, 2), (1, 3), (1, 4)],
    [(1, 0), (1, 1), (2, 2), (1, 3), (1, 4)],
    [(0, 0), (1, 1), (1, 2), (1, 3), (2, 4)],
    [(2, 0), (1, 1), (1, 2), (1, 3), (0, 4)],
    [(1, 0), (0, 1), (1, 2), (0, 3), (1, 4)],
    [(1, 0), (2, 1), (1, 2), (2, 3), (1, 4)],
    [(0, 0), (1, 1), (2, 2), (2, 3), (2, 4)],
    [(2, 0), (1, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 0), (0, 1), (2, 2), (0, 3), (0, 4)],
    [(2, 0), (2, 1), (0, 2), (2, 3), (2, 4)]
]
FLAT_LINES = np.array([[r*5+c for (r,c) in line]for line in RAW_LINES])


# ===========游戏===========
def calc_base_wins(screens):
    B = screens.shape[0]

    batch_lines = screens[:,FLAT_LINES]

    max_line_pays = np.zeros((B,len(RAW_LINES)))

    for s in range(8):
        matches = (batch_lines==s) | (batch_lines==8)
        lengths = np.cumprod(matches,axis=2).sum(axis=2)

        symbol_pay_table = np.array(PAYTABLE_ARR[s])
        max_line_pays = np.maximum(max_line_pays,symbol_pay_table[lengths])

    matches_w = (batch_lines==8)
    lengths_w = np.cumprod(matches_w, axis=2).sum(axis=2)
    wild_pay_table = np.array(PAYTABLE_ARR[8])
    max_line_pays= np.maximum(max_line_pays,wild_pay_table[lengths_w])

    round_wins = max_line_pays.sum(axis=1)

    # 计算scatter
    scatters = (screens==9).sum(axis=1)
    scatters_wins = np.zeros(B)
    s_mask = scatters >= 3
    s_counts = np.minimum(scatters[s_mask],5)
    scatters_wins[s_mask] = SCATTER_PAY_MAP[s_counts]

    return round_wins+scatters_wins,scatters

def run_free_spins(initial_s_count,rng):
    free_spins_remaining = FREE_SPIN_AWARD[initial_s_count]
    fs_win = 0

    while free_spins_remaining > 0:
        free_spins_remaining -= 1

        fs_screen = np.empty(15, dtype=int)
        for c in range(5):
            fs_screen[c]      = rng.choice(10, p=FREE_PROBS[c])
            fs_screen[c + 5]  = rng.choice(10, p=FREE_PROBS[c])
            fs_screen[c + 10] = rng.choice(10, p=FREE_PROBS[c])

        upgrade_mask = (fs_screen!=9) & (fs_screen!=8)
        rand_vals = rng.random(15)
        fs_screen[upgrade_mask & (rand_vals<0.1)] = 8

        win_amt,fs_s_count = calc_base_wins(fs_screen.reshape(1,-1))
        fs_win += win_amt[0]*2

        s_cnt = fs_s_count[0]
        if s_cnt >= 3:
            free_spins_remaining += FREE_SPIN_AWARD[min(s_cnt,5)]
    return fs_win

    return

# ===========模拟===========
def simulate_game(num_games=500000,batch_size=25000):
    rng = np.random.default_rng()


    num_batches = num_games//batch_size
    total_wins_ar = []

    for b in range(num_batches):
        base_screens = np.empty((batch_size, 15), dtype=int)
        for c in range(5):          # 5 个滚轮
            # 一次生成该 column 的 3 个行样本 (batch_size, 3)
            col_samples = rng.choice(10, size=(batch_size, 3), p=BASE_PROBS[c])
            base_screens[:, c]      = col_samples[:, 0]   # 第 0 行
            base_screens[:, c + 5]  = col_samples[:, 1]   # 第 1 行
            base_screens[:, c + 10] = col_samples[:, 2]   # 第 2 行

        base_wins,scatter_counts = calc_base_wins(base_screens)

        batch_total_wins = base_wins.copy()

        fs_trigger_indices = np.where(scatter_counts>=3)[0]
        for idx in fs_trigger_indices:
            s_count = min(scatter_counts[idx],5)

            batch_total_wins[idx] += run_free_spins(s_count,rng)

        total_wins_ar.append(batch_total_wins)

    total_round = np.array(total_wins_ar)
    total_wins = total_round.sum()
    total_hits = np.sum(total_round>0)

    total_bet = num_games * len(RAW_LINES)
    rtp = (total_wins/total_bet) * 100
    hit_rate = total_hits/num_games
    game_std = total_round.std()

    print('\n============统计结果============')
    print(f'总模拟局数：  {num_games}')
    print(f'平均rtp：   {rtp:.2f}%')
    print(f'中奖率：    {hit_rate*100:.2f}%')
    print(f'标准差   {game_std:.2f}')

if __name__ == "__main__":
    import time

    start = time.time()
    simulate_game(500000)
    print(f"总耗时: {time.time() - start:.4f} 秒")
