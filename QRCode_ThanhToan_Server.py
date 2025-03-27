import requests
import re  # Thư viện regex để trích xuất thông tin
import subprocess  # Để gọi AutoHotkey từ Python
import time  # Để tạo vòng lặp kiểm tra liên tục

# Thay API Key của bạn vào đây
API_KEY = "AK_CS.6507d3700ab711f097089522635f3f80.1gLQbfnm3eO9TqwMfBVgGkUVeIwqKBqbroCyXAjoN53uuHZ6yQ6Ezfq7mf9AUnYDdZ2ASgxZ"

# URL API của Casso
URL = "https://oauth.casso.vn/v2/transactions?fromDate=2021-04-01&page=1&pageSize=10&sort=ASC"

# Headers (sử dụng API Key)
headers = {
    "Authorization": f"Apikey {API_KEY}"
}

def get_transactions():
    # Gửi yêu cầu GET
    response = requests.get(URL, headers=headers)
    
    # Kiểm tra mã trạng thái HTTP
    if response.status_code == 200:
        data = response.json()  # Chuyển phản hồi thành JSON

        # Kiểm tra "data" có tồn tại không
        transactions_data = data.get("data", {})
        records = transactions_data.get("records", [])

        return records
    else:
        print(f"Lỗi API: {response.status_code} - {response.text}")
        return []

# Chạy liên tục để kiểm tra giao dịch mới
while True:
    records = get_transactions()

    if records:
        # Duyệt qua từng giao dịch và gửi dữ liệu vào AutoHotkey
        for transaction in records:
            description = transaction.get("description", "")
            amount = transaction.get("amount", "N/A")

            # Tìm nội dung giữa 'IBFT' và 'GD' trong mô tả (nếu có)
            match = re.search(r'IBFT(.*?)GD', description)
            if match:
                content_between_IBFT_and_GD = match.group(1).strip()

                # Gọi AutoHotkey để truyền dữ liệu
                ahk_script = r"C:\path\to\your\script.ahk"  # Đường dẫn tới file AutoHotkey của bạn
                # Truyền nội dung và số tiền vào AutoHotkey
                subprocess.run([ahk_script, content_between_IBFT_and_GD, str(amount)])
                print(f"Đã gửi giao dịch: {content_between_IBFT_and_GD}, {amount}")
                break  # Sau khi gửi giao dịch đầu tiên, dừng lại và kiểm tra giao dịch tiếp theo

    # Chờ 10 giây trước khi kiểm tra lại giao dịch mới
    time.sleep(10)
