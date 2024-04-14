import vk_api, vk_api.longpoll, random, sys, datetime, time, dataSec, data

def IIstepAuth(): # Получение кода двухэтапной аутентификации
    authCode = input('Введите код аутентификации: ') # Код двухэтапной аутентификации
    rememberDevice = True # Запомнить устройство
    return authCode, rememberDevice

def main(): # Тело бота
    login = dataSec.login # Получение логина из файла (можно вписать свой)
    password = dataSec.password # Получение пароля из файла (можно вписать свой)
    vk_session = vk_api.VkApi(login, password, auth_handler=IIstepAuth) # Сессия ВК
    
    try:  # Попытытка аутентификации
        vk_session.auth()
    except vk_api.AuthError: # Блок с инструкциями в случае ошибки аутентификации
        print( '\n''Ошибка аутентификации', '\n', sep='')
        return

    print(' \n Успешная аутентификация \n', sep='')

    longpoll =  vk_api.longpoll.VkLongPoll(vk_session, mode=2) # Инициализация подключения к Long Poll серверу

    for event in longpoll.listen(): # Цикл обработки событий, полученных при прослушке Long Poll сервера
        #print('Новое событие, ', event.type, sep='')

        #try:
        #   zzz = event.user_id
        #   zzz = event.type
        #except AttributeError:
        #    time.sleep(3)
        #    print('ATTRIBUTE ERROR '*10)
        #    main()

        if event.type != event.type.MESSAGES_COUNTER_UPDATE and event.type != event.type.READ_ALL_INCOMING_MESSAGES  and event.type != event.type.READ_ALL_OUTGOING_MESSAGES: # Не обращаться к айди пользователя при ЭТИХ событиях (будет ошибка)
            USER_ID = vk_session.get_api().users.get(user_ids=event.user_id)[0].get('id')
            USER_NAME= vk_session.get_api().users.get(user_ids=event.user_id)[0].get('first_name')
            USER_SURENAME = vk_session.get_api().users.get(user_ids=event.user_id)[0].get('last_name')
            USER_NAME_AND_SURNAME = USER_NAME+' '+USER_SURENAME


        if event.type == event.type.MESSAGE_NEW: #Событие - новое сообщение
            if event.from_user: #Событие - от диалога с пользователем
                if event.from_me: #Прислано мной в диалог с пользователем
                    print('Новое сообщение от меня для пользователя: ', USER_NAME_AND_SURNAME, '\nТекст: ', event.text, sep='')
                elif event.from_user: #Прислано пользователем в диалоге с пользователем
                    print('Новое сообщение от пользователя: ', USER_NAME_AND_SURNAME, '\nТекст: ', event.text, sep='')
            elif event.from_chat: #Событие - от беседы
                if event.from_me: #Прислано мной в беседу
                    print('Новое сообщение от меня в беседе: ', event.chat_id, '\nТекст: ', event.text, sep='')
                if event.from_user: #Прислано пользователем в беседу
                    print('Новое сообщение от ', USER_NAME_AND_SURNAME , ' в беседе ', event.chat_id, '\nТекст: ', event.text, sep='')
        elif event.type == event.type.MESSAGE_EDIT: #Событие - сообщение изменено
            if event.from_user: #Событие - от диалога с пользователем
                print('Сообщение отредактировано пользователем: ', USER_NAME_AND_SURNAME, ', на: ', event.text, sep='')
            elif event.from_chat: #Событие - от беседы
                print('Сообщение отредактировано: ', USER_NAME_AND_SURNAME, ', в беседе: ', event.chat_id, sep='')
        elif event.type == event.type.USER_ONLINE: #Событие - пользователь онлайн
            if event.platform == event.platform.ANDROID: #Проверка платформы
                print(''+USER_NAME_AND_SURNAME, ' сейчас онлайн с ANDROID', sep='')
            elif event.platform == event.platform.WINDOWS: #Проверка платформы
                print(''+USER_NAME_AND_SURNAME, ' сейчас онлайн с WINDOWS', sep='')
            elif event.platform == event.platform.MOBILE: #Проверка платформы
                print(''+USER_NAME_AND_SURNAME, ' сейчас онлайн с MOBILE', sep='')
            elif event.platform == event.platform.WEB: #Проверка платформы
                print(''+USER_NAME_AND_SURNAME, ' сейчас онлайн с WEB', sep='')
            elif event.platform == event.platform.IPHONE: #Проверка платформы
                print(''+USER_NAME_AND_SURNAME, ' сейчас онлайн с IPHONE', sep='')
        elif event.type == event.type.USER_OFFLINE:
            print(''+USER_NAME_AND_SURNAME, ' вышла/вышел из сети', sep='')



if __name__ == '__main__':
    main()