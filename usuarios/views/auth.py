from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from usuarios.permissions import IsAdmin, IsManager, IsAccountant
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from ..models import CustomUser   # Importar desde el módulo de usuarios
from ..serializers import SerializadorUsuario, UsuarioSerializer  # Importar desde el módulo de usuarios
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view


class ListarUsuarios(generics.ListAPIView):
    queryset = CustomUser.objects.all()  # Obtener todos los usuarios
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminUser]  # Solo accesible para administradores

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "¡Hola, administrador!"})

# Vista para módulos de estadísticas (gerente)
class ManagerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsManager]

    # Lógica para reportes y estadísticas
    def get(self, request):
        return Response({"message": "¡Hola, gerente!"})

# Vista para módulos financieros (contador)
class AccountantView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsAccountant]

    # Lógica para datos contables
    def get(self, request):
        return Response({"message": "¡Hola, contador!"})
        

class FinancialSummaryView(APIView):
    """
    Permite a los administradores, contadores y gerentes ver un resumen financiero.
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | IsAccountant]

    def get(self, request):
        # Lógica para mostrar un resumen financiero
        return Response({"message": "Resumen financiero"})


class VistaRegistroUsuario(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SerializadorUsuario
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        # Verificar el rol del usuario
        if usuario.role not in ['gerente', 'contador']:
            return Response({'error': 'Solo se pueden registrar gerentes y contadores.'}, status=400)

        # Generar el token JWT
        refresh = RefreshToken.for_user(usuario)

        # Devolver la respuesta con el token
        return Response({
            'message': 'Usuario registrado exitosamente.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': usuario.role
        }, status=status.HTTP_201_CREATED)


class VistaCerrarSesion(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # Asegúrate de que el usuario esté autenticado

    def post(self, request, *args, **kwargs):
        try:
            # Obtener el token de refresco del cuerpo de la solicitud
            refresh_token = request.data.get('refresh')

            # Marcar el token de refresco como inválido
            token = OutstandingToken.objects.get(token=refresh_token)
            BlacklistedToken.objects.create(token=token)

            return Response({'message': 'Sesión cerrada exitosamente.'}, status=204)
        except OutstandingToken.DoesNotExist:
            return Response({'error': 'Token no encontrado.'}, status=404)



class VistaRecursoProtegido(APIView):
    permission_classes = [IsAuthenticated]  # Solo accesible para usuarios autenticados

    def get(self, request, *args, **kwargs):
        # Aquí puedes incluir la lógica para obtener los datos que deseas proteger
        data = {
            "message": "Este es un recurso protegido.",
            "user": request.user.username,  # Puedes acceder a la información del usuario autenticado
        }
        return Response(data, status=200)


class VistaLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'role': user.role,
                })
            else:
                return Response({'error': 'Credenciales incorrectas.'}, status=400)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=404)


@api_view(['POST'])
def validar_token(request):
    token = request.data.get('token')

    try:
        # Verificar el token
        validated_token = JWTAuthentication().get_validated_token(token)
        return Response({'message': 'Token válido', 'token': validated_token}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


class VistaRegistroUsuario(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SerializadorUsuario
    permission_classes = [AllowAny]  # Permitir registro sin autenticación

class VistaObtenerToken(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            usuario = CustomUser.objects.get(username=username)
            if usuario.check_password(password):
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'rol': usuario.role,
                    'redirect_url': '/validar-token/'
                })
            else:
                return Response({'error': 'Credenciales incorrectas'}, status=400)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
