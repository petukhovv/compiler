# Репозиторий с тестами для учебного компилятора

## Структура репозитория
- `core` - небольшой набор тестов, в котором есть (или будет) хотя бы по одному тесту
  на все необходимые к реализации части реализуемого языка;
- `expressions` и `deep-expressions` - много тестов на базовое подмножество языка
  (арифметические выражения + ввод / вывод);
- `performance` - пара тестов на сравнение эффективности компилятора с gcc.

В папках `core`, `expressions` и `deep-expressions` есть пачка тестов (`*.expr`),
входы для тестов (`*.input`), эталонные выводы (`orig/*.log`) и `Makefile`.

## Предполагаемый сценарий использования репозитория
Этот репозиторий добавляется как подмодуль (submodule) в корень репозитория компилятора.

В корне также находится папка `runtime`, в которой по запуску `make` генерируется объектный
файл окружения (`runtime.o`).  Таким образом, путь до `runtime.o` из подмодуля
`compiler-tests` - `../runtime/runtime.o`.

По запуску `make` в корне репозитория компилятора должен создаваться бинарник самого компилятора
с именем `rc`. Таким образом, путь до бинарника из подмодуля - `../rc`.

Интерфейс бинарника:
- `rc -i filename.expr` - интерпретация программы из файла `filename.expr`;
- `rc -s filename.expr` - компиляция программы из файла `filename.expr` в представление стековой машины с последующей интерпретацией стековой машиной;
- `rc -o filename.expr` - компиляция программы из файла `filename.expr` в запускаемый файл `filename`;
Во всех случаях для ввода и вывода используются стандартные потоки ввода и вывода.

## Описание корневого Makefile
TODO

```makefile
TESTS=test001 test002 test003 test004 test005 test006 test007 test008 test009 test010 test011 test012 test013 test014 test015 test016 test017 test018 test019 test020 test021 test022 test023 test024 test025 test026 test027 test028 

.PHONY: check $(TESTS) 

check: $(TESTS) 

$(TESTS): %: %.expr
	RC_RUNTIME=../runtime ../rc.native -o $< && cat $@.input | ./$@ > $@.log && diff $@.log orig/$@.log
	cat $@.input | ../rc.native -i $< > $@.log && diff $@.log orig/$@.log
	cat $@.input | ../rc.native -s $< > $@.log && diff $@.log orig/$@.log

clean:
	rm -f test*.log *.s *~ $(TESTS)
```
