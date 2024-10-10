import pandas as pd

class UserRecommendationSystem:
    """
    A class to represent a recommendation system for a social matching platform.
    The system recommends potential matches based on shared interests, gender, and optionally location proximity.
    """

    def __init__(self, users_dataframe):
        """
        Initialize the recommendation system with a dataset of user profiles.
        
        Parameters:
        users_dataframe (pd.DataFrame): A DataFrame containing user profiles with columns 'UserID', 'Age', 'Gender', 'Location', and 'Interests'.
        """
        # Store the user data in an instance variable
        self.users_df = users_dataframe

    def recommend_matches(self, user_id):
        """
        Recommend the top 3 potential matches for a given user based on shared interests.
        
        Parameters:
        user_id (int): The UserID of the user for whom we want to generate recommendations.
        
        Returns:
        List[int]: A list of UserIDs representing the top 3 recommended matches based on shared interests.
        """
        # Get the details of the user making the request
        current_user = self.users_df[self.users_df['UserID'] == user_id].iloc[0]

        # Extract the current user's gender and interests
        current_user_gender = current_user['Gender']
        current_user_interests = set(current_user['Interests'].split(', '))

        # Determine the gender to match with (opposite of current user's gender)
        matching_gender = 'Female' if current_user_gender == 'Male' else 'Male'

        # Filter potential matches based on the opposite gender
        potential_matches_df = self.users_df[self.users_df['Gender'] == matching_gender].copy()

        # Compute the number of shared interests for each potential match
        potential_matches_df.loc[:, 'SharedInterestsCount'] = potential_matches_df['Interests'].apply(
            lambda interests: len(current_user_interests.intersection(set(interests.split(', '))))
        )

        # Sort potential matches by the number of shared interests in descending order
        sorted_matches_df = potential_matches_df.sort_values(by='SharedInterestsCount', ascending=False)

        # Retrieve the top 3 matches
        top_matches_df = sorted_matches_df.head(3)

        # Return the list of UserIDs of the top 3 matches
        return top_matches_df['UserID'].tolist()


# Example dataset of users
user_data = {
    'UserID': [1, 2, 3, 4, 5],
    'Age': [25, 28, 30, 22, 26],
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Female'],
    'Location': ['New York', 'San Diego', 'Seattle', 'New York', 'San Diego'],
    'Interests': [
        'Music, Hiking, Technology', 
        'Travel, Cooking, Reading', 
        'Sports, Technology, Movies', 
        'Music, Reading, Yoga', 
        'Technology, Travel, Cooking'
    ]
}

# Create a pandas DataFrame for the dataset
user_profiles_df = pd.DataFrame(user_data)

# Instantiate the recommendation system with the dataset
recommendation_system = UserRecommendationSystem(user_profiles_df)

# Example usage: Get the top 3 recommended matches for the user with UserID 1
print(recommendation_system.recommend_matches(5))  # Output might look like [2, 5, 4]
