"""!
@file
@brief Создание необходимых файлов начальных значений
"""

class BeginValue:
    """!
    @brief Генерирование текстового представления файла начальных значений

    Этот класс генерирует текстовое представления файла начальных значений и возвращает в виде строки
    """

    def __init__(self, name, typeValue, dimensions, internalField, boundaryField):
        """!
        @brief Конструктор класса.

        Инициализация начальных значений.
        @param name (str) - название начального значения соответствующее перемееной в формуле решателя
        @param typeValue (str) - тип начального значения (пример: "volScalarField")
        @param dimensions (str) - единицы измерения значения (пример: "[0 1 -1 0 0 0 0 ]")
        @param internalField (str) - значение внутри модели
        @param boundaryField (list(dict)) - значения на границах модели (пример:
            {
                'name': '<название границы>',
                'type': '<тип значения>',
                'value': '<значение>'
            },
            {
                ...
            };
            где name (str), type (str), value (str)
            )
        """

        self.name = name
        self.typeValue = typeValue
        self.dimensions = dimensions
        self.internalField = internalField
        self.boundaryField = boundaryField

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        result += "dimensions\t" + self.dimensions + ";\n\n"
        result += "internalField uniform " + self.internalField + ";\n\n"

        result += "boundaryField\n{\n"
        for boun in self.boundaryField:
            result += "\t" + boun["name"] + "\n\t{\n\t\ttype " + boun["type"] + ";\n"
            if boun["type"] == "fixedValue":
                result += "\t\tvalue uniform " + boun["value"] + ";\n"
            result += "\t}\n"
        result += "}"

        return result

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        result += "dimensions\t" + self.dimensions + ";\n\n"
        result += "internalField uniform " + self.internalField + ";\n\n"

        result += "boundaryField\n{\n"
        for boun in self.boundaryField:
            result += "\t" + boun["name"] + "\n\t{\n\t\ttype " + boun["type"] + ";\n"
            if boun["type"] == "fixedValue":
                result += "\t\tvalue uniform "+boun["value"]+";\n"
            result += "\t}\n"
        result += "}"

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
    class       """+self.typeValue+""";
    object      """+self.name+""";
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"""