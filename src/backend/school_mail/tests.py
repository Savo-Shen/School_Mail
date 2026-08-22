"""账号接口的回归测试。

运行：uv run python manage.py test
"""

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

VALID_PASSWORD = "Idec-Ce-2026!"

# 测试里关掉限流，否则跑几个用例就会被 login 10/min、register 5/hour 拦住。
#
# 注意：不能用 override_settings(REST_FRAMEWORK={...}) 改限流阈值 —— DRF 的
# SimpleRateThrottle.THROTTLE_RATES 是在类定义时就绑定到原始 dict 的，
# 改 settings 影响不到它。限流的计数存在 cache 里，换成 DummyCache 即可
# 让每次请求读到的历史都是空的，等价于关闭限流。
NO_THROTTLE = override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
)


@NO_THROTTLE
class HealthTests(APITestCase):
    def test_health_is_public(self):
        response = self.client.get(reverse("school_mail:health"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")


@NO_THROTTLE
class RegisterTests(APITestCase):
    url = None

    def setUp(self):
        self.url = reverse("school_mail:register")

    def test_register_success(self):
        response = self.client.post(
            self.url,
            {"username": "savo", "email": "savo@example.com", "password": VALID_PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"]["username"], "savo")
        # 密码必须是哈希存储，不能是明文
        user = User.objects.get(username="savo")
        self.assertNotEqual(user.password, VALID_PASSWORD)
        self.assertTrue(user.check_password(VALID_PASSWORD))

    def test_duplicate_username_rejected(self):
        User.objects.create_user("savo", "a@example.com", VALID_PASSWORD)
        response = self.client.post(
            self.url,
            {"username": "savo", "email": "b@example.com", "password": VALID_PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "用户名已被注册")
        self.assertIn("username", response.data["errors"])

    def test_duplicate_email_rejected(self):
        User.objects.create_user("a", "savo@example.com", VALID_PASSWORD)
        response = self.client.post(
            self.url,
            {"username": "b", "email": "savo@example.com", "password": VALID_PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "邮箱已被注册")

    def test_weak_password_rejected(self):
        response = self.client.post(
            self.url,
            {"username": "savo", "email": "savo@example.com", "password": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="savo").exists())

    @override_settings(ALLOW_REGISTRATION=False)
    def test_registration_can_be_disabled(self):
        response = self.client.post(
            self.url,
            {"username": "savo", "email": "savo@example.com", "password": VALID_PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@NO_THROTTLE
class AuthFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("savo", "savo@example.com", VALID_PASSWORD)
        self.login_url = reverse("school_mail:login")
        self.me_url = reverse("school_mail:me")

    def _login(self):
        response = self.client.post(
            self.login_url,
            {"username": "savo", "password": VALID_PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_login_returns_tokens_and_user(self):
        data = self._login()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertEqual(data["user"]["username"], "savo")

    def test_login_with_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"username": "savo", "password": "wrong-password"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "账号或密码错误")

    def test_me_requires_authentication(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_with_token(self):
        access = self._login()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "savo")

    def test_refresh_rotates_token(self):
        refresh = self._login()["refresh"]
        response = self.client.post(
            reverse("school_mail:token-refresh"), {"refresh": refresh}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        # 开启了轮换，旧 refresh 应当已经失效
        replay = self.client.post(
            reverse("school_mail:token-refresh"), {"refresh": refresh}, format="json"
        )
        self.assertEqual(replay.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_blacklists_refresh_token(self):
        refresh = self._login()["refresh"]
        response = self.client.post(
            reverse("school_mail:logout"), {"refresh": refresh}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reuse = self.client.post(
            reverse("school_mail:token-refresh"), {"refresh": refresh}, format="json"
        )
        self.assertEqual(reuse.status_code, status.HTTP_401_UNAUTHORIZED)


@NO_THROTTLE
class DeleteAccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("savo", "savo@example.com", VALID_PASSWORD)
        self.me_url = reverse("school_mail:me")
        response = self.client.post(
            reverse("school_mail:login"),
            {"username": "savo", "password": VALID_PASSWORD},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_delete_requires_correct_password(self):
        response = self.client.delete(self.me_url, {"password": "wrong"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "密码错误")
        self.assertTrue(User.objects.filter(username="savo").exists())

    def test_delete_success(self):
        response = self.client.delete(
            self.me_url, {"password": VALID_PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username="savo").exists())

    def test_delete_requires_authentication(self):
        self.client.credentials()
        response = self.client.delete(
            self.me_url, {"password": VALID_PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_endpoint_leaks_user_list(self):
        """旧版本有个 /api/account_list/ 会把所有用户名+邮箱吐出来，确认已经移除。"""
        for path in ("/api/account_list/", "/api/auth/account_list/"):
            self.assertEqual(self.client.get(path).status_code, status.HTTP_404_NOT_FOUND)


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
)
class ThrottleTests(APITestCase):
    """确认防暴力破解的限流是真的生效的（这里刻意不关限流）。"""

    def setUp(self):
        from django.core.cache import cache

        cache.clear()
        User.objects.create_user("savo", "savo@example.com", VALID_PASSWORD)

    def test_login_is_rate_limited(self):
        url = reverse("school_mail:login")
        payload = {"username": "savo", "password": "wrong-password"}

        statuses = [self.client.post(url, payload, format="json").status_code for _ in range(12)]

        self.assertIn(
            status.HTTP_429_TOO_MANY_REQUESTS,
            statuses,
            "登录接口没有限流，存在被暴力破解的风险",
        )
        throttled = self.client.post(url, payload, format="json")
        self.assertEqual(throttled.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn("retry_after", throttled.data)


@NO_THROTTLE
class DeletedUserTokenTests(APITestCase):
    """账号注销后，客户端往往还留着 token。这些请求必须干净地返回 401，
    而不是 500 —— 500 会让前端拿不到明确信号，用户卡在坏状态里出不来。"""

    def setUp(self):
        from rest_framework_simplejwt.tokens import RefreshToken

        user = User.objects.create_user("ghost", "ghost@example.com", VALID_PASSWORD)
        token = RefreshToken.for_user(user)
        self.refresh = str(token)
        self.access = str(token.access_token)
        user.delete()

    def test_refresh_with_deleted_user_returns_401(self):
        response = self.client.post(
            reverse("school_mail:token-refresh"), {"refresh": self.refresh}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_me_with_deleted_user_returns_401(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.get(reverse("school_mail:me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_deleted_user_does_not_error(self):
        response = self.client.post(
            reverse("school_mail:logout"), {"refresh": self.refresh}, format="json"
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED),
            f"登出不应该抛 500，实际返回 {response.status_code}",
        )
