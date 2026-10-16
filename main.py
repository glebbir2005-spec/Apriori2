import sys
import time
import matplotlib.pyplot as plt
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


def visualize_task_2_3(confidences, exec_times, rules_counts, support_val):
    """Визуализация графиков для Задания 3."""
    exec_times_ms = [t * 1000 for t in exec_times]

    plt.figure(figsize=(9, 5))
    plt.plot(confidences, exec_times_ms, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    plt.title(f'Зависимость времени поиска от достоверности\n(Фиксированная поддержка = {support_val}%)', fontsize=14)
    plt.xlabel('Порог достоверности (%)', fontsize=12)
    plt.ylabel('Время выполнения (мс)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(confidences)
    
    for x, y in zip(confidences, exec_times_ms):
        plt.annotate(f"{y:.2f} мс", (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.tight_layout()
    plt.savefig('rules_execution_time_chart.png')
    plt.show()

    plt.figure(figsize=(9, 5))
    plt.plot(confidences, rules_counts, marker='s', linestyle='-', color='g', linewidth=2, markersize=8)
    plt.title(f'Зависимость количества правил от достоверности\n(Фиксированная поддержка = {support_val}%)', fontsize=14)
    plt.xlabel('Порог достоверности (%)', fontsize=12)
    plt.ylabel('Количество найденных правил', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(confidences)

    for x, y in zip(confidences, rules_counts):
        plt.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('rules_total_count_chart.png')
    plt.show()


def run_experiments():
    filename = 'baskets.csv'
    
    print("Загрузка данных...")
    transactions = load_dataset(filename)
    print(f"Всего загружено транзакций: {len(transactions)}\n")
    
    fixed_support_pct = 2
    confidence_thresholds = [10, 20, 30, 40, 50, 60]

    execution_times = []
    total_rules_counts = []
    
    print(f"--- Этап 1: Поиск частых наборов (Поддержка {fixed_support_pct}%) ---")
    start_apriori = time.perf_counter()
    frequent_itemsets = apriori(transactions, fixed_support_pct)
    end_apriori = time.perf_counter()
    print(f"Найдено частых наборов: {len(frequent_itemsets)}")
    print(f"Время работы Apriori: {end_apriori - start_apriori:.6f} сек.\n")

    print("--- Этап 2: Эксперименты с достоверностью ---")
    for conf in confidence_thresholds:
        print(f"Генерация правил: Достоверность = {conf}%")
        
        start_time = time.perf_counter()
        rules = generate_rules(frequent_itemsets, conf)
        
        sorted_rules = sort_rules(rules, sort_method='support')
        end_time = time.perf_counter()
        
        exec_time = end_time - start_time
        
        execution_times.append(exec_time)
        total_rules_counts.append(len(sorted_rules))
        
        print(f"  -> Найдено правил: {len(sorted_rules)}")
        print(f"  -> Время поиска: {exec_time * 1000:.2f} мс\n")
        
        output_filename = f"rules_supp{fixed_support_pct}_conf{conf}.txt"
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            out_file.write(f"=== Ассоциативные правила ===\n")
            out_file.write(f"Поддержка: {fixed_support_pct}% | Достоверность: {conf}%\n")
            out_file.write(f"Всего найдено: {len(sorted_rules)}\n")
            out_file.write("="*50 + "\n\n")
            for rule in sorted_rules:
                ant_str = "{" + ", ".join(sorted(list(rule['antecedent']))) + "}"
                con_str = "{" + ", ".join(sorted(list(rule['consequent']))) + "}"
                out_file.write(f"{ant_str:<35} -> {con_str:<25} | Поддержка: {rule['support']:>5.2f}% | Достоверность: {rule['confidence']:>5.2f}%\n")

    print(f"{'='*40}")
    print("Все эксперименты завершены! Открываю графики...")

    visualize_task_2_3(confidence_thresholds, execution_times, total_rules_counts, fixed_support_pct)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    run_experiments()