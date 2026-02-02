from .normal_form_game import NormalFormGame

class StagHunt(NormalFormGame):

    name = "stag_hunt"

    def __init__(self, max_t=1):
        self.max_t = max_t
        self.reward_matrix = (
            ((1, 1), (0.1, 0.8)),
            ((0.8, 0.1), (0.5, 0.5))
        )
        super().__init__()
