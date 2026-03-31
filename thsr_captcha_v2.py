#!/usr/bin/env python3
"""
高鐵驗證碼辨識模組
使用 ddddocr 進行驗證碼識別
"""

import os
import time
import base64
from io import BytesIO
from PIL import Image
import numpy as np

try:
    import ddddocr
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("⚠️ 請安裝: pip install ddddocr")


class THSRCaptcha:
    """高鐵驗證碼識別"""
    
    def __init__(self):
        if HAS_OCR:
            self.ocr = ddddocr.DdddOcr(show_ad=False)
            print("✅ 驗證碼辨識已初始化")
        else:
            self.ocr = None
    
    def recognize(self, image_data):
        """
        識別驗證碼
        image_data: bytes 或 Image 對象
        返回: 識別的文字
        """
        if not self.ocr:
            return None
        
        try:
            # 如果是 PIL Image，轉為 bytes
            if isinstance(image_data, Image.Image):
                img_bytes = BytesIO()
                image_data.save(img_bytes, format='PNG')
                image_data = img_bytes.getvalue()
            
            # 如果是路徑
            if isinstance(image_data, str):
                with open(image_data, 'rb') as f:
                    image_data = f.read()
            
            # 識別
            result = self.ocr.classification(image_data)
            return result.strip()
            
        except Exception as e:
            print(f"❌ 識別失敗: {e}")
            return None
    
    def preprocess_and_recognize(self, image):
        """
        圖像前處理 + 識別
        """
        try:
            import cv2
            
            # 轉為灰度
            gray = image.convert('L')
            img_array = np.array(gray)
            
            # 二值化
            _, binary = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 轉回 PIL
            processed = Image.fromarray(binary)
            
            # 識別
            return self.recognize(processed)
            
        except Exception as e:
            # 如果沒有 OpenCV，直接識別
            return self.recognize(image)


# ============== 快捷函數 ==============

captcha = THSRCaptcha()


def recognize(image_data):
    """快捷識別"""
    return captcha.recognize(image_data)


# ============== 主程式 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("🔐 THSR Captcha Test")
    print("=" * 50)
    
    if not HAS_OCR:
        print("❌ 請先安裝 ddddocr")
        exit(1)
    
    # 測試 - 嘗試從網頁獲取驗證碼
    from playwright.sync_api import sync_playwright
    
    BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("\n📥 訪問高鐵訂票網站...")
        page.goto(BOOKING_URL, timeout=30000)
        
        # 等待頁面加載
        page.wait_for_timeout(2000)
        
        # 點擊同意
        try:
            page.click('button:has-text("我同意")', timeout=2000)
        except:
            pass
        
        # 嘗試找到驗證碼圖片
        try:
            # 驗證碼圖片的常見選擇器
            captcha_img = page.locator('img[captcha="true"]').first
            if not captcha_img.count():
                captcha_img = page.locator('img[id*="Captcha"]').first
            if not captcha_img.count():
                captcha_img = page.locator('//img[contains(@src, "captcha")]').first
            
            if captcha_img.count():
                print("✅ 找到驗證碼圖片")
                
                # 獲取圖片二進制
                captcha_bytes = captcha_img.screenshot()
                
                # 識別
                result = captcha.recognize(captcha_bytes)
                print(f"🔤 識別結果: {result}")
            else:
                print("⚠️ 未找到驗證碼圖片")
                
                # 嘗試截圖查看
                page.screenshot(path="thsrc_page.png")
                print("📸 已截圖: thsrc_page.png")
                
        except Exception as e:
            print(f"❌ 獲取驗證碼失敗: {e}")
        
        browser.close()
    
    print("\n✅ 測試完成")
