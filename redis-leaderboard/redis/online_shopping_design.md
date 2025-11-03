# Redis Data Structures for Online Shopping

## Entities
- **Users**: Hash `user:{id}` with fields: username, email, created_at
- **Products**: Hash `product:{id}` with fields: name, price, description, created_at
- **Orders**: Hash `order:{id}` with fields: user_id, total, created_at
- **Reviews**: Hash `review:{id}` with fields: user_id, product_id, rating, comment, created_at

## Relationships
- **Orders by User**: Set `orders:{user_id}` containing order_ids
- **Reviews by Product**: Set `reviews:{product_id}` containing review_ids
- **Reviews by User**: Set `reviews:{user_id}` containing review_ids

## Rankings
- **Top Products by Rating**: Sorted Set `top_products:rating` with product_id as member, average_rating as score
- **Top Products by Sales**: Sorted Set `top_products:sales` with product_id as member, sales_count as score
- **User Spending**: Sorted Set `user_spending` with user_id as member, total_spent as score

## Indexes
- **User by Username**: Hash `username_to_id` with username as field, id as value
- **Product by Name**: Hash `productname_to_id` with name as field, id as value