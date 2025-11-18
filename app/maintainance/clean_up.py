import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import WeatherHourly, AirQualityHourly, TrafficHourly

logger = logging.getLogger("Cleanup")

def cleanup_old_data(days=30):
    """
    Deletes data older than X days (default 30).
    Safe for long-term deployment.
    """

    db: Session = SessionLocal()
    cutoff = datetime.utcnow() - timedelta(days=days)

    try:
        db.query(WeatherHourly).filter(WeatherHourly.timestamp < cutoff).delete()
        db.query(TrafficHourly).filter(TrafficHourly.timestamp < cutoff).delete()
        db.query(AirQualityHourly).filter(AirQualityHourly.timestamp < cutoff).delete()
        db.commit()

        logger.info(f"🧹 Cleanup done. Removed entries older than {days} days.")

    except Exception as e:
        logger.exception(f"❌ Cleanup failed: {e}")
        db.rollback()
    finally:
        db.close()
