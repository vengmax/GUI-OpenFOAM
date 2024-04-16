# Импортируем необходимые модули
from paraview.simple import *
import tempfile
import shutil
import os
import sys
from decimal import Decimal

# Получение параметров из аргументов командной строки
argvList = sys.argv
pathFileFoam = argvList[1]
if argvList[3].startswith("-"):
    argvList[3] = argvList[3][1:]
if argvList[4].startswith("-"):
    argvList[4] = argvList[4][1:]
if argvList[5].startswith("-"):
    argvList[5] = argvList[5][1:]
if argvList[6].startswith("-"):
    argvList[6] = argvList[6][1:]
valueAxis = int(argvList[2])
valueOffset = float(argvList[3])
valueXRotation = int(argvList[4])
valueYRotation = int(argvList[5])
valueZRotation = int(argvList[6])
nameVar = ""
timeValue = 0
if (len(argvList) > 8):
    nameVar = argvList[7]
    timeValue = Decimal(argvList[8])


# Открываем файл с расширением .foam
reader = OpenFOAMReader(FileName=pathFileFoam)
reader.UpdatePipeline()

# Устанавливаем временной шаг
# animationScene1 = GetAnimationScene()
# animationScene1.AnimationTime = timeValue

slice = Slice(Input=reader)
slice.SliceType = 'Plane'
slice.SliceType.Origin = [0.0, 0.0, 0.0]
if(valueAxis == 0):
    slice.SliceType.Normal = [1.0, 0.0, 0.0]
    if (valueOffset < 0):
        slice.SliceOffsetValues = [reader.GetDataInformation().DataInformation.GetBounds()[0] * abs(valueOffset)]
    elif (valueOffset > 0):
        slice.SliceOffsetValues = [reader.GetDataInformation().DataInformation.GetBounds()[1] * abs(valueOffset)]
    else:
        slice.SliceOffsetValues = [0.0]
elif(valueAxis == 1):
    slice.SliceType.Normal = [0.0, 1.0, 0.0]
    if (valueOffset < 0):
        slice.SliceOffsetValues = [reader.GetDataInformation().DataInformation.GetBounds()[2] * abs(valueOffset)]
    elif (valueOffset > 0):
        slice.SliceOffsetValues = [reader.GetDataInformation().DataInformation.GetBounds()[3] * abs(valueOffset)]
    else:
        slice.SliceOffsetValues = [0.0]
elif(valueAxis == 2):
    slice.SliceType.Normal = [0.0, 0.0, 1.0]
    if (valueOffset < 0):
        slice.SliceOffsetValues = [reader.GetDataInformation().DataInformation.GetBounds()[4] * abs(valueOffset)]
    elif (valueOffset > 0):
        slice.SliceOffsetValues = [reader.GetDataInformation().DataInformation.GetBounds()[5] * abs(valueOffset)]
    else:
        slice.SliceOffsetValues = [0.0]

# Получаем активное представление
view = GetActiveViewOrCreate('RenderView')
view.ViewSize = [819, 600]
view.OrientationAxesVisibility = 0

# Поворот камеры
camera = GetActiveCamera()
transform = Transform(Input=slice)
if(valueAxis == 0):
    transform.Transform.Rotate = [valueXRotation, valueZRotation + 90, valueYRotation + 90]
elif(valueAxis == 1):
    camera.Yaw(90)
    transform.Transform.Rotate = [valueXRotation, -valueYRotation + 90, valueZRotation + 90]
elif(valueAxis == 2):
    transform.Transform.Rotate = [-valueZRotation, valueXRotation, valueYRotation]

# Получаем прокси объект переменной
variable = FindSource(nameVar)

# Получаем дисплей для переменной
display = GetDisplayProperties(variable, view)

# Создание легенды
if nameVar != "":
    colorLookupTable = GetColorTransferFunction(nameVar)
    legend = GetScalarBar(colorLookupTable, view)
    legend.ComponentTitle = ""
    legend.Title = 'T' # Заголовок легенды (имя переменной)

view.ViewTime = timeValue
view.Update()

# Устанавливаем заголовок шкалы цветов
ColorBy(display, ('POINTS', nameVar))

Render()

# Создаем временный файл
temp_dir = tempfile.gettempdir()
custom_temp_dir = os.path.join(temp_dir, 'GUIopenFoam')
os.makedirs(custom_temp_dir, exist_ok=True)
temp_file_path = os.path.join(custom_temp_dir, 'screenshot.png')

SaveScreenshot(temp_file_path, view)
# Interact()
