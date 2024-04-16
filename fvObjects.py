"""!
@file
@brief Создание необходимых файлов FV
"""

class FvSchemes:
    """!
    @brief Генерирование текстового представления файла fvSchemes

    Этот класс генерирует текстовое представления файла fvSchemes и возвращает в виде строки
    """

    def __init__(self):
        """!
        @brief Конструктор класса.

        Конструктор класса
        """
        self.solver = ""

    def setSolver(self, solver):
        """!
        @brief Метод установки решателя.

        Метод установки решателя для создания соответствующего файла fvShemes.

        @param solver (str) - название решателя
        """
        self.solver = solver

    def getSolver(self):
        """!
        @brief Метод получения решателя.

        Метод получения решателя.

        @return solver (str) - название решателя
        """
        return self.solver

    def setText(self, text):
        """!
        @brief Метод установки содержимого fvSchemes.

        Метод установки содержимого fvSchemes.

        @patam text (str) - текст файла
        """

        if self.solver == "icoFoam":
            self.icoFoamScheme = text
        elif self.solver == "laplacianFoam":
            self.laplacianFoamScheme = text

    def getText(self):
        """!
        @brief Метод получения содержимого fvSchemes.

        Метод получения содержимого fvSchemes.

        @return text (str) - текст файла
        """

        if self.solver == "icoFoam":
            return self.icoFoamScheme
        elif self.solver == "laplacianFoam":
            return self.laplacianFoamScheme
        else:
            return ""

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        if self.solver == "icoFoam":
            return self.icoFoamScheme
        elif self.solver == "laplacianFoam":
            return self.laplacianFoamScheme
        else:
            return ""

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        if self.solver == "icoFoam":
            return self.icoFoamScheme
        elif self.solver == "laplacianFoam":
            return self.laplacianFoamScheme
        else:
            return ""

    laplacianFoamScheme = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
    grad(T)         Gauss linear;
}

divSchemes
{
    default         none;
}

laplacianSchemes
{
    default         none;
    laplacian(DT,T) Gauss linear corrected;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         corrected;
}


// ************************************************************************* //
"""

    """Переменная содержащая представление файла"""
    icoFoamScheme = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
    grad(p)         Gauss linear;
}

divSchemes
{
    default         none;
    div(phi,U)      Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear orthogonal;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         orthogonal;
}


// ************************************************************************* //
"""


class FvSolution:
    """!
    @brief Генерирование текстового представления файла fvSolution

    Этот класс генерирует текстовое представления файла fvSolution и возвращает в виде строки
    """

    def __init__(self):
        """!
        @brief Конструктор класса.

        Описание конструктора класса.

        @param solver (str) - название решателя.
        """

        self.solver = ""

    def setSolver(self, solver):
        """!
        @brief Метод установки решателя.

        Метод установки решателя для создания соответствующего файла fvSolution.

        @param solver (str) - название решателя
        """
        self.solver = solver

    def getSolver(self):
        """!
        @brief Метод получения решателя.

        Метод получения решателя.

        @return solver (str) - название решателя
        """
        return self.solver

    def setText(self, text):
        """!
        @brief Метод установки содержимого fvSolution.

        Метод установки содержимого fvSolution.

        @patam text (str) - текст файла
        """

        if self.solver == "icoFoam":
            self.icoFoamSolution = text
        elif self.solver == "laplacianFoam":
            self.laplacianFoamSolution = text

    def getText(self):
        """!
        @brief Метод получения содержимого fvSolution.

        Метод получения содержимого fvSolution.

        @return text (str) - текст файла
        """

        if self.solver == "icoFoam":
            return self.icoFoamSolution
        elif self.solver == "laplacianFoam":
            return self.laplacianFoamSolution
        else:
            return ""

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        if self.solver == "icoFoam":
            return self.icoFoamSolution
        elif self.solver == "laplacianFoam":
            return self.laplacianFoamSolution
        else:
            return ""

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        if self.solver == "icoFoam":
            return self.icoFoamSolution
        elif self.solver == "laplacianFoam":
            return self.laplacianFoamSolution
        else:
            return ""

    laplacianFoamSolution = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

solvers
{
    T
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0;
    }
}

SIMPLE
{
    nNonOrthogonalCorrectors 2;

    residualControl
    {
	T		1e-06;
    }
    
}


// ************************************************************************* //
"""

    icoFoamSolution = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

solvers
{
    p
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-06;
        relTol          0.05;
    }

    pFinal
    {
        $p;
        relTol          0;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-05;
        relTol          0;
    }
}

PISO
{
    nCorrectors     2;
    nNonOrthogonalCorrectors 0;
    pRefCell        0;
    pRefValue       0;
}


// ************************************************************************* //
"""