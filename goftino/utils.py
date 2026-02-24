
class AddButton:
    """Methods for adding buttons to the list.
    """

    @staticmethod
    def button_link(message, button_title, link):
        return f'{message}\n[button title=\"{button_title}\" action="open_url" data=\"{link}\"]'

    @staticmethod
    def button_showtext(message, button_title, text):
        return f'{message}\n[button title=\"{button_title}\" action="show_message" data=\"{text}\"]'

    @staticmethod
    def button_assignchat(message, button_title, operator_id : str | list | None = None, message_after_click = None):
        if type(operator_id) is str:
            return f'{message}\n[button title=\"{button_title}\" action="assign" data=\"{operator_id}\"'\
                   f'{AddButton.__add_message_after_click(message_after_click) if message_after_click is not None else ""}]'

        elif type(operator_id) is list:
            return f'{message}\n[button title=\"{button_title}\" action="assign" data=\"{",".join(operator_id)}\"'\
                   f'{AddButton.__add_message_after_click(message_after_click) if message_after_click is not None else ""}]'
        
        elif operator_id is None:
            return f'{message}\n[button title=\"{button_title}\" action="assign" data=\"all_operators\"'\
                   f'{AddButton.__add_message_after_click(message_after_click) if message_after_click is not None else ""}]'     
      
    @staticmethod
    def button_webhook(message, button_title, event, message_after_click = None):
        return f'{message}\n[button title=\"{button_title}\" action="send_webhook" data=\"{event}\"'\
                f'{AddButton.__add_message_after_click(message_after_click) if message_after_click is not None else ""}]'     

    @staticmethod
    def __add_message_after_click(message):
        return f' message_after_click="{message}"'
    

if __name__ == '__main__':
    print(AddButton.button_link("Hi this was the message before" , "Button", "google.com"))
    print(AddButton.button_assignchat("Text", "Button", message_after_click="MessageAfterClick"))
    print(AddButton.button_assignchat("Text", "Button"))
    print(AddButton.button_assignchat("Text", "Button", "1234"))
