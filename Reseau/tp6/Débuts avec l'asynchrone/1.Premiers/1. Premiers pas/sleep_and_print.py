import time

def count_to_ten():
    for i in range(1, 11):
        print(i)
        time.sleep(0.5)

# Appeler la fonction deux fois
def main():
    print("Starting tasks...")
    tasks=[count_to_ten(),count_to_ten()]   
    for task in tasks:
        task()
    print("All tasks completed.")

# Exécuter la fonction principale
if __name__ == "__main__":
    main()

