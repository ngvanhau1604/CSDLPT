from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
import uuid

app = FastAPI(title="Flash Sale Simulator")

# Kết nối tới MongoDB
# Lưu ý: "mongo:27017" là địa chỉ mặc định khi chạy trong Kubernetes sau này.
# Nếu bạn muốn chạy thử cục bộ mà chưa có MongoDB, code vẫn chạy nhưng sẽ báo lỗi kết nối CSDL khi gọi API.
try:
    client = MongoClient("mongodb://mongo:27017/", serverSelectionTimeoutMS=5000)
    db = client["flash_sale_db"]
    orders_collection = db["orders"]
except Exception as e:
    print("Chưa kết nối được MongoDB, nhưng API vẫn khởi động.")


def simulate_order_processing(order_id: str) -> int:
    """Tạo một chút tải CPU để HPA có tín hiệu rõ hơn khi flash sale bùng nổ."""
    checksum = 0
    for _ in range(50000):
        checksum = (checksum * 31 + len(order_id)) % 1000000007
    return checksum

@app.post("/buy")
async def place_order():
    """
    Hàm này mô phỏng việc nhận 1 yêu cầu mua hàng.
    Mỗi lần được gọi, nó sẽ tạo một đơn hàng với ID ngẫu nhiên và lưu vào MongoDB.
    """
    try:
        # Tạo dữ liệu đơn hàng giả lập
        order_data = {
            "order_id": str(uuid.uuid4()),
            "item": "Iphone 15 Pro Max - Flash Sale",
            "timestamp": datetime.now()
        }

        simulate_order_processing(order_data["order_id"])
        
        # Lưu vào MongoDB
        orders_collection.insert_one(order_data)
        
        return {"status": "success", "message": "Order placed!", "order_id": order_data["order_id"]}
    except Exception as e:
        # Nếu CSDL quá tải hoặc chết, trả về lỗi 500
        raise HTTPException(status_code=500, detail="Database error or overload")

@app.get("/health")
async def health_check():
    """Hàm để Kubernetes kiểm tra xem ứng dụng còn sống không"""
    return {"status": "ok"}