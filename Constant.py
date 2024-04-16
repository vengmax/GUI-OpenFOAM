"""!
@file
@brief Создание необходимых файлов констант
"""

class Constant:
    """!
    @brief Генерирование текстового представления файла physicalProperties

    Этот класс генерирует текстовое представления файла physicalProperties и возвращает в виде строки
    """

    def __init__(self, name, value, unit, typePropetries):
        """!
        @brief Конструктор класса.

        Конструктора класса.
        @param name (str) - название константы соответствующее названию константы в формуле решателя
        @param value (str) - значение константы name
        @param unit (str) - единицы измерения в формате openFoam (пример: "[0 1 -1 0 0 0 0 ]")
        @param typePropetries (str) - тип значения в формате openFoam (пример: "transportProperties")
        """
        self.properties = [name, value, unit]
        self.typePropetries = typePropetries

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        result += self.properties[0] + "\t" + self.properties[2] + "\t" + self.properties[1] + ";\n\n"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        result += self.properties[0] + "\t" + self.properties[2] + "\t" + self.properties[1] + ";\n\n"
        return result

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
    location    "constant";
    object      """+self.typePropetries+""";
}
"""