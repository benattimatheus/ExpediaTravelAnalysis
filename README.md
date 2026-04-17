# Welcome to Expedia Dataset Analysis!

This project focuses on analyzing the Expedia Travel Dataset, which was made available by Jacopo Ferretti on Kaggle (https://www.kaggle.com/datasets/jacopoferretti/expedia-travel-dataset)

Objective: Develop a data pipeline and predictive system to model user travel behavior, identify drivers of booking conversion, and recommend hotel clusters based on search context and user profile.

# Columns meaning

 1. id: Data ID
 2. date_time: Timestamp  
 3. site_name: ID of the Expedia point of sale 
 4. posa_continent: ID of continent associated with site_name  
 5. user_location_country: ID of the country the customer is located 
 6. user_location_region: ID of the region the customer is located  
 7. user_location_city: ID of the city the customer is located  
 8. orig_destination_distance: Physical distance between hotel and customer at the time of search 
 9. user_id: Customer ID  
 10. is_mobile: 1 if the user connected from mobile, 0 otherwise  
 11. is_package: 1 if the click/booking was generated as part of a package, 0 otherwise   
 12. channel: ID of marketing channel  
 13. srch_ci: Checkin date  
 14. srch_co: Checkout date  
 15. srch_adults_cnt: Number of adults in the hotel room  
 16. srch_children_cnt: Number of children in the hotel room  
 17. srch_rm_cnt: Number of hotel rooms in the search  
 18. srch_destination_id: ID of the destination  
 19. srch_destination_type_id: Type of destination  
 20. is_booking: 1 if booking, 0 if click  
 21. cnt: Number of similar events in the context of the same user session  
 22. hotel_continent: Continent of the hotel  
 23. hotel_country: Country of the hotel  
 24. hotel_market: Hotel market  
 25. hotel_cluster: ID of a hotel cluster