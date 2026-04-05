from .normal_form_game import NormalFormGame

class Prisoners(NormalFormGame):

    name = "prisoners"
    action_names = (("coop", "betray"), ("coop", "betray"))

    def __init__(self, max_t=1):
        self.reward_matrix = (
            ((2, 2), (0, 3)),
            ((3, 0), (1, 1))
        )
        super().__init__(max_t)
