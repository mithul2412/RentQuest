# RentQuest (Team 3)

## Description

RentQuest is a smart web application designed to help users find their ideal rental property using data-driven techniques. By integrating property listings, neighborhood crime statistics, and local amenities, RentQuest provides personalized rental recommendations based on user-defined preferences. The system leverages an advanced ranking algorithm—the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)—to balance various criteria and deliver a top 10 list of rental options tailored to each user's needs. This project came out as the Runner-Up in the University of Washington Data Science Hackathon 2024.

Key Features

- Data-Driven Decisions: Integrates multiple data sources such as property listings, crime data, and amenity information to provide a comprehensive view of each rental option.
- Advanced Ranking Algorithm: Utilizes the TOPSIS algorithm to rank rental properties by considering both costs (rent, parking fees) and benefits (crime score, amenities).
- Personalized Recommendations: Allows users to adjust the weight of each criterion for a customized ranking experience.
- Interactive Web Platform: Built using Flask with a dynamic JavaScript, HTML, and CSS frontend for seamless exploration of rental options.
- Seamless Data Integration: Features custom data scraping and API integrations to fetch real-time rental data directly from various sources.

## Technologies Used

- Python: Core language for data processing, feature engineering, and implementing the TOPSIS algorithm.
- Flask: Used to develop the API layer and web platform.
- JavaScript, HTML, CSS: For building an interactive and responsive user interface.
- Data Scraping & APIs: Custom scripts to gather property data, crime statistics, and amenity information.
- Feature Engineering: Techniques such as standardizing crime scores, aggregating amenity counts, and calculating parking fees to enhance data reliability.

## Acknowledgments

Developed as part of the University of Washington Data Science Hackathon




