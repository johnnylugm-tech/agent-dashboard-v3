#!/usr/bin/env python3
"""
高鐵驗證碼辨識模組
使用 OpenCV + Tesseract OCR 進行驗證碼識別
"""

import os
import time
import base64
from io import BytesIO

try:
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("⚠️ 驗證碼辨識需要: pip install opencv-python pillow pytesseract")


def preprocess_image(image_data):
    """圖像前處理"""
    # 轉為灰度
    gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    
    # 去噪
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # 二值化
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 銳化
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(binary, -1, kernel)
    
    return sharpened


def recognize_captcha(image):
    """
    識別驗證碼
    返回: 識別的文字
    """
    if not HAS_OCR:
        return None
    
    try:
        # 轉為 PIL Image
        if isinstance(image, np.ndarray):
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # 前處理
        img_array = np.array(image)
        processed = preprocess_image(img_array)
        
        # OCR 識別
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text = pytesseract.image_to_string(processed, config=custom_config)
        
        # 清理結果
        text = ''.join(c for c in text.upper() if c.isalnum())
        
        return text[:4] if len(text) >= 4 else text
        
    except Exception as e:
        print(f"❌ OCR 識別失敗: {e}")
        return None


def solve_captcha_ocr(page, max_attempts=3):
    """
    嘗試自動解決驗證碼
    返回: 是否成功
    """
    if not HAS_OCR:
        return False
    
    for attempt in range(max_attempts):
        try:
            # 取得驗證碼圖片
            captcha_img = page.query_selector('img[src*="Captcha"], img[id*="Captcha"]')
            
            if not captcha_img:
                # 嘗試其他選擇器
                captcha_img = page.query_selector('img[alt*="captcha"], img[class*="captcha"]')
            
            if captcha_img:
                # 截圖
                screenshot = captcha_img.screenshot()
                
                # 辨識
                result = recognize_captcha(screenshot)
                
                if result and len(result) >= 4:
                    print(f"🔐 驗證碼辨識結果: {result}")
                    
                    # 填入驗證碼
                    page.fill('input[id*="captcha"], input[name*="captcha"]', result)
                    
                    return True
                    
        except Exception as e:
            print(f"⚠️ 嘗試 {attempt + 1} 失敗: {e}")
            time.sleep(1)
    
    return False


def manual_captcha(page, timeout=120):
    """
    手動輸入驗證碼（顯示圖片讓用戶輸入）
    """
    print("\n🔐 需要輸入驗證碼...")
    print("="*50)
    
    # 截取驗證碼區域的截圖
    try:
        captcha_element = page.query_selector('img[src*="Captcha"], input + img')
        
        if captcha_element:
            # 取得驗證碼圖片
            captcha_img = page.query_selector('img')
            
            if captcha_img:
                # 截圖保存
                screenshot = page.screenshot()
                
                # 保存圖片
                img_path = "/Users/johnny/.openclaw/workspace-musk/data/captcha.png"
                with open(img_path, "wb") as f:
                    f.write(screenshot)
                
                print(f"📸 驗證碼已截圖: {img_path}")
        
        # 等待用戶輸入
        print("⏳ 請在瀏覽器中輸入驗證碼...")
        print(f"   (超時 {timeout} 秒)")
        
        # 等待一段時間讓用戶輸入
        page.wait_for_timeout(timeout * 1000)
        
        return True
        
    except Exception as e:
        print(f"⚠️ 取得驗證碼失敗: {e}")
        page.wait_for_timeout(timeout * 1000)
        return True


# 測試
if __name__ == "__main__":
    if HAS_OCR:
        print("✅ 驗證碼辨識模組已就緒")
        
        # 測試圖像處理
        test_img = np.zeros((50, 150, 3), dtype=np.uint8)
        result = recognize_captcha(test_img)
        print(f"🔬 測試結果: {result}")
    else:
        print("❌ 缺少必要函式庫")
        print("   pip install opencv-python pillow pytesseract")
