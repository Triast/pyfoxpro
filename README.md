# pyfoxpro

[![pipeline status](http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/badges/master/pipeline.svg)](http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/commits/master) 
[![Latest Release](http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/badges/release.svg)](http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/releases) 

CLI для выполнения различных полезных команд с проектами, написанными на Visual FoxPro.

## Возможности приложения

Данное приложение имеет следующие возможности:

* Форматирование форм (.scx);
* Форматирование текстовых файлов (.prg);
* Форматирование библиотек классов (.vcx);
* Форматирование отчётов (.frx);
* Форматирование меню (.mnx) как нового формата Visual FoxPro 9.0, так и старого формата Visual FoxPro 6.0 с помощью параметра `--vfp6`.

## Использование приложения

### Зависимости

Приложению для работы необходим [Python](https://www.python.org/) версии не ниже 3.12. Python можно установить с помощью [Chocolatey](https://chocolatey.org/):

``` bash
choco install python312
```

Также для установки приложения рекомендуется использовать [pipx](https://github.com/pypa/pipx). Инструкция с установкой находится в README.md.

Для модификации и компиляции бинарных файлов необходимо установить среду разработки Visual FoxPro 9.0 SP2 и добавить папку с файлом `vfp9.exe` в `PATH`.

Для формирования текстовых файлов на основе бинарных файлов FoxPro необходимо установить [foxbin2prg](https://github.com/fdbozzo/foxbin2prg) и добавить папку с файлом `foxbin2prg.exe` в `PATH`.

## Установка

Чтобы избежать проблем с сертификатами при работе с [pypi.org](https://pypi.org/) из внутренней сети Энергосбыта и добавить в доверенные репозитории [GitLab Энергосбыта](http://gitlab.sbyt.gomelenergo.by) можно выполнить следующую команду:

``` bash
pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org gitlab.sbyt.gomelenergo.by"
```

Для установки приложения выполните следующую команду:

``` bash
pip install pyfoxpro --user --index-url http://gitlab.sbyt.gomelenergo.by/api/v4/projects/13/packages/pypi/simple
```

Или с помощью `pipx`:

``` bash
pipx install pyfoxpro --index-url http://gitlab.sbyt.gomelenergo.by/api/v4/projects/13/packages/pypi/simple
```

После выполнения данной команды в консоли появится возможность выполнения следующей команды:

``` bash
pyfoxpro /path/to/file
```

Или:

``` bash
python -m pyfoxpro /path/to/file
```

Данная команда должна отформатировать файл по пути /path/to/file. Файл должен иметь расширение .scx, .prg, .vcx, .frx или .mnx.

## Что нового?

Просмотреть историю версий можно в файле [CHANGELOG](/CHANGELOG.md).

## Разработка

Для начала необходимо установить следующее ПО:

* [git](https://git-scm.com/downloads)
* [foxbin2prg](https://github.com/fdbozzo/foxbin2prg)
* [Python](https://www.python.org/) версии не ниже 3.13
* [build](https://pypi.org/project/build/)

`git` и `Python` можно установить с помощью [Chocolatey](https://chocolatey.org/) следующими командами:

``` bash
choco install git.install
choco install python313
```

Или с помощью [Scoop](https://scoop.sh/):

``` bash
scoop install main/git
scoop install main/python
```

`build` можно установить с помощью следующей команды:

``` bash
pip install --user build
```

Или с помощью `pipx`:

``` bash
pipx install build
```

Для запуска и разработки выполните следующее:

* В консоли выполните ```git clone http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro.git```
* `cd ./pyfoxpro`
* `python -m venv ./venv/`
* `source ./venv/Scripts/activate`
* Для компиляции выполните `pyproject-build`
* Для установки проекта в режиме редактирования выполните `pip install --editable .`
* Для запуска `pyfoxpro /path/to/file` или `python -m pyfoxpro /path/to/file` или `python ./pyfoxpro/main.py /path/to/file`
* Для разработки откройте папку с проектом с помощью предпочитаемой среды разработки. К примеру, с помощью Visual Studio Code команда `code .`
