from .normal_form_game import NormalFormGame

class Prisoners(NormalFormGame):

    name = "prisoners"

    def __init__(self, max_t=1):
        self.max_t = max_t
        self.reward_matrix = (
            ((2, 2), (0, 3)),
            ((3, 0), (1, 1))
        )
        super().__init__()
