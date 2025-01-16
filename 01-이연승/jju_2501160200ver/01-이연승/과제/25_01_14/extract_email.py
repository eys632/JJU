import email
from email.policy import default

def extract_email_data(eml_file):
    """
    .eml 파일에서 이메일 데이터를 추출
    """
    with open(eml_file, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f, policy=default)

    # 필요한 필드 추출
    sender = msg.get('From')
    recipient = msg.get('To')
    subject = msg.get('Subject')
    date = msg.get('Date')

    # 본문 추출
    if msg.is_multipart():
        body = ""
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                body = part.get_content()
                break
    else:
        body = msg.get_content()

    return {
        'sender': sender,
        'recipient': recipient,
        'subject': subject,
        'date': date,
        'body': body.strip()
    }
