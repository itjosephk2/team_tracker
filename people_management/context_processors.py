def inject_person(request):
    user = request.user
    person = getattr(user, 'person', None) if user.is_authenticated else None
    return {'person': person}