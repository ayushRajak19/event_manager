"""
Seed data script for populating database with sample data.

Run this script to create sample admin, users, vendors, and products for testing.

Usage:
    python seed_data.py
"""
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import (
    Admin, User, Vendor, Product,
    Order, OrderItem, ItemRequest
)
from app.models.enums import ProductStatus, VendorStatus, OrderStatus, ItemRequestStatus
from app.core.security import hash_password
from app.db.base import Base


def seed_database():
    """Populate database with sample data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Admin).first():
            print("Database already populated with sample data!")
            return
        
        print("🌱 Seeding database with sample data...")
        
        # 1. Create Admin
        print("  ✓ Creating admin...")
        admin = Admin(
            name="System Administrator",
            email="admin@eventmgmt.com",
            password_hash=hash_password("Admin@123")
        )
        db.add(admin)
        db.flush()
        
        # 2. Create Users
        print("  ✓ Creating users...")
        users = [
            User(
                name="John Doe",
                email="john@example.com",
                password_hash=hash_password("User@123"),
                phone="9876543210",
                is_active=1
            ),
            User(
                name="Jane Smith",
                email="jane@example.com",
                password_hash=hash_password("User@123"),
                phone="9876543211",
                is_active=1
            ),
            User(
                name="Bob Wilson",
                email="bob@example.com",
                password_hash=hash_password("User@123"),
                phone="9876543212",
                is_active=1
            ),
        ]
        db.add_all(users)
        db.flush()
        
        # 3. Create Vendors
        print("  ✓ Creating vendors...")
        vendors = [
            Vendor(
                name="Alex Johnson",
                email="vendor1@eventmgmt.com",
                password_hash=hash_password("Vendor@123"),
                company_name="TechGear Solutions",
                phone="9123456789",
                status=VendorStatus.ACTIVE
            ),
            Vendor(
                name="Maria Garcia",
                email="vendor2@eventmgmt.com",
                password_hash=hash_password("Vendor@123"),
                company_name="EventPro Supplies",
                phone="9123456790",
                status=VendorStatus.ACTIVE
            ),
            Vendor(
                name="Kumar Patel",
                email="vendor3@eventmgmt.com",
                password_hash=hash_password("Vendor@123"),
                company_name="Audio Visual Systems",
                phone="9123456791",
                status=VendorStatus.ACTIVE
            ),
        ]
        db.add_all(vendors)
        db.flush()
        
        # 4. Create Products
        print("  ✓ Creating products...")
        products = [
            # Vendor 1 - Audio Equipment
            Product(
                name="Microphone - Condenser",
                description="Professional condenser microphone for events",
                category="Audio",
                quantity=15,
                price=5000.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[0].id
            ),
            Product(
                name="Speaker System - 2000W",
                description="High-power speaker system for large venues",
                category="Audio",
                quantity=5,
                price=35000.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[0].id
            ),
            Product(
                name="Audio Mixer - 16 Channel",
                description="Professional audio mixing console",
                category="Audio",
                quantity=8,
                price=12000.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[0].id
            ),
            # Vendor 2 - Lighting Equipment
            Product(
                name="LED Stage Lights",
                description="RGB LED stage lighting system",
                category="Lighting",
                quantity=20,
                price=8000.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[1].id
            ),
            Product(
                name="Projector - 4K",
                description="4K resolution projector for presentations",
                category="Lighting",
                quantity=3,
                price=50000.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[1].id
            ),
            Product(
                name="Fog Machine",
                description="Professional fog/smoke machine for events",
                category="Lighting",
                quantity=10,
                price=3000.00,
                status=ProductStatus.OUT_OF_STOCK,
                vendor_id=vendors[1].id
            ),
            # Vendor 3 - Decor
            Product(
                name="Backdrop Banner Stand",
                description="Adjustable backdrop stand for event branding",
                category="Decor",
                quantity=12,
                price=2000.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[2].id
            ),
            Product(
                name="Table Setup - Round",
                description="Elegant round table with cover",
                category="Decor",
                quantity=25,
                price=1500.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[2].id
            ),
            Product(
                name="Chair - Premium",
                description="Premium event chair with padding",
                category="Decor",
                quantity=50,
                price=800.00,
                status=ProductStatus.AVAILABLE,
                vendor_id=vendors[2].id
            ),
        ]
        db.add_all(products)
        db.flush()
        
        # 5. Create Orders
        print("  ✓ Creating orders...")
        orders = [
            Order(
                user_id=users[0].id,
                order_number="ORD-001-001",
                total_amount=13000.00,
                status=OrderStatus.DELIVERED
            ),
            Order(
                user_id=users[1].id,
                order_number="ORD-002-002",
                total_amount=8000.00,
                status=OrderStatus.DISPATCHED
            ),
        ]
        db.add_all(orders)
        db.flush()
        
        # 6. Create Order Items
        print("  ✓ Creating order items...")
        order_items = [
            OrderItem(
                order_id=orders[0].id,
                product_id=products[0].id,
                quantity=2,
                price=5000.00
            ),
            OrderItem(
                order_id=orders[0].id,
                product_id=products[2].id,
                quantity=1,
                price=3000.00
            ),
            OrderItem(
                order_id=orders[1].id,
                product_id=products[3].id,
                quantity=1,
                price=8000.00
            ),
        ]
        db.add_all(order_items)
        db.flush()
        
        # 7. Create Item Requests
        print("  ✓ Creating item requests...")
        item_requests = [
            ItemRequest(
                user_id=users[2].id,
                item_name="Hologram Display",
                description="3D hologram projector for product showcase",
                category="Technology",
                status=ItemRequestStatus.PENDING
            ),
            ItemRequest(
                user_id=users[0].id,
                item_name="LED Dance Floor",
                description="Interactive LED dance floor 20x20",
                category="Technology",
                status=ItemRequestStatus.APPROVED,
                vendor_id=vendors[1].id
            ),
            ItemRequest(
                user_id=users[1].id,
                item_name="Catering Station",
                description="Mobile catering station with warming units",
                category="Catering",
                status=ItemRequestStatus.FULFILLED
            ),
        ]
        db.add_all(item_requests)
        db.flush()
        
        # Commit all changes
        db.commit()
        
        print("\n✅ Database seeding completed successfully!\n")
        print("Sample Credentials:")
        print("  Admin:")
        print("    Email: admin@eventmgmt.com")
        print("    Password: Admin@123")
        print("\n  User Examples:")
        print("    Email: john@example.com")
        print("    Password: User@123")
        print("\n  Vendor Examples:")
        print("    Email: vendor1@eventmgmt.com")
        print("    Password: Vendor@123")
        print("\n📊 Data Created:")
        print(f"  - Admins: 1")
        print(f"  - Users: {len(users)}")
        print(f"  - Vendors: {len(vendors)}")
        print(f"  - Products: {len(products)}")
        print(f"  - Orders: {len(orders)}")
        print(f"  - Item Requests: {len(item_requests)}")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
