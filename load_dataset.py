def load_dataset(filename):
    """Загрузка транзакций из CSV файла."""
    transactions = []
    with open(filename, 'r', encoding='windows-1251') as f:
        for line in f:
            items = line.strip().split(',')
            if items and items[0] != '':
                transactions.append(items)
    return transactions