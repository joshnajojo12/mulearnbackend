from django.apps import AppConfig
from decouple import config


class SystemUserNotFoundError(Exception):
    pass


class DbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "db"

    def ready(self) -> None:
        # from db import organization
        _ready = super().ready()
        self.check_system_user_exists()
        self.run_total_views_migration()
        return _ready

    @staticmethod
    def run_total_views_migration():
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'company_jobs'
                      AND COLUMN_NAME = 'total_views';
                """)
                exists = cursor.fetchone()[0] > 0
                if not exists:
                    cursor.execute("ALTER TABLE company_jobs ADD COLUMN total_views INT NOT NULL DEFAULT 0;")
                    print("[DbConfig] Added column 'total_views' to 'company_jobs' table.")
                
                # Check system settings version update
                cursor.execute("SELECT COUNT(*) FROM system_setting WHERE `key` = 'db.version';")
                has_key = cursor.fetchone()[0] > 0
                if has_key:
                    cursor.execute("UPDATE system_setting SET value = '1.61', updated_at = now() WHERE `key` = 'db.version';")
                    print("[DbConfig] Updated system_setting version to 1.61.")
        except Exception as e:
            print(f"[DbConfig] Migration check skipped: {e}")

    @classmethod
    def check_system_user_exists(cls):
        from db.organization import District as _
        from db.user import User
        if not User.objects.filter(id=config("SYSTEM_ADMIN_ID")).exists():
            raise SystemUserNotFoundError(
                f"Create a System User with pk -\"{config('SYSTEM_ADMIN_ID')}\""
            )
