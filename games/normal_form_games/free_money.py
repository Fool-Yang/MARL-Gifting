from .normal_form_game import NormalFormGame

class FreeMoney(NormalFormGame):

    name = "free_money"
    action_names = (("no", "yes"), ("no", "yes"))

    def __init__(self, max_t=1):
        self.reward_matrix = (
            ((0, 0), (0, 0)),
            ((0, 0), (1, 1))
        )
        super().__init__(max_t)
