"""账号相关的 API 视图。

认证方式：JWT（Bearer token）。
前端把 access token 放进 Authorization 头，过期后用 refresh token 换新的。
不使用 Session Cookie —— 前后端分属不同域名时 Cookie 会被浏览器的
SameSite 策略拦掉，JWT 没有这个问题。
"""

import logging

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    DeleteAccountSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ —— 注册新账号。"""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "register"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info("新用户注册: %s", user.username)
        return Response(
            {"detail": "注册成功", "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ —— 用用户名密码换取 access / refresh token。"""

    serializer_class = LoginSerializer
    throttle_scope = "login"


class RefreshView(TokenRefreshView):
    """POST /api/auth/refresh/ —— 用 refresh token 换新的 access token。"""

    serializer_class = RefreshSerializer
    throttle_scope = "login"


class LogoutView(APIView):
    """POST /api/auth/logout/ —— 把 refresh token 拉黑。

    刻意允许匿名调用：access token 已经过期的用户同样需要能登出。
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            # token 已经失效/已拉黑：对调用方来说结果是一样的，按成功处理
            pass
        return Response({"detail": "已登出"}, status=status.HTTP_200_OK)


class MeView(APIView):
    """当前登录用户。

    GET    /api/auth/me/ —— 取用户信息（顺带可以用来校验 token 是否有效）
    DELETE /api/auth/me/ —— 注销账号，需要在请求体里带 password 确认
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_throttles(self):
        # 只对删号做严格限流，读取用户信息走默认限流
        if self.request.method == "DELETE":
            self.throttle_scope = "destructive"
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def delete(self, request):
        serializer = DeleteAccountSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        username = user.username
        # OutstandingToken / BlacklistedToken 都通过外键级联删除，
        # 账号删掉后该用户手上的 refresh token 自然全部失效。
        user.delete()
        logger.warning("用户注销账号: %s", username)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
@throttle_classes([])
def health(request):
    """GET /api/health/ —— 给部署平台做健康检查用。"""
    return Response({"status": "ok"})
