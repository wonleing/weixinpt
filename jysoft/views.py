# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from jysoft.models import *

def finance(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    t_income = 0
    t_expense = 0
    months = JysoftFinance.objects.values("year", "month").distinct()
    ret = JysoftFinance.objects.all().order_by("id")
    if year and month:
        ret = ret.filter(year=year, month=month)
    Inc = ret.filter(type=1)
    Exp = ret.filter(type=0)
    for d in Inc:
        t_income += d.amount
    for e in Exp:
        t_expense += e.amount
    context = { 'income': Inc,
                'expense': Exp,
                'months': months,
                't_income': t_income,
                't_expense': t_expense,
                'total': t_income - t_expense,
              }
    return render(request, 'jysoft_finance.html', context)

def miaochun(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    t_income = 0
    t_expense = 0
    months = JysoftMiaochun.objects.values("year", "month").distinct()
    ret = JysoftMiaochun.objects.all().order_by("id")
    if year and month:
        ret = ret.filter(year=year, month=month)
    Inc = ret.filter(type=1)
    Exp = ret.filter(type=0)
    for d in Inc:
        t_income += d.amount
    for e in Exp:
        t_expense += e.amount
    context = { 'income': Inc,
                'expense': Exp,
                'months': months,
                't_income': t_income,
                't_expense': t_expense,
                'total': t_income - t_expense,
              }
    return render(request, 'jysoft_finance.html', context)
