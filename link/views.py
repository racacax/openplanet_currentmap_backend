from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView

from api.models import Player
from currentmap.settings import TRACKMANIA_API_BASE_URL, TRACKMANIA_APP_ID, MANIAPLANET_API_BASE_URL, \
    MANIAPLANET_APP_ID, BASE_URL, TMUF_API_BASE_URL, TMUF_API_USERNAME
from link.api import Trackmania2020API, ManiaPlanet4API, TMUFAPI
from link.utils import get_reset_token_from_login


class ResetView(TemplateView):
    template_name = "reset_template.html"

    def get_context_data(self, **kwargs):
        context_data = super(ResetView, self).get_context_data(**kwargs)
        context_data["tm2020_link"] = f"{TRACKMANIA_API_BASE_URL}oauth/authorize?response_type=code" \
                                      f"&client_id={TRACKMANIA_APP_ID}" \
                                      f"&scope=" \
                                      f"&redirect_uri={BASE_URL + reverse('reset_2020')}"
        context_data["mp4_link"] = f"{MANIAPLANET_API_BASE_URL}login/oauth2/authorize?response_type=code" \
                                   f"&client_id={MANIAPLANET_APP_ID}" \
                                   f"&scope=basic" \
                                   f"&redirect_uri={BASE_URL + reverse('reset_mp4')}"
        context_data["tmuf_link"] = f"{TMUF_API_BASE_URL}oauth2/authorize/?response_type=code" \
                                    f"&client_id={TMUF_API_USERNAME}" \
                                    f"&scope=basic" \
                                    f"&redirect_uri={BASE_URL + reverse('reset_tmuf')}"

        return context_data


class Reset2020View(TemplateView):
    template_name = "reset_final_template.html"

    def get_context_data(self, **kwargs):
        context_data = super(Reset2020View, self).get_context_data(**kwargs)
        code = self.request.GET.get("code")
        if code:
            api = Trackmania2020API(code, self.request)
            user = api.get_user_data()
            if "login" in user:
                token = get_reset_token_from_login(user["login"], 0)
                context_data["token"] = token
                context_data["login"] = user["login"]
                context_data["display_name"] = user["display_name"]
        else:
            get_object_or_404(Player, pk=0)

        return context_data


class ResetMP4View(TemplateView):
    template_name = "reset_final_template.html"

    def get_context_data(self, **kwargs):
        context_data = super(ResetMP4View, self).get_context_data(**kwargs)
        code = self.request.GET.get("code")
        if code:
            api = ManiaPlanet4API(code, self.request)
            user = api.get_user_data()
            if "login" in user:
                token = get_reset_token_from_login(user["login"], 1)
                context_data["token"] = token
                context_data["login"] = user["login"]
                context_data["display_name"] = user["nickname"]
        else:
            get_object_or_404(Player, pk=0)

        return context_data


class ResetTMUFView(TemplateView):
    template_name = "reset_final_template.html"

    def get_context_data(self, **kwargs):
        context_data = super(ResetTMUFView, self).get_context_data(**kwargs)
        code = self.request.GET.get("code")
        if code:
            api = TMUFAPI(code, self.request)
            user = api.get_user_data()
            print(user)
            if "login" in user:
                token = get_reset_token_from_login(user["login"], 3)
                context_data["token"] = token
                context_data["login"] = user["login"]
                context_data["display_name"] = user["nickname"]
        else:
            get_object_or_404(Player, pk=0)

        return context_data
