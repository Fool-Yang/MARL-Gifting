from .normal_form_game import NormalFormGame

class StagHuntClassic(NormalFormGame):

    name = "stag_hunt"
    action_names = (("stag", "hare"), ("stag", "hare"))

    def __init__(self, max_t=1):
        self.reward_matrix = (
            ((1, 1), (0, 0.5)),
            ((0.5, 0), (0.4, 0.4))
        )
        super().__init__(max_t)
