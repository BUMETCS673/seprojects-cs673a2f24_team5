@patch('fetch_file')
def test_file_to_string(file, app):
    file = 'mock_file'  # File content
    file_to_text = file_to_string(text)

    assert file_to_text == 'abcdefg'

@patch('de_encryption_1')
def test_de_encryption(text, app):
    text = 'abcdefg'  # Set up the application context
    encrypted_text = encryption_1(text)

    assert encrypted_text == 'gfedcba'

    original_text = decryption_1(encrypted_text)

    assert encrypted_text == 'abcdefg'


@patch('de_encryption_2')
def test_de_encryption(text, app):
    text = 'abcdefg'  # Set up the application context
    encrypted_text = encryption_2(text)

    assert encrypted_text == '123456'

    original_text = decryption_2(encrypted_text)

    assert encrypted_text == 'abcdefg'

