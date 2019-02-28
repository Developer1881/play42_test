from django.shortcuts import render
from .forms import DoubleBetForm, TripleBetForm, NBetForm
from django.shortcuts import redirect
from django.utils import timezone
from .models import Bet, DoubleBet, TripleBet, NBet, play42_duel_test, play42_all_r
from django.shortcuts import render, get_object_or_404
import pandas as pd
import numpy as np


def functions_list(request):
    return render(request, 'play42_proto/main.html')


def bet_double_result(request, pk):
    bet_double = get_object_or_404(DoubleBet, pk=pk)
    return render(request, 'play42_proto/bet_double_result.html', {'bet_double': bet_double})


def bet_double(request):
    if request.method == "POST":
        form = DoubleBetForm(request.POST)
        if form.is_valid():
            bet_double1 = form.save(commit=False)

            a = ['player_a', bet_double1.probability1, bet_double1.sum1]
            b = ['player_b', bet_double1.probability2, bet_double1.sum2]

            bettable = [a, b]
            headers = ['name', 'p', 'sum']
            betdf = pd.DataFrame(bettable, columns=headers)

            res_tmp = play42_all_r(betdf)
            row_list = res_tmp.to_csv(None, header=False, index=False).split('\n')

            t1 = max(0, (float(row_list[0].split(',')[3]) +
                         float(row_list[0].split(',')[5]) - (
                                 1 / bet_double1.probability1) * bet_double1.sum1) * 0.25)
            c1 = min(bet_double1.sum1 * 0.025, t1)

            t2 = max(0, (float(row_list[1].split(',')[3]) +
                         float(row_list[1].split(',')[5]) - (
                                 1 / bet_double1.probability2) * bet_double1.sum2) * 0.25)

            c2 = min(bet_double1.sum2 * 0.025, t2)


            t12 = max(0, (float(row_list[0].split(',')[4]) +float(row_list[0].split(',')[5]) - (1 / (
                            1 - bet_double1.probability1)) * bet_double1.sum1) * 0.25)

            c12 = min(bet_double1.sum1 * 0.025, t12)

            t22 = max(0, (float(row_list[1].split(',')[4]) +
                          float(row_list[1].split(',')[5]) - (1 / (
                            1 - bet_double1.probability2)) * bet_double1.sum2) * 0.25)
            c22 = min(bet_double1.sum2 * 0.025, t22)

            bet_double1.player1_win1 = round(float(row_list[0].split(',')[3]) + float(row_list[0].split(',')[5]) - c1, 2)
            bet_double1.player1_win2 = round(float(row_list[0].split(',')[4]) + float(row_list[0].split(',')[5]) - c12, 2)
            bet_double1.player2_win1 = round(float(row_list[1].split(',')[3]) + float(row_list[1].split(',')[5]) - c2, 2)
            bet_double1.player2_win2 = round(float(row_list[1].split(',')[4]) + float(row_list[1].split(',')[5]) - c22, 2)

            bet_double1.commission1 = c1 + c2
            bet_double1.commission2 = c12 + c22

            bet_double1.garanty_moneyback1 = round(float(row_list[0].split(',')[5]), 2)
            bet_double1.garanty_moneyback2 = round(float(row_list[1].split(',')[5]), 2)

            if (bet_double1.sum1 - bet_double1.garanty_moneyback1) > 0:
                bet_double1.player1_fact_coef1 = round((bet_double1.player1_win1 - bet_double1.garanty_moneyback1)/(bet_double1.sum1 - bet_double1.garanty_moneyback1), 2)
                bet_double1.player1_fact_coef2 = round((bet_double1.player1_win2 - bet_double1.garanty_moneyback1)/(bet_double1.sum1 - bet_double1.garanty_moneyback1), 2)

            if (bet_double1.sum2 - bet_double1.garanty_moneyback2) > 0:
                bet_double1.player2_fact_coef1 = round((bet_double1.player2_win1 - bet_double1.garanty_moneyback2)/(bet_double1.sum2 - bet_double1.garanty_moneyback2), 2)
                bet_double1.player2_fact_coef2 = round((bet_double1.player2_win2 - bet_double1.garanty_moneyback2)/(bet_double1.sum2 - bet_double1.garanty_moneyback2), 2)

            bet_double1.player1_coef1 = round((1 / bet_double1.probability1), 2)
            bet_double1.player1_coef2 = round((1 / (1 - bet_double1.probability1)), 2)
            bet_double1.player2_coef1 = round((1 / bet_double1.probability2), 2)
            bet_double1.player2_coef2 = round((1 / (1 - bet_double1.probability1)), 2)

            bet_double1.published_date = timezone.now()
            bet_double1.save()

            return redirect('bet_double_result', pk=bet_double1.pk)
    else:
        form = DoubleBetForm()
    return render(request, 'play42_proto/bet_double.html', {'form': form})


def bet_triple_result(request, pk):
    bet_triple = get_object_or_404(TripleBet, pk=pk)
    return render(request, 'play42_proto/bet_triple_result.html', {'bet_triple': bet_triple})


def bet_triple(request):
    if request.method == "POST":
        form = TripleBetForm(request.POST)
        if form.is_valid():
            bet_triple1 = form.save(commit=False)

            a = ['player_a', bet_triple1.probability1, bet_triple1.sum1]
            b = ['player_b', bet_triple1.probability2, bet_triple1.sum2]
            c = ['player_c', bet_triple1.probability3, bet_triple1.sum3]

            bettable = [a, b, c]
            headers = ['name', 'p', 'sum']
            betdf = pd.DataFrame(bettable, columns=headers)

            res_tmp = play42_all_r(betdf)
            row_list = res_tmp.to_csv(None, header=False, index=False).split('\n')

            t1 = max(0, (float(row_list[0].split(',')[3]) +
                                                float(row_list[0].split(',')[5]) - (
                                                        1 / bet_triple1.probability1) * bet_triple1.sum1) * 0.25)
            c1 = min(bet_triple1.sum1 * 0.025, t1)

            t2 = max(0, (float(row_list[1].split(',')[3]) +
                                                float(row_list[1].split(',')[5]) - (
                                                        1 / bet_triple1.probability2) * bet_triple1.sum2) * 0.25)

            c2 = min(bet_triple1.sum2 * 0.025, t2)


            t3 = max((float(row_list[2].split(',')[3]) +
                                                float(row_list[2].split(',')[5]) - (
                                                        1 / bet_triple1.probability3) * bet_triple1.sum3) * 0.25, 0)
            c3 = min(bet_triple1.sum2 * 0.025, t3)

            t12 = max(0,(float(row_list[0].split(',')[4]) +
                                                 float(row_list[0].split(',')[5]) - (1 / (
                            1 - bet_triple1.probability1)) * bet_triple1.sum1) * 0.25)

            c12 = min(bet_triple1.sum1 * 0.025, t12)

            t22 =max(0, (float(row_list[1].split(',')[4]) +
                                                 float(row_list[1].split(',')[5]) - (1 / (
                            1 - bet_triple1.probability2)) * bet_triple1.sum2) * 0.25)
            c22 = min(bet_triple1.sum2 * 0.025, t22)

            t32 = max(0, (float(row_list[2].split(',')[4]) +
                                                 float(row_list[2].split(',')[5]) - (1 / (
                            1 - bet_triple1.probability3)) * bet_triple1.sum3) * 0.25)
            c32 = min(bet_triple1.sum2 * 0.025, t32)

            bet_triple1.player1_win1 = round(float(row_list[0].split(',')[3]) + float(row_list[0].split(',')[5]) - c1, 2)
            bet_triple1.player1_win2 = round(float(row_list[0].split(',')[4]) + float(row_list[0].split(',')[5]) - c12, 2)
            bet_triple1.player2_win1 = round(float(row_list[1].split(',')[3]) + float(row_list[1].split(',')[5]) - c2, 2)
            bet_triple1.player2_win2 = round(float(row_list[1].split(',')[4]) + float(row_list[1].split(',')[5]) - c22, 2)
            bet_triple1.player3_win1 = round(float(row_list[2].split(',')[3]) + float(row_list[2].split(',')[5]) - c3, 2)
            bet_triple1.player3_win2 = round(float(row_list[2].split(',')[4]) + float(row_list[2].split(',')[5]) - c32, 2)

            bet_triple1.commission1 = c1 + c2 + c3
            bet_triple1.commission2 = c12 + c22 + c32

            bet_triple1.garanty_moneyback1 = round(float(row_list[0].split(',')[5]), 2)
            bet_triple1.garanty_moneyback2 = round(float(row_list[1].split(',')[5]), 2)
            bet_triple1.garanty_moneyback3 = round(float(row_list[2].split(',')[5]), 2)

            if bet_triple1.sum1 - bet_triple1.garanty_moneyback1 > 0:
                bet_triple1.player1_fact_coef1 = round((bet_triple1.player1_win1 - bet_triple1.garanty_moneyback1)/(bet_triple1.sum1 - bet_triple1.garanty_moneyback1), 2)
                bet_triple1.player1_fact_coef2 = round((bet_triple1.player1_win2 - bet_triple1.garanty_moneyback1)/(bet_triple1.sum1 - bet_triple1.garanty_moneyback1), 2)

            if bet_triple1.sum2 - bet_triple1.garanty_moneyback2 > 0:
                bet_triple1.player2_fact_coef1 = round((bet_triple1.player2_win1 - bet_triple1.garanty_moneyback2)/(bet_triple1.sum2 - bet_triple1.garanty_moneyback2), 2)
                bet_triple1.player2_fact_coef2 = round((bet_triple1.player2_win2 - bet_triple1.garanty_moneyback2)/(bet_triple1.sum2 - bet_triple1.garanty_moneyback2), 2)

            if bet_triple1.sum3 - bet_triple1.garanty_moneyback3 > 0:
                bet_triple1.player3_fact_coef1 = round((bet_triple1.player3_win1 - bet_triple1.garanty_moneyback3)/(bet_triple1.sum3 - bet_triple1.garanty_moneyback3), 2)
                bet_triple1.player3_fact_coef2 = round((bet_triple1.player3_win2 - bet_triple1.garanty_moneyback3)/(bet_triple1.sum3 - bet_triple1.garanty_moneyback3), 2)

            bet_triple1.player1_coef1 = round((1 / bet_triple1.probability1), 2)
            bet_triple1.player1_coef2 = round((1 / (1 - bet_triple1.probability1)), 2)
            bet_triple1.player2_coef1 = round((1 / bet_triple1.probability2), 2)
            bet_triple1.player2_coef2 = round((1 / (1 - bet_triple1.probability1)), 2)
            bet_triple1.player3_coef1 = round((1 / bet_triple1.probability3), 2)
            bet_triple1.player3_coef2 = round((1 / (1 - bet_triple1.probability3)), 2)


            bet_triple1.published_date = timezone.now()
            bet_triple1.save()

            return redirect('bet_triple_result', pk=bet_triple1.pk)
    else:
        form = TripleBetForm()
    return render(request, 'play42_proto/bet_triple.html', {'form': form})


def bet_n_result(request, pk):
    bet_n1 = get_object_or_404(NBet, pk=pk)
    return render(request, 'play42_proto/bet_n_result.html', {'bet_n': bet_n1})


def bet_n(request):
    if request.method == "POST":
        form = NBetForm(request.POST)
        if form.is_valid():
            bet_n1 = form.save(commit=False)
            bet_n1.probability = 0.5
            bet_n1.published_date = timezone.now()

            mu, sigma = 2.883, 0.5  # mean and standard deviation
            bets = np.random.lognormal(mu, sigma, bet_n1.n_players)

            a = range(1, bet_n1.n_players + 1)
            users = [str(item) for item in a]

            mu, sigma = 0.5, 0.024  # mean and standard deviation
            probabilities = np.random.normal(mu, sigma, bet_n1.n_players)

            d = {'name': users, 'p': probabilities, 'sum': bets}
            df = pd.DataFrame(data=d)

            result_1000 = play42_all_r(df)

            result = pd.merge(result_1000, df, on='name', how='outer')
            result = result.loc[result['rest_sum'] < 1]
            result['helper'] = 0
            result['win1_fare'] = (1 / result['p_x']) * result['sum_y']
            result['win2_fare'] = (1 / (1 - result['p_x'])) * result['sum_y']
            result['w1profit'] = result['w1'] - result['win1_fare']
            result['w2profit'] = result['w2'] - result['win2_fare']
            result['final_profit_user'] = result[['w1profit', 'w2profit', 'helper']].max(axis=1)
            result['final_profit_user25'] = result['final_profit_user'] * 0.25
            result['bet2a5'] = result['sum_y'] * 0.025
            result['final_company_profit'] = result[['final_profit_user25', 'bet2a5']].min(axis=1)
            result['coeficient1'] = (result['w1'] + result['rest_sum'] - result['final_company_profit']) / (
                    result['sum_y'] - result['rest_sum'])
            result['coeficient2'] = (result['w2'] + result['rest_sum'] - result['final_company_profit']) / (
                    result['sum_y'] - result['rest_sum'])
            result['fare_coeficient1'] = (result['p_x']) ** (-1)
            result['fare_coeficient2'] = (1 - result['p_x']) ** (-1)
            result['coeficient_profit1'] = result['coeficient1'] / result['fare_coeficient1'] - 1
            result['coeficient_profit2'] = result['coeficient2'] / result['fare_coeficient2'] - 1
            result['coeficient_profit'] = result[['coeficient_profit1', 'coeficient_profit2']].max(axis=1)

            bet_n1.coeficient_profit = sum(result['coeficient_profit']) / result.shape[0] * 100
            bet_n1.final_company_profit = sum(result['final_company_profit'])
            bet_n1.total_bet = sum(result['sum_y'])
            bet_n1.avg_bet = np.mean(bets)

            bet_n1.save()

            return redirect('bet_n_result', pk=bet_n1.pk)
    else:
        form = NBetForm()
    return render(request, 'play42_proto/bet_n.html', {'form': form})

# Create your views here.
