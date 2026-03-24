# Connect to MongoDB/
client = pymongo.MongoClient(
    "mongodb+srv://superuser:superuser123@cluster0.s3aalbl.mongodb.net/images?retryWrites=true&w=majority&appName=Cluster0")
db = client["images"]
collection = db["images"]


def get_all_image_ids():
    ids = []
    for doc in collection.find():
        ids.append(str(doc["_id"]))

    return ids


# Specify the _id of the image document you want to retrieve
image_id = get_all_image_ids()

# Query MongoDB to find the image document with the specified _id
def fetch_img():
    for i in range(len(image_id)):
        image_document = collection.find_one({"_id": ObjectId(image_id[i])})  # Use bson.ObjectId

        if image_document:
            # Get the binary image data and content type from the document
            image_data = image_document.get("data")

            # Convert binary image data to NumPy array
            nparr = np.frombuffer(image_data, np.uint8)

            # Decode NumPy array to OpenCV image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Display or process the OpenCV image as needed
            cv2.imshow('Image', img)  # Display the image
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Image not found")