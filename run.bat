@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo YtubeData - أداة استخراج البيانات الوصفية من يوتيوب
echo المبرمج: Sayers Linux
echo.

:: التحقق من وجود Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo خطأ: لم يتم العثور على Python. يرجى تثبيت Python 3.6 أو أحدث.
    echo يمكنك تنزيل Python من https://www.python.org/downloads/
    pause
    exit /b 1
)

:: التحقق من وجود المكتبات المطلوبة
echo جاري التحقق من المكتبات المطلوبة...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo حدث خطأ أثناء تثبيت المكتبات المطلوبة.
    pause
    exit /b 1
)

:menu
cls
echo YtubeData - أداة استخراج البيانات الوصفية من يوتيوب
echo ====================================================
echo.
echo 1. استخراج بيانات فيديو
echo 2. استخراج بيانات قناة
echo 3. تشغيل الأمثلة
echo 4. تشغيل الاختبارات
echo 5. خروج
echo.

set /p choice=اختر رقم العملية: 

if "%choice%"=="1" goto video
if "%choice%"=="2" goto channel
if "%choice%"=="3" goto examples
if "%choice%"=="4" goto tests
if "%choice%"=="5" goto end

echo خيار غير صالح. يرجى المحاولة مرة أخرى.
pause
goto menu

:video
cls
echo استخراج بيانات فيديو
echo =================
echo.
set /p url=أدخل رابط الفيديو: 

echo.
echo اختر تنسيق الإخراج:
echo 1. عرض في وحدة التحكم
echo 2. حفظ كملف JSON
echo 3. حفظ كملف CSV
echo.

set /p format=اختر رقم التنسيق: 

if "%format%"=="1" (
    python YtubeData.py "%url%" -t video -f console
) else if "%format%"=="2" (
    set /p filename=أدخل اسم ملف الإخراج (الافتراضي: video_data.json): 
    if "!filename!"=="" set filename=video_data.json
    python YtubeData.py "%url%" -t video -f json -o "!filename!"
) else if "%format%"=="3" (
    set /p filename=أدخل اسم ملف الإخراج (الافتراضي: video_data.csv): 
    if "!filename!"=="" set filename=video_data.csv
    python YtubeData.py "%url%" -t video -f csv -o "!filename!"
) else (
    echo خيار غير صالح.
)

pause
goto menu

:channel
cls
echo استخراج بيانات قناة
echo =================
echo.
set /p url=أدخل رابط القناة: 

echo.
echo اختر تنسيق الإخراج:
echo 1. عرض في وحدة التحكم
echo 2. حفظ كملف JSON
echo 3. حفظ كملف CSV
echo.

set /p format=اختر رقم التنسيق: 

if "%format%"=="1" (
    python YtubeData.py "%url%" -t channel -f console
) else if "%format%"=="2" (
    set /p filename=أدخل اسم ملف الإخراج (الافتراضي: channel_data.json): 
    if "!filename!"=="" set filename=channel_data.json
    python YtubeData.py "%url%" -t channel -f json -o "!filename!"
) else if "%format%"=="3" (
    set /p filename=أدخل اسم ملف الإخراج (الافتراضي: channel_data.csv): 
    if "!filename!"=="" set filename=channel_data.csv
    python YtubeData.py "%url%" -t channel -f csv -o "!filename!"
) else (
    echo خيار غير صالح.
)

pause
goto menu

:examples
cls
echo تشغيل الأمثلة
echo ============
echo.
echo سيتم تشغيل ملف examples.py الذي يوضح كيفية استخدام YtubeData برمجياً.
echo قد تحتاج إلى تعديل روابط الفيديوهات والقنوات في الملف قبل التشغيل.
echo.
set /p confirm=هل تريد المتابعة؟ (y/n): 

if /i "%confirm%"=="y" (
    python examples.py
)

pause
goto menu

:tests
cls
echo تشغيل الاختبارات
echo ==============
echo.
python test_ytubedata.py

pause
goto menu

:end
echo.
echo شكراً لاستخدام YtubeData!
echo المبرمج: Sayers Linux
echo البريد الإلكتروني: sayerlinux@gmail.com
echo.

endlocal
exit /b 0