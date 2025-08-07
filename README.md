## Тестовое на позицию junior python разработчик

Парсер логов в json-формате, сделанный в виде класса LogParser. 
Для запуска нужно склонировать этот репозиторий:
```
git clone https://github.com/serpens2/test_task1.git
cd test_task1
pip install -r 'requirements.txt'
```
после чего можно использовать файл log_parser.py из командной строки:
```
python log_parser.py --file example1.log example2.log --report my_report
```
Результат выполнения команды выше (сохраняется в my_report.txt):
<img width="701" height="215" alt="Screenshot 2025-08-07 143342" src="https://github.com/user-attachments/assets/ee90313e-21ae-4950-a920-fc7444e98f3e" />


Предусмотрена фильтрация по дате:
<img width="841" height="168" alt="Screenshot 2025-08-07 144925" src="https://github.com/user-attachments/assets/fe67200d-6225-48a9-b083-be53f4e5e42b" />


Если нужно парсить другие логи, но оформленные так же, то достаточно поменять названия полей у метода make_report без необходимости переписывать половину кода.

Если нужно добавить агрегатные функции, это легко сделать по аналогии с уже реализованными функциями среднего, максимума и минимума.
