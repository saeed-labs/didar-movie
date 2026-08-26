from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class JsonResponse404Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return JsonResponse({
                'error': 'صفحه مورد نظر یافت نشد',
                'message': 'صفحه مورد نظر شما وجود ندارد یا حذف شده است',
                'statusCode': 404
            }, status=404)
        return response


class JsonResponse403Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 403:
            return JsonResponse({
                'error': 'دسترسی غیرمجاز',
                'message': 'شما اجازه دسترسی به این صفحه را ندارید',
                'statusCode': 403
            }, status=403)
        return response