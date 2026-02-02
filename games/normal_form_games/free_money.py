from .normal_form_game import NormalFormGame

class FreeMoney(NormalFormGame):

    name = "free_money"

    def __init__(self, max_t=1):
        self.max_t = max_t
        self.reward_matrix = (
            ((0, 0), (0, 0)),
            ((0, 0), (1, 1))
        )
        super().__init__()
