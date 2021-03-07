CREATE TABLE `cities` (
  `city_id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `active` boolean
);

CREATE TABLE `locality` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `pincode` int,
  `city_id` int,
  `is_active` boolean,
  `order_on_phone` varchar(10),
  `helpline_no` varchar(10)
);

CREATE TABLE `users` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `mobile_no` varchar(10) UNIQUE,
  `active` boolean,
  `admin` boolean,
  `created_on` timestamp,
  `pincode` int
);

CREATE TABLE `address` (
  `address_id` int PRIMARY KEY,
  `user_id` int,
  `name` varchar(255),
  `address1` varchar(500),
  `address2` varchar(500),
  `landmark` varchar(500),
  `pincode` int,
  `mobile_no` varchar(10),
  `active` boolean
);

CREATE TABLE `validate_code` (
  `code_id` int PRIMARY KEY,
  `mobile_no` varchar(10),
  `code` int,
  `expire_time` timestamp
);

CREATE TABLE `complain_reasons` (
  `id` int,
  `reason` varchar(500),
  `active` boolean
);

CREATE TABLE `complains` (
  `id` int,
  `user_id` int,
  `reason_id` int,
  `comment` varchar(500),
  `active` boolean
);

CREATE TABLE `home_category` (
  `id` int,
  `name` varchar(200),
  `category_order` int,
  `num_columns` 3,
  `active` boolean
);

CREATE TABLE `landing` (
  `id` int,
  `name` varchar(200),
  `order_no` int,
  `image` longtext,
  `category_id` int,
  `search_value` varchar(200)
);

CREATE TABLE `category_dimension` (
  `category_id` int,
  `category_name` varchar(100)
);

CREATE TABLE `product_type` (
  `type_id` int,
  `name` varchar(100),
  `category_id` int
);

CREATE TABLE `proudct_category` (
  `category_id` int,
  `name` varchar(255),
  `product_type_id` int
);

CREATE TABLE `product_dimension` (
  `product_id` int,
  `product_key` int,
  `product_description` varchar(255),
  `product_category` int,
  `image` longtext
);

CREATE TABLE `product_version` (
  `version_id` int,
  `product_id` int,
  `weight` varchar(255),
  `measure_unit` varchar(255),
  `price` int,
  `quantity` int,
  `market_price` int
);

CREATE TABLE `cart` (
  `cart_id` int,
  `user_id` int,
  `cart_item` varchar(255)
);

CREATE TABLE `orders` (
  `id` int,
  `order_id` varchar(255),
  `user_id` int,
  `order_on` timestamp,
  `status` varchar(255),
  `active` boolean,
  `address_id` int,
  `payment_mode` varchar(100),
  `sub_total` int,
  `tax` int,
  `delivery_charge` int,
  `promo_code` varchar(100),
  `discount` int,
  `total_amount` int
);

CREATE TABLE `order_items` (
  `id` int,
  `order_id` varchar(255),
  `product_id` int,
  `quantity` int,
  `weight` int,
  `product_name` varchar(255),
  `measure_unit` varchar(255),
  `price` int
);

ALTER TABLE `address` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `locality` ADD FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`);

ALTER TABLE `address` ADD FOREIGN KEY (`pincode`) REFERENCES `locality` (`pincode`);

ALTER TABLE `users` ADD FOREIGN KEY (`pincode`) REFERENCES `locality` (`pincode`);

ALTER TABLE `users` ADD FOREIGN KEY (`user_id`) REFERENCES `complains` (`user_id`);

ALTER TABLE `complains` ADD FOREIGN KEY (`reason_id`) REFERENCES `complain_reasons` (`id`);

ALTER TABLE `home_category` ADD FOREIGN KEY (`id`) REFERENCES `landing` (`category_id`);

ALTER TABLE `product_type` ADD FOREIGN KEY (`category_id`) REFERENCES `category_dimension` (`category_id`);

ALTER TABLE `proudct_category` ADD FOREIGN KEY (`product_type_id`) REFERENCES `product_type` (`type_id`);

ALTER TABLE `product_dimension` ADD FOREIGN KEY (`product_key`) REFERENCES `product_type` (`type_id`);

ALTER TABLE `proudct_category` ADD FOREIGN KEY (`category_id`) REFERENCES `product_dimension` (`product_category`);

ALTER TABLE `product_version` ADD FOREIGN KEY (`product_id`) REFERENCES `product_dimension` (`product_id`);

ALTER TABLE `cart` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`);

ALTER TABLE `order_items` ADD FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`);

ALTER TABLE `order_items` ADD FOREIGN KEY (`product_id`) REFERENCES `product_dimension` (`product_id`);
