with open('referat.txt', 'r', encoding='utf-8') as referat:
    a = referat.read()
    # Количество символов
    print(len(a))
    # Количество слов
    print(len(a.split()))
with open('referat2.txt', 'w', encoding='utf-8') as referat2:
    referat2.write(a.replace('.', '!'))