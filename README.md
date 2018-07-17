## Актуальность

**На данный момент README требует дополнения с описанием:**
1. Реализации интерпретатора;
2. Реализации компилятора в код стековой машины;
3. Реализации стековой виртуальной машины;
4. Реализации компилятора в ASM-код (NASM) под X86 и процесса сборки мусора.

Через некоторое время README будет обновлен.

# Simple programming language

This repository contains toolkit for a simple programming language:
* Interpreter,
* Virtual stack machine,
* Stack machine code compiler,
* ASM X86 code compiler (with simple garbage collector).

**A toolkit was created for educational purposes.**

## Language features

1. **Arithmetic expressions**<br />
    Supported arithmetic operators (by priority):
    1. `*`, `/`, `%`
    2. `+`, `-`

    Example: `4 - 100 % (2 + 90) * 8 / 3`

2. **Logical expressions**<br />
    Supported logical operators (by priority):
    1. `==`, `!=`, `>`, `>=`, `<`, `<=`
    2. `&&`
    3. `||`, `!!`

    Examples:
    1. `a && b || c && (d !! e)`
    2. `a - b >= c % 10 && d != e`

3. **Variables** with supports reassign.<br />
    Examples:
    1. `x := 5 * y`
    2. `x := x <= y`

4. **I/O operations** using stdin/stdout<br />
    Examples:
    1. `x := read()`
    2. `write(x)`

5. **Conditions**<br />
    Example:
    ```
    if x >= y && z then
        write(x)
    elif !z then
        write(y)
    else
        write(z) fi
    ```
6. **`while` loop**<br />
    Example:
    ```
    while k > 0
    do
        res := res * n;
        k := k - 1
    od;
    ```
7. **`for` loop**<br />
    Example 1:
    ```
    for c := 2, c * c <= p && f, c := c + 1
    do
        f := p % c != 0
    od;
    ```
    Example 2:
    ```
    for skip, n >= 1, n := n-1
    do
        f := f * n
    od;
    ```
8. **Functions**<br />
    Example:
    ```
    fun A (m, n)
    begin
        if m == 0 then return n+1
        elif m > 0 && n == 0 then return A (m-1, 1)
        else return A (m-1, A(m, n-1))
        fi
    end

    write (A (1, 21))
    ```

    **All variables have the function scope or root scope.**

9. **Chars**<br />
    Example: `C := 'a'`

10. **Strings** and some build-in functions:<br />
    String assign example: `S := "I will remember April."`

    Built-in functions:
    1. **strlen** - get string length:<br />
        Example: `strlen(S)` => `22`
    2. **strget** - get specified string character:<br />
        Example: `strget(S, 2)` => `w`
    3. **strsub** - get a substring, starting with the character `n`, of length `k` characters:<br />
        Example: `strsub (S, 7, 8)` => `remember`
    4. **strdup** - copy string:<br />
        Example: `strdup(S)` => `I will remember April.`,
    5. **strset** - set `i` string character:<br />
        Example: `strset(S, 4, 'j')` => `I wijl remember April.`,
    6. **strcat** - concatenation of two strings:<br />
        Example: `strcat(S, " It was very cold.")` => `I will remember April. It was very cold.`,
    7. **strcmp** - comparison of two strings (the comparison is performed by the character codes of the strings, from left to right):<br />
        Examples:
        * `strcmp(S, "I wijl remember April.")` => `1`
        * `strcmp(S, "I wiz")` => `-1`
        * `strcmp(S, "I will")` => `-1`
        * `strcmp(S, "I will remember April.")` => `0`
    8. **strmake** - create a string of `n` repeating characters:<br />
        Example: `strmake (10, 'a')` => `aaaaaaaaaa`

11. **Values array** (unboxed-array) and some build-in functions:<br />
    1. **arrmake** - create unboxed-array:<br />
        Examples:
        * `S := arrmake (5)` => `[0, 0, 0, 0, 0]`
        * `S := arrmake (5, 0)` => `[0, 0, 0, 0, 0]`
        * `S := arrmake (5, [])` => `[0, 0, 0, 0, 0]`
        * `S := arrmake (5, [1, 2, 3, 4, 5])` => `[1, 2, 3, 4, 5]`
    2. **arrlen** - get array length:<br />
        `arrlen(S)` => `5`
    4. Value assign to array element by index:<br />
        `S[1] := 4` => `[0, 4, 0, 0, 0]`
    5. Get value of array element by index:<br />
        `write(S[1])` => `4`

12. **Pointers array** (boxed-array), some build-in functions and garbage collection:<br />
    1. **Arrmake** - create boxed-array:<br />
        Examples:
        1. `S := Arrmake (5)` => `[nullptr, nullptr, nullptr, nullptr, nullptr]`
        2. `S := Arrmake (5, {})` => `[nullptr, nullptr, nullptr, nullptr, nullptr]`
        3. Assign with default value:<br />
            1. `S1 := arrmake (2, 1)` => `[1, 1]`
            2. `S2 := arrmake (2, 3)` => `[3, 3]`
            3. `S := Arrmake (2, {S1, S2})` => `[S1, S2]`
            4. `S2[1] := 4`
            5. `write(S[0][1])` => `1`
            6. `write(S[1][0])` => `3`
            7. `write(S[1][1])` => `4`
    2. **arrlen** - get array length:<br />
        `arrlen(S)` => `5`
    4. Pointer assign to array element by index:<br />
        `S[1] := S1` => `[1, 1]`
    5. Get value of array element by index:<br />
        `write(S[1][0])` => `1`

13. **Objects** with properties and methods:<br />
    1. Defining property and getting it value:
    ```
        rabbit := {
            val weight := read(),
            val growth := read(),
            val name := "Ralph"
        }
        write(rabbit.weight)
        write(rabbit.name)
    ```
    2. Defining and calling methods, changing property values (`this` and other objects), using properties and methods of another objects:
    ```
        obj1 := {
            val prop1 := read(),
            fun method1() begin
                write(2)
            end
        }

        obj2 := {
            val prop1 := read(),
            fun method1(a, b) begin
                this.prop1 := read()
                write(obj1.prop1)
                obj1.prop1 := read()
                write(obj1.prop1)
                obj1.method1()
            end,
            fun method2(a, b) begin
                write(obj1.prop1)
                write(a * b)
                write(this.prop1)
                this.method1(a, b)
            end
        }

        obj2.method2(5, 8)
        obj2.method2(22, 4)
        write(obj1.prop1)
    ```

#### Предопределенные функции

В данном языке строки и массивы предлагают преопределенные функции (также, к ним относятся и input/output функции).

В файлах соответствующих парсеров (`arrays`, `strings`, `io`) составлены мапы, отображающие название функции на соответствующий ей AST-класс.
Данные мапы используется в парсере `fun_call_stmt`, который первым делом проверяет функцию на относящуюся к предопределенным, и если она к ним относится, то берет соответствующий AST-класс (вместо стандартного - `FunctionCallStatement`).

#### Расположение

Парсеры находся в директории `Parser/Parsers`.
1. `basic.py` - парсинг простых и общих выражений: таких как перечисления, числовые литералы, boolean.
2. `arithmetic_exprs.py` - парсинг арифметических выражений в соответствии с порядком группировки и уровнями старшества.
3. `boolean_exprs.py` - парсинг логических выражений в соответствии с порядком группировки и уровнями старшества.
4. `statements.py` - парсинг утверждений: присвоений, циклов, условий.
5. `io.py` - парсинг выражений, соответствующих операциям ввода-вывода.
6. `functions.py` - парсинг конструкций, связанных с реализацией функций.
7. `strings.py` - парсинг строк и символов, а также определение предопределенных функций для работы со строками и символами.
8. `arrays.py` - парсинг конструкций, связанных с реализацией массивов, а также определение предопределенных функций.

AST-классы находся в директории `Parser/AST`.

Файловая структура AST-классов почти в точности повторяет файловую структуру парсеров.

В `common.py` находятся AST-классы `Pointer` (реализация указателей для интерпреатора) и `Enumeration` (перечисления: используются для описания массивов и аргументов функций)

**Результат работы парсера - AST.**

### Запуск

Запуск интерпретатора осуществляется следующим образом:

```
./rc -i program.expr
```
Где `program.expr` - путь к файлу с программой, которую нужно интерпретировать.

Например:
```
./rc -i compiler-tests/core/test025.expr
```

Запуск компилятора в код стековой виртуальной машины:

```
./rc -s program.expr
```
Где `program.expr` - путь к файлу с программой, которую нужно компилировать.

Например:
```
./rc -s compiler-tests/core/test025.expr
```

Запуск компилятора в ASM-код под X86:

```
./rc -o program.expr
```
Где `program.expr` - путь к файлу с программой, которую нужно компилировать.

Например:
```
./rc -o compiler-tests/core/test025.expr
```

### Запуск тестов

Запуск тестов может быть осуществлен "из коробки", все пути уже замаплены нужным образом.

Для запуска набора тестов необходимо выполнить:
```
make -f checkInterpreter
```
Где `checkInterpreter` - make-файл, с командами запуска тестов и сверки результатов.

Например:
```
cd compiler-tests/core && make -f checkInterpreter
```
```
cd compiler-tests/core && make -f checkStackMachine
```
```
cd compiler-tests/core && make -f checkCompiler
```
