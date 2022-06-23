import face_recognition

class FaceRecognition:
    def __init__(self, pic1, pic2):
        self.image_1 = pic1
        self.image_2 = pic2
        # Load the known images
        image_of_person = face_recognition.load_image_file(self.image_1)

        # Get the face encoding of each person. This can fail if no one is found in the image
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]

        # Create a list of all known face encodings
        known_face_encodings = [person_face_encoding]

        # Load the image we want to check
        unknown_image = face_recognition.load_image_file(self.image_2)

        # Get face encodings for any people in the picture
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        # There might be more than one person in the photo, so we need to loop over each face
        for unknown_face_encoding in unknown_face_encodings:

            # Test if this unknown face encoding matches any of the three people we know
            results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)

            if results[0]:
                return True
            else:
                return False
