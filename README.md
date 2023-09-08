# pyfoxpro

CLI для выполнения различных полезных команд с проектами, написанными на Visual FoxPro.

## Возможности приложения

Данное приложение имеет следующие возможности:

* Форматирование форм (.scx);
* Форматирование текстовых файлов (.prg).

## Использование приложения

### Зависимости

Приложению для работы необходим [Python](https://www.python.org/) версии не ниже 3.11. Python можно установить с помощью [Chocolatey](https://chocolatey.org/):

``` bash
choco install python311
```

Также для установки приложения рекомендуется использовать [pipx](https://github.com/pypa/pipx). Инструкция с установкой находится в README.md.

Для модификации и компиляции бинарных файлов необходимо установить среду разработки Visual FoxPro 9.0 SP2 и добавить папку с файлом `vfp9.exe` в `PATH`.

Для формирования текстовых файлов на основе бинарных файлов FoxPro необходимо установить [foxbin2prg](https://github.com/fdbozzo/foxbin2prg) и добавить папку с файлом `foxbin2prg.exe` в `PATH`.

## Установка

Для установки приложения выполните следующую команду:

``` bash
pipx install pyfoxpro
```

После выполнения данной команды в консоли появится возможность выполнения следующей команды:

``` bash
pyfoxpro /path/to/file
```

Данная команда должна отформатировать файл по пути /path/to/file. Файл должен иметь расширение .scx или .prg.

## Что нового?

Просмотреть историю версий можно в файле [CHANGELOG](/CHANGELOG.md).

## Разработка

Для начала необходимо установить следующее ПО:

* [git](https://git-scm.com/downloads)
* [foxbin2prg](https://github.com/fdbozzo/foxbin2prg)
* [Python](https://www.python.org/) версии не ниже 3.11
* [Poetry](https://python-poetry.org/)

`git` и `Python` можно установить с помощью [Chocolatey](https://chocolatey.org/) следующими командами:

``` bash
choco install git.install
choco install python311
```

Для запуска и разработки выполните следующее:

* В консоли выполните ```git clone http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro.git```
* `cd ./pyfoxpro`
* `poetry install`
* Для запуска `poetry run pyfoxpro /path/to/file` или `poetry run python ./pyfoxpro/main.py /path/to/file`
* Для разработки откройте папку с проектом с помощью предпочитаемой среды разработки. К примеру, с помощью Visual Studio Code следующие команды:

    ``` bash
    poetry shell
    code .
    ```