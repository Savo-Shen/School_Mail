"""统一的 API 错误响应格式。

DRF 默认的错误体有好几种形状（字符串、列表、字典嵌套），前端处理起来很麻烦。
这里统一成：

    {
        "detail": "用户名已被注册",      # 一句可以直接展示给用户的中文提示
        "code":   "invalid",            # 机器可读的错误码
        "errors": {"username": ["用户名已被注册"]}   # 字段级错误（表单高亮用），可能为空
    }
"""

import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def _first_message(detail) -> str:
    """从任意形状的 DRF error detail 里取出第一条可读文案。"""
    if isinstance(detail, dict):
        for value in detail.values():
            message = _first_message(value)
            if message:
                return message
        return ""
    if isinstance(detail, list):
        for item in detail:
            message = _first_message(item)
            if message:
                return message
        return ""
    return str(detail)


# simplejwt 的 InvalidToken 把 detail 塞成 {"detail": ..., "code": ...}，
# 这两个键不是表单字段，不应该出现在 errors 里
_NON_FIELD_KEYS = {"detail", "code", "non_field_errors", "messages"}


def _field_errors(detail) -> dict:
    """只有字典形状才有字段级错误。"""
    if isinstance(detail, dict):
        return {
            key: value if isinstance(value, list) else [str(value)]
            for key, value in detail.items()
            if key not in _NON_FIELD_KEYS
        }
    return {}


def api_exception_handler(exc, context):
    # 把 Django 原生异常翻译成 DRF 异常，保证走同一套格式
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)

    if response is None:
        # 未处理的异常：交给 Django 走 500，日志里留全量堆栈
        logger.exception("未处理的服务端异常: %s", exc)
        return None

    detail = getattr(exc, "detail", response.data)

    payload = {
        "detail": _first_message(detail) or "请求失败，请稍后重试",
        "code": getattr(exc, "default_code", "error"),
        "errors": _field_errors(detail),
    }

    # 限流时告诉前端还要等多久
    if isinstance(exc, exceptions.Throttled) and exc.wait:
        payload["retry_after"] = int(exc.wait)
        payload["detail"] = f"操作过于频繁，请 {int(exc.wait)} 秒后再试"

    return Response(payload, status=response.status_code, headers=_safe_headers(response))


def _safe_headers(response) -> dict:
    """保留 DRF 生成的 WWW-Authenticate / Retry-After 等响应头。"""
    return {
        key: value
        for key, value in response.headers.items()
        if key.lower() in {"www-authenticate", "retry-after"}
    }
