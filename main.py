from utils import *
from setup import *
# eng_speech = text_to_speech(eng_text)
# hindi_translation = translate_text(eng_text, "hi")
# hindi_speech = text_to_speech(hindi_translation)
# input_audio = "speech_20250215_164013.mp3"
# output_text = speech_to_text(input_audio)
#Replace your no to test
contact_number_test="+910000000000"



user = get_one_user_without_interaction()


conversation_log={}
if user:
    user_id, name, contact_number, product_id= user
else:
    print("No users left to call.")

if user:
    user_id, name, contact_number, product_id = user
    contact_number=contact_number_test
    conversation_log = {user_id: []}

    # AI-generated greeting
    greeting = get_ai_response(f"Greet {name} and ask if this is a good time to talk.")
    file1=text_to_speech(greeting)
    conversation_log[user_id].append({"AI": greeting})

    # Call user with greeting
    call_sid = make_call(greeting)
    conversation_log[user_id].append({"Call SID": call_sid})
    save_conversation(user_id,conversation_log)

    # Assume the user responds (in real implementation, capture user input)
    user_response = input(f"{greeting}\nUser: ")  # Simulated response
    conversation_log[user_id].append({"User": user_response})
    save_conversation(user_id, conversation_log)
    if user_response.lower() in ["yes", "yeah", "sure", "okay"]:
        # Fetch product details
        conn = sqlite3.connect("agent.db")
        cursor = conn.cursor()
        cursor.execute("SELECT product_name FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()

        if product:
            product_name = product[0]
            ai_message = get_ai_response(f"Tell {name} about {product_name} in a friendly way.")
            conversation_log[user_id].append({"AI": ai_message})
            save_conversation(user_id, conversation_log)

            # Call user with product details
            call_sid = make_call(ai_message)
            conversation_log[user_id].append({"Call SID": call_sid})
            save_conversation(user_id, conversation_log)
            # Simulate user response
            user_response = input(f"{ai_message}\nUser: ")
            conversation_log[user_id].append({"User": user_response})
            save_conversation(user_id, conversation_log)

        else:
            ai_message = "We couldn't find product details. Sorry!"
            conversation_log[user_id].append({"AI": ai_message})
            save_conversation(user_id, conversation_log)

    else:
        ai_message = get_ai_response(f"Politely say goodbye to {name} and let them know we will contact them later.")
        conversation_log[user_id].append({"AI": ai_message})
        save_conversation(user_id, conversation_log)
        call_sid = make_call(ai_message)
        conversation_log[user_id].append({"Call SID": call_sid})

    # Save conversation log
    #save_conversation(user_id, conversation_log)

    # Mark user as contacted
    update_user_status(user_id)

    print("\nConversation Log Saved:", conversation_log)

else:
    print("No users left to call.")
