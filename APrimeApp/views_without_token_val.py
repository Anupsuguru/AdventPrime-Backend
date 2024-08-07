import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction


def index(request):
    try:
        # Extract student email from headers
        student_email_id = request.headers.get('studentEmail')

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


@csrf_exempt
@require_http_methods(["GET", "POST"])
def student_preferences(request):
    student_email_id = request.headers.get('studentEmail')

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
                    color_code = pref.get('color_code', '')
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
                        'category_name': category_name,
                        'color_code': color_code
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


@require_http_methods(["GET"])
def get_workshop_details(request, workshop_id):
    try:
        # Fetch the workshop object by ID
        workshop = Workshop.objects.get(id=workshop_id)

        # Serialize the workshop object
        workshop_details = {
            'id': str(workshop.id),
            'workshop_name': workshop.workshop_name,
            'conducted_by': workshop.conducted_by,
            'conducted_by_department': workshop.conducted_by_department_id.department_name,
            'workshop_date': workshop.workshop_date.isoformat(),
            'workshop_start_time': workshop.workshop_start_time.isoformat(),
            'workshop_end_time': workshop.workshop_end_time.isoformat(),
            'workshop_location': workshop.workshop_location,
            'resource': workshop.resource,
            'category': workshop.category.category_name
        }

        return JsonResponse({
            'message': 'Success',
            'content': workshop_details
        }, status=200)

    except Workshop.DoesNotExist:
        return JsonResponse({'message': 'Workshop not found'}, status=404)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@require_http_methods(['GET'])
def get_all_workshops(request, preference_id: int = -1):
    try:
        if preference_id >= 0:
            workshops = Workshop.objects.filter(id=preference_id)
        else:
            workshops = Workshop.objects.all()
        workshop_details: list[dict] = list()

        for workshop in workshops:
            workshop_details.append({
                'id': str(workshop.id),
                'workshop_name': workshop.workshop_name,
                'conducted_by': workshop.conducted_by,
                'workshop_date': workshop.workshop_date.isoformat(),
                'workshop_start_time': workshop.workshop_start_time.isoformat(),
                'workshop_end_time': workshop.workshop_end_time.isoformat(),
                'workshop_location': workshop.workshop_location,
                'resource': workshop.resource,
                'category': workshop.category.category_name,
                'conducted_by_department': workshop.conducted_by_department_id.department_name,
                'description': workshop.description,
            })
        # Serialize the workshop object

        return JsonResponse({
            'message': 'Success',
            'content': workshop_details
        }, status=200)

    except Workshop.DoesNotExist:
        return JsonResponse({'message': 'Workshop not found'}, status=404)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def register_for_workshop(request):
    try:
        student_email_id = request.headers.get('studentEmail')

        # Load JSON payload from request body
        payload = json.loads(request.body)
        workshop_id = payload.get('workshopId')
        status = payload.get('status')  # Can be 'confirmed' or 'waitlisted'

        if not student_email_id or not workshop_id or not status:
            return JsonResponse({'message': 'studentEmail, workshopId, and status are required'}, status=400)

        # Fetch student and workshop objects
        student = get_object_or_404(Student, student_email=student_email_id)
        workshop = get_object_or_404(Workshop, id=workshop_id)

        # Start a transaction to lock the Registration row exclusively
        with transaction.atomic():
            # Fetch or create the registration object with locking
            registration, created = Registration.objects.select_for_update().get_or_create(
                workshop=workshop,
                defaults={
                    'waitlist': json.dumps([]),
                    'confirmed_registration': json.dumps([]),
                    'total_seats': workshop.total_seats,  # Use actual workshop capacity
                    'seats_filled': 0,
                    'seats_available': workshop.total_seats  # Initial seats available should match total seats
                }
            )

            if status == 'confirmed':
                confirmed_list = registration.get_confirmed_registration()
                if student_email_id in confirmed_list:
                    return JsonResponse({'message': 'Already registered'}, status=400)
                if registration.seats_available <= 0:
                    return JsonResponse({'message': 'No seats available'}, status=400)
                confirmed_list.append(student_email_id)
                registration.set_confirmed_registration(confirmed_list)
                registration.seats_filled += 1
                registration.seats_available -= 1

                # Update Student table
                student.no_of_workshop_scheduled += 1

            elif status == 'waitlisted':
                waitlist = registration.get_waitlist()
                if student_email_id in waitlist:
                    return JsonResponse({'message': 'Already waitlisted'}, status=400)
                waitlist.append(student_email_id)
                registration.set_waitlist(waitlist)
                student.no_of_workshop_waitlisted += 1

            else:
                return JsonResponse({'message': 'Invalid status'}, status=400)

            # Save the registration and student within the transaction
            registration.save()
            student.save()

        return JsonResponse({'message': 'Registered successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON payload'}, status=400)
    except Student.DoesNotExist:
        return JsonResponse({'message': 'Student not found'}, status=404)
    except Workshop.DoesNotExist:
        return JsonResponse({'message': 'Workshop not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def upcoming_registered_workshops(request):
    try:
        student_email_id = request.headers.get('studentEmail')

        if not student_email_id:
            return JsonResponse({'message': 'studentEmail is required'}, status=400)

        # Fetch student object
        student = get_object_or_404(Student, student_email=student_email_id)

        # Fetch registrations for the student
        registrations = Registration.objects.filter(
            confirmed_registration__contains=student_email_id
        )

        # Get current date and time
        current_time = timezone.now()

        # Filter and sort upcoming workshops
        upcoming_workshops = [
            {
                'id': str(registration.workshop.id),
                'workshop_name': registration.workshop.workshop_name,
                'conducted_by': registration.workshop.conducted_by,
                'workshop_date': registration.workshop.workshop_date.isoformat(),
                'workshop_start_time': registration.workshop.workshop_start_time.isoformat(),
                'workshop_end_time': registration.workshop.workshop_end_time.isoformat(),
                'workshop_location': registration.workshop.workshop_location,
                'resource': registration.workshop.resource,
                'category': registration.workshop.category.category_name,
                'conducted_by_department': registration.workshop.conducted_by_department_id.department_name,
                'description': registration.workshop.description,
            }
            for registration in registrations
            if registration.workshop.workshop_date >= current_time.date()
        ]

        # Sort workshops by date and time
        upcoming_workshops.sort(key=lambda x: (x['workshop_date'], x['workshop_start_time']))

        return JsonResponse({
            'message': 'Success',
            'content': upcoming_workshops
        }, status=200)

    except Student.DoesNotExist:
        return JsonResponse({'message': 'Student not found'}, status=404)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


def cancel_workshop(request, workshop_id:int):
    try:
        student_email_id = request.headers.get('studentEmail')

        if not student_email_id:
            return JsonResponse({'message': 'studentEmail is required'}, status=400)

        # Fetch student object
        student = get_object_or_404(Student, student_email=student_email_id)

        # Fetch registrations for the student
        registrations = Registration.objects.get(
            confirmed_registration__contains=student_email_id,
            workshop__id=workshop_id
        )
        registrations.confirmed_registration.replace(student_email_id, "")
        registrations.seats_available += 1
        registrations.save()

    except Student.DoesNotExist:
        return JsonResponse({'message': 'Student not found'}, status=404)

    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
