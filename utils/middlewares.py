from utils.jwtauth import JWTAuthentication


class LoginMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            JWTAuthentication().authenticate(request)

        if (not request.user) or (not request.user.is_authenticated):
            response = self.get_response(request)
            return response

        response = self.get_response(request)
        return response
