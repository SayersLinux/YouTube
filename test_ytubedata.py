#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة لأداة YtubeData
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# إضافة المجلد الحالي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from YtubeData import (
    format_date,
    format_duration,
    format_number,
    get_video_metadata,
    get_channel_metadata
)


class TestFormatFunctions(unittest.TestCase):
    """اختبارات لدوال التنسيق"""
    
    def test_format_date(self):
        """اختبار دالة تنسيق التاريخ"""
        self.assertEqual(format_date("20210101"), "2021-01-01")
        self.assertEqual(format_date(""), "غير متوفر")
        self.assertEqual(format_date(None), "غير متوفر")
        self.assertEqual(format_date("invalid"), "invalid")
    
    def test_format_duration(self):
        """اختبار دالة تنسيق المدة"""
        self.assertEqual(format_duration(3661), "1:01:01")
        self.assertEqual(format_duration(61), "01:01")
        self.assertEqual(format_duration(59), "00:59")
        self.assertEqual(format_duration(""), "غير متوفر")
        self.assertEqual(format_duration(None), "غير متوفر")
        self.assertEqual(format_duration("invalid"), "invalid")
    
    def test_format_number(self):
        """اختبار دالة تنسيق الأرقام"""
        self.assertEqual(format_number(1000), "1,000")
        self.assertEqual(format_number(1000000), "1,000,000")
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(""), "غير متوفر")
        self.assertEqual(format_number(None), "غير متوفر")
        self.assertEqual(format_number("invalid"), "invalid")


class TestVideoMetadata(unittest.TestCase):
    """اختبارات لدالة استخراج بيانات الفيديو"""
    
    @patch('YtubeData.YouTube')
    def test_get_video_metadata(self, mock_youtube):
        """اختبار استخراج بيانات الفيديو"""
        # إعداد المحاكاة
        mock_instance = MagicMock()
        mock_youtube.return_value = mock_instance
        
        # تكوين خصائص المحاكاة
        mock_instance.title = "عنوان الفيديو الاختباري"
        mock_instance.description = "وصف الفيديو الاختباري"
        mock_instance.video_id = "test_video_id"
        mock_instance.author = "اسم القناة الاختبارية"
        mock_instance.channel_id = "test_channel_id"
        
        from datetime import datetime
        mock_instance.publish_date = datetime(2021, 1, 1)
        
        mock_instance.length = 3661
        mock_instance.views = 1000000
        mock_instance.rating = 4.9
        mock_instance.keywords = ["كلمة1", "كلمة2"]
        mock_instance.age_restricted = False
        mock_instance.thumbnail_url = "https://example.com/thumbnail.jpg"
        
        # محاكاة الدفق المتاح
        mock_stream = MagicMock()
        mock_stream.itag = 22
        mock_stream.resolution = "720p"
        mock_stream.mime_type = "video/mp4"
        mock_stream.fps = 30
        mock_stream.filesize = 10485760  # 10 MB
        
        mock_streams = MagicMock()
        mock_streams.filter.return_value = [mock_stream]
        mock_instance.streams = mock_streams
        
        # استدعاء الدالة المراد اختبارها
        result = get_video_metadata("https://www.youtube.com/watch?v=test_video_id")
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result["عنوان الفيديو"], "عنوان الفيديو الاختباري")
        self.assertEqual(result["معرف الفيديو"], "test_video_id")
        self.assertEqual(result["اسم القناة"], "اسم القناة الاختبارية")
        self.assertEqual(result["المدة (ثواني)"], 3661)
        self.assertEqual(result["المدة (منسقة)"], "1:01:01")
        self.assertEqual(result["عدد المشاهدات"], "1,000,000")
        self.assertEqual(result["مقيد بالعمر"], "لا")
        
        # التحقق من معلومات الدقة
        self.assertIn("الدقة المتاحة", result)
        self.assertEqual(len(result["الدقة المتاحة"]), 1)
        self.assertEqual(result["الدقة المتاحة"][0]["الدقة"], "720p")
        self.assertEqual(result["الدقة المتاحة"][0]["الحجم (MB)"], 10.0)


class TestChannelMetadata(unittest.TestCase):
    """اختبارات لدالة استخراج بيانات القناة"""
    
    @patch('YtubeData.Channel')
    def test_get_channel_metadata(self, mock_channel):
        """اختبار استخراج بيانات القناة"""
        # إعداد المحاكاة
        mock_instance = MagicMock()
        mock_channel.return_value = mock_instance
        
        # تكوين خصائص المحاكاة
        mock_instance.channel_name = "اسم القناة الاختبارية"
        mock_instance.channel_id = "test_channel_id"
        mock_instance.channel_about = "وصف القناة الاختبارية"
        
        # محاكاة الفيديوهات
        mock_video1 = MagicMock()
        mock_video1.title = "عنوان الفيديو الاختباري 1"
        mock_video1.video_id = "test_video_id_1"
        from datetime import datetime
        mock_video1.publish_date = datetime(2021, 1, 1)
        mock_video1.views = 1000000
        mock_video1.length = 3661
        
        mock_video2 = MagicMock()
        mock_video2.title = "عنوان الفيديو الاختباري 2"
        mock_video2.video_id = "test_video_id_2"
        mock_video2.publish_date = datetime(2021, 1, 2)
        mock_video2.views = 2000000
        mock_video2.length = 1800
        
        mock_instance.videos = [mock_video1, mock_video2]
        
        # استدعاء الدالة المراد اختبارها
        result = get_channel_metadata("https://www.youtube.com/channel/test_channel_id")
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertEqual(result["اسم القناة"], "اسم القناة الاختبارية")
        self.assertEqual(result["معرف القناة"], "test_channel_id")
        self.assertEqual(result["الوصف"], "وصف القناة الاختبارية")
        
        # التحقق من معلومات الفيديوهات
        self.assertIn("آخر الفيديوهات", result)
        self.assertEqual(len(result["آخر الفيديوهات"]), 2)
        self.assertEqual(result["آخر الفيديوهات"][0]["عنوان الفيديو"], "عنوان الفيديو الاختباري 1")
        self.assertEqual(result["آخر الفيديوهات"][1]["عنوان الفيديو"], "عنوان الفيديو الاختباري 2")


if __name__ == "__main__":
    unittest.main()