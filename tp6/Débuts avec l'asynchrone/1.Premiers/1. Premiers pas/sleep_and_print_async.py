import asyncio

async def count_to_ten():
    for i in range(1, 11):
        print(i)
        await asyncio.sleep(0.5)

# Appeler la fonction deux fois
async def main():
    print("Starting tasks...")
    tasks=[count_to_ten(),count_to_ten()]   
    for task in tasks:
        await task
    print("All tasks completed.")

# Exécuter la fonction principale
if __name__ == "__main__":
    asyncio.run(main())

