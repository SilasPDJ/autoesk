def hora_mensagem_default():
    from datetime import datetime as dt
    hora = dt.now().time().hour
    if 18 > hora >= 12:
        return 'Boa tarde'
    elif 12 > hora > 0:
        return 'Bom dia'
    elif hora >= 18:
        return 'Boa noite'
    else:
        return 'Meia noite'
