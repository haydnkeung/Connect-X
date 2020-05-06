def my_agent(obs, config):
    # Your code here: Amend the agent!
    import numpy as np
    import random
    
    # Gets board at next step if agent drops piece in selected column
    def drop_piece(grid, col, piece, config):
        next_grid = grid.copy()
        for row in range(config.rows-1, -1, -1):
            if next_grid[row][col] == 0:
                break
        next_grid[row][col] = piece
        return next_grid

    # Returns True if dropping piece in column results in game win
    def check_winning_move(obs, config, col, piece):
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        next_grid = drop_piece(grid, col, piece, config)
        # horizontal
        for row in range(config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[row,col:col+config.inarow])
                if window.count(piece) == config.inarow:
                    return True
        # vertical
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns):
                window = list(next_grid[row:row+config.inarow,col])
                if window.count(piece) == config.inarow:
                    return True
        # positive diagonal
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        # negative diagonal
        for row in range(config.inarow-1, config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
                if window.count(piece) == config.inarow:
                    return True
        return False
    
    # Helper function for score_move: calculates value of heuristic for grid
    def get_heuristic(grid, mark, config):
        A = 0 
        B = 1
        C = 1e2
        D = 1e3
        
        E = 0
        F = -1e2
        G = -1e3
        H = -1e5
        num_one = count_windows(grid, 1, mark, config)
        num_two = count_windows(grid, 2, mark, config)
        num_three = count_windows(grid, 3, mark, config)
        num_four = count_windows(grid, 4, mark, config)
        
        num_one_opp = count_windows(grid, 1, mark%2+1, config)
        num_two_opp = count_windows(grid, 2, mark%2+1, config)
        num_three_opp = count_windows(grid, 3, mark%2+1, config)
        num_four_opp = count_windows(grid, 4, mark%2+1, config)
        score = num_one * A + num_two * B + num_three * C + num_four * D + num_one_opp * E + num_two_opp * F + num_three_opp * G + num_four_opp * H
        return score

    # Helper function for get_heuristic: checks if window satisfies heuristic conditions
    def check_window(window, num_discs, piece, config):
        return (window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs)

    # Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
    def count_windows(grid, num_discs, piece, config):
        num_windows = 0
        # horizontal
        for row in range(config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(grid[row, col:col+config.inarow])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        # vertical
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns):
                window = list(grid[row:row+config.inarow, col])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        # positive diagonal
        for row in range(config.rows-(config.inarow-1)):
            for col in range(config.columns-(config.inarow-1)):
                window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        # negative diagonal
        for row in range(config.inarow-1, config.rows):
            for col in range(config.columns-(config.inarow-1)):
                window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        return num_windows
    
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    for attempt in valid_moves:
        if check_winning_move(obs, config, attempt, obs.mark):
            return attempt
    for attempt in valid_moves:
        if check_winning_move(obs, config, attempt, obs.mark%2+1):
            return attempt
    heuristics = list()
    for col in valid_moves:
        temp = drop_piece(np.asarray(obs.board).reshape(config.rows, config.columns), col, obs.mark, config)
        heuristics.append(get_heuristic(temp, obs.mark, config))
    best_val = max(heuristics)
    best_choices = list()
    for i in range(len(heuristics)):
         if heuristics[i] == best_val:
            best_choices.append(valid_moves[i])
    return random.choice(best_choices)
