"""账号相关的序列化器。"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

User = get_user_model()


# Django 自带的中文翻译对 password_too_short 是缺失的（会回落成英文），
# 这里按错误码统一接管文案，不依赖 locale 文件的完整度。
PASSWORD_ERROR_MESSAGES = {
    "password_too_short": "密码至少需要 8 个字符",
    "password_too_common": "密码过于常见，请换一个",
    "password_entirely_numeric": "密码不能全部是数字",
    "password_too_similar": "密码和用户名或邮箱太相似",
}


def _password_messages(exc: DjangoValidationError) -> list[str]:
    messages = []
    for error in exc.error_list:
        messages.append(PASSWORD_ERROR_MESSAGES.get(error.code) or "".join(error.messages))
    return messages



class UserSerializer(serializers.ModelSerializer):
    """对外暴露的用户信息，只包含用户自己可见的字段。"""

    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined", "is_staff")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    # 显式声明 username，去掉 ModelSerializer 自动加上的 UniqueValidator
    # （它的报错文案是 Django 内置的“已存在一位使用该名字的用户。”，
    #   我们在 validate_username 里给出统一的中文提示）
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value: str) -> str:
        value = value.strip()
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("用户名已被注册")
        return value

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(_password_messages(exc)) from exc
        return value

    def validate(self, attrs):
        if not settings.ALLOW_REGISTRATION:
            raise serializers.ValidationError("当前暂未开放注册")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    """在标准 JWT 登录响应里附带用户信息，省掉前端登录后再请求一次 /me/。"""

    default_error_messages = {
        "no_active_account": "账号或密码错误",
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class RefreshSerializer(TokenRefreshSerializer):
    """把「用户已被删除」翻译成 401，而不是 500。

    开启 ROTATE_REFRESH_TOKENS 后，simplejwt 会在刷新时反查用户以检查 is_active，
    但没有捕获 User.DoesNotExist。用户注销账号后本地往往还留着 refresh token，
    再刷新就会打出一个 500。对调用方来说这就是一个失效的 token，应该返回 401。
    """

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except User.DoesNotExist as exc:
            raise InvalidToken("用户不存在或已注销") from exc


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class DeleteAccountSerializer(serializers.Serializer):
    """注销账号必须重新输入密码确认，避免 token 被盗后直接删号。"""

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate_password(self, value: str) -> str:
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("密码错误")
        return value
