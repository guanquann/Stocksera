from helpers import *
from .forms import NewUserForm
from .models import Preferences, Watchlist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
# from rest_framework.authtoken.models import Token

BASE_URL = config_keys['STOCKSERA_BASE_URL']
HEADERS = {f'Authorization': f"Api-Key {config_keys['STOCKSERA_API']}"}


def signup(request):
    # token = Token.objects.create(user=request.user)
    # print(token.key)
    if request.user.is_authenticated:
        return redirect('/accounts/watchlist')

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            pref = Preferences(username=user)
            pref.save()
            wlist = Watchlist(username=user, ticker="SPY")
            wlist.save()
            messages.success(request, "Registration successful.")
            return redirect("/accounts/watchlist")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "registration/sign_up.html", {"form": form})


def preferences(request):
    post_req = request.POST
    if request.user.is_authenticated:
        if post_req:
            query = {
                "wsb_trending": False,
                "crypto_trending": False,
                "government": False,
                "insider": False,
                "jim_cramer": False,
                "earnings": False,
                "short_vol": False,
                "ctb": False,
            }
            for i in post_req:
                query[i] = not query.get(i, False)
            Preferences.objects.filter(username=request.user).update(wsb_trending=query["wsb_trending"],
                                                                               crypto_trending=query["crypto_trending"],
                                                                               government=query["government"],
                                                                               insider=query["insider"],
                                                                               jim_cramer=query["jim_cramer"],
                                                                               earnings=query["earnings"],
                                                                               short_vol=query["short_vol"],
                                                                               ctb=query["ctb"])
        else:
            filtered_pref = Preferences.objects.filter(username=request.user)
            if filtered_pref:
                filtered_pref = filtered_pref[0]
                query = {
                    "wsb_trending": filtered_pref.wsb_trending,
                    "crypto_trending": filtered_pref.crypto_trending,
                    "government": filtered_pref.government,
                    "insider": filtered_pref.insider,
                    "jim_cramer": filtered_pref.jim_cramer,
                    "earnings": filtered_pref.earnings,
                    "short_vol": filtered_pref.short_vol,
                    "ctb": filtered_pref.ctb,
                }
            else:
                query = {}
        return render(request, "users/preferences.html", {"query": query})
    else:
        return redirect("/accounts/login")


def developers(request):
    if request.user.is_authenticated:
        user = request.user
        filtered_api = APIKey.objects.filter(name=user)
        if request.POST:
            if filtered_api.count() >= 1:
                APIKey.objects.filter(name=user).delete()
            _, prefix = APIKey.objects.create_key(name=str(user))
        else:
            prefix = filtered_api.values_list("prefix").first()
            if prefix is not None:
                prefix = prefix[0] + ".********************************"
            else:
                prefix = ""
        return render(request, "users/developers.html", {"prefix": prefix})
    else:
        return redirect("/accounts/login")


def watchlist(request):
    if request.user.is_authenticated:
        ticker_selected = default_ticker(request, "SPY")
        if request.POST:
            Watchlist.objects.filter(username=request.user, ticker=ticker_selected).delete()
            messages.success(request, f"{ticker_selected} successfully deleted from watchlist.")
            return redirect("/accounts/watchlist")

        all_wlist = Watchlist.objects.filter(username=request.user)

        if Watchlist.objects.filter(username=request.user, ticker=ticker_selected).count() == 0:
            if all_wlist.count() >= 8:
                messages.warning(request, f"You have reached your maximum watchlist limit. "
                                          f"Please remove another ticker first before adding {ticker_selected}.")
            else:
                wlist = Watchlist(username=request.user, ticker=ticker_selected)
                wlist.save()
                messages.success(request, f"{ticker_selected} successfully added to watchlist.")

        # BASE_URL = "http://stocksera.pythonanywhere.com/api"
        borrowed_shares = requests.get(f"{BASE_URL}/stocks/borrowed_shares/{ticker_selected}", headers=HEADERS).json()

        ftd = requests.get(f"{BASE_URL}/stocks/failure_to_deliver/{ticker_selected}", headers=HEADERS).json()

        short_vol = requests.get(f"{BASE_URL}/stocks/short_volume/{ticker_selected}/", headers=HEADERS).json()

        wsb = requests.get(f"{BASE_URL}/reddit/wsb/{ticker_selected}/?days=100", headers=HEADERS).json()

        return render(request, "users/watchlist.html", {"ticker_selected": ticker_selected,
                                                        "borrowed_shares": borrowed_shares,
                                                        "ftd": ftd,
                                                        "short_vol": short_vol,
                                                        "wsb": wsb,
                                                        "all_wlist": all_wlist})
    else:
        messages.warning(request, f"Sign in or create an account first before adding to watchlist.")
        return redirect("/accounts/login")


def settings(request):
    if request.user.is_authenticated:
        return render(request, "users/settings.html")
    else:
        return redirect("/accounts/login")


def delete_account(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=str(request.user))
        u.delete()
        messages.info(request, "Your account has been deleted successfully.")
    return redirect("/accounts/login")
