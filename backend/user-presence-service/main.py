from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from google.cloud import firestore

app = Flask(__name__)


cred = credentials.Certificate("/Users/abhinavpandey/Desktop/chat-application/notif-service/serviceAccountsKey.json")
default_app = initialize_app(cred)
db = firestore.Client()

def get_fcm_tokens(user_id):
    pass
    # sos_contact_ref = db.collection('sos_contacts').document(user_id)
    # sos_contact_data = sos_contact_ref.get().to_dict()

    # if not sos_contact_data:
    #     return []

    # phone_numbers = sos_contact_data.get('phone_numbers', [])
    # fcm_tokens = []

    # for phone_number in phone_numbers:
    #     user_details_ref = db.collection('user_details').where('phone_number', '==', phone_number).stream()

    #     for user_doc in user_details_ref:
    #         user_data = user_doc.to_dict()
    #         fcm_token = user_data.get('fcm_token')
    #         if fcm_token:
    #             fcm_tokens.append(fcm_token)

    # return fcm_tokens


@app.route("/sendNotification/<user_id>", methods=["GET"])
def index(user_id):
    print("server is runnig fine")


if __name__ == "__main__":
    app.run(port=8000)


# # Kafka producer setup
# producer_config = {'bootstrap.servers': 'localhost:9092'}
# producer = Producer(producer_config)
# # Route to send a new message
# @app.route('/api/send_message', methods=['POST'])
# def send_message():
#     try:
#         data = request.json
#         username = data.get('username')

#         if username:
#             # Publish the message to the 'received_messages' topic
#             kafka_message = {
#                 'username': username
#             }
#             producer.produce('received_messages', value=json.dumps(kafka_message))
#             producer.flush()

#             # socketio.emit('new_message', kafka_message)

#             return jsonify({'status': 'success', 'message': 'Message sent successfully!'})

#         else:
#             return jsonify({'status': 'error', 'message': 'Invalid request format'}), 400

#     except Exception as e:
#         logging.info(f"Error sending message: {e}")
#         return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
