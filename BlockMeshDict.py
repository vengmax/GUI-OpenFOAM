"""!
@file
@brief Создание файла blockMeshDict
"""

class BlockMeshDictBoundaries():
    """!
    @brief Генерирование текстового представления блока boundary в файле blockMeshDict

    Этот класс генерирует текстовое представления блока boundary в файле blockMeshDict и возвращает в виде строки
    """

    correct = True
    def __init__(self, boundary):
        """!
        @brief Конструктор класса.

        Инициализация блока boundary файла blockMeshDict
        @param boundary (list(dict)) - границы модели (пример:
            {
                'name': '<название границы>',
                'type': '<тип границы>',
                'faces': '<список>'
            },
            {
                ...
            };
            где name (str), type (str), faces (list(list(int))
            )
        """

        self.boundary=boundary

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        if (self.correct):
            result += "boundary\n("
            for boun in self.boundary:
                result += "\n\t" + boun["name"] + "\n\t{\n\t\ttype " + boun["type"] + ";\n"
                result += "\t\tfaces\n\t\t(\n"
                for bounFaces in boun["faces"]:
                    result += "\t\t\t(" + ' '.join(str(n) for n in bounFaces) + ")\n"
                result += "\t\t);\n\t}\n"
            result += ");"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        if (self.correct):
            result += "boundary\n("
            for boun in self.boundary:
                result += "\n\t" + boun["name"] + "\n\t{\n\t\ttype "+ boun["type"] + ";\n"
                result += "\t\tfaces\n\t\t(\n"
                for bounFaces in boun["faces"]:
                    result += "\t\t\t(" + ' '.join(str(n) for n in bounFaces) + ")\n"
                result += "\t\t);\n\t}\n"
            result += ");"
        return result

class BlockMeshDictVertices():
    """!
    @brief Генерирование текстового представления блока vertices в файле blockMeshDict

    Этот класс генерирует текстовое представления блока vertices в файле blockMeshDict и возвращает в виде строки
    """

    correct = True
    def __init__(self,coordinates):
        """!
        @brief Конструктор класса.

        Инициализация вершин фигуры
        @param coordinates (list(list(int))) - координаты(x,y,z) вершин
        """

        self.coordinates=coordinates
        if (len(self.coordinates) != 8):
            self.correct = False

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        if (self.correct):
            result += "vertices\n(\n"
            i = 0
            for vert in self.coordinates:
                result += "\t(" + ' '.join(str(n) for n in vert) + f")\t//{i}\n"
                i += 1
            result += ");"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        if(self.correct):
            result += "vertices\n(\n"
            i = 0
            for vert in self.coordinates:
                result += "\t("+' '.join(str(n) for n in vert)+f")\t//{i}\n"
                i += 1
            result += ");"
        return result

class BlockMeshDictBlocks():
    """!
    @brief Генерирование текстового представления блока blocks в файле blockMeshDict

    Этот класс генерирует текстовое представления блока blocks в файле blockMeshDict и возвращает в виде строки
    """

    def __init__(self, nx, ny, nz):
        """!
        @brief Конструктор класса.

        Инициализация количество ячеек по Ox, Oy, Oz.
        @param nx - количество ячеек по Ox
        @param ny - количество ячеек по Oy
        @param nz - количество ячеек по Oz
        """

        self.nx = nx
        self.ny = ny
        self.nz = nz

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = f"blocks\n(\n\t hex (0 1 2 3 4 5 6 7) ({self.nx} {self.ny} {self.nz}) simpleGrading (1 1 1)\n);"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result=f"blocks\n(\n\t hex (0 1 2 3 4 5 6 7) ({self.nx} {self.ny} {self.nz}) simpleGrading (1 1 1)\n);"
        return result

class BlockMeshDictEdges():
    """!
    @brief Генерирование текстового представления блока edges в файле blockMeshDict

    Этот класс генерирует текстовое представления блока edges в файле blockMeshDict и возвращает в виде строки
    """

    def __init__(self, settingsEdges):
        """!
        @brief Конструктор класса.

        Инициализация блока edges в файле blockMeshDict.
        @param settingsEdges (list(list)) - настройки для edges (пример: [["arc", 0, 1, "origin", [0, 0, 0]], [...], ...])
        """

        self.settingsEdges=settingsEdges

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += "edges\n(\n"
        for val in self.settingsEdges:
            result += "\t" + val[0] + " " + str(val[1]) + " " + str(val[2]) + " "+val[3]+" (" + ' '.join(str(n) for n in val[4]) + f")\n"
        result += ");"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += "edges\n(\n"
        for val in self.settingsEdges:
            result += "\t" + val[0] + " " + str(val[1]) + " " + str(val[2]) + " "+val[3]+" (" + ' '.join(str(n) for n in val[4]) + f")\n"
        result += ");"
        return result

class BlockMeshDictFaces():
    """!
    @brief Генерирование текстового представления блока faces в файле blockMeshDict

    Этот класс генерирует текстовое представления блока faces в файле blockMeshDict и возвращает в виде строки
    """

    def __init__(self, settingsFaces):
        """!
        @brief Конструктор класса.

        Инициализация блока faces в файле blockMeshDict.
        @param settingsFaces (list(list)) - настройки для faces (пример: [[[0, 0], "sphere"], [...], ...])
        """

        self.settingsFaces = settingsFaces

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += "faces\n(\n"
        for val in self.settingsFaces:
            result += "\tproject (" + ' '.join(str(n) for n in val[0]) + f") " + val[1] + "\n"
        result += ");"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += "faces\n(\n"
        for val in self.settingsFaces:
            result += "\tproject (" + ' '.join(str(n) for n in val[0]) + f") "+ val[1] +"\n"
        result += ");"
        return result

class BlockMeshDictGeometry():
    """!
    @brief Генерирование текстового представления блока geometry в файле blockMeshDict

    Этот класс генерирует текстовое представления блока geometry в файле blockMeshDict и возвращает в виде строки
    """

    def __init__(self, geometry):
        """!
        @brief Конструктор класса.

        Инициализация блока geometry в файле blockMeshDict.
        @param geometry (list(dict)) - настройки для geometry (пример: [
                {
                    'name': '<название>',
                    'type': '<тип>',
                    'origin': '<начальная точка>',
                    'radius': '<радиус>',
                },
            ])
            где name (str), type (str), origin (str), radius (str).
        """

        self.geometry=geometry

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += "geometry\n{"
        for geom in self.geometry:
            result += "\n\t" + geom["name"] + "\n\t{\n\t\ttype " + geom["type"] + ";\n"
            result += "\t\torigin " + geom["origin"] + ";\n"
            result += "\t\tradius " + geom["radius"] + ";\n"
            result += "\t}\n"
        result += "};"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += "geometry\n{"
        for geom in self.geometry:
            result += "\n\t" + geom["name"] + "\n\t{\n\t\ttype " + geom["type"] + ";\n"
            result += "\t\torigin " + geom["origin"] + ";\n"
            result += "\t\tradius " + geom["radius"] + ";\n"
            result += "\t}\n"
        result += "};"
        return result

class BlockMeshDict:
    """!
    @brief Генерирование текстового представления файла blockMeshDict

    Этот класс генерирует текстовое представления файла blockMeshDict и возвращает в виде строки
    """

    def __init__(self, scale, vertices, blocks, boundary):
        """!
        @brief Конструктор класса.

        Инициализация файла blockMeshDict.
        @param scale (str) - значение масштабирование в модели openFoam
        @param vertices (BlockMeshDictVertices) - вершины
        @param blocks (BlockMeshDictBlocks) - ячейки
        @param boundary (BlockMeshDictBoundaries) - границы
        """

        self.scale = scale
        self.vertices = vertices
        self.blocks = blocks
        self.boundary = boundary
        self.edges = None
        self.faces = None
        self.geometry = None

    def setEndges(self, edges):
        """!
        @brief Метод добавления блока edges.

        Метод добавления блока edges в файл BlockMeshDict.
        @param edges (BlockMeshDictEdges) - edges
        """

        self.edges = edges

    def setFaces(self, faces):
        """!
        @brief Метод добавления блока faces.

        Метод добавления блока faces в файл BlockMeshDict.
        @param faces (BlockMeshDictFaces) - faces
        """

        self.faces = faces

    def setGeometry(self, geometry):
        """!
        @brief Метод добавления блока edges.

        Метод добавления блока geometry в файл BlockMeshDict.
        @param geometry (BlockMeshDictGeometry) - geometry
        """

        self.geometry = geometry

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        result += f"scale {self.scale};" + "\n\n"
        if (self.geometry != None):
            result += str(self.geometry) + "\n\n"
        result += str(self.vertices) + "\n\n"
        result += str(self.blocks) + "\n\n"
        if (self.edges != None):
            result += str(self.edges) + "\n\n"
        if (self.faces != None):
            result += str(self.faces) + "\n\n"
        result += str(self.boundary) + "\n\n"
        return result

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        result = ""
        result += self.header() + "\n\n"
        result += f"scale {self.scale};" + "\n\n"
        if (self.geometry != None):
            result += str(self.geometry) + "\n\n"
        result += str(self.vertices) + "\n\n"
        result += str(self.blocks) + "\n\n"
        if (self.edges != None):
            result += str(self.edges) + "\n\n"
        if (self.faces != None):
            result += str(self.faces) + "\n\n"
        result += str(self.boundary) + "\n\n"
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
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"""