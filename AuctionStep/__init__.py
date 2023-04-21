from otree.api import *
c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'AuctionStep'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    UTILITY_A = cu(100)
    UTILITY_B = cu(200)
    UTILITY_C = cu(400)

    MONEY_INTERVALS = ['[0; 25)', '(25; 50]', '(50; 75]', '(75; 99]']


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    subsession.group_randomly()


class Group(BaseGroup):
    pass


def set_payoffs(group: Group):
    from random import randint

    players = group.get_players()
    max_a = max([p.bid_a for p in players])
    max_b = max([p.bid_b for p in players])
    max_c = max([p.bid_c for p in players])
    
    winner_a = [p for p in players if p.bid_a == max_a]
    winner_a = winner_a[randint(0, len(winner_a) - 1)]
    winner_b = [p for p in players if p.bid_b == max_b]
    winner_b = winner_b[randint(0, len(winner_b) - 1)]
    winner_c = [p for p in players if p.bid_c == max_c]
    winner_c = winner_c[randint(0, len(winner_c) - 1)]
    
    for player in players:
        player.did_win_a = winner_a == player
        player.did_win_b = winner_b == player
        player.did_win_c = winner_c == player
        player.money_left = player.available_money - player.bid_a - player.bid_b - player.bid_c
        player.payoff = player.available_money - player.bid_a - player.bid_b - player.bid_c + int(player.did_win_a) * C.UTILITY_A + int(player.did_win_b) * C.UTILITY_B + int(player.did_win_c) * C.UTILITY_C


def set_initial_money(group: Group):
    import random
    
    for player in group.get_players():
        player.available_money = random.randint(0, 99)


class Player(BasePlayer):
    name = models.StringField(label='Имя и фамилия')
    bid_a = models.CurrencyField(initial=0, label='Ставка на товар А (ценность 100)', max=99, min=0)
    bid_b = models.CurrencyField(initial=0, label='Ставка на товар В (ценность 200)', max=99, min=0)
    bid_c = models.CurrencyField(initial=0, label='Ставка на товар С (ценность 400)', max=99, min=0)
    available_money = models.CurrencyField()
    did_win_a = models.BooleanField()
    did_win_b = models.BooleanField()
    did_win_c = models.BooleanField()
    money_left = models.CurrencyField()


def get_money_interval(player: Player):
    if 0 <= player.available_money < 25:
        return C.MONEY_INTERVALS[0]
    elif 25 <= player.available_money < 50:
        return C.MONEY_INTERVALS[1]
    elif 50 <= player.available_money < 75:
        return C.MONEY_INTERVALS[2]
    else:
        return C.MONEY_INTERVALS[3]


class WaitPlayers(WaitPage):
    after_all_players_arrive = set_initial_money


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_a', 'bid_b', 'bid_c']

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        group = player.group
        table_headers = [f'Игрок {p.id_in_group}' for p in group.get_players()]
        table_headers[player.id_in_group - 1] += ' (ВЫ)'
        
        money_interval = [get_money_interval(p) for p in group.get_players()]
        return dict(
            table_headers=table_headers,
            money_interval=money_interval,
            show_others_score=session.config['show_others_score'],
            show_others_score_as_interval=session.config['show_others_score_as_interval']
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random
        
        if timeout_happened:
            player.bid_a = random.randint(0, player.available_money // 3)
            player.bid_b = random.randint(0, (player.available_money - player.bid_a) // 3)
            player.bid_c = player.available_money - player.bid_a - player.bid_b

    @staticmethod
    def error_message(player: Player, values):
        if values['bid_a'] + values['bid_b'] + values['bid_c'] > player.available_money:
            return f'Сумма не может быть больше {player.available_money}'


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        table_headers = [f'Игрок {i}' for i in range(1, 5)]
        table_headers[player.id_in_group - 1] += ' (ВЫ)'
        
        return dict(
            table_headers=table_headers
        )


page_sequence = [WaitPlayers, Bid, ResultsWaitPage, Results]
