from django.shortcuts import render
from django.http import JsonResponse

def cookie_consent_view(request):
    if request.method == "POST":
        consent_given = request.POST.get("consent")
        # handle saving consent
        return JsonResponse({"status": "success"})

    return render(request, "swing_cookie/consent_form.html")