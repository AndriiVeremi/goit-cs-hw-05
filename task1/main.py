import argparse
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source: AsyncPath, output: AsyncPath):
    """
    Рекурсивно читає файли у вихідній папці та її підпапках і копіює їх.
    """
    try:
        async for item in source.iterdir():
            if await item.is_dir():
                await read_folder(item, output)
            else:
                await copy_file(item, output)
    except Exception as e:
        logging.error(f"Помилка під час читання папки {source}: {e}")

async def copy_file(file_path: AsyncPath, output: AsyncPath):
    """
    Копіює файл у відповідну підпапку у цільовій директорії на основі розширення.
    """
    try:
        extension = file_path.suffix[1:] if file_path.suffix else 'no_extension'
        target_dir = output / extension
        await target_dir.mkdir(exist_ok=True, parents=True)
        await copyfile(file_path, target_dir / file_path.name)
        logging.info(f"Скопійовано {file_path} до {target_dir / file_path.name}")
    except Exception as e:
        logging.error(f"Не вдалося скопіювати файл {file_path}: {e}")

async def main():
    """
    Головна функція для запуску сортування файлів.
    """
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширеннями.")
    parser.add_argument("--source", type=str, required=True, help="Вихідна папка з файлами.")
    parser.add_argument("--output", type=str, default="dist", help="Папка для відсортованих файлів.")

    args = parser.parse_args()

    source_path = AsyncPath(args.source)
    output_path = AsyncPath(args.output)

    if not await source_path.is_dir():
        logging.error(f"Вихідна папка не існує: {args.source}")
        return

    await output_path.mkdir(exist_ok=True, parents=True)

    await read_folder(source_path, output_path)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Процес перервано користувачем.")
    except Exception as e:
        logging.error(f"Виникла непередбачувана помилка: {e}")

