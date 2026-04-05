from .normal_form_game import NormalFormGame

class BeNice(NormalFormGame):

    name = "be_nice"
    action_names = (("nice", "no"), ("nice", "no"))

    def __init__(self, max_t=1):
        self.reward_matrix = (
            ((1, 1), (0, 1)),
            ((1, 0), (0, 0))
        )
        super().__init__(max_t)
