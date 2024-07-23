from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student, Category
import json
import requests
from .decorators import validate_user_token


# Create your views here.
@validate_user_token
def index(request):
    try:
        # Extract student email from headers
        student_email_id = request.headers.get('studentEmail')
        # student_email_id = request.user_principal_name

        # Extract Student Details from Student Model
        studentObj = Student.objects.get(student_email=student_email_id)

        # Parse the preferences string into a dictionary
        preferences = json.loads(studentObj.preferences) if studentObj.preferences else {}

        # Manually construct the JSON response
        student_data = {
            'student_email': studentObj.student_email,
            'student_name': studentObj.student_name,
            'term': studentObj.term,
            'course_registered': studentObj.course_registered,
            'last_login': studentObj.last_login.isoformat() if studentObj.last_login else None,
            'no_of_workshop_attended': studentObj.no_of_workshop_attended,
            'no_of_workshop_waitlisted': studentObj.no_of_workshop_waitlisted,
            'no_of_workshop_scheduled': studentObj.no_of_workshop_scheduled,
            'preferences': preferences  # Convert JSON string to a dictionary
        }

        data = {
            "message": "Success",
            "content": student_data
        }
        return JsonResponse(data, status=200)

    except Student.DoesNotExist:
        data = {
            "message": "Failure",
            "error": "Student not found"
        }
        return JsonResponse(data, status=404)

    except Exception as e:
        data = {
            "message": "Failure",
            "error": str(e)
        }
        return JsonResponse(data, status=500)


@validate_user_token
@require_http_methods(["GET"])
def get_all_categories(request):
    try:
        # Fetch all category objects
        categories = Category.objects.all()

        # Serialize category objects
        category_list = [
            {
                'id': str(category.id),
                'category_name': category.category_name,
                'total_no_of_workshop_conducted': category.total_no_of_workshop_conducted,
            }
            for category in categories
        ]

        return JsonResponse({
            'message': 'Success',
            'content': category_list
        }, status=200)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@validate_user_token
@csrf_exempt
@require_http_methods(["GET", "POST"])
def student_preferences(request):
    student_email_id = request.headers.get('studentEmail')
    # student_email_id = request.user_principal_name

    if student_email_id is None:
        return JsonResponse({'message': 'studentEmail is required'}, status=400)

    if request.method == 'POST':
        try:
            # Load the JSON payload from request body
            try:
                payload = json.loads(request.body)
                student_preferences = payload.get('student_preferences')
                if student_preferences is None:
                    return JsonResponse({'message': 'student_preferences is required'}, status=400)

                # Fetch student object using student_email_id
                studentObj = Student.objects.get(student_email=student_email_id)

                # Create a list of preferences as dictionaries
                preferences_list = []
                for pref in student_preferences:
                    category_id = pref.get('id')
                    category_name = pref.get('category_name')
                    if category_id is None or category_name is None:
                        return JsonResponse({'message': 'Each preference must contain id and category_name'},
                                            status=400)

                    # Optionally, validate that the category exists
                    if not Category.objects.filter(id=category_id, category_name=category_name).exists():
                        return JsonResponse(
                            {'message': f'Category with ID {category_id} and name {category_name} does not exist'},
                            status=400)

                    preferences_list.append({
                        'id': category_id,
                        'category_name': category_name
                    })

                studentObj.set_data(preferences_list)
                studentObj.save()
                return JsonResponse({'message': 'Student Preferences Updated!!!'}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON payload'}, status=400)

        except Student.DoesNotExist:
            return JsonResponse({'message': 'Student not found'}, status=404)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    elif request.method == 'GET':
        try:
            # Fetch student object using student_email_id
            studentObj = Student.objects.get(student_email=student_email_id)
            preferences = studentObj.get_preferences()  # Using the method to get preferences as a list of dictionaries

            return JsonResponse({
                'message': 'Success',
                'content': preferences
            }, status=200)

        except Student.DoesNotExist:
            return JsonResponse({'message': 'Student not found'}, status=404)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
