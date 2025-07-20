def user_roles(request):
    user = request.user

    return {
        'is_authenticated': user.is_authenticated,
        'is_partner': getattr(user, 'is_partner', False),
        'is_admin': user.is_superuser,
        'is_staff': user.is_staff,
    }