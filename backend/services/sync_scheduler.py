"""Background scheduler for real-time data synchronization."""
import schedule
import time
import threading
from .realtime_sync import RealtimeDataSync

class DataSyncScheduler:
    """Schedule periodic data syncs in background."""
    
    def __init__(self, interval_minutes=30):
        self.syncer = RealtimeDataSync()
        self.interval_minutes = interval_minutes
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the background sync scheduler."""
        if self.running:
            print("⚠️  Scheduler already running")
            return
            
        self.running = True
        
        # Schedule sync every N minutes
        schedule.every(self.interval_minutes).minutes.do(self._sync_job)
        
        # Run initial sync immediately
        print(f"🚀 Starting data sync scheduler (every {self.interval_minutes} minutes)")
        self._sync_job()
        
        # Start background thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        print(f"✅ Scheduler started in background")
        
    def _sync_job(self):
        """Job to run on schedule."""
        try:
            print(f"\n⏰ Scheduled sync triggered at {time.strftime('%H:%M:%S')}")
            self.syncer.sync_all()
        except Exception as e:
            print(f"❌ Sync job failed: {e}")
            
    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🛑 Scheduler stopped")


# Global scheduler instance
_scheduler = None

def start_sync_scheduler(interval_minutes=30):
    """Start the global sync scheduler."""
    global _scheduler
    if _scheduler is None:
        _scheduler = DataSyncScheduler(interval_minutes)
        _scheduler.start()
    return _scheduler

def stop_sync_scheduler():
    """Stop the global sync scheduler."""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
        _scheduler = None
