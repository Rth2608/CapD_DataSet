def load_stock_list(file_path="stock_list.txt"):
    with open(file_path, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]