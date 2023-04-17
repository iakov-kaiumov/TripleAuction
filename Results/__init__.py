from otree.api import *
c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'Results'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    feedback = models.LongStringField(
        label='Кратко опишите свою стратегию в каждой из трех игр и поделитесь впечатлениями:'
    )


class WaitFinalResults(WaitPage):
    pass


class FinalResults(Page):
    form_model = 'player'
    form_fields = ['feedback']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            show_others_score=session.config['show_others_score'],
            show_others_score_as_interval=session.config['show_others_score_as_interval']
        )


class TheEnd(Page):
    form_model = 'player'


page_sequence = [WaitFinalResults, FinalResults, TheEnd]
