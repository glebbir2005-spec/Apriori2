import sys
import time
import matplotlib.pyplot as plt
from apriori import apriori
from load_dataset import load_dataset

def visualize_results(thresholds, exec_times, total_counts):
    """
    Функция визуализации результатов экспериментов.
    """
    if isinstance(total_counts, dict):
        total_counts = [sum(total_counts[t].values()) for t in thresholds]

    exec_times_ms = [t * 1000 for t in exec_times]

    plt.figure(figsize=(9, 5))
    plt.plot(thresholds, exec_times_ms, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    plt.title('Зависимость времени выполнения от порога поддержки', fontsize=14)
    plt.xlabel('Порог поддержки (%)', fontsize=12)
    plt.ylabel('Время выполнения (мс)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(thresholds)
    
    for x, y in zip(thresholds, exec_times_ms):
        plt.annotate(f"{y:.2f} мс", (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.tight_layout()
    plt.savefig('execution_time_chart.png')
    plt.show()

    plt.figure(figsize=(9, 5))
    plt.plot(thresholds, total_counts, marker='s', linestyle='-', color='g', linewidth=2, markersize=8)
    plt.title('Зависимость количества частых наборов от порога поддержки', fontsize=14)
    plt.xlabel('Порог поддержки (%)', fontsize=12)
    plt.ylabel('Количество частых наборов', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(thresholds)

    for x, y in zip(thresholds, total_counts):
        plt.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('total_itemsets_chart.png')
    plt.show()


def run_experiments():
    filename = 'baskets.csv'
    
    print("Загрузка данных...")
    transactions = load_dataset(filename)
    print(f"Всего загружено транзакций: {len(transactions)}\n")
    
    thresholds = [1, 3, 5, 10, 15]

    execution_times = []
    total_counts = []
    
    for threshold in thresholds:
        print(f"{'='*40}")
        print(f"Запуск алгоритма: Порог поддержки = {threshold}%")
        
        start_time = time.perf_counter()
        
        raw_results = apriori(transactions, threshold)
        
        end_time = time.perf_counter()
        exec_time = end_time - start_time
        
        print(f"Найдено частых наборов: {len(raw_results)}")
        print(f"Время выполнения алгоритма: {exec_time:.6f} секунд")
        
        execution_times.append(exec_time)
        total_counts.append(len(raw_results))
        
        formatted_results = []
        for itemset, supp in raw_results:
            sorted_itemset = tuple(sorted(list(itemset)))
            formatted_results.append((sorted_itemset, supp))
            
        formatted_results.sort(key=lambda x: -x[1])
        
        output_filename = f"apriori_results_{threshold}pct.txt"
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            out_file.write(f"=== Результаты алгоритма Apriori ===\n")
            out_file.write(f"Порог поддержки: {threshold}%\n")
            out_file.write(f"Всего найдено частых наборов: {len(formatted_results)}\n")
            out_file.write(f"Чистое время выполнения: {exec_time:.6f} сек.\n")
            out_file.write("="*40 + "\n\n")
            
            out_file.write("--- Сортировка по убыванию поддержки ---\n")
            for itemset, supp in formatted_results:
                itemset_str = "{" + ", ".join(itemset) + "}"
                out_file.write(f"Набор: {itemset_str:<30} | Поддержка: {supp:.2f}%\n")
                
        print(f"Результаты сохранены в файл: {output_filename}")
    
    print(f"\n{'='*40}")
    print("Все эксперименты завершены!")

    visualize_results(thresholds, execution_times, total_counts)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    run_experiments()