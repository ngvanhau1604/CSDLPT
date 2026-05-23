from locust import HttpUser, task, between

class FlashSaleUser(HttpUser):

    @task
    def buy_item(self):
        # Bắn request POST vào API /buy để mô phỏng việc mua hàng
        self.client.post("/buy")