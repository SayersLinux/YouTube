#!/bin/bash

# YtubeData - أداة استخراج البيانات الوصفية من يوتيوب
# المبرمج: Sayers Linux
# البريد الإلكتروني: sayerlinux@gmail.com

# التأكد من أن النص العربي يظهر بشكل صحيح
export LANG=en_US.UTF-8

# ألوان النص
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}خطأ: لم يتم العثور على Python. يرجى تثبيت Python 3.6 أو أحدث.${NC}"
    echo "يمكنك تنزيل Python من https://www.python.org/downloads/"
    exit 1
fi

# التحقق من وجود pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}خطأ: لم يتم العثور على pip. يرجى تثبيت pip.${NC}"
    exit 1
fi

# التحقق من وجود المكتبات المطلوبة
echo -e "${BLUE}جاري التحقق من المكتبات المطلوبة...${NC}"
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}حدث خطأ أثناء تثبيت المكتبات المطلوبة.${NC}"
    exit 1
fi

# جعل الملف قابل للتنفيذ
chmod +x YtubeData.py

# دالة عرض القائمة الرئيسية
show_menu() {
    clear
    echo -e "${CYAN}YtubeData - أداة استخراج البيانات الوصفية من يوتيوب${NC}"
    echo "===================================================="
    echo ""
    echo "1. استخراج بيانات فيديو"
    echo "2. استخراج بيانات قناة"
    echo "3. تشغيل الأمثلة"
    echo "4. تشغيل الاختبارات"
    echo "5. خروج"
    echo ""
    echo -n "اختر رقم العملية: "
    read choice
    
    case $choice in
        1) extract_video ;;
        2) extract_channel ;;
        3) run_examples ;;
        4) run_tests ;;
        5) exit_app ;;
        *) 
            echo -e "${RED}خيار غير صالح. يرجى المحاولة مرة أخرى.${NC}"
            read -p "اضغط Enter للمتابعة..."
            show_menu
            ;;
    esac
}

# دالة استخراج بيانات فيديو
extract_video() {
    clear
    echo -e "${CYAN}استخراج بيانات فيديو${NC}"
    echo "================="
    echo ""
    echo -n "أدخل رابط الفيديو: "
    read url
    
    echo ""
    echo "اختر تنسيق الإخراج:"
    echo "1. عرض في وحدة التحكم"
    echo "2. حفظ كملف JSON"
    echo "3. حفظ كملف CSV"
    echo ""
    echo -n "اختر رقم التنسيق: "
    read format
    
    case $format in
        1)
            python3 YtubeData.py "$url" -t video -f console
            ;;
        2)
            echo -n "أدخل اسم ملف الإخراج (الافتراضي: video_data.json): "
            read filename
            if [ -z "$filename" ]; then
                filename="video_data.json"
            fi
            python3 YtubeData.py "$url" -t video -f json -o "$filename"
            ;;
        3)
            echo -n "أدخل اسم ملف الإخراج (الافتراضي: video_data.csv): "
            read filename
            if [ -z "$filename" ]; then
                filename="video_data.csv"
            fi
            python3 YtubeData.py "$url" -t video -f csv -o "$filename"
            ;;
        *)
            echo -e "${RED}خيار غير صالح.${NC}"
            ;;
    esac
    
    read -p "اضغط Enter للمتابعة..."
    show_menu
}

# دالة استخراج بيانات قناة
extract_channel() {
    clear
    echo -e "${CYAN}استخراج بيانات قناة${NC}"
    echo "================="
    echo ""
    echo -n "أدخل رابط القناة: "
    read url
    
    echo ""
    echo "اختر تنسيق الإخراج:"
    echo "1. عرض في وحدة التحكم"
    echo "2. حفظ كملف JSON"
    echo "3. حفظ كملف CSV"
    echo ""
    echo -n "اختر رقم التنسيق: "
    read format
    
    case $format in
        1)
            python3 YtubeData.py "$url" -t channel -f console
            ;;
        2)
            echo -n "أدخل اسم ملف الإخراج (الافتراضي: channel_data.json): "
            read filename
            if [ -z "$filename" ]; then
                filename="channel_data.json"
            fi
            python3 YtubeData.py "$url" -t channel -f json -o "$filename"
            ;;
        3)
            echo -n "أدخل اسم ملف الإخراج (الافتراضي: channel_data.csv): "
            read filename
            if [ -z "$filename" ]; then
                filename="channel_data.csv"
            fi
            python3 YtubeData.py "$url" -t channel -f csv -o "$filename"
            ;;
        *)
            echo -e "${RED}خيار غير صالح.${NC}"
            ;;
    esac
    
    read -p "اضغط Enter للمتابعة..."
    show_menu
}

# دالة تشغيل الأمثلة
run_examples() {
    clear
    echo -e "${CYAN}تشغيل الأمثلة${NC}"
    echo "============"
    echo ""
    echo "سيتم تشغيل ملف examples.py الذي يوضح كيفية استخدام YtubeData برمجياً."
    echo "قد تحتاج إلى تعديل روابط الفيديوهات والقنوات في الملف قبل التشغيل."
    echo ""
    echo -n "هل تريد المتابعة؟ (y/n): "
    read confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        python3 examples.py
    fi
    
    read -p "اضغط Enter للمتابعة..."
    show_menu
}

# دالة تشغيل الاختبارات
run_tests() {
    clear
    echo -e "${CYAN}تشغيل الاختبارات${NC}"
    echo "=============="
    echo ""
    python3 test_ytubedata.py
    
    read -p "اضغط Enter للمتابعة..."
    show_menu
}

# دالة الخروج
exit_app() {
    echo ""
    echo -e "${GREEN}شكراً لاستخدام YtubeData!${NC}"
    echo "المبرمج: Sayers Linux"
    echo "البريد الإلكتروني: sayerlinux@gmail.com"
    echo ""
    exit 0
}

# بدء البرنامج
show_menu