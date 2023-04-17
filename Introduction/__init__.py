from otree.api import *
c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(label='Имя и фамилия')


class Survey(Page):
    form_model = 'player'
    form_fields = ['name']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        participant.label = player.name


class Instructions(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        return dict(
            show_others_score=session.config['show_others_score'],
            show_others_score_as_interval=session.config['show_others_score_as_interval']
        )


page_sequence = [Survey, Instructions]
