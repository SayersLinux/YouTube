#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
أمثلة على استخدام YtubeData برمجياً

هذا الملف يوضح كيفية استخدام وظائف YtubeData في مشاريع Python الأخرى
"""

import json
import pandas as pd
from YtubeData import get_video_metadata, get_channel_metadata


def example_get_video_data():
    """مثال على استخراج بيانات فيديو وحفظها بتنسيق JSON"""
    print("\n=== مثال على استخراج بيانات فيديو ===\n")
    
    # استبدل هذا برابط فيديو حقيقي
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # استخراج البيانات
    metadata = get_video_metadata(video_url)
    
    if metadata:
        # طباعة بعض البيانات الأساسية
        print(f"عنوان الفيديو: {metadata['عنوان الفيديو']}")
        print(f"اسم القناة: {metadata['اسم القناة']}")
        print(f"تاريخ النشر: {metadata['تاريخ النشر']}")
        print(f"عدد المشاهدات: {metadata['عدد المشاهدات']}")
        
        # حفظ البيانات كملف JSON
        with open("video_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print("\nتم حفظ البيانات الكاملة في ملف video_metadata.json")
        
        # استخراج معلومات الدقة إلى DataFrame
        if "الدقة المتاحة" in metadata and metadata["الدقة المتاحة"]:
            streams_df = pd.DataFrame(metadata["الدقة المتاحة"])
            print("\nمعلومات الدقة المتاحة:")
            print(streams_df)


def example_get_channel_data():
    """مثال على استخراج بيانات قناة وتحليلها"""
    print("\n=== مثال على استخراج بيانات قناة ===\n")
    
    # استبدل هذا برابط قناة حقيقية
    channel_url = "https://www.youtube.com/c/GoogleDevelopers"
    
    # استخراج البيانات
    metadata = get_channel_metadata(channel_url)
    
    if metadata:
        # طباعة بعض البيانات الأساسية
        print(f"اسم القناة: {metadata['اسم القناة']}")
        print(f"معرف القناة: {metadata['معرف القناة']}")
        print(f"الوصف: {metadata['الوصف']}")
        
        # تحليل آخر الفيديوهات
        if "آخر الفيديوهات" in metadata and metadata["آخر الفيديوهات"]:
            videos_df = pd.DataFrame(metadata["آخر الفيديوهات"])
            print("\nآخر الفيديوهات المنشورة:")
            print(videos_df[["عنوان الفيديو", "تاريخ النشر", "عدد المشاهدات"]])
            
            # حساب متوسط عدد المشاهدات
            try:
                views = [int(v.replace(",", "")) for v in videos_df["عدد المشاهدات"] if v != "غير متوفر"]
                if views:
                    avg_views = sum(views) / len(views)
                    print(f"\nمتوسط عدد المشاهدات للفيديوهات الأخيرة: {avg_views:,.0f}")
            except (ValueError, TypeError):
                pass


def example_batch_processing():
    """مثال على معالجة مجموعة من الفيديوهات"""
    print("\n=== مثال على معالجة مجموعة من الفيديوهات ===\n")
    
    # قائمة بروابط الفيديوهات (استبدلها بروابط حقيقية)
    video_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    ]
    
    # جمع البيانات من كل الفيديوهات
    all_data = []
    for url in video_urls:
        print(f"جاري معالجة: {url}")
        metadata = get_video_metadata(url)
        if metadata:
            # استخراج البيانات الأساسية فقط
            basic_data = {
                "عنوان": metadata["عنوان الفيديو"],
                "قناة": metadata["اسم القناة"],
                "تاريخ": metadata["تاريخ النشر"],
                "مشاهدات": metadata["عدد المشاهدات"],
                "مدة": metadata["المدة (منسقة)"],
                "رابط": url
            }
            all_data.append(basic_data)
    
    # إنشاء DataFrame وحفظه كملف CSV
    if all_data:
        df = pd.DataFrame(all_data)
        print("\nملخص البيانات:")
        print(df)
        
        # حفظ البيانات
        df.to_csv("videos_summary.csv", index=False, encoding="utf-8")
        print("\nتم حفظ البيانات في ملف videos_summary.csv")


if __name__ == "__main__":
    print("أمثلة على استخدام YtubeData برمجياً\n")
    print("ملاحظة: قد تحتاج إلى تعديل روابط الفيديوهات والقنوات في الأمثلة لتجربتها")
    
    try:
        example_get_video_data()
        example_get_channel_data()
        example_batch_processing()
    except Exception as e:
        print(f"\nحدث خطأ: {str(e)}")
    
    print("\nانتهت الأمثلة")