# from config import dp
# from states import Setup, CallbackWait, UserStates, PointsSetup
# from aiogram.dispatcher import FSMContext
#
# @dp.message_handler(lambda message: message.text in ['Y', 'N'], state=UserStates.user_setup)
# async def answer_setup(message, state: FSMContext):
#     if message.text.lower() == 'y':
#         await message.reply(f"Ok lets get started - well start with your username and wallet")
#         await state.finish()
#     elif message.text.lower() == 'n':
#         await message.reply("User configuration has been canceled")
#         await UserStates.user_setup.set()
#     else:
#         await message.reply("Invalid response. Please select either 'Y' or 'N'.")
