from django.http import JsonResponse
from django.shortcuts import render


def cookie_consent_view(request):
    if request.method == "POST":
        consent_given = request.POST.get("consent")
        # handle saving consent
        return JsonResponse({"status": "success"})

    return render(request, "swing_cookie/consent_form.html")
