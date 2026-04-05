from .normal_form_game import NormalFormGame

class ShapleyRPS(NormalFormGame):

    name = "shapley_rps"
    action_names = (("r", "p", "s"), ("r", "p", "s"))

    def __init__(self, max_t=1):
        self.reward_matrix = (
            ((0, 0), (1, 2), (2, 1)),
            ((2, 1), (0, 0), (1, 2)),
            ((1, 2), (2, 1), (0, 0))
        )
        super().__init__(max_t)
