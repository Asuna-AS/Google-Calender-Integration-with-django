from django.shortcuts import redirect
from django.views import View
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from django.conf import settings


class GoogleCalendarInitView(View):
    def get(self, request):
        print("..................working init")
        flow = Flow.from_client_secrets_file(
            'C:/Users/Arunim Singhal/Documents/GitHub/Google-Calender-Integration-with-django/backendTask/client_secret_787589429866-pkdf50i3qdjh79iok9qdvcmg9l1o6ma3.apps.googleusercontent.com.json',
            scopes=settings.GOOGLE_SCOPES,
            redirect_uri=settings.GOOGLE_AUTH_REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
        request.session['google_auth_state'] = state
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        print("..................working redirect")
        state = request.session.get('google_auth_state')
        flow = Flow.from_client_secrets_file(
            'C:/Users/Arunim Singhal/Documents/GitHub/Google-Calender-Integration-with-django/backendTask/client_secret_787589429866-pkdf50i3qdjh79iok9qdvcmg9l1o6ma3.apps.googleusercontent.com.json',
            scopes=settings.GOOGLE_SCOPES,
            redirect_uri=settings.GOOGLE_AUTH_REDIRECT_URI,
            state=state
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        
        # list of events
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        return HttpResponse('Events retrieved successfully!')
