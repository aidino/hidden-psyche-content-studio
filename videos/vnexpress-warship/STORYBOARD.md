# Storyboard

Format: Portrait (1080x1920) for short-form social, or Landscape (1920x1080) for YouTube. We will build Landscape as default for News briefs.

## Scene 1: The Incident
- **Duration**: ~10s
- **Narration**: "Điểm nóng Trung Đông tiếp tục leo thang dữ dội. Mới đây, khu trục hạm USS Spruance của Mỹ đã dùng pháo hạm 127 ly bắn thẳng vào tàu hàng Touska mang cờ Iran trên biển Oman."
- **Visuals**:
  - Background: Fullbleed white `#FFFFFF` with VnExpress Header mockup (Logo `logo.svg` + Search Icon).
  - Main Media: The hero image `og-image.jpg` or `iran-1776642420-8819-1776642675.png` animates in with a slow zoom (Ken Burns).
  - Typography: Massive headline in Merriweather (color `#222222`), animating in strictly line-by-line: "CHIẾN HẠM MỸ NÃ PHÁO\nBẮT TÀU HÀNG IRAN".
  - Accent: A red line (`#9F224E`) expands below the text.
- **Motion**: Fast cuts, sharp CSS transitions, avoiding bounce or lag.

## Scene 2: The Blockade
- **Duration**: ~10s
- **Narration**: "Theo Tổng thống Donald Trump công bố, tàu Touska đã cố tình vượt vòng phong tỏa của hải quân Mỹ và liên tục từ chối lệnh dừng tàu. Hậu quả, phòng máy của con tàu này đã bị trúng đạn."
- **Visuals**:
  - Background shifts to `#FCFAF6`.
  - A stylized quote block appears, referencing Donald Trump's Truth Social post. Font: Merriweather Italic.
  - Image `image-16.jpg` (or another appropriate thumbnail) slides in. 
  - Text highlights: "Vượt vòng phong tỏa", "Phòng máy trúng đạn" highlighting in `#9F224E`.

## Scene 3: The Boarding
- **Duration**: ~10s
- **Narration**: "Lực lượng Mỹ cáo buộc thủy thủ đoàn cố tình chạy hướng về cảng Bandar Abbas suốt 6 tiếng đồng hồ mà không tuân thủ cảnh báo. Ngay sau đó, binh sĩ Mỹ đã đổ bộ và kiểm soát hoàn toàn phương tiện này."
- **Visuals**:
  - A timer or typographic counter counting `6 TIẾNG`.
  - Darker section: background turns to dark grey/black `#222222` to signal the boarding.
  - Text: "ĐỔ BỘ & KIỂM SOÁT" pops in with a typewriter effect.

## Scene 4: Iran's Response
- **Duration**: ~10s
- **Narration**: "Iran lập tức lên tiếng phản pháo, cáo buộc hành động của Mỹ là vi phạm lệnh ngừng bắn và gọi đây là hành vi cướp biển trắng trợn. Lực lượng vũ trang Iran tuyên bố sẽ sớm có biện pháp trả đũa."
- **Visuals**:
  - Layout splits. Left side: Image of Iranian authorities or troops (e.g. `image-41.jpg` if relevant, or solid red).
  - Huge "TRẢ ĐŨA" text fills the screen in a flash.

## Scene 5: Map of Hormuz
- **Duration**: ~10s
- **Narration**: "Xung đột nổ ra trong bối cảnh eo biển Hormuz - tuyến hàng hải huyết mạch của thế giới - đang bị phong tỏa. Vài ngày trước, Iran vừa tuyên bố mở cửa khu vực này nhưng lại đóng ngay sau đó để đáp trả Mỹ."
- **Visuals**:
  - Map image `hormuz-1776633369-2901-1776633489.jpg`.
  - SVG circle-drawing animation around the Strait of Hormuz using `<path stroke="#9F224E" stroke-dasharray="..." />` (MotionPath style).

## Scene 6: Outro
- **Duration**: ~10s
- **Narration**: "Tình hình tại Vùng Vịnh vẫn đang vô cùng căng thẳng, đe dọa trực tiếp tới chuỗi cung ứng dầu mỏ và khí đốt toàn cầu."
- **Visuals**:
  - Deep red overlay (`#9F224E`) fades in.
  - White bold text: "CHUỖI CUNG ỨNG TOÀN CẦU LÂM NGUY".
  - Outro: VnExpress logo centered, fading out with an auto-progress bar completing.
