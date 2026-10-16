import sys
import time
from apriori import apriori, generate_rules
from load_dataset import load_dataset


def sort_rules(rules, sort_method='support'):
    """Сортировка ассоциативных правил."""
    if sort_method == 'support':
        return sorted(rules, key=lambda x: (x['support'], x['confidence']), reverse=True)
    elif sort_method == 'lexicographical':
        return sorted(rules, key=lambda x: (tuple(sorted(list(x['antecedent']))), tuple(sorted(list(x['consequent'])))))
    else:
        return rules


def run_task_1():
    filename = 'baskets.csv'
    
    print("Загрузка данных...")
    transactions = load_dataset(filename)
    print(f"Всего загружено транзакций: {len(transactions)}\n")
    
    min_support_pct = 10        # порог поддержки (%)
    min_confidence_pct = 70     # порог достоверности (%)
    sort_method = 'support'     # метод сортировки

    print(f"=== Запуск алгоритма ===")
    print(f"Порог поддержки: {min_support_pct}%")
    print(f"Порог достоверности: {min_confidence_pct}%")
    print(f"Сортировка: {sort_method}\n")
    
    start_time = time.perf_counter()
    
    frequent_itemsets = apriori(transactions, min_support_pct)
    rules = generate_rules(frequent_itemsets, min_confidence_pct)
    sorted_rules = sort_rules(rules, sort_method)
    
    end_time = time.perf_counter()
    exec_time = end_time - start_time
    
    print(f"Найдено частых наборов: {len(frequent_itemsets)}")
    print(f"Найдено ассоциативных правил: {len(sorted_rules)}")
    print(f"Время выполнения алгоритма: {exec_time:.6f} секунд\n")
    
    # Сохранение результатов в читаемом виде
    output_filename = f"rules_{min_support_pct}supp_{min_confidence_pct}conf.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(f"Ассоциативные правила\n")
        out_file.write(f"Порог поддержки: {min_support_pct}%\n")
        out_file.write(f"Порог достоверности: {min_confidence_pct}%\n")
        out_file.write(f"Метод сортировки: {sort_method}\n")
        out_file.write(f"Всего найдено правил: {len(sorted_rules)}\n")
        out_file.write("="*60 + "\n\n")
        
        for rule in sorted_rules:
            ant_str = "{" + ", ".join(sorted(list(rule['antecedent']))) + "}"
            con_str = "{" + ", ".join(sorted(list(rule['consequent']))) + "}"
            
            line = f"{ant_str:<35} -> {con_str:<25} | Поддержка: {rule['support']:>5.2f}% | Достоверность: {rule['confidence']:>5.2f}%"
            out_file.write(line + "\n")
            
    print(f"Результаты сохранены в файл: {output_filename}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    run_task_1()