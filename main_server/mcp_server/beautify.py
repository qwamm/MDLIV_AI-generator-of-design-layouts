from jsbeautifier import beautify_file

#Ф-ция, преобразующая минифицированные js файлы в читаемый вид
def beautify_files(files: list):
    for file in files:
        t = beautify_file(file)
        w = open(file, "w", encoding='utf-8')
        w.write(t)
        w.close()
