from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class IsTokenValid(BasePermission):
    """
    Verifica se o token do usuário é válido e se é o último token emitido
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        jwt_auth = JWTAuthentication()

        try:
            header = jwt_auth.get_header(request)
            if not header:
                return False

            raw_token = jwt_auth.get_raw_token(header)
            if not raw_token:
                return False

            validated_token = jwt_auth.get_validated_token(raw_token)
            jti = validated_token['jti']

            # Verifica se o token está na blacklist
            token = OutstandingToken.objects.filter(jti=jti).first()
            if not token:
                return False

            if BlacklistedToken.objects.filter(token=token).exists():
                return False

            # Verifica se é o último token válido do usuário
            if jti != user.token_jti:
                return False

            return True
        except Exception as e:
            print(f'IsTokenValid ERROR - {str(e)}')
            return False
