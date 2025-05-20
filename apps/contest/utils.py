import shortuuid

def generate_short_uid():
    return shortuuid.uuid()  # длина 22 символа, base57, уникально
