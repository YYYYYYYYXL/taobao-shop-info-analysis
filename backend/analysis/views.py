from django.http import JsonResponse
import pandas as pd
from pathlib import Path
from src.data_analysis import run_all_analysis




def analysis_summary(request):
    # 1. 先找到 cleaned_data.csv 的绝对路径
    # Path(__file__) 表示当前这个 views.py 文件
    # resolve() 表示拿到完整绝对路径
    # parent.parent 表示回到 backend 目录
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / 'data' / 'cleaned_data.csv'

    # 2. 读取清洗后的数据
    df = pd.read_csv(file_path)

    # 3. 调用你原来的分析函数
    results = run_all_analysis(df)

    # 4. 因为 results 里的值是 DataFrame，不能直接返回 JSON
    # 所以这里把每个 DataFrame 转成 records 格式
    json_results = {}
    limit_map = {
        'category_sales': 10,
        'province_sales': 10,
        'shop_sales': 20,
        'style_price': 15,
        'pattern_price': 15,
        'fabric_price': 15,
        'fit_price': 10,
    }
    for key, value in results.items():
        limit = limit_map.get(key,10)
        json_results[key] = value.head(limit).to_dict(orient='records')

    # 5. 返回给前端
    return JsonResponse({
        'code': 200,
        'msg': 'success',
        'data': json_results
    }, json_dumps_params={'ensure_ascii': False})

import json
import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from .models import AppUser


def api_response(code="0", msg="success", data=None, request=None, status=200):
    return JsonResponse(
        {
            "code": code,
            "msg": msg,
            "data": data,
            "deviceId": request.headers.get("X-Device-Id", "") if request else "",
        },
        json_dumps_params={"ensure_ascii": False},
        status=status,
    )


def parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def build_menu_tree(role):
    menu_list = [
        {
            "id": 100,
            "name": "个人信息",
            "path": "/person-info",
            "icon": "user",
            "pagePath": "PersonInfo",
            "role": "USER",
        },
        {
            "id": 101,
            "name": "修改密码",
            "path": "/password",
            "icon": "lock",
            "pagePath": "Password",
            "role": "USER",
        },
        {
            "id": 200,
            "name": "分析视图",
            "icon": "data-analysis",
            "children": [
                {
                    "id": 201,
                    "pid": 200,
                    "name": "分类销量分析",
                    "path": "/analysis-category-sales",
                    "icon": "pie-chart",
                    "pagePath": "analysis/AnalysisCategorySales",
                    "role": "USER",
                }
            ],
        },
    ]
    if role == "ADMIN":
        menu_list.insert(
            0,
            {
                "id": 102,
                "name": "用户管理",
                "path": "/user-manager",
                "icon": "s-custom",
                "pagePath": "UserManager",
                "role": "ADMIN",
            },
        )
    return menu_list


def user_to_dict(user, include_menu=False):
    data = {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "token": user.token or "",
        "avatar": user.avatar,
        "createdAt": user.created_at.isoformat() if user.created_at else None,
    }
    if include_menu:
        data["menuList"] = build_menu_tree(user.role)
    return data


def get_current_user(request, user_id=None):
    token = request.headers.get("token", "").strip()
    if not token:
        return None
    queryset = AppUser.objects.filter(token=token, status=1)
    if user_id is not None:
        queryset = queryset.filter(id=user_id)
    return queryset.first()


@csrf_exempt
def analysis_summary(request):
      base_dir = Path(__file__).resolve().parent.parent
      file_path = base_dir / "data" / "cleaned_data.csv"

      df = pd.read_csv(file_path)
      results = run_all_analysis(df)

      raw_data = results["category_sales"].head(10).copy()
      raw_data.columns = ["name", "value"]

      data = raw_data.to_dict(orient="records")
      return api_response(data=data, request=request)



@csrf_exempt
def analysis_province_sales(request):
      base_dir = Path(__file__).resolve().parent.parent
      file_path = base_dir / "data" / "cleaned_data.csv"

      df = pd.read_csv(file_path)
      results = run_all_analysis(df)

      raw_data = results["province_sales"].head(10).copy()
      raw_data.columns = ["name", "value"]

      data = raw_data.to_dict(orient="records")
      return api_response(data=data, request=request)


@csrf_exempt
def analysis_shop_sales(request):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / "cleaned_data.csv"

    df = pd.read_csv(file_path)
    results = run_all_analysis(df)

    raw_data = results["shop_sales"].head(20).copy()
    raw_data.columns = ["name", "value"]

    data = raw_data.to_dict(orient="records")
    return api_response(data=data, request=request)


@csrf_exempt
def analysis_style_price(request):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / "cleaned_data.csv"

    df = pd.read_csv(file_path)
    results = run_all_analysis(df)

    raw_data = results["style_price"].head(15).copy()
    raw_data.columns = ["name", "value"]

    data = raw_data.to_dict(orient="records")
    return api_response(data=data, request=request)


@csrf_exempt
def analysis_pattern_price(request):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / "cleaned_data.csv"

    df = pd.read_csv(file_path)
    results = run_all_analysis(df)

    raw_data = results["pattern_price"].head(15).copy()
    raw_data.columns = ["name", "value"]

    data = raw_data.to_dict(orient="records")
    return api_response(data=data, request=request)


@csrf_exempt
def analysis_fabric_price(request):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / "cleaned_data.csv"

    df = pd.read_csv(file_path)
    results = run_all_analysis(df)

    raw_data = results["fabric_price"].head(15).copy()
    raw_data.columns = ["name", "value"]

    data = raw_data.to_dict(orient="records")
    return api_response(data=data, request=request)


@csrf_exempt
def analysis_fit_price(request):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / "cleaned_data.csv"

    df = pd.read_csv(file_path)
    results = run_all_analysis(df)

    raw_data = results["fit_price"].head(10).copy()
    raw_data.columns = ["name", "value"]

    data = raw_data.to_dict(orient="records")
    return api_response(data=data, request=request)




@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return api_response(code="1", msg="请求方式错误", request=request, status=405)

    payload = parse_json_body(request)
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    role = str(payload.get("role", "USER")).strip() or "USER"
    status_value = int(payload.get("status", 1) or 1)

    if not all([username, password, name, email]):
        return api_response(code="1", msg="请完整填写注册信息", request=request)
    if len(username) < 3 or len(password) < 6:
        return api_response(code="1", msg="用户名或密码长度不符合要求", request=request)
    if AppUser.objects.filter(username=username).exists():
        return api_response(code="1", msg="用户名已存在", request=request)
    if AppUser.objects.filter(email=email).exists():
        return api_response(code="1", msg="邮箱已存在", request=request)

    user = AppUser.objects.create(
        username=username,
        password=make_password(password),
        name=name,
        email=email,
        role=role if role in {"ADMIN", "USER"} else "USER",
        status=1 if status_value == 1 else 0,
        device_id=request.headers.get("X-Device-Id", ""),
    )
    return api_response(msg="注册成功", data=user_to_dict(user), request=request)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return api_response(code="1", msg="请求方式错误", request=request, status=405)

    payload = parse_json_body(request)
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()
    user = AppUser.objects.filter(username=username).first()

    if not user or not check_password(password, user.password):
        return api_response(code="1", msg="用户名或密码错误", request=request)
    if user.status != 1:
        return api_response(code="1", msg="账号已被禁用", request=request)

    user.token = uuid.uuid4().hex
    user.device_id = request.headers.get("X-Device-Id", "")
    user.save(update_fields=["token", "device_id", "updated_at"])

    return api_response(msg="登录成功", data=user_to_dict(user, include_menu=True), request=request)


@csrf_exempt
def user_page(request):
    current_user = get_current_user(request)
    if not current_user:
        return api_response(code="401", msg="未登录或登录已失效", request=request, status=401)

    current_page = int(request.GET.get("currentPage", 1) or 1)
    size = int(request.GET.get("size", 10) or 10)
    username = str(request.GET.get("username", "")).strip()
    role = str(request.GET.get("role", "")).strip()
    status_value = request.GET.get("status", "")

    queryset = AppUser.objects.all()
    if current_user.role != "ADMIN":
        queryset = queryset.filter(id=current_user.id)
    if username:
        queryset = queryset.filter(username__icontains=username)
    if role:
        queryset = queryset.filter(role=role)
    if status_value != "":
        queryset = queryset.filter(status=int(status_value))

    total = queryset.count()
    start = max(current_page - 1, 0) * size
    records = [user_to_dict(item) for item in queryset[start : start + size]]
    return api_response(data={"records": records, "total": total}, request=request)


@csrf_exempt
def update_user(request, user_id):
    current_user = get_current_user(request)
    if not current_user:
        return api_response(code="401", msg="未登录或登录已失效", request=request, status=401)
    if request.method != "PUT":
        return api_response(code="1", msg="请求方式错误", request=request, status=405)

    target_user = AppUser.objects.filter(id=user_id).first()
    if not target_user:
        return api_response(code="1", msg="用户不存在", request=request, status=404)
    if current_user.role != "ADMIN" and current_user.id != target_user.id:
        return api_response(code="403", msg="无权限操作该用户", request=request, status=403)

    payload = parse_json_body(request)
    fields_to_update = []

    if "name" in payload:
        target_user.name = str(payload.get("name", "")).strip() or target_user.name
        fields_to_update.append("name")
    if "email" in payload:
        email = str(payload.get("email", "")).strip()
        if email and AppUser.objects.filter(email=email).exclude(id=target_user.id).exists():
            return api_response(code="1", msg="邮箱已存在", request=request)
        if email:
            target_user.email = email
            fields_to_update.append("email")
    if "avatar" in payload:
        target_user.avatar = payload.get("avatar") or None
        fields_to_update.append("avatar")
    if current_user.role == "ADMIN":
        if "role" in payload:
            role = str(payload.get("role", "")).strip()
            if role in {"ADMIN", "USER"}:
                target_user.role = role
                fields_to_update.append("role")
        if "status" in payload:
            target_user.status = 1 if int(payload.get("status", 1)) == 1 else 0
            fields_to_update.append("status")

    if fields_to_update:
        fields_to_update.append("updated_at")
        target_user.save(update_fields=fields_to_update)

    return api_response(msg="保存成功", data=user_to_dict(target_user), request=request)


@csrf_exempt
def update_password(request, user_id):
    current_user = get_current_user(request, user_id=user_id)
    if not current_user:
        return api_response(code="401", msg="未登录或登录已失效", request=request, status=401)
    if request.method != "PUT":
        return api_response(code="1", msg="请求方式错误", request=request, status=405)

    payload = parse_json_body(request)
    old_password = str(payload.get("oldPassword", "")).strip()
    new_password = str(payload.get("newPassword", "")).strip()
    confirm_password = str(payload.get("confirmPassword", "")).strip()

    if not check_password(old_password, current_user.password):
        return api_response(code="1", msg="原密码错误", request=request)
    if len(new_password) < 6:
        return api_response(code="1", msg="新密码长度不能少于6位", request=request)
    if new_password != confirm_password:
        return api_response(code="1", msg="两次输入的新密码不一致", request=request)

    current_user.password = make_password(new_password)
    current_user.token = ""
    current_user.save(update_fields=["password", "token", "updated_at"])
    return api_response(msg="密码修改成功", request=request)


@csrf_exempt
def upload_avatar(request, user_id):
    current_user = get_current_user(request, user_id=user_id)
    if not current_user:
        return api_response(code="401", msg="未登录或登录已失效", request=request, status=401)
    if request.method != "POST":
        return api_response(code="1", msg="请求方式错误", request=request, status=405)

    file = request.FILES.get("file")
    if not file:
        return api_response(code="1", msg="未接收到头像文件", request=request)

    avatar_root = settings.MEDIA_ROOT / "avatars"
    avatar_root.mkdir(parents=True, exist_ok=True)
    storage = FileSystemStorage(location=avatar_root, base_url=f"{settings.MEDIA_URL}avatars/")
    filename = storage.save(f"{uuid.uuid4().hex}_{file.name}", file)
    current_user.avatar = storage.url(filename)
    current_user.save(update_fields=["avatar", "updated_at"])
    return api_response(msg="头像上传成功", data=user_to_dict(current_user), request=request)


@csrf_exempt
def delete_user(request, user_id):
    current_user = get_current_user(request)
    if not current_user:
        return api_response(code="401", msg="未登录或登录已失效", request=request, status=401)
    if current_user.role != "ADMIN":
        return api_response(code="403", msg="无权限删除用户", request=request, status=403)
    if request.method != "DELETE":
        return api_response(code="1", msg="请求方式错误", request=request, status=405)

    target_user = AppUser.objects.filter(id=user_id).first()
    if not target_user:
        return api_response(code="1", msg="用户不存在", request=request, status=404)
    target_user.delete()
    return api_response(msg="删除成功", request=request)


@csrf_exempt
def menu_tree(request, user_id):
    current_user = get_current_user(request)
    if not current_user:
        return api_response(code="401", msg="未登录或登录已失效", request=request, status=401)
    if current_user.role != "ADMIN" and current_user.id != user_id:
        return api_response(code="403", msg="无权限查看菜单", request=request, status=403)
    return api_response(data=build_menu_tree(current_user.role), request=request)


@csrf_exempt
def actionlog_statistics(request):
    user_total = AppUser.objects.count()
    active_users = AppUser.objects.filter(status=1).count()

    return api_response(
        data={
            "totalPageViews": 0,
            "totalLogs": 0,
            "todayActiveUsers": active_users,
            "todayViews": user_total,
        },
        request=request
    )


@csrf_exempt
def actionlog_page_ranking(request):
      data = [
          {"rank": 1, "pageName": "首页", "count": 120},
          {"rank": 2, "pageName": "用户管理", "count": 88},
          {"rank": 3, "pageName": "数据管理", "count": 76},
          {"rank": 4, "pageName": "分类销量分析", "count": 63},
          {"rank": 5, "pageName": "店铺销量分析", "count": 52},
      ]
      return api_response(data=data, request=request)


@csrf_exempt
def actionlog_weekly_data(request):
      data = [
          {"day": "周一", "count": 12},
          {"day": "周二", "count": 18},
          {"day": "周三", "count": 15},
          {"day": "周四", "count": 22},
          {"day": "周五", "count": 30},
          {"day": "周六", "count": 26},
          {"day": "周日", "count": 19},
      ]
      return api_response(data=data, request=request)



@csrf_exempt
def actionlog_monthly_day_data(request):
      data = [
          {"day": "1日", "count": 5},
          {"day": "5日", "count": 9},
          {"day": "10日", "count": 13},
          {"day": "15日", "count": 18},
          {"day": "20日", "count": 14},
          {"day": "25日", "count": 21},
          {"day": "30日", "count": 17},
      ]
      return api_response(data=data, request=request)