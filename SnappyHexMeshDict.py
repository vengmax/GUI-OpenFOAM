"""!
@file
@brief Создание необходимых файлов для импорта STL
"""

class SnappyHexMeshDict:
    """!
    @brief Генерирование текстового представления файла snappyHexMeshDict

    Этот класс генерирует текстовое представления файла snappyHexMeshDict и возвращает в виде строки
    """

    def __init__(self, name, scale, minPointBoundingBox, maxPointBoundingBox, locationInMesh):
        """!
        @brief Конструктор класса.

        Инициализация значений параметров файла snappyHexMeshDict
        @param name (str) - название файла stl с расширение
        @param scale (str) - масштаб модели stl относительно основной фигуры
        @param minPointBoundingBox (str) - начальная точка границы stl (пример: "0 0 0")
        @param maxPointBoundingBox (str) - конечная точка границы stl (пример: "1 1 1")
        @param locationInMesh (str) - точка ограничения построения сетки (пример: "0.95 0.95 0.95")
        """

        self.name = name
        self.scale = scale
        self.minPointBoundingBox = minPointBoundingBox
        self.maxPointBoundingBox = maxPointBoundingBox
        self.locationInMesh = locationInMesh
        self.initSnappyHexMeshDict()

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        return self.snappyHexMeshDict

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        return self.snappyHexMeshDict

    def initSnappyHexMeshDict(self):
        """!
        @brief Приватный метод инициализация строкого представления файла snappyHexMeshDict.

        Приватный метод инициализация строкого представления файла snappyHexMeshDict.
        """

        self.snappyHexMeshDict = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      snappyHexMeshDict;
}

castellatedMesh true;
snap            true;
addLayers       false;

geometry
{
    """+self.name+"""
    {
        type triSurfaceMesh;
		scale """+self.scale+""";
        name stl_surface;
    }
    
	refinementBox
	{
	 type searchableBox;
	 min ("""+self.minPointBoundingBox+""");
	 max ("""+self.maxPointBoundingBox+""");
	}
};

castellatedMeshControls
{
    maxLocalCells 100000;
    maxGlobalCells 2000000;
    minRefinementCells 0;
    nCellsBetweenLevels 1;

    features
    (
    );

    refinementSurfaces
    {
        stl_surface
        {
            level (1 2);
        }
    }

    resolveFeatureAngle 30;

    refinementRegions
    {
            refinementBox
                  {
                      mode inside;
                      levels ((1 2));
                  }
    }

    locationInMesh ("""+self.locationInMesh+"""); 
    allowFreeStandingZoneFaces true;
}

snapControls
{
    nSmoothPatch 3;
    tolerance 1.0;
    nSolveIter 300;
    nRelaxIter 5;

    nFeatureSnapIter 10;
    implicitFeatureSnap false;
    explicitFeatureSnap true;
    multiRegionFeatureSnap true;
}

addLayersControls
{
    relativeSizes true;

    layers
    {
    }

    expansionRatio 1.0;
    finalLayerThickness 0.3;
    minThickness 0.25;
    nGrow 0;

    featureAngle 30;
    nRelaxIter 5;
    nSmoothSurfaceNormals 1;
    nSmoothNormals 3;
    nSmoothThickness 10;
    maxFaceThicknessRatio 0.5;
    maxThicknessToMedialRatio 0.3;
    minMedianAxisAngle 90;
    nBufferCellsNoExtrude 0;
    nLayerIter 50;
    nRelaxedIter 20;
}

meshQualityControls
{
    #include "meshQualityDict"

    relaxed
    {
        maxNonOrtho 75;
    }

    nSmoothScale 4;
    errorReduction 0.75;
}

writeFlags
(
    scalarLevels    // write volScalarField with cellLevel for postprocessing
    layerSets       // write cellSets, faceSets of faces in layer
    layerFields     // write volScalarField for layer coverage
);

mergeTolerance 1E-6;

"""

class MeshQualityDict:
    """!
    @brief Генерирование текстового представления файла meshQualityDict

    Этот класс генерирует текстовое представления файла meshQualityDict и возвращает в виде строки
    """

    def __init__(self):
        """!
        @brief Конструктор класса.

        Конструктора класса.
        """

        pass

    def __str__(self):
        """!
        @brief Метод преобразования в строку.

        Возвращает строковое представление объекта.
        @return Строковое представление объекта.
        """

        return self.meshQualityDict

    def __repr__(self):
        """!
        @brief Метод представления объекта.

        Возвращает формальное строковое представление объекта,
        которое может быть использовано для его воссоздания.
        @return Формальное строковое представление объекта.
        """

        return self.meshQualityDict

    meshQualityDict = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      meshQualityDict;
}

#includeEtc "caseDicts/meshQualityDict"

"""