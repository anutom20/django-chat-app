import json
import heapq
import os

data = []

current_directory = os.getcwd()
file_path = os.path.join(current_directory, "chatapp/friends/users.json")

with open(file_path, "r") as file:
    data = json.load(file)

data = data["users"]
# print(data)


def calculate_dissimilarity(user1, user2):
    interest_dissimilarity = 0
    for interest in user1["interests"]:
        if interest not in user2["interests"]:
            interest_dissimilarity += 100
        else:
            interest_dissimilarity += (
                abs(user1["interests"][interest] - user2["interests"][interest]) ** 2
            )

    age_dissimilarity = abs(user1["age"] - user2["age"])

    return interest_dissimilarity + 0.2 * age_dissimilarity


def get_suggested_friends(user_id):
    user_data = None
    for user in data:
        if user["id"] == user_id:
            user_data = user
            break

    if user_data is None:
        return ["User not found"]

    # Calculate the dissimilarity between the given user and all other users
    dissimilarities = []
    for user in data:
        if user["id"] != user_id:
            dissimilarity_score = calculate_dissimilarity(user_data, user)
            dissimilarities.append((dissimilarity_score, user["id"]))

    heapq.heapify(dissimilarities)
    suggested_friends_id = []

    while len(suggested_friends_id) < 5 and dissimilarities:
        score, friend_id = heapq.heappop(dissimilarities)
        suggested_friends_id.append(friend_id)

    suggested_friends = []

    for user in data:
        if user["id"] in suggested_friends_id:
            suggested_friends.append(user)

    return suggested_friends
