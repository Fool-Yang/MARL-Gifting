from .normal_form_game import NormalFormGame

class BiasedRPS(NormalFormGame):

    name = "biased_rps"
    action_names = (("r", "p", "s"), ("r", "p", "s"))

    def __init__(self, max_t=1):
        self.max_t = max_t
##        self.reward_matrix = (
##            ((50, 50), (25, 75), (100, 0)),
##            ((75, 25), (50, 50), (45, 55)),
##            ((0, 100), (55, 45), (50, 50))
##        )
        self.reward_matrix = (
            ((0.5, 0.5), (0.25, 0.75), (1.0, 0)),
            ((0.75, 0.25), (0.5, 0.5), (0.45, 0.55)),
            ((0, 1.0), (0.55, 0.45), (0.5, 0.5))
        )
        super().__init__()
