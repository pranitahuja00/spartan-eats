hall = db['hall']
dishes = db['dishes']
rating = db['rating']
reviews = db['reviews']
stations = db['stations']
people = db['people']

def get_menu(hall, meal):
    return data[(data[hall['hall_name']] == hall) & (data[dishes['meal_cat']] == meal)]

def display_menu(hall, meal):
    menu_items = get_menu(hall, meal)
    for index, row in menu_items.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:

            st.text(row[dishes['dish_name']])
        with col2:
            default_value = st.session_state.get(f"rating_{row[dishes['dish_name']]}", None)
            rating = st.radio(
                "Rate this dish:",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                key=f"rate_{row[dishes['dish_name']]}",
                index=default_value - 1 if default_value else None 
            )
            st.session_state[f"rating_{row[dishes['dish_name']]}"] = rating
        with col3:
            if st.button('Clear', key=f"clear_{index}"):
                st.session_state[f"rating_{row[dishes['dish_name']]}"] = None
                st.experimental_rerun()

users = {
    'student': {'password': '123', 'role': 'student'},
    'admin': {'password': '123', 'role': 'admin'},
}

def login(username, password):
    user_info = users.get(username)
    if user_info and user_info['password'] == password:
        st.session_state['username'] = username
        st.session_state['role'] = user_info['role']
        st.session_state['logged_in'] = True
        return True
    return False

def get_ratings_from_db():
    # This would be a real database call in production
    # For example: SELECT * FROM ratings
    return pd.DataFrame({
        'Dish': ['Dish1', 'Dish2', 'Dish3', 'Dish1', 'Dish2'],
        'Rating': [5, 3, 2, 4, 3]
    })



def display_insights(ratings_df):
    # Calculate average rating for each dish
    avg_ratings = ratings_df.groupby('Dish')['Rating'].mean().sort_values()

    # Identify the most liked dishes
    most_liked = avg_ratings.tail(3)
    # Identify the least liked dishes
    least_liked = avg_ratings.head(3)

    # Display the most and least liked dishes
    st.write("Most liked dishes:")
    st.dataframe(most_liked)
    
    st.write("Least liked dishes:")
    st.dataframe(least_liked)

    # Visualization
    fig, ax = plt.subplots()
    sns.barplot(x=avg_ratings.values, y=avg_ratings.index, ax=ax)
    ax.set_title('Average Dish Ratings')
    ax.set_xlabel('Average Rating')
    ax.set_ylabel('Dish')
    st.pyplot(fig)

    # Recommendations for new menu (based on this simple logic)
    # In a real scenario, you might use more complex criteria
    st.write("Recommended changes for the new menu:")
    st.write("Consider removing the following dishes:")
    st.dataframe(least_liked)
    
    st.write("Consider keeping or adding similar dishes to the following:")
    st.dataframe(most_liked)


def main():
    if 'logged_in' not in st.session_state:
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        role = st.sidebar.radio("Role", ["student", "admin"])

        if st.sidebar.button("Login"):
            if login(username, password) and st.session_state['role'] == role:
                st.sidebar.success(f"Logged in as {role} successfully!")
            else:
                st.sidebar.error("Incorrect username or password.")
    else:
        if st.session_state['role'] == 'admin':
            st.sidebar.title("Admin Panel")
            if st.sidebar.button("View Insights"):
                ratings_df = get_ratings_from_db()
                display_insights(ratings_df)

        if st.session_state['role'] == 'student':
            st.sidebar.title("Navigation")
            hall = st.sidebar.selectbox("Select Hall", data['Hall'].unique())
            meal = st.sidebar.selectbox("Select Meal", data['Meal'].unique())
            # Display the selected menu
            display_menu(hall, meal)
            comment = st.text_area("Comments", "Enter your feedback here...")
            if st.button('Submit'):
                # Here you would process the feedback and the ratings
                # For example, saving them to a database or a file
                st.success('')     
        

if __name__ == "__main__":
    main()
