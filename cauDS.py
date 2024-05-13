import json
import random
from nltk.tokenize import sent_tokenize

def process_text(text):
    # Tokenize văn bản thành các câu
    sentences = sent_tokenize(text)
    return sentences

def summarize_sentence(sentence):
    # Tách câu thành danh sách các từ
    words = sentence.split()
    # Tính chỉ số giữa của danh sách các từ
    middle_index = len(words) // 2
    # Kiểm tra xem có từ nào trong câu không
    if words:
        # Tóm tắt câu bằng cách lấy nửa đoạn đầu của câu
        summary = ' '.join(words[:middle_index + 1])
    else:
        summary = ""  # Trả về chuỗi rỗng nếu không có từ trong câu
    return summary


def generate_questions(sentences, paragraphs):
    questions = []
    # Danh sách các lựa chọn đáp án 
    choices = ['A', 'B', 'C', 'D']
    for sentence in sentences:
        # Loại bỏ dấu câu cuối cùng
        sentence = sentence[:-1] if sentence.endswith('.') else sentence
        # Tạo câu hỏi từ câu văn
        question = sentence
        # Chọn một lựa chọn đáp án ngẫu nhiên từ danh sách
        correct_answer = random.choice(choices)
        # Nếu A hoặc B đúng, chọn một câu hỏi làm đáp án A và đáp án B
        if correct_answer in ['A', 'B']:
            random_paragraph = random.choice(paragraphs)
        # Nếu C đúng, chọn cả hai lựa chọn đều là câu hỏi
        elif correct_answer == 'C':
            random_paragraph = ""
        # Nếu D đúng, chọn hai đoạn văn bản ngẫu nhiên
        else:
            random_paragraph = random.choice(paragraphs), random.choice(paragraphs)
        # Tạo danh sách lựa chọn đáp án
        options = choices.copy()
        # Nếu đáp án là 'A', 'B', 'C', hoặc 'D', loại bỏ nó khỏi danh sách lựa chọn
        if correct_answer in options:
            options.remove(correct_answer)
        # Thêm câu hỏi và đáp án vào danh sách
        questions.append((question, correct_answer, options, random_paragraph))
    return questions

def main(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    paragraphs = []  # Danh sách các đoạn văn bản từ tệp JSON
    for chapter in data:
        for section in chapter['sections']:
            for subsection in section['subsections']:
                for paragraph in subsection['paragraphs']:
                    paragraphs.append(paragraph['sentence'])

    # Xử lý từng đoạn văn trong tệp JSON
    for chapter in data:
        for section in chapter['sections']:
            for subsection in section['subsections']:
                for paragraph in subsection['paragraphs']:
                    # Xử lý văn bản từ mỗi đoạn văn
                    text = paragraph['sentence']
                    # Phân tích văn bản thành các câu
                    sentences = process_text(text)
                    # Tạo câu hỏi từ các câu văn và các đoạn văn bản
                    questions = generate_questions(sentences, paragraphs)

                    # In ra câu hỏi và đáp án tương ứng
                    for i, (question, correct_answer, options, random_paragraph) in enumerate(questions, start=1):
                        print(f"Câu Hỏi :Câu nào đúng sau đây?")
                        if 'A' == correct_answer:
                            print("A.", question)
                            print("B.", random_paragraph)
                        elif 'B' == correct_answer:
                            print("A.", random_paragraph)
                            print("B.", question)
                        elif 'C' == correct_answer:
                            summary = summarize_sentence(question)
                            print("A.", question)
                            print("B.", summary)
                        elif 'D' == correct_answer:
                            print("A.", random_paragraph[0])
                            print("B.", random_paragraph[1])
                        print("C.", "A và B đều đúng") if 'C' == correct_answer else print("C.", "A và B đều đúng")
                        print("D.", "A và B đều sai") if 'D' == correct_answer else print("D.", "A và B đều sai")
                        print("Đáp án chính xác:", correct_answer)
                        print()

if __name__ == "__main__":
    json_file = "output_json.json"  # Thay đổi tên tệp JSON của bạn tại đây
    main(json_file)
