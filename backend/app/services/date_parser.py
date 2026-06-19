from datetime import datetime, timedelta
import calendar

def parse_date_range(prompt: str) -> dict | None:
    text = prompt.lower()
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    start_time = None
    end_time = None

    if "today" in text:
        start_time = today_start
        end_time = today_start + timedelta(days=1)
    
    elif "yesterday" in text:
        start_time = today_start - timedelta(days=1)
        end_time = today_start
    
    elif "last 7 days" in text:
        start_time = today_start - timedelta(days=7)
        end_time = today_start + timedelta(days=1)
    
    elif "last 30 days" in text:
        start_time = today_start - timedelta(days=30)
        end_time = today_start + timedelta(days=1)
    
    elif "this week" in text:
        # Monday is 0, Sunday is 6
        start_time = today_start - timedelta(days=today_start.weekday())
        end_time = start_time + timedelta(days=7)
        
    elif "last week" in text:
        start_time = today_start - timedelta(days=today_start.weekday() + 7)
        end_time = start_time + timedelta(days=7)
        
    elif "this month" in text:
        start_time = today_start.replace(day=1)
        # Add a month
        next_month = start_time.replace(day=28) + timedelta(days=4)
        end_time = next_month.replace(day=1)
        
    elif "last month" in text:
        this_month_start = today_start.replace(day=1)
        last_month_end = this_month_start - timedelta(days=1)
        start_time = last_month_end.replace(day=1)
        end_time = this_month_start
        
    elif "this year" in text:
        start_time = today_start.replace(month=1, day=1)
        end_time = start_time.replace(year=start_time.year + 1)

    if start_time and end_time:
        return {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": "Asia/Jakarta",
            "source": "rule_based"
        }
    
    # Default Date Range: Last 30 days
    start_time_default = today_start - timedelta(days=30)
    end_time_default = today_start + timedelta(days=1)
    
    return {
        "start_time": start_time_default.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time_default.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "Asia/Jakarta",
        "source": "default"
    }
