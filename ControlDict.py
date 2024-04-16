"""!
@file
@brief Создание файла controlDict
"""

class ControlDict:
    """!
    @brief Генерирование текстового представления файла controlDict

    Этот класс генерирует текстовое представления файла controlDict и возвращает в виде строки
    """

    def __init__(self):
        """!
        @brief Конструктор класса.

        Конструктора класса.
        """

        self.content = {}

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        for key, value in self.content.items():
            result += str(key) + "\t" + str(value) + "\n"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        for key, value in self.content.items():
            result += str(key) + "\t" + str(value) + ";\n\n"
        return result


    def __getitem__(self,key):
        """!
        Получает элемент по указанному ключу.

        @param key: Ключ для доступа к элементу.
        @return Элемент, связанный с указанным ключом.
        @exception KeyError: Если ключ не найден.
        """

        return self.content[key]

    def __setitem__(self,key,value):
        """!
        Устанавливает значение для указанного ключа.

        @param key: Ключ, для которого устанавливается значение.
        @param value: Устанавливаемое значение.
        @exception KeyError: Если ключ не найден.
        """

        self.content[key]=value

    def header(self):
        """!
        @brief Метод получения шапки файла openFoam.

        Возвращает строковое представление шапки файла openFoam.
        @return Строковое представление шапки файла openFoam.
        """

        return """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2306                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"""