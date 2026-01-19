"""
Database initialization script
"""
import json
from sqlalchemy.orm import Session
from app.db.base import Base, engine, SessionLocal
from app.models import Role, User, SystemConfig
from app.core.security import get_password_hash


def init_roles(db: Session):
    """Initialize default roles"""
    roles_data = [
        {
            "name": "admin",
            "display_name": "管理员",
            "description": "拥有所有权限",
            "permissions": json.dumps(["*"])
        },
        {
            "name": "developer",
            "display_name": "开发者",
            "description": "可以创建和管理爬虫",
            "permissions": json.dumps([
                "crawler:create",
                "crawler:edit",
                "crawler:delete",
                "crawler:view",
                "task:create",
                "task:view",
                "task:execute",
                "data:view",
                "data:export"
            ])
        },
        {
            "name": "viewer",
            "display_name": "查看者",
            "description": "只能查看数据",
            "permissions": json.dumps([
                "crawler:view",
                "task:view",
                "data:view"
            ])
        }
    ]

    for role_data in roles_data:
        existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)

    db.commit()


def init_admin_user(db: Session):
    """Initialize default admin user"""
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        print("Admin role not found. Please run init_roles first.")
        return

    existing_admin = db.query(User).filter(User.username == "admin").first()
    if not existing_admin:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),  # Default password
            full_name="System Administrator",
            role_id=admin_role.id,
            status="active"
        )
        db.add(admin_user)
        db.commit()
        print("Default admin user created:")
        print("  Username: admin")
        print("  Password: admin123")
        print("  Email: admin@example.com")
        print("\n⚠️  Please change the default password after first login!")


def init_system_configs(db: Session):
    """Initialize system configurations"""
    configs = [
        {
            "key": "max_concurrent_tasks",
            "value": "10",
            "description": "最大并发任务数",
            "category": "performance"
        },
        {
            "key": "default_request_timeout",
            "value": "30",
            "description": "默认请求超时时间（秒）",
            "category": "network"
        },
        {
            "key": "data_retention_days",
            "value": "90",
            "description": "数据保留天数",
            "category": "storage"
        }
    ]

    for config_data in configs:
        existing_config = db.query(SystemConfig).filter(
            SystemConfig.key == config_data["key"]
        ).first()
        if not existing_config:
            config = SystemConfig(**config_data)
            db.add(config)

    db.commit()


def init_database():
    """Initialize database with tables and default data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

    db = SessionLocal()
    try:
        print("\nInitializing default roles...")
        init_roles(db)
        print("✓ Default roles initialized")

        print("\nInitializing admin user...")
        init_admin_user(db)
        print("✓ Admin user initialized")

        print("\nInitializing system configurations...")
        init_system_configs(db)
        print("✓ System configurations initialized")

        print("\n✅ Database initialization completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
