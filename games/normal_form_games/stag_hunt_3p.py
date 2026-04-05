from .normal_form_game import NormalFormGame

class StagHunt3P(NormalFormGame):

    name = "stag_hunt_3_players"
    action_names = (("stag", "hare"), ("stag", "hare"), ("stag", "hare"))

    def __init__(self, max_t=1):
        self.reward_matrix = (
            (
                ((1, 1, 1), (0.1, 0.1, 0.8)),
                ((0.1, 0.8, 0.1), (0.1, 0.8, 0.8))
            ),
            (
                ((0.8, 0.1, 0.1), (0.8, 0.1, 0.8)),
                ((0.8, 0.8, 0.1), (0.5, 0.5, 0.5))
            )
        )
        super().__init__(max_t)
