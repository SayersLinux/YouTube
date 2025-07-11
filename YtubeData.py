#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YtubeData - أداة لاستخراج البيانات الوصفية من يوتيوب

المبرمج: Sayers Linux
البريد الإلكتروني: sayerlinux@gmail.com

وصف: أداة قوية لاستخراج البيانات الوصفية لفيديوهات وقنوات يوتيوب
وإظهار المعلومات الحساسة والتفاصيل الدقيقة.
"""

import sys
import os
import json
import argparse
import datetime
import pytz
import requests
import re
import pandas as pd
from tabulate import tabulate
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from pytube import YouTube, Channel
from pytube.exceptions import RegexMatchError, VideoUnavailable

# إنشاء كائن Console للطباعة الملونة
console = Console()

# تعريف الألوان
COLORS = {
    "title": "bold cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "info": "bold blue",
    "highlight": "bold magenta"
}


def print_banner():
    """عرض شعار البرنامج"""
    banner = """
╭──────────────────────────────────────────────────────────╮
│                                                          │
│  ██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗██████╗  █████╗ ████████╗ █████╗   │
│  ╚██╗ ██╔╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗  │
│   ╚████╔╝    ██║   ██║   ██║██████╔╝█████╗  ██║  ██║███████║   ██║   ███████║  │
│    ╚██╔╝     ██║   ██║   ██║██╔══██╗██╔══╝  ██║  ██║██╔══██║   ██║   ██╔══██║  │
│     ██║      ██║   ╚██████╔╝██████╔╝███████╗██████╔╝██║  ██║   ██║   ██║  ██║  │
│     ╚═╝      ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝  │
│                                                          │
│                  By: Sayers Linux                       │
│            Email: sayerlinux@gmail.com                  │
│                                                          │
╰──────────────────────────────────────────────────────────╯
    """
    console.print(Panel(banner, style="bold green"))


def format_date(date_str):
    """تنسيق التاريخ بشكل أفضل"""
    if not date_str:
        return "غير متوفر"
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return date_str


def format_duration(duration_seconds):
    """تحويل المدة من ثواني إلى تنسيق ساعات:دقائق:ثواني"""
    if not duration_seconds:
        return "غير متوفر"
    
    try:
        duration_seconds = int(duration_seconds)
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    except (ValueError, TypeError):
        return str(duration_seconds)


def format_number(number):
    """تنسيق الأرقام بإضافة فواصل للآلاف"""
    if not number:
        return "غير متوفر"
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        return str(number)


def fallback_get_video_info(video_id):
    """طريقة احتياطية للحصول على معلومات الفيديو باستخدام requests"""
    try:
        console.print(f"[{COLORS['info']}]استخدام الطريقة الاحتياطية للحصول على معلومات الفيديو...[/{COLORS['info']}]")
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return None
            
        html_content = response.text
        
        # استخراج العنوان
        title_match = re.search(r'<title>(.*?) - YouTube</title>', html_content)
        title = title_match.group(1) if title_match else "غير متوفر"
        
        # استخراج اسم القناة
        channel_name_match = re.search(r'"ownerChannelName":"([^"]+)"', html_content)
        channel_name = channel_name_match.group(1) if channel_name_match else "غير متوفر"
        
        # استخراج معرف القناة
        channel_id_match = re.search(r'"channelId":"([^"]+)"', html_content)
        channel_id = channel_id_match.group(1) if channel_id_match else "غير متوفر"
        
        # استخراج عدد المشاهدات
        views_match = re.search(r'"viewCount":"([^"]+)"', html_content)
        views = views_match.group(1) if views_match else "غير متوفر"
        
        # استخراج تاريخ النشر
        date_match = re.search(r'"publishDate":"([^"]+)"', html_content)
        publish_date = date_match.group(1) if date_match else "غير متوفر"
        
        # استخراج صورة الغلاف
        thumbnail_match = re.search(r'"thumbnailUrl":\["([^"]+)"', html_content)
        thumbnail = thumbnail_match.group(1) if thumbnail_match else "غير متوفر"
        
        metadata = {
            "عنوان الفيديو": title,
            "معرف الفيديو": video_id,
            "اسم القناة": channel_name,
            "معرف القناة": channel_id,
            "رابط القناة": f"https://www.youtube.com/channel/{channel_id}" if channel_id != "غير متوفر" else "غير متوفر",
            "عدد المشاهدات": format_number(views),
            "تاريخ النشر": publish_date,
            "صورة الغلاف": thumbnail,
            "ملاحظة": "تم استخراج البيانات باستخدام الطريقة الاحتياطية. بعض المعلومات قد تكون غير متاحة."
        }
        
        return metadata
    except Exception as e:
        console.print(f"[{COLORS['error']}]فشل في الطريقة الاحتياطية: {str(e)}[/{COLORS['error']}]")
        return None


def fallback_get_channel_info(channel_id):
    """طريقة احتياطية للحصول على معلومات القناة باستخدام requests"""
    try:
        console.print(f"[{COLORS['info']}]استخدام الطريقة الاحتياطية للحصول على معلومات القناة...[/{COLORS['info']}]")
        url = f"https://www.youtube.com/channel/{channel_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return None
            
        html_content = response.text
        
        # استخراج اسم القناة
        channel_name_match = re.search(r'<meta name="title" content="([^"]+)"', html_content)
        channel_name = channel_name_match.group(1) if channel_name_match else "غير متوفر"
        
        # استخراج الوصف
        description_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
        description = description_match.group(1) if description_match else "غير متوفر"
        
        # محاولة استخراج بعض الفيديوهات
        videos_info = []
        video_titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}\]}', html_content)
        video_ids = re.findall(r'"videoId":"([^"]+)"', html_content)
        
        # جمع معلومات الفيديوهات المتاحة (حتى 5 فيديوهات)
        for i in range(min(5, len(video_ids))):
            if i < len(video_titles):
                video_info = {
                    "عنوان الفيديو": video_titles[i],
                    "معرف الفيديو": video_ids[i],
                    "رابط الفيديو": f"https://www.youtube.com/watch?v={video_ids[i]}",
                    "تاريخ النشر": "غير متوفر",  # صعب استخراجه بهذه الطريقة
                    "عدد المشاهدات": "غير متوفر",  # صعب استخراجه بهذه الطريقة
                    "المدة": "غير متوفر"  # صعب استخراجه بهذه الطريقة
                }
                videos_info.append(video_info)
        
        metadata = {
            "اسم القناة": channel_name,
            "معرف القناة": channel_id,
            "الوصف": description[:200] + "..." if description and len(description) > 200 else description,
            "رابط القناة": url,
            "عدد المشتركين": "غير متاح (بسبب قيود API)",
            "آخر الفيديوهات": videos_info,
            "ملاحظة": "تم استخراج البيانات باستخدام الطريقة الاحتياطية. بعض المعلومات قد تكون غير متاحة."
        }
        
        return metadata
    except Exception as e:
        console.print(f"[{COLORS['error']}]فشل في الطريقة الاحتياطية للقناة: {str(e)}[/{COLORS['error']}]")
        return None


def get_video_metadata(url):
    """استخراج البيانات الوصفية للفيديو"""
    try:
        console.print(f"[{COLORS['info']}]جاري استخراج البيانات من: {url}[/{COLORS['info']}]")
        
        # استخراج معرف الفيديو من الرابط
        video_id = None
        if "youtube.com/watch" in url and "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        
        if not video_id:
            console.print(f"[{COLORS['error']}]خطأ: لم يتم العثور على معرف الفيديو في الرابط.[/{COLORS['error']}]")
            return None
        
        # إضافة محاولة إصلاح مشكلة HTTP Error 400
        try:
            from pytube.innertube import InnerTube
            innertube_client = InnerTube("WEB", use_oauth=False, allow_cache=True)
        except ImportError:
            pass
            
        # محاولة استخدام pytube
        try:
            yt = YouTube(url)
            
            # محاولة الحصول على البيانات مع إعادة المحاولة
            retry_count = 0
            max_retries = 3
            while retry_count < max_retries:
                try:
                    # جمع البيانات الأساسية
                    metadata = {
                        "عنوان الفيديو": yt.title,
                        "وصف الفيديو": yt.description[:200] + "..." if yt.description and len(yt.description) > 200 else yt.description,
                        "معرف الفيديو": yt.video_id,
                        "اسم القناة": yt.author,
                        "رابط القناة": f"https://www.youtube.com/channel/{yt.channel_id}",
                        "معرف القناة": yt.channel_id,
                        "تاريخ النشر": yt.publish_date.strftime("%Y-%m-%d %H:%M:%S") if yt.publish_date else "غير متوفر",
                        "المدة (ثواني)": yt.length,
                        "المدة (منسقة)": format_duration(yt.length),
                        "عدد المشاهدات": format_number(yt.views),
                        "تقييم الفيديو": yt.rating if hasattr(yt, 'rating') else "غير متوفر",
                        "الكلمات المفتاحية": yt.keywords if hasattr(yt, 'keywords') else "غير متوفر",
                        "مناسب للعائلة": "نعم" if not yt.age_restricted else "لا",
                        "مقيد بالعمر": "نعم" if yt.age_restricted else "لا",
                        "صورة الغلاف": yt.thumbnail_url,
                    }
                    
                    # جمع معلومات الدقة المتاحة
                    streams_info = []
                    for stream in yt.streams.filter(progressive=True):
                        streams_info.append({
                            "itag": stream.itag,
                            "الدقة": stream.resolution,
                            "نوع الملف": stream.mime_type,
                            "FPS": stream.fps,
                            "الحجم (MB)": round(stream.filesize / (1024 * 1024), 2) if stream.filesize else "غير متوفر"
                        })
                    
                    metadata["الدقة المتاحة"] = streams_info
                    
                    return metadata
                    
                except Exception as inner_e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise inner_e
                    console.print(f"[{COLORS['warning']}]محاولة إعادة الاتصال ({retry_count}/{max_retries})...[/{COLORS['warning']}]")
                    import time
                    time.sleep(2)  # انتظار قبل إعادة المحاولة
        
        except (VideoUnavailable, RegexMatchError, Exception) as e:
            console.print(f"[{COLORS['warning']}]فشل استخدام pytube: {str(e)}[/{COLORS['warning']}]")
            console.print(f"[{COLORS['info']}]محاولة استخدام الطريقة الاحتياطية...[/{COLORS['info']}]")
            
            # استخدام الطريقة الاحتياطية
            fallback_metadata = fallback_get_video_info(video_id)
            if fallback_metadata:
                return fallback_metadata
            else:
                raise Exception("فشلت الطريقة الاحتياطية أيضاً")
    
    except VideoUnavailable:
        console.print(f"[{COLORS['error']}]خطأ: الفيديو غير متاح أو تم حذفه.[/{COLORS['error']}]")
        return None
    except RegexMatchError:
        console.print(f"[{COLORS['error']}]خطأ: الرابط غير صالح.[/{COLORS['error']}]")
        return None
    except Exception as e:
        console.print(f"[{COLORS['error']}]خطأ غير متوقع: {str(e)}[/{COLORS['error']}]")
        console.print(f"[{COLORS['info']}]نصيحة: قد تكون هناك مشكلة في مكتبة pytube أو تغيير في واجهة برمجة التطبيقات الخاصة بيوتيوب.[/{COLORS['info']}]")
        return None


def get_channel_metadata(url):
    """استخراج البيانات الوصفية للقناة"""
    try:
        console.print(f"[{COLORS['info']}]جاري استخراج بيانات القناة من: {url}[/{COLORS['info']}]")
        
        # استخراج معرف القناة من الرابط
        channel_id = None
        if '/channel/' in url:
            channel_id = url.split('/channel/')[1].split('/')[0]
        elif '/c/' in url or '/user/' in url or '@' in url:
            # للقنوات المخصصة، نحتاج إلى زيارة الصفحة أولاً للحصول على معرف القناة
            try:
                # محاولة استيراد InnerTube لإصلاح مشكلة HTTP Error 400
                try:
                    from pytube.innertube import InnerTube
                    innertube_client = InnerTube("WEB", use_oauth=False, allow_cache=True)
                except ImportError:
                    pass
                    
                channel = Channel(url)
                channel_id = channel.channel_id
            except Exception as e:
                console.print(f"[{COLORS['warning']}]فشل في استخراج معرف القناة من الرابط المخصص: {str(e)}[/{COLORS['warning']}]")
        
        # إضافة محاولة إصلاح مشكلة HTTP Error 400
        try:
            from pytube.innertube import InnerTube
            innertube_client = InnerTube("WEB", use_oauth=False, allow_cache=True)
        except ImportError:
            pass
            
        # محاولة الحصول على البيانات مع إعادة المحاولة
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                channel = Channel(url)
                
                # جمع البيانات الأساسية للقناة
                metadata = {
                    "اسم القناة": channel.channel_name,
                    "معرف القناة": channel.channel_id,
                    "الوصف": channel.channel_about[:200] + "..." if hasattr(channel, 'channel_about') and channel.channel_about and len(channel.channel_about) > 200 else getattr(channel, 'channel_about', "غير متوفر"),
                    "رابط القناة": url,
                    "عدد المشتركين": "غير متاح (بسبب قيود API)" # يوتيوب لم يعد يوفر هذه المعلومة بسهولة
                }
                
                # جمع معلومات آخر 5 فيديوهات
                videos_info = []
                count = 0
                
                console.print(f"[{COLORS['info']}]جاري استخراج معلومات آخر 5 فيديوهات...[/{COLORS['info']}]")
                for video in channel.videos:
                    if count >= 5:
                        break
                        
                    video_info = {
                        "عنوان الفيديو": video.title,
                        "معرف الفيديو": video.video_id,
                        "رابط الفيديو": f"https://www.youtube.com/watch?v={video.video_id}",
                        "تاريخ النشر": video.publish_date.strftime("%Y-%m-%d") if video.publish_date else "غير متوفر",
                        "عدد المشاهدات": format_number(video.views),
                        "المدة": format_duration(video.length)
                    }
                    
                    videos_info.append(video_info)
                    count += 1
                
                metadata["آخر الفيديوهات"] = videos_info
                
                return metadata
                
            except Exception as inner_e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise inner_e
                console.print(f"[{COLORS['warning']}]محاولة إعادة الاتصال ({retry_count}/{max_retries})...[/{COLORS['warning']}]")
                import time
                time.sleep(2)  # انتظار قبل إعادة المحاولة
        
        # إذا فشلت جميع المحاولات، استخدم الطريقة الاحتياطية
        console.print(f"[{COLORS['warning']}]فشلت جميع المحاولات باستخدام pytube. جاري تجربة الطريقة الاحتياطية...[/{COLORS['warning']}]")
        if channel_id:
            fallback_metadata = fallback_get_channel_info(channel_id)
            if fallback_metadata:
                return fallback_metadata
    
    except Exception as e:
        console.print(f"[{COLORS['error']}]خطأ في استخراج بيانات القناة: {str(e)}[/{COLORS['error']}]")
        console.print(f"[{COLORS['info']}]نصيحة: قد تكون هناك مشكلة في مكتبة pytube أو تغيير في واجهة برمجة التطبيقات الخاصة بيوتيوب.[/{COLORS['info']}]")
        return None


def display_video_metadata(metadata, output_format="console", output_file=None):
    """عرض البيانات الوصفية للفيديو بالتنسيق المطلوب"""
    if not metadata:
        return
    
    if output_format == "console":
        # عرض البيانات الأساسية في جدول
        table = Table(title=f"البيانات الوصفية للفيديو: {metadata['عنوان الفيديو']}")
        table.add_column("الخاصية", style="cyan")
        table.add_column("القيمة", style="green")
        
        for key, value in metadata.items():
            if key != "الدقة المتاحة":
                if isinstance(value, list):
                    table.add_row(key, ", ".join(str(item) for item in value) if value else "غير متوفر")
                else:
                    table.add_row(key, str(value) if value else "غير متوفر")
        
        console.print(table)
        
        # عرض معلومات الدقة في جدول منفصل
        if "الدقة المتاحة" in metadata and metadata["الدقة المتاحة"]:
            streams_table = Table(title="معلومات الدقة المتاحة")
            streams_table.add_column("itag", style="cyan")
            streams_table.add_column("الدقة", style="green")
            streams_table.add_column("نوع الملف", style="yellow")
            streams_table.add_column("FPS", style="blue")
            streams_table.add_column("الحجم (MB)", style="magenta")
            
            for stream in metadata["الدقة المتاحة"]:
                streams_table.add_row(
                    str(stream["itag"]),
                    str(stream["الدقة"]),
                    str(stream["نوع الملف"]),
                    str(stream["FPS"]),
                    str(stream["الحجم (MB)"])
                )
            
            console.print(streams_table)
    
    elif output_format == "json":
        # تصدير البيانات بتنسيق JSON
        json_data = json.dumps(metadata, ensure_ascii=False, indent=4)
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
            console.print(f"[{COLORS['success']}]تم حفظ البيانات في الملف: {output_file}[/{COLORS['success']}]")
        else:
            print(json_data)
    
    elif output_format == "csv":
        # تصدير البيانات الأساسية بتنسيق CSV
        basic_data = {k: v for k, v in metadata.items() if k != "الدقة المتاحة" and not isinstance(v, list)}
        df = pd.DataFrame([basic_data])
        
        if output_file:
            df.to_csv(output_file, index=False, encoding='utf-8')
            console.print(f"[{COLORS['success']}]تم حفظ البيانات في الملف: {output_file}[/{COLORS['success']}]")
        else:
            print(df.to_csv(index=False))
        
        # تصدير بيانات الدقة في ملف منفصل إذا كان متاحاً
        if "الدقة المتاحة" in metadata and metadata["الدقة المتاحة"] and output_file:
            streams_df = pd.DataFrame(metadata["الدقة المتاحة"])
            streams_file = output_file.replace('.csv', '_streams.csv')
            streams_df.to_csv(streams_file, index=False, encoding='utf-8')
            console.print(f"[{COLORS['success']}]تم حفظ بيانات الدقة في الملف: {streams_file}[/{COLORS['success']}]")


def display_channel_metadata(metadata, output_format="console", output_file=None):
    """عرض البيانات الوصفية للقناة بالتنسيق المطلوب"""
    if not metadata:
        return
    
    if output_format == "console":
        # عرض البيانات الأساسية في جدول
        table = Table(title=f"البيانات الوصفية للقناة: {metadata['اسم القناة']}")
        table.add_column("الخاصية", style="cyan")
        table.add_column("القيمة", style="green")
        
        for key, value in metadata.items():
            if key != "آخر الفيديوهات":
                table.add_row(key, str(value) if value else "غير متوفر")
        
        console.print(table)
        
        # عرض معلومات آخر الفيديوهات في جدول منفصل
        if "آخر الفيديوهات" in metadata and metadata["آخر الفيديوهات"]:
            videos_table = Table(title="آخر الفيديوهات في القناة")
            videos_table.add_column("العنوان", style="cyan")
            videos_table.add_column("تاريخ النشر", style="green")
            videos_table.add_column("المشاهدات", style="yellow")
            videos_table.add_column("المدة", style="blue")
            videos_table.add_column("الرابط", style="magenta")
            
            for video in metadata["آخر الفيديوهات"]:
                videos_table.add_row(
                    video["عنوان الفيديو"],
                    video["تاريخ النشر"],
                    video["عدد المشاهدات"],
                    video["المدة"],
                    video["رابط الفيديو"]
                )
            
            console.print(videos_table)
    
    elif output_format == "json":
        # تصدير البيانات بتنسيق JSON
        json_data = json.dumps(metadata, ensure_ascii=False, indent=4)
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_data)
            console.print(f"[{COLORS['success']}]تم حفظ البيانات في الملف: {output_file}[/{COLORS['success']}]")
        else:
            print(json_data)
    
    elif output_format == "csv":
        # تصدير البيانات الأساسية بتنسيق CSV
        basic_data = {k: v for k, v in metadata.items() if k != "آخر الفيديوهات"}
        df = pd.DataFrame([basic_data])
        
        if output_file:
            df.to_csv(output_file, index=False, encoding='utf-8')
            console.print(f"[{COLORS['success']}]تم حفظ البيانات في الملف: {output_file}[/{COLORS['success']}]")
        else:
            print(df.to_csv(index=False))
        
        # تصدير بيانات الفيديوهات في ملف منفصل إذا كان متاحاً
        if "آخر الفيديوهات" in metadata and metadata["آخر الفيديوهات"] and output_file:
            videos_df = pd.DataFrame(metadata["آخر الفيديوهات"])
            videos_file = output_file.replace('.csv', '_videos.csv')
            videos_df.to_csv(videos_file, index=False, encoding='utf-8')
            console.print(f"[{COLORS['success']}]تم حفظ بيانات الفيديوهات في الملف: {videos_file}[/{COLORS['success']}]")


def main():
    """الدالة الرئيسية للبرنامج"""
    parser = argparse.ArgumentParser(description="YtubeData - أداة لاستخراج البيانات الوصفية من يوتيوب")
    parser.add_argument("url", help="رابط فيديو أو قناة يوتيوب")
    parser.add_argument("-t", "--type", choices=["video", "channel"], default="video",
                        help="نوع الرابط (فيديو أو قناة)، الافتراضي: video")
    parser.add_argument("-f", "--format", choices=["console", "json", "csv"], default="console",
                        help="تنسيق الإخراج (console, json, csv)، الافتراضي: console")
    parser.add_argument("-o", "--output", help="اسم ملف الإخراج (للتنسيقات json و csv)")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.type == "video":
        metadata = get_video_metadata(args.url)
        if metadata:
            display_video_metadata(metadata, args.format, args.output)
    else:  # channel
        metadata = get_channel_metadata(args.url)
        if metadata:
            display_channel_metadata(metadata, args.format, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{COLORS['warning']}]تم إيقاف البرنامج بواسطة المستخدم.[/{COLORS['warning']}]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[{COLORS['error']}]خطأ غير متوقع: {str(e)}[/{COLORS['error']}]")
        sys.exit(1)