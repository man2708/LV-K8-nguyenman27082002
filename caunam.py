import json
import random
import string

def load_json(input_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def generate_cloze_questions(data):
    questions = []
    for chapter in data:
        for section in chapter['sections']:
            for subsection in section['subsections']:
                for paragraph in subsection['paragraphs']:
                    text = paragraph['sentence']
                    # Tạo câu hỏi trắc nghiệm khuyết dựa trên các năm trong văn bản
                    question, cloze_text, answer = create_cloze_question(text)
                    if question:  # Chỉ thêm câu hỏi vào danh sách nếu có một năm làm đáp án
                        options = generate_options(answer)
                        questions.append({'question': question, 'cloze_text': cloze_text, 'options': options, 'answer': answer})
    return questions

def create_cloze_question(text):
    words = text.split()
    year_options = [word for word in words if word.isdigit() and len(word) == 4]  # Lọc ra các năm từ văn bản
    if len(year_options) == 0:
        return None, None, None  # Trả về None nếu không tìm thấy năm nào trong văn bản
    # Chọn một năm ngẫu nhiên từ danh sách các năm
    answer = random.choice(year_options)
    # Tạo câu hỏi trắc nghiệm khuyết với năm làm đáp án và từ bị thiếu
    cloze_text = text.replace(answer, '______')
    question = f"Trong văn bản sau, năm nào được đề cập?\n{cloze_text}"
    return question, cloze_text, answer

def generate_options(answer):
    options = [answer]
    for _ in range(3):
        # Tạo một năm ngẫu nhiên gần với đáp án
        random_year = str(int(answer) + random.randint(-10, 10))
        while random_year in options:  # Đảm bảo không trùng lặp với đáp án và các lựa chọn khác
            random_year = str(int(answer) + random.randint(-10, 10))
        options.append(random_year)
    random.shuffle(options)
    return options

if __name__ == '__main__':
    input_file = 'output.json'  # Thay đổi thành tên file JSON thực tế của bạn
    data = load_json(input_file)
    questions = generate_cloze_questions(data)
    for i, q in enumerate(questions, 1):
        print(f"Câu hỏi {i}:")
        print(q['question'])
        for j, option in enumerate(q['options'], 1):
            print(f"{string.ascii_uppercase[j]}. {option}")
        print("Câu trả lời:", q['answer'])
        print()
