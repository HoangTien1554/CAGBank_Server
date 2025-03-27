import requests
import re  # Thư viện regex để trích xuất thông tin

# Thay API Key của bạn vào đây
API_KEY = "AK_CS.6507d3700ab711f097089522635f3f80.1gLQbfnm3eO9TqwMfBVgGkUVeIwqKBqbroCyXAjoN53uuHZ6yQ6Ezfq7mf9AUnYDdZ2ASgxZ"

# URL API của Casso
URL = "https://oauth.casso.vn/v2/transactions?fromDate=2021-04-01&page=1&pageSize=10&sort=ASC"

# Headers (sử dụng API Key)
headers = {
    "Authorization": f"Apikey {API_KEY}"
}

# Gửi yêu cầu GET
response = requests.get(URL, headers=headers)

# Kiểm tra mã trạng thái HTTP
if response.status_code == 200:
    data = response.json()  # Chuyển phản hồi thành JSON

    # Kiểm tra "data" có tồn tại không
    transactions_data = data.get("data", {})
    records = transactions_data.get("records", [])

    if not records:
        print("Không có giao dịch nào.")
    else:
        # Duyệt qua từng giao dịch và hiển thị dữ liệu
        for transaction in records:
            description = transaction.get("description", "")
            amount = transaction.get("amount", "N/A")

            # Tìm nội dung giữa 'IBFT' và 'GD' trong mô tả (nếu có)
            match = re.search(r'IBFT(.*?)GD', description)
            if match:
                content_between_IBFT_and_GD = match.group(1).strip()
                print(f"ID Giao Dịch: {transaction.get('id', 'N/A')}")
                print(f"Mã giao dịch: {transaction.get('tid', 'N/A')}")
                print(f"Số Tiền: {amount} VND")
                print(f"Nội dung giữa IBFT và GD: {content_between_IBFT_and_GD}")
                print("=" * 40)
            else:
                print(f"Không tìm thấy nội dung giữa 'IBFT' và 'GD' trong mô tả.")
else:
    print(f"Lỗi API: {response.status_code} - {response.text}")
