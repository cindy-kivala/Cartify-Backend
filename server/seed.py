# server/seed.py
import os
import sys
import random
from dotenv import load_dotenv

# Load environment variables (useful locally & on Render)
load_dotenv()

# Make sure root project dir is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.app import create_app
from server.models import db, User, Product

app = create_app()

def seed_users():
    u1 = User(username="Alice", email="alice@example.com", password="password")
    u2 = User(username="Bob", email="bob@example.com", password="password")
    db.session.add_all([u1, u2])
    print("Users ready!")

def seed_products():
    products = [
        Product(
            name="Laptop",
            price=1200,
            image_url="https://cdn.mos.cms.futurecdn.net/iCPyXMDUqz8ABHaK4zxiaF.jpg",
            description="High-performance laptop with 16GB RAM, 512GB SSD and a 14-inch display.",
            category="Computers",
            brand="Razor",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Headphones",
            price=150,
            image_url="https://cdn.mos.cms.futurecdn.net/fzfrjb5R7oekedSA6XUhaX.jpg",
            description="Noise-cancelling wireless headphones with up to 20 hours of battery life.",
            category="Audio",
            brand="Sony",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Mouse",
            price=50,
            image_url="https://cdn.thewirecutter.com/wp-content/media/2022/11/gaming-mouse-2048px-6823.jpg?auto=webp&quality=75&width=1024",
            description="Ergonomic wireless gaming mouse with adjustable DPI and programmable buttons.",
            category="Accessories",
            brand="Razor",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Keyboard",
            price=80,
            image_url="https://cdn.thewirecutter.com/wp-content/media/2024/12/BEST-GAMING-KEYBOARDS-2048px-5821.jpg?auto=webp&quality=75&width=1024",
            description="Mechanical keyboard with RGB backlighting and tactile switches.",
            category="Accessories",
            brand="Corsair",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Monitor",
            price=300,
            image_url="https://dlcdnwebimgs.asus.com/files/media/0e92cabf-067b-433c-a590-abdf68c9e029/v1/img/gallery/accessory_3.jpg",
            description="27-inch QHD IPS monitor with 144Hz refresh rate and thin bezels.",
            category="Monitors",
            brand="ASUS",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Webcam",
            price=100,
            image_url="https://images.wondershare.com/filmora/article-images/logitech-c920.jpg",
            description="Full HD webcam with autofocus and built-in dual microphones.",
            category="Peripherals",
            brand="Logitech",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Microphone",
            price=120,
            image_url="https://cdn.mos.cms.futurecdn.net/9APZ8Xgt6ZR9H7y6g4Sq5d.jpg",
            description="USB condenser microphone ideal for streaming, podcasting and voiceovers.",
            category="Audio",
            brand="Blue",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Smartphone",
            price=900,
            image_url="https://www.cnet.com/a/img/resize/1c11b5b2887090599d6d92528d24f1d56cfc4d15/hub/2025/09/09/45bc736c-8211-4627-a911-6016ceef6977/iphone-17-pro-and-pro-max.png?auto=webp&fit=crop&height=675&width=1200",
            description="Flagship smartphone with OLED display, advanced camera system and long battery life.",
            category="Mobile",
            brand="Apple",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Tablet",
            price=600,
            image_url="https://www.zdnet.com/a/img/2025/04/30/5ee373e8-fb54-4c23-b981-74d8a0c65984/3.jpg",
            description="Lightweight 10-inch tablet with high-resolution display and stylus support.",
            category="Mobile",
            brand="Apple",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Charger",
            price=30,
            image_url="https://thumbs.dreamstime.com/b/white-usb-type-c-charger-cable-background-176589900.jpg",
            description="Compact USB-C fast charger with 65W Power Delivery support.",
            category="Accessories",
            brand="Anker",
            stock=random.randint(5, 50)
        ),
        Product(
            name="External HDD",
            price=150,
            image_url="https://media.istockphoto.com/id/496402410/photo/external-hard-drive-for-backup.jpg?s=612x612&w=0&k=20&c=Ul6uXVrMdFEmIC7xH_f54tWfYQSExa1_j70eP-5fuyM=",
            description="2TB portable external hard drive for reliable backups and extra storage.",
            category="Storage",
            brand="Seagate",
            stock=random.randint(5, 50)
        ),
        Product(
            name="SSD",
            price=200,
            image_url="https://www.avg.com/hs-fs/hubfs/Blog_Content/Avg/Signal/AVG%20Signal%20Images/What%20Is%20an%20SSD/What_is_an_SSD-01.jpg?width=660&name=What_is_an_SSD-01.jpg",
            description="1TB NVMe SSD for fast boot times and improved application loading.",
            category="Storage",
            brand="Samsung",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Graphics Card",
            price=500,
            image_url="https://wallpapercave.com/wp/wp12175244.jpg",
            description="High-performance graphics card for gaming and GPU-accelerated workloads.",
            category="Components",
            brand="NVIDIA",
            stock=random.randint(5, 50)
        ),
        Product(
            name="RAM 16GB",
            price=120,
            image_url="https://backend.pcd.com.sa/uploads/RM_XP_LB_32_D5_B48_1_ce3d938d59.webp?format=webp&resize=250x250&embed",
            description="16GB DDR4 memory kit for smooth multitasking and gaming.",
            category="Components",
            brand="Corsair",
            stock=random.randint(5, 50)
        ),
        Product(
            name="RAM 32GB",
            price=220,
            image_url="https://thumbs.dreamstime.com/b/close-up-computer-ram-module-featuring-unique-design-great-wall-china-chinese-flag-installed-motherboard-red-360473223.jpg",
            description="32GB DDR4 memory kit for content creators and heavy multitasking.",
            category="Components",
            brand="G.Skill",
            stock=random.randint(5, 50)
        ),
        Product(
            name="CPU",
            price=350,
            image_url="https://plus.unsplash.com/premium_photo-1681426701125-bed484a8c829?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8Y3B1fGVufDB8fDB8fHww",
            description="6-core/12-thread desktop CPU offering a balance of performance and efficiency.",
            category="Components",
            brand="Intel",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Motherboard",
            price=250,
            image_url="https://thumbs.dreamstime.com/b/%C4%8Derven%C3%A1-t%C5%99eme%C5%A1n%C3%A1-may-gaming-motherboard-asus-tuf-plus-illuminated-colored-lights-260713444.jpg",
            description="ATX motherboard with multiple M.2 slots and robust power delivery.",
            category="Components",
            brand="ASUS",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Power Supply",
            price=100,
            image_url="https://asset-us-store.msi.com/image/cache/catalog/Pd_page/PSU/A650BE/A650BE-6-228x228.png",
            description="650W 80+ Bronze power supply with modular cables for tidy builds.",
            category="Components",
            brand="MSI",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Cooling Fan",
            price=40,
            image_url="https://cdn.mos.cms.futurecdn.net/3m9Nu4Up8xkWC432Z93Fo4.jpg",
            description="120mm case fan designed for quiet operation and good airflow.",
            category="Cooling",
            brand="Noctua",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Laptop Stand",
            price=35,
            image_url="https://rukminim2.flixcart.com/image/612/612/xif0q/laptop-stand/d/l/u/0-18-white-small-laptop-stand-sbffurniture-original-imahdnn6zmzg7awc.jpeg?q=70",
            description="Adjustable aluminum laptop stand that improves ergonomics and cooling.",
            category="Accessories",
            brand="Rain Design",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Gaming Chair",
            price=300,
            image_url="https://thumbs.dreamstime.com/b/gaming-chair-sitting-front-computer-monitor-374839078.jpg",
            description="Ergonomic gaming chair with lumbar support and adjustable armrests.",
            category="Furniture",
            brand="Secretlab",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Desk Lamp",
            price=60,
            image_url="https://m.media-amazon.com/images/I/61amB41VAyL.jpg",
            description="Adjustable LED desk lamp with multiple brightness levels and color temps.",
            category="Accessories",
            brand="BenQ",
            stock=random.randint(5, 50)
        ),
        Product(
            name="Mouse Pad",
            price=25,
            image_url="https://djd1xqjx2kdnv.cloudfront.net/photos/37/15/493044_19522_L2.jpg",
            description="Extended cloth mouse pad with stitched edges for durability.",
            category="Accessories",
            brand="SteelSeries",
            stock=random.randint(5, 50)
        ),
        Product(
            name="USB Hub",
            price=20,
            image_url="https://www.ugreen.com/cdn/shop/products/ugreen-5-in-1-4k-hdmi-usb-c-hub-405023.png?v=1692790950&width=600",
            description="5-in-1 USB-C hub with HDMI, USB-A ports and pass-through charging.",
            category="Accessories",
            brand="UGREEN",
            stock=random.randint(5, 50)
        ),
    ]

    db.session.add_all(products)
    print("Products ready!")

if __name__ == "__main__":
    with app.app_context():
        if "--force" in sys.argv:
            db.drop_all()
            db.create_all()
            print("Dropped and recreated all tables!")

        seed_users()
        seed_products()
        db.session.commit()
        print("Database seeding complete!")
