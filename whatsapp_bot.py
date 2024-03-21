from whatsapp_logic.query import *

response = send_whatsapp_manager()

##################
#   POSTPONED
##################

# print(response.status_code) DOne
# print(response.json())

# if __name__ == '__main__':
#     print('Starting Bot')
#     app = Application.builder().token(BOT_TOKEN).build()
#     app.add_handler(CommandHandler('start', start_command))

#     app.add_handler(MessageHandler(filters.TEXT, handle_message))

#     app.add_error_handler(error)

#     print('Polling')
#     app.run_polling(poll_interval=3)