from django.db import models
from django.utils import timezone

import pandas as pd
import numpy as np


def play42_duel_test(c, d, s):  # функция для равных ставок
    if c[0] < d[0]:
        a = d
        b = c
        gp = (a[0] + b[0]) / 2  # game probability
        sg = 2 * s  # sum game
        w1 = min(s / gp, sg)
        w2 = min(s / (1 - gp), sg)
        aw = [w1, sg - w2]
        bw = [sg - w1, w2]
        return bw, aw

    elif c[0] > d[0]:
        a = c
        b = d
        gp = (a[0] + b[0]) / 2  # game probability
        sg = 2 * s  # sum game
        w1 = min(s / gp, sg)
        w2 = min(s / (1 - gp), sg)
        aw = [w1, sg - w2]
        bw = [sg - w1, w2]
        return aw, bw

    else:
        aw = [s, s]
        bw = [s, s]
        return aw, bw


def play42_duel_e(c, d, s):  # функция для равных ставок
    if c[1] < d[1]:
        a = d
        b = c
        gp = (a[1] + b[1]) / 2  # game probability
        sg = 2 * s  # sum game
        w1 = min(s / gp, sg)
        w2 = min(s / (1 - gp), sg)
        aw = [a[0], w1, sg - w2]
        bw = [b[0], sg - w1, w2]
        return bw, aw

    elif c[1] > d[1]:
        a = c
        b = d
        gp = (a[1] + b[1]) / 2  # game probability
        sg = 2 * s  # sum game
        w1 = min(s / gp, sg)
        w2 = min(s / (1 - gp), sg)
        aw = [a[0], w1, sg - w2]
        bw = [b[0], sg - w1, w2]
        return aw, bw

    else:
        aw = [c[0], s, s]
        bw = [d[0], s, s]
        return aw, bw


def play42_r1_e(betdf):
    betdf = betdf.sort_values('sum').reset_index(drop=True)
    res_d = pd.DataFrame()
    res_d = res_d.append(betdf)
    res_d['w1'] = 0.0
    res_d['w2'] = 0.0
    nr = res_d.shape[0]
    for i in range(nr - 1):
        user_playing = res_d[i:i + 1].values.tolist()[0][:3]
        play_sum = user_playing[2] / (nr - (i + 1))

        ri = []
        rj = []
        for j in range(i + 1, nr):
            s_user = res_d[j:j + 1].values.tolist()[0][:3]
            p_i_res, p_j_res = play42_duel_e(user_playing, s_user, play_sum)
            ri.append(p_i_res[1:3])
            rj.append(p_j_res[1:3])

        res_d.loc[i + 1:, 'sum'] = res_d.loc[i + 1:, 'sum'] - play_sum
        rit = [sum(i) for i in zip(*ri)]  # sumed up result for player i
        res_d.set_value(i, 'w1', rit[0] + res_d.iloc[i]['w1'])
        res_d.set_value(i, 'w2', rit[1] + res_d.iloc[i]['w2'])
        other_result = pd.DataFrame(rj, columns=['w1', 'w2'], index=None)
        other_result.index = other_result.index + 1 + i

        res_d.loc[i + 1:, 'w1'] = res_d.loc[i + 1:, 'w1'] + other_result.loc[:, 'w1']
        res_d.loc[i + 1:, 'w2'] = res_d.loc[i + 1:, 'w2'] + other_result.loc[:, 'w2']

    res_d.set_value(nr - 1, 'w2', res_d.iloc[nr - 1]['w2'] + res_d.iloc[nr - 1]['sum'])
    res_d.set_value(nr - 1, 'w1', res_d.iloc[nr - 1]['w1'] + res_d.iloc[nr - 1]['sum'])

    res_d['rest_sum'] = res_d[['w1', 'w2']].min(axis=1)
    res_d['w1'] = res_d['w1'] - res_d['rest_sum']
    res_d['w2'] = res_d['w2'] - res_d['rest_sum']

    return (res_d)


def play42_all_r(betdf):
    save_t = play42_r1_e(betdf)
    betdf2 =  save_t.loc[save_t['rest_sum'] > 0.5][['name', 'p', 'rest_sum']].rename(columns={'rest_sum':'sum'})  ### wheek place
    counter = 0
    while betdf2.shape[0] > 1 and counter < 50:
        save_1 = play42_r1_e(betdf2)
        betdf2 =  save_1.loc[save_1['rest_sum'] > 0.05][['name', 'p', 'rest_sum']].rename(columns={'rest_sum':'sum'})
        tmp = pd.merge(save_t, save_1, how='left', on = ['name'])
        tmp.fillna(value=0, inplace=True)
        save_t['w1'] = tmp['w1_x'] + tmp['w1_y']
        save_t['w2'] = tmp['w2_x'] + tmp['w2_y']
        save_t['rest_sum'] = tmp['rest_sum_y']
        counter += 1
    return save_t


class Bet(models.Model):
    probability = models.FloatField(null=True, blank=True, default=None)
    sum = models.FloatField(null=True, blank=True, default=None)

    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class DoubleBet(models.Model):
    probability1 = models.FloatField(null=True, blank=True, default=None)
    sum1 = models.FloatField(null=True, blank=True, default=None)

    probability2 = models.FloatField(null=True, blank=True, default=None)
    sum2 = models.FloatField(null=True, blank=True, default=None)

    published_date = models.DateTimeField(
        blank=True, null=True)


    player1_win1 = models.FloatField(null=True, blank=True, default=None)
    player1_win2 = models.FloatField(null=True, blank=True, default=None)
    player2_win1 = models.FloatField(null=True, blank=True, default=None)
    player2_win2 = models.FloatField(null=True, blank=True, default=None)

    commission1 = models.FloatField(null=True, blank=True, default=None)
    commission2 = models.FloatField(null=True, blank=True, default=None)

    player1_fact_coef1 = models.FloatField(null=True, blank=True, default=None)
    player1_fact_coef2 = models.FloatField(null=True, blank=True, default=None)
    player2_fact_coef1 = models.FloatField(null=True, blank=True, default=None)
    player2_fact_coef2 = models.FloatField(null=True, blank=True, default=None)

    player1_coef1 = models.FloatField(null=True, blank=True, default=None)
    player1_coef2 = models.FloatField(null=True, blank=True, default=None)
    player2_coef1 = models.FloatField(null=True, blank=True, default=None)
    player2_coef2 = models.FloatField(null=True, blank=True, default=None)

    garanty_moneyback1 = models.FloatField(null=True, blank=True, default=None)
    garanty_moneyback2 = models.FloatField(null=True, blank=True, default=None)


    def publish(self):
        self.published_date = timezone.now()
        self.save()


class TripleBet(models.Model):
    probability1 = models.FloatField(null=True, blank=True, default=None)
    sum1 = models.FloatField(null=True, blank=True, default=None)

    probability2 = models.FloatField(null=True, blank=True, default=None)
    sum2 = models.FloatField(null=True, blank=True, default=None)

    probability3 = models.FloatField(null=True, blank=True, default=None)
    sum3 = models.FloatField(null=True, blank=True, default=None)

    published_date = models.DateTimeField(
        blank=True, null=True)

    player1_win1 = models.FloatField(null=True, blank=True, default=None)
    player1_win2 = models.FloatField(null=True, blank=True, default=None)
    player2_win1 = models.FloatField(null=True, blank=True, default=None)
    player2_win2 = models.FloatField(null=True, blank=True, default=None)
    player3_win1 = models.FloatField(null=True, blank=True, default=None)
    player3_win2 = models.FloatField(null=True, blank=True, default=None)

    player1_fact_coef1 = models.FloatField(null=True, blank=True, default=None)
    player1_fact_coef2 = models.FloatField(null=True, blank=True, default=None)
    player2_fact_coef1 = models.FloatField(null=True, blank=True, default=None)
    player2_fact_coef2 = models.FloatField(null=True, blank=True, default=None)
    player3_fact_coef1 = models.FloatField(null=True, blank=True, default=None)
    player3_fact_coef2 = models.FloatField(null=True, blank=True, default=None)

    player1_coef1 = models.FloatField(null=True, blank=True, default=None)
    player1_coef2 = models.FloatField(null=True, blank=True, default=None)
    player2_coef1 = models.FloatField(null=True, blank=True, default=None)
    player2_coef2 = models.FloatField(null=True, blank=True, default=None)
    player3_coef1 = models.FloatField(null=True, blank=True, default=None)
    player3_coef2 = models.FloatField(null=True, blank=True, default=None)

    commission1 = models.FloatField(null=True, blank=True, default=None)
    commission2 = models.FloatField(null=True, blank=True, default=None)

    garanty_moneyback1 = models.FloatField(null=True, blank=True, default=None)
    garanty_moneyback2 = models.FloatField(null=True, blank=True, default=None)
    garanty_moneyback3 = models.FloatField(null=True, blank=True, default=None)


    def publish(self):
        self.published_date = timezone.now()
        self.save()



class NBet(models.Model):
    n_players = models.IntegerField(null=True, blank=True, default=None)
    probability = models.FloatField(null=True, blank=True, default=None)

    coeficient_profit = models.FloatField(null=True, blank=True, default=None)
    final_company_profit = models.FloatField(null=True, blank=True, default=None)
    total_bet = models.FloatField(null=True, blank=True, default=None)
    avg_bet = models.FloatField(null=True, blank=True, default=None)

    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()



