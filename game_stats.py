class GameStats:
    """更新游戏的统计信息"""
    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.ship_left = self.settings.ship_limit
        self.reset_stats()
        # 最高分,不会被重置
        self.high_score = 0
        

    def reset_stats(self):
        """
        初始化游戏中的统计信息
        不在init中初始化是因为在游戏中仍可调用其进行设置
        """
        self.ship_left = self.settings.ship_limit
        # 每次开启游戏时都重新计分，故在reset中初始化
        self.score = 0 
        