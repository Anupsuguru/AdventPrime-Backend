from functools import wraps
from django.http import JsonResponse
import requests
from .models import Student


# Old decorator function
# def validate_user_token(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return JsonResponse({
#                 "error": "Authorization header missing or invalid."
#             }, status=401)
#
#         token = auth_header.split(' ')[1]  # Extract the token part
#
#         url = "https://graph.microsoft.com/beta/me/profile/"
#         headers = {
#             "Authorization": f"Bearer {token}",
#         }
#
#         response = requests.get(url, headers=headers)
#
#         if response.status_code == 200:
#             data = response.json()
#
#             # Extract 'userPrincipalName' from the 'account' list
#             user_principal_name = None
#             for account in data.get('account', []):
#                 if 'userPrincipalName' in account:
#                     user_principal_name = account['userPrincipalName']
#                     break
#
#             if user_principal_name:
#                 # Attach user_principal_name to the request object for further use
#                 request.user_principal_name = user_principal_name
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return JsonResponse({"error": "userPrincipalName not found in response."}, status=404)
#         else:
#             return JsonResponse({
#                 "error": f"Failed to retrieve profile data. Status code: {response.status_code}, Response: {response.text}"
#             }, status=response.status_code)
#
#     return _wrapped_view


# New decorator function
def validate_user_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                "error": "Authorization header missing or invalid."
            }, status=401)

        token = auth_header.split(' ')[1]  # Extract the token part

        url = "https://graph.microsoft.com/beta/me/profile/"
        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Extract 'userPrincipalName' from the 'account' list
            user_principal_name = None
            for account in data.get('account', []):
                if 'userPrincipalName' in account:
                    user_principal_name = account['userPrincipalName']
                    break

            if user_principal_name:
                # Attach user_principal_name to the request object for further use
                request.user_principal_name = user_principal_name

                # Check if the user_principal_name exists in the Student model
                if not Student.objects.filter(student_email=user_principal_name).exists():
                    # If not exists, create a new Student record
                    Student.objects.create(
                        student_email=user_principal_name,
                        student_name="Unknown",  # Assign a default name or get it from data if available
                        term="",  # Set defaults or fetch from data if available
                        course_registered="",
                        last_login=None,
                        no_of_workshop_attended=0,
                        no_of_workshop_waitlisted=0,
                        no_of_workshop_scheduled=0
                    )

                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({"error": "userPrincipalName not found in response."}, status=404)
        else:
            return JsonResponse({
                "error": f"Failed to retrieve profile data. Status code: {response.status_code}, Response: {response.text}"
            }, status=response.status_code)

    return _wrapped_view
