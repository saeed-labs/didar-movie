error_page 403 = /403.json;
error_page 404 = /404.json;
error_page 413 = /413.json;
error_page 502 = /502.json;
error_page 429 = /429.json;
error_page 503 = /503.json;



location = /403.json {
    internal;
    default_type application/json;
    return 403 '{
        "error": "Forbidden",
        "message": "دسترسی به این بخش برای شما مجاز نیست. در صورت نیاز با پشتیبانی تماس بگیرید.",
        "statusCode": 403
    }';
}

location = /404.json {
    internal;
    default_type application/json;
    return 404 '{"error":"Not Found",
    "message":"مسیر مورد نظر پیدا نشد.",
    "statusCode":404
    }';
}

location = /413.json {
    internal;
    default_type application/json;
    return 413 '{"error":"Request Entity Too Large",
    "message":"حجم درخواست بیش از حد مجاز است.",
    "statusCode":413
    }';
}


location = /502.json {
    internal;
    default_type application/json;
    return 502 '{"error":"Bad Gateway",
    "message":"ارتباط با سرور اصلی برقرار نشد. لطفاً بعداً دوباره تلاش کنید.",
    "statusCode":502
    }';
}


location = /429.json {
    internal;
    default_type application/json;
    return 429 '{"error":"Too Many Requests",
    "message":"تعداد درخواست‌ها بیش از حد مجاز است. لطفاً کمی صبر کنید.",
    "statusCode":429
    }';
}


location = /503.json {
    internal;
    default_type application/json;
    return 503 '{"error":"Service Unavailable",
    "message":"سرویس در حال حاضر در دسترس نیست.",
    "statusCode":503
    }';
}