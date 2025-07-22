import csv
import json

input_file = 'results.csv'
output_file = 'results.json'

data = []

# جرب عدة ترميزات لوحدة اللغة
encodings_to_try = ['windows-1256', 'utf-8', 'utf-8-sig', 'cp1252']

for enc in encodings_to_try:
    try:
        with open(input_file, mode='r', encoding=enc) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 3:
                    continue
                seat_number, full_name, score = row

                # تجاهل الصف اللي فيه العناوين
                if (
                    seat_number.strip().lower() in ['id', 'رقم_الجلوس']
                    or score.strip().lower() in ['total', 'total_degree', 'الدرجة']
                ):
                    continue

                data.append({
                    "id": seat_number.strip(),
                    "name": full_name.strip(),
                    "score": float(score.strip())
                })
        print(f"✅ تم التحويل بنجاح باستخدام الترميز: {enc}")
        break
    except Exception as e:
        print(f"❌ فشل في القراءة باستخدام الترميز: {enc} – {str(e)}")
        data = []

if data:
    with open(output_file, mode='w', encoding='utf-8') as f:
        # حفظ مضغوط بدون فراغات (separators = minify)
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f"✅ تم حفظ {len(data)} طالب في {output_file} بحجم مضغوط")
else:
    print("❌ لم يتم التحويل. تحقق من الملف أو الترميز.")
