from flask import Flask, render_template, jsonify, request
import requests
import os
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch



api_base = "https://api.endpoints.anyscale.com/v1"
api_key = "esecret_qvsm393q5xuqilb2kbfyr17fbl"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
url = f"{api_base}/chat/completions"


chat_history = []
def llama34b_response(text):
    history_text = ''
    for index, i in enumerate(chat_history):
        if index%2 == 0:
            history_text = history_text + '\n' + 'user:' + i
        else:
            history_text = history_text + '\n' + 'system:' + i

    all_text = history_text + '\n'+ 'user:' + text


    data = {
        "model": "codellama/CodeLlama-34b-Instruct-hf",
        "messages": [
            {"role": "user", "content": f'''{all_text}'''}
            # {"role": "user", "content": "Hello!"}
        ],
        "temperature": 0.7,
        "top_p":0.1,
        "max_token":128
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return (f"Request failed with status code: {response.status_code}")

def wrap_text(text, max_line_length):
    lines = text.split('\n')  # Tách văn bản thành các dòng dựa trên ký tự xuống dòng
    wrapped_lines = []

    for line in lines:
        words = line.split()
        current_line = []

        for word in words:
            # Kiểm tra xem từ tiếp theo có khiến dòng hiện tại vượt quá giới hạn độ dài hay không
            if len(' '.join(current_line + [word])) <= max_line_length:
                current_line.append(word)
            else:
                # Nếu vượt quá, thêm dòng hiện tại vào danh sách và bắt đầu một dòng mới
                wrapped_lines.append(' '.join(current_line))
                current_line = [word]

        # Thêm dòng cuối cùng vào danh sách
        wrapped_lines.append(' '.join(current_line))

    return '\n'.join(wrapped_lines)

def vinallama_responces(text):
    return "Vinallama"

def chatgpt_4_response(text):
    return "Chatgpt"
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/verify")
def verify():
    return render_template('verify.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/chat")
def chat_page():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    model = request.form["model"] # Default is 'Select Model'
    document = request.form["document"] # Defaultis "Select Document"

    output = llama34b_response(msg)
    if model == "Llama 34b" or model == "Select Model":
        output = llama34b_response(msg)
    elif model == "VinaLlama 7b":
        output = vinallama_responces(msg)
    elif model == "ChatGPT 4":
        output = chatgpt_4_response(msg)

    output = wrap_text(output, 80)
    chat_history.append(msg)
    chat_history.append(output)
    return output


@app.route('/upload', methods=['PUT'])
def upload_file():
    file = request.files['file']
    file_name = file.filename
    try:
        user_name = request.form['user_name']
    except:
        user_name = 'trunglq'

    s3_url = f'https://bxvel9b1vi.execute-api.ap-southeast-2.amazonaws.com/dev/chatbot-user-upload/{user_name}/{file_name}'
    ec2_url = 'https://qotvnsyf13.execute-api.ap-southeast-2.amazonaws.com/vector-database-stage/upload'

    # Gửi file đến API S3 sử dụng phương thức PUT
    files = {'file': (file_name, file.stream, file.mimetype)}
    response_s3 = requests.put(s3_url, files=files)


    if response_s3.status_code == 200:
        # Gửi yêu cầu PUT đến EC2
        data = {'user_name': user_name, 'file_name': file_name}
        response_ec2 = requests.put(ec2_url, json=data)

        if response_ec2.status_code == 200:
            return jsonify({'message': 'Tải lên thành công và xử lý thành công'})
        else:
            return jsonify({'error': 'Lỗi khi xử lý trên EC2'}), 500
    else:
        return jsonify({'error': 'Lỗi khi tải lên S3'}), 500


if __name__ == '__main__':
    app.run(port=8888)
#sudo systemctl stop apache2
#sudo systemctl disable apache2