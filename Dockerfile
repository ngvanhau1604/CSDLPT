# Sử dụng môi trường Python nhẹ
FROM python:3.9-slim

# Chuyển vào thư mục làm việc trong container
WORKDIR /app

# Copy file code của bạn vào container
COPY main.py .

# Cài đặt các thư viện cần thiết
RUN pip install fastapi uvicorn pymongo

# Mở cổng 8000
EXPOSE 8000

# Lệnh chạy ứng dụng khi container khởi động
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]