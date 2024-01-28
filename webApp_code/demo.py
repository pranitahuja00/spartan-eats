import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data('SH9 - Dining Halls Menu.xlsx')

def get_menu(hall, meal):
    return data[(data['Hall'] == hall) & (data['Meal'] == meal)]

def display_menu(hall, meal):
    menu_items = get_menu(hall, meal)
    for index, row in menu_items.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.text(row['Dish'])
        with col2:
            default_value = st.session_state.get(f"rating_{row['Dish']}", None)
            rating = st.radio(
                "Rate this dish:",
                options=[1, 2, 3, 4, 5],
                horizontal=True,
                key=f"rate_{row['Dish']}",
                index=default_value - 1 if default_value else None 
            )
            st.session_state[f"rating_{row['Dish']}"] = rating
        with col3:
            if st.button('Clear', key=f"clear_{index}"):
                st.session_state[f"rating_{row['Dish']}"] = None
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


def display_insights(dishes, ratings):
    # Combine dishes and ratings into a DataFrame
    ratings_df = pd.DataFrame({'Dish': dishes, 'Rating': ratings})

    # Calculate average rating for each dish
    avg_ratings = ratings_df.groupby('Dish')['Rating'].mean().sort_values()

    pivot_table = data.pivot_table(index='Meal', columns='Station', values='Rating', aggfunc='mean')
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title('Heatmap of Average Ratings by Meal and Station')
    st.pyplot(plt)

    plt.clf()  # Clear the figure for the next plot

    # Visualization: Count Plot of Ratings by Station
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Rating', hue='Station', data=data)
    plt.title('Count Plot of Ratings by Station')
    st.pyplot(plt)

    plt.clf()  # Clear the figure for the next plot

    # Visualization: Box Plot of Ratings by Meal
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Meal', y='Rating', data=data)
    plt.title('Box Plot of Ratings by Meal')
    st.pyplot(plt)

    # Display insights
    st.write("Most liked dishes (Top 3):")
    st.dataframe(avg_ratings.tail(3))
    
    st.write("Least liked dishes (Bottom 3):")
    st.dataframe(avg_ratings.head(3))

    # Recommendations for new menu
    st.write("Recommended changes for the new menu:")
    st.write("Consider removing the following dishes:")
    st.dataframe(avg_ratings.head(3))
    st.write("Consider keeping or adding similar dishes to the following:")
    st.dataframe(avg_ratings.tail(3))


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
                ratings = data['Rating']
                dish = data['Dish']
                display_insights(dish, ratings)

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
