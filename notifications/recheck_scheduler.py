from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from notifications.whatsapp_notifier import WhatsAppNotifier

scheduler = BackgroundScheduler()
scheduler.start()

notifier = WhatsAppNotifier()


def schedule_recheck(symbol: str, advice: dict):
    minutes = advice["estimated_wait_minutes"]

    run_time = datetime.utcnow() + timedelta(minutes=minutes)

    message = (
        f"📊 Trading Bot Reminder\n\n"
        f"Symbol: {symbol}\n"
        f"Market State: {advice['market_state']}\n"
        f"Reason: {advice['next_check_hint']}\n\n"
        f"⏰ Time to re-check now ({advice['recheck_timeframe']})"
    )

    scheduler.add_job(
        notifier.send,
        "date",
        run_date=run_time,
        args=[message],
        id=f"{symbol}_{run_time.timestamp()}",
        replace_existing=False
    )
